import logging
import csv
import os
import random
import time
import pandas as pd
import simpy

from dataclasses import dataclass, field
from typing import Dict, List

from .Times import *
from datetime import datetime

file_log_name = f"{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}.log"

typ_filename = "debug_airtime.log"

logging.basicConfig(filename=typ_filename,
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


colors = [
    "\033[30m",
    "\033[32m",
    "\033[31m",
    "\033[33m",
    "\033[34m",
    "\033[35m",
    "\033[36m",
    "\033[37m",
]  # colors to distinguish stations in output

big_num = 10000000  # some big number for quesing in peeemtive resources - big starting point


@dataclass()
class Config:
    data_size: int = 1472  # size od payload in b
    cw_min: int = 15  # min cw window size
    cw_max: int = 1023  # max cw window size
    r_limit: int = 7
    mcs: int = 7


@dataclass()
class Config_NR:
    deter_period: int = 16  # time used for waiting in prioritization period, microsec
    observation_slot_duration: int = 9  # observation slot in mikros
    synchronization_slot_duration: int = 1000  # synchronization slot lenght in mikros
    max_sync_slot_desync: int = 1000
    min_sync_slot_desync: int = 0
    # channel access class related:
    M: int = 3  # amount of observation slots to wait after deter perion in prioritization period
    cw_min: int = 15
    cw_max: int = 63
    mcot: int = 8  # max ocupancy time


def random_sample(max, number, min_distance=0):  # func used to desync gNBs
    # returns number * elements <0, max>
    samples = random.sample(range(max - (number - 1) * (min_distance - 1)), number)
    indices = sorted(range(len(samples)), key=lambda i: samples[i])
    ranks = sorted(indices, key=lambda i: indices[i])
    return [sample + (min_distance - 1) * rank for sample, rank in zip(samples, ranks)]


def log(gnb, mes: str):
    logger.info(
        f"{gnb.col}Time: {gnb.env.now} Station: {gnb.name} Message: {mes}"
    )
# def log(station, mes: str):
#     logging.info(
#         f"{station.col}Time: {station.env.now} Station: {station.name} Message: {mes}"
#     )

class Station:
    def __init__(
            self,
            env: simpy.Environment,
            name: str,
            channel: dataclass,
            config: Config = Config(),
    ):
        self.config = config
        self.times = Times(config.data_size, config.mcs)  # using Times script to get time calculations
        self.name = name  # name of the station
        self.env = env  # simpy environment
        self.col = random.choice(colors)  # color of output -- for future station distinction
        self.frame_to_send = None  # the frame object which is next to send
        self.succeeded_transmissions = 0  # all succeeded transmissions for station
        self.failed_transmissions = 0  # all failed transmissions for station
        self.failed_transmissions_in_row = 0  # all failed transmissions for station in a row
        self.cw_min = config.cw_min  # cw min parameter value
        self.cw_max = config.cw_max  # cw max parameter value
        self.channel = channel  # channel obj
        env.process(self.start())  # starting simulation process
        self.process = None  # waiting back off process
        self.channel.airtime_data.update({name: 0})
        self.channel.airtime_control.update({name: 0})

    def start(self):
        while True:
            self.frame_to_send = self.generate_new_frame()
            was_sent = False
            while not was_sent:
                self.process = self.env.process(self.wait_back_off())
                yield self.process
                was_sent = yield self.env.process(self.send_frame())

    def wait_back_off(self):
        back_off_time = self.generate_new_back_off_time(
            self.failed_transmissions_in_row)  # generating the new Back Off time

        while back_off_time > -1:
            try:
                with self.channel.tx_lock.request() as req:  # waiting  for idle channel -- empty channel
                    yield req
                back_off_time += Times.t_difs  # add DIFS time
                log(self, f"Starting to wait backoff: ({back_off_time})u...")
                start = self.env.now  # store the current simulation time
                self.channel.back_off_list.append(self)  # join the list off stations which are waiting Back Offs

                yield self.env.timeout(back_off_time)  # join the environment action queue

                log(self, f"Backoff waited, sending frame...")
                back_off_time = -1  # leave the loop

                self.channel.back_off_list.remove(self)  # leave the waiting list as Backoff was waited successfully

            except simpy.Interrupt:  # handle the interruptions from transmitting stations
                log(self, "Waiting was interrupted, waiting to resume backoff...")
                back_off_time -= (self.env.now - start)  # set the Back Off to the remaining one
                back_off_time -= 9  # simulate the delay of sensing the channel state

    def send_frame(self):
        self.channel.tx_list.append(self)  # add station to currently transmitting list
        res = self.channel.tx_queue.request(
            priority=(big_num - self.frame_to_send.frame_time))  # create request basing on this station frame length

        try:
            result = yield res | self.env.timeout(
                0)  # try to hold transmitting lock(station with the longest frame will get this)

            if res not in result:  # check if this station got lock, if not just wait you frame time
                raise simpy.Interrupt("There is a longer frame...")

            with self.channel.tx_lock.request() as lock:  # this station has the longest frame so hold the lock
                yield lock
                log(self, self.channel.back_off_list)

                for station in self.channel.back_off_list:  # stop all station which are waiting backoff as channel is not idle
                    station.process.interrupt()
                for gnb in self.channel.back_off_list_NR:  # stop all station which are waiting backoff as channel is not idle
                    gnb.process.interrupt()

                log(self, self.frame_to_send.frame_time)

                yield self.env.timeout(self.frame_to_send.frame_time)  # wait this station frame time
                self.channel.back_off_list.clear()  # channel idle, clear backoff waiting list
                was_sent = self.check_collision()  # check if collision occurred

                if was_sent:  # transmission successful
                    self.channel.airtime_control[self.name] += self.times.get_ack_frame_time()
                    yield self.env.timeout(self.times.get_ack_frame_time())  # wait ack
                    self.channel.tx_list.clear()  # clear transmitting list
                    self.channel.tx_queue.release(res)  # leave the transmitting queue
                    return True

            # there was collision
            self.channel.tx_list.clear()  # clear transmitting list
            self.channel.tx_queue.release(res)  # leave the transmitting queue
            self.channel.tx_queue = simpy.PreemptiveResource(self.env,
                                                             capacity=1)  # create new empty transmitting queue
            yield self.env.timeout(self.times.ack_timeout)  # simulate ack timeout after failed transmission
            return False

        except simpy.Interrupt:  # this station does not have the longest frame, waiting frame time
            yield self.env.timeout(self.frame_to_send.frame_time)

        was_sent = self.check_collision()

        if was_sent:  # check if collision occurred
            yield self.env.timeout(self.times.get_ack_frame_time())  # wait ack
        else:
            log(self, "waiting wck timeout slave")
            yield self.env.timeout(Times.ack_timeout)  # simulate ack timeout after failed transmission
        return was_sent

    def check_collision(self):  # check if the collision occurred
        if (len(self.channel.tx_list) > 1 or len(self.channel.tx_list_NR) > 1):  # check if there was more then one station transmitting
            self.sent_failed()
            return False
        else:
            self.sent_completed()
            return True

    def generate_new_back_off_time(self, failed_transmissions_in_row):
        upper_limit = (pow(2, failed_transmissions_in_row) * (
                self.cw_min + 1) - 1)  # define the upper limit basing on  unsuccessful transmissions in the row
        upper_limit = (
            upper_limit if upper_limit <= self.cw_max else self.cw_max)  # set upper limit to CW Max if is bigger then this parameter
        back_off = random.randint(0, upper_limit)  # draw the back off value
        self.channel.backoffs[back_off][self.channel.n_of_stations] += 1  # store drawn value for future analyzes
        return back_off * self.times.t_slot

    def generate_new_frame(self):
        frame_length = self.times.get_ppdu_frame_time()
        return Frame(frame_length, self.name, self.col, self.config.data_size, self.env.now)

    def sent_failed(self):
        log(self, "There was a collision")
        self.frame_to_send.number_of_retransmissions += 1
        self.channel.failed_transmissions += 1
        self.failed_transmissions += 1
        self.failed_transmissions_in_row += 1
        log(self, self.channel.failed_transmissions)
        if self.frame_to_send.number_of_retransmissions > self.config.r_limit:
            self.frame_to_send = self.generate_new_frame()
            self.failed_transmissions_in_row = 0

    def sent_completed(self):
        log(self, f"Successfully sent frame, waiting ack: {self.times.get_ack_frame_time()}")
        self.frame_to_send.t_end = self.env.now
        self.frame_to_send.t_to_send = (self.frame_to_send.t_end - self.frame_to_send.t_start)
        self.channel.succeeded_transmissions += 1
        self.succeeded_transmissions += 1
        self.failed_transmissions_in_row = 0
        self.channel.bytes_sent += self.frame_to_send.data_size
        self.channel.airtime_data[self.name] += self.frame_to_send.frame_time
        return True


# Gnb -- mirroring station
class Gnb:
    def __init__(
            self,
            env: simpy.Environment,
            name: str,
            channel: dataclass,
            config_nr: Config_NR = Config_NR(),
    ):
        self.config_nr = config_nr
        # self.times = Times(config.data_size, config.mcs)  # using Times script to get time calculations
        self.name = name  # name of the station
        self.env = env  # simpy environment
        self.col = random.choice(colors)  # color of output -- for future station distinction
        self.transmission_to_send = None  # the transmision object which is next to send
        self.succeeded_transmissions = 0  # all succeeded transmissions for station
        self.failed_transmissions = 0  # all failed transmissions for station
        self.failed_transmissions_in_row = 0  # all failed transmissions for station in a row
        self.cw_min = config_nr.cw_min  # cw min parameter value
        self.N = None  # backoff counter
        self.desync = 0
        self.next_sync_slot_boundry = 0
        self.cw_max = config_nr.cw_max  # cw max parameter value
        self.channel = channel  # channel obj
        env.process(self.start())  # starting simulation process
        env.process(self.sync_slot_counter())
        self.process = None  # waiting back off process
        self.channel.airtime_data.update({name: 0})
        self.channel.airtime_control.update({name: 0})
        self.first_transmission = True
        self.desync_done = False

    def start(self):

        yield self.env.timeout(self.desync)
        while True:
            # loop with runn proces TO DO
            # zainicjalizuj N, jako licznik ile stloów backoffu ma czekać startowo
            # tak samo zainicjalizować jakiś różny desync time :P

            #self.transmission_to_send = self.gen_new_transmission()
            was_sent = False
            while not was_sent:
                self.process = self.env.process(self.wait_prioritization_period())
                yield self.process
                if not self.first_transmission:
                    self.process = self.env.process(self.wait_back_off())
                    yield self.process
                was_sent = yield self.env.process(self.send_transmission())

    def wait_prioritization_period(self):
        # wait initial 16 us + m x observation_slot_duration ------- possibly bug -> not checking channel every slot
        m = self.config_nr.M
        prioritization_period_time = self.config_nr.deter_period + m * self.config_nr.observation_slot_duration
        while prioritization_period_time > -1:  # if m == 0 continig to backoff
            try:
                with self.channel.tx_lock.request() as req:  # waiting  for idle channel -- empty channel
                    yield req

                log(self, f"Channel is idle, waiting deter period {self.config_nr.deter_period} us")
                start = self.env.now  # store start time
                self.channel.back_off_list_NR.append(self)
                if not self.desync_done:
                    log(self, f"Waiting first desynch time: {self.desync}")
                    yield self.env.timeout(self.desync)
                    self.desync_done = True
                yield self.env.timeout(prioritization_period_time)
                log(self, f"Prior period waited")

                prioritization_period_time = -1  # leave the loop

                self.channel.back_off_list_NR.remove(
                    self)  # leave the waiting list as prioritization period was succesfully waited

            except simpy.Interrupt:  # handle the interruptions from transmitting stations
                log(self, "Waiting prioritization period was interrupted - channel busy")
                self.first_transmission = False
                prioritization_period_time -= (self.env.now - start)

    def wait_back_off(self):
        # Wait random number of slots N x OBSERVATION_SLOT_DURATION us
        back_off_time = self.generate_new_back_off_time(self.failed_transmissions_in_row)
        while back_off_time > -1:
            try:
                with self.channel.tx_lock.request() as req:  # waiting  for idle channel -- empty channel
                    yield req
                # back_off_time += Times.t_difs  # add DIFS time
                log(self, f"Starting to wait backoff: ({back_off_time})u...")
                start = self.env.now  # store the current simulation time
                self.channel.back_off_list_NR.append(self)  # join the list off stations which are waiting Back Offs

                yield self.env.timeout(back_off_time)  # join the environment action queue

                log(self, f"Backoff waited, sending frame...")
                back_off_time = -1  # leave the loop

                self.channel.back_off_list_NR.remove(self)  # leave the waiting list as Backoff was waited successfully

            except simpy.Interrupt:  # handle the interruptions from transmitting stations
                log(self, "Waiting was interrupted, waiting to resume backoff...")
                back_off_time -= (self.env.now - start)  # set the Back Off to the remaining one
                back_off_time -= 9  # simulate the delay of sensing the channel state
                self.first_transmission = False

    def sync_slot_counter(self):
        # Process responsible for keeping the next sync slot boundry timestamp
        self.desync = random.randint(self.config_nr.min_sync_slot_desync, self.config_nr.max_sync_slot_desync)
        self.next_sync_slot_boundry = self.desync
        log(self, f"Selected random desync to {self.desync} us")
        yield self.env.timeout(self.desync)  # randomly desync tx starting points
        while True:
            self.next_sync_slot_boundry += self.config_nr.synchronization_slot_duration
            log(self, f"Next synch slot boundry is: {self.next_sync_slot_boundry}")
            yield self.env.timeout(self.config_nr.synchronization_slot_duration)

    def send_transmission(self):
        self.channel.tx_list_NR.append(self)  # add station to currently transmitting list
        self.transmission_to_send = self.gen_new_transmission()
        res = self.channel.tx_queue.request(priority=(
                    big_num - self.transmission_to_send.transmission_time))  # create request basing on this station frame length

        try:
            result = yield res | self.env.timeout(
                0)  # try to hold transmitting lock(station with the longest frame will get this)

            if res not in result:  # check if this station got lock, if not just wait you frame time
                self.first_transmission = False
                raise simpy.Interrupt("There is a longer frame...")


            with self.channel.tx_lock.request() as lock:  # this station has the longest frame so hold the lock
                yield lock
                log(self, self.channel.back_off_list_NR)

                for station in self.channel.back_off_list:  # stop all station which are waiting backoff as channel is not idle
                    station.process.interrupt()
                for gnb in self.channel.back_off_list_NR:  # stop all station which are waiting backoff as channel is not idle
                    gnb.process.interrupt()

                log(self, self.transmission_to_send.transmission_time)

                yield self.env.timeout(self.transmission_to_send.rs_time)  # wait this rs time
                yield self.env.timeout(self.transmission_to_send.airtime)  # wait this airtime time
                self.channel.back_off_list_NR.clear()  # channel idle, clear backoff waiting list
                was_sent = self.check_collision()  # check if collision occurred

                if was_sent:  # transmission successful
                    self.channel.airtime_control[self.name] += self.transmission_to_send.rs_time
                    self.channel.airtime_data[self.name] += self.transmission_to_send.airtime
                    # yield self.env.timeout(self.times.get_ack_frame_time())  # wait ack
                    self.channel.tx_list_NR.clear()  # clear transmitting list
                    self.channel.tx_queue.release(res)  # leave the transmitting queue
                    return True

            # there was collision
            self.channel.tx_list_NR.clear()  # clear transmitting list
            self.channel.tx_queue.release(res)  # leave the transmitting queue
            self.channel.tx_queue = simpy.PreemptiveResource(self.env,
                                                             capacity=1)  # create new empty transmitting queue
            # yield self.env.timeout(self.times.ack_timeout)  # simulate ack timeout after failed transmission
            return False

        except simpy.Interrupt:  # this station does not have the longest frame, waiting frame time
            self.first_transmission = False
            yield self.env.timeout(self.transmission_to_send.transmission_time)

        was_sent = self.check_collision()

        # if was_sent:  # check if collision occurred
        #     #yield self.env.timeout(self.times.get_ack_frame_time())  # wait ack
        # else:
        #     log(self, "waiting wck timeout slave")
        #     #yield self.env.timeout(Times.ack_timeout)  # simulate ack timeout after failed transmission
        return was_sent

    def check_collision(self):  # check if the collision occurred
        if (len(self.channel.tx_list) > 1 or len(self.channel.tx_list_NR) > 1) :  # check if there was more then one station transmitting
            self.sent_failed()
            return False
        else:
            self.sent_completed()
            return True

    def gen_new_transmission(self):
        transmission_time = self.config_nr.mcot * 1000  # transforming to usec
        rs_time = self.next_sync_slot_boundry - self.env.now
        airtime = transmission_time - rs_time
        return Transmission_NR(transmission_time, self.name, self.col, self.env.now, airtime, rs_time)

    def generate_new_back_off_time(self, failed_transmissions_in_row):
        # BACKOFF TIME GENERATION
        upper_limit = (pow(2, failed_transmissions_in_row) * (
                    self.cw_min + 1) - 1)  # define the upper limit basing on  unsuccessful transmissions in the row
        upper_limit = (
            upper_limit if upper_limit <= self.cw_max else self.cw_max)  # set upper limit to CW Max if is bigger then this parameter
        back_off = random.randint(0, upper_limit)  # draw the back off value
        self.channel.backoffs[back_off][self.channel.n_of_stations] += 1  # store drawn value for future analyzes
        return back_off * self.config_nr.synchronization_slot_duration

    def sent_failed(self):
        log(self, "There was a collision")
        self.transmission_to_send.number_of_retransmissions += 1
        self.channel.failed_transmissions += 1
        self.failed_transmissions += 1
        self.failed_transmissions_in_row += 1
        log(self, self.channel.failed_transmissions)
        # if self.transmission_to_send.number_of_retransmissions > self.config.r_limit:
        #     self.frame_to_send = self.generate_new_frame()
        #     self.failed_transmissions_in_row = 0

    def sent_completed(self):
        log(self, f"Successfully sent frame")
        self.transmission_to_send.t_end = self.env.now
        self.transmission_to_send.t_to_send = (self.transmission_to_send.t_end - self.transmission_to_send.t_start)
        self.channel.succeeded_transmissions += 1
        self.succeeded_transmissions += 1
        self.failed_transmissions_in_row = 0
        # self.channel.bytes_sent += self.frame_to_send.data_size
        #self.channel.airtime_data[self.name] += self.transmission_to_send.transmission_time
        return True


@dataclass()
class Channel:
    tx_queue: simpy.PreemptiveResource  # lock for the stations with the longest frame to transmit
    tx_lock: simpy.Resource  # channel lock (locked when there is ongoing transmission)
    n_of_stations: int  # number of transmitting stations in the channel
    n_of_eNB: int
    backoffs: Dict[int, Dict[int, int]]
    airtime_data: Dict[str, int]
    airtime_control: Dict[str, int]
    tx_list: List[Station] = field(default_factory=list)  # transmitting stations in the channel
    back_off_list: List[Station] = field(default_factory=list)  # stations in backoff phase
    tx_list_NR: List[Gnb] = field(default_factory=list)  # transmitting stations in the channel
    back_off_list_NR: List[Gnb] = field(default_factory=list)  # stations in backoff phase
    ## problem list of station objects, what if we 2 differenet station objects???

    failed_transmissions: int = 0  # total failed transmissions
    succeeded_transmissions: int = 0  # total succeeded transmissions
    bytes_sent: int = 0  # total bytes sent


@dataclass()
class Frame:
    frame_time: int  # time of the frame
    station_name: str  # name of the owning it station
    col: str  # output color
    data_size: int  # payload size
    t_start: int  # generation time
    number_of_retransmissions: int = 0  # retransmissions count
    t_end: int = None  # sent time
    t_to_send: int = None  # how much time it took to sent successfully

    def __repr__(self):
        return (self.col + "Frame: start=%d, end=%d, frame_time=%d, retransmissions=%d"
                % (self.t_start, self.t_end, self.t_to_send, self.number_of_retransmissions)
                )


@dataclass()
class Transmission_NR:
    transmission_time: int
    enb_name: str  # name of the owning it station
    col: str
    t_start: int  # generation time / transmision start (including RS)
    airtime: int  # time spent on sending data
    rs_time: int  # time spent on sending reservation signal before data
    number_of_retransmissions: int = 0
    t_end: int = None  # sent time / transsmision end = start + rs_time + airtime
    t_to_send: int = None
    collided: bool = False  # true if transmission colided with another one


def run_simulation(
        number_of_stations: int,
        number_of_gnb: int,
        seed: int,
        simulation_time: int,
        config: Config,
        backoffs: Dict[int, Dict[int, int]],
        airtime_data: Dict[str, int],
        airtime_control: Dict[str, int],
):
    random.seed(seed)
    environment = simpy.Environment()
    channel = Channel(
        simpy.PreemptiveResource(environment, capacity=1),
        simpy.Resource(environment, capacity=1),
        number_of_stations,
        number_of_gnb,
        backoffs,
        airtime_data,
        airtime_control,
    )
    config_nr = Config_NR()

    for i in range(1, number_of_stations + 1):
        Station(environment, "Station {}".format(i), channel, config)

    for i in range(1, number_of_gnb + 1):
        Gnb(environment, "Gnb {}".format(i), channel, config_nr)

    environment.run(until=simulation_time * 1000000)

    p_coll = "{:.4f}".format(
        channel.failed_transmissions / (channel.failed_transmissions + channel.succeeded_transmissions))

    # normalizedChannelOccupancyTime = channel.succeeded_transmissions * ()

    print(
        f"SEED = {seed} N_stations:={number_of_stations}  CW_MIN = {config.cw_min} CW_MAX = {config.cw_max}  PCOLL: {p_coll} THR:"
        f" {(channel.bytes_sent * 8) / (simulation_time * 1000000)} "
        f"FAILED_TRANSMISSIONS: {channel.failed_transmissions}"
        f" SUCCEEDED_TRANSMISSION {channel.succeeded_transmissions}"
    )

    print('stats for GNB ------------------')

    print(
        f"SEED = {seed} N_gnbs={number_of_gnb} CW_MIN = {config_nr.cw_min} CW_MAX = {config_nr.cw_max}  PCOLL: {p_coll}"
        f"FAILED_TRANSMISSIONS: {channel.failed_transmissions}"
        f" SUCCEEDED_TRANSMISSION {channel.succeeded_transmissions}"
    )

    print('airtimes ---- 1)data, 2)control')

    print(channel.airtime_data)
    print(channel.airtime_control)

    # colison probability:
    # with open("results.csv", mode='a', newline="") as result_file:
    #     result_adder = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #
    #     colision = (channel.failed_transmissions / (channel.failed_transmissions + channel.succeeded_transmissions)) * 100
    #
    #     result_adder.writerow(
    #         [seed, number_of_stations, channel.failed_transmissions, channel.succeeded_transmissions, colision])

    # airtime 34:
    # with open("airtime34.csv", mode='a', newline="") as result_file:
    #     result_adder = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #
    #     channel_occupancy_time = 0
    #     channel_efficiency = 0
    #     time = simulation_time * 1000000
    #     for i in range(1, number_of_stations + 1):
    #         channel_occupancy_time += channel.airtime_data["Station {}".format(i)] + channel.airtime_control["Station {}".format(i)]
    #         channel_efficiency += channel.airtime_data["Station {}".format(i)]
    #
    #     normalized_channel_occupancy_time = channel_occupancy_time / time
    #     normalized_channel_efficiency = channel_efficiency / time
    #
    #
    #     result_adder.writerow(
    #         [seed, number_of_stations, normalized_channel_occupancy_time, normalized_channel_efficiency])

    # airtime 12:
    # with open("airtime12_new2.csv", mode='a', newline="") as result_file:
    #     result_adder = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #
    #     time = simulation_time * 1000000
    #     time_conv = 1000000
    #     for i in range(1, number_of_stations + 1):
    #         station_airtime = (channel.airtime_data["Station {}".format(i)] + channel.airtime_control[
    #             "Station {}".format(i)]) / time_conv
    #         norm_station_airtime = (channel.airtime_data["Station {}".format(i)] + channel.airtime_control[
    #             "Station {}".format(i)]) / time
    #         result_adder.writerow([number_of_stations, seed, i, station_airtime, norm_station_airtime])


    #nru airtime
    with open("nru_airtime2.csv", mode='a', newline="") as result_file:
        result_adder = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        channel_occupancy_time = 0
        channel_efficiency = 0
        time = simulation_time * 1000000

        #nodes = number_of_stations + number_of_gnb

        for i in range(1, number_of_gnb + 1):
            channel_occupancy_time += channel.airtime_data["Gnb {}".format(i)] + channel.airtime_control["Gnb {}".format(i)]
            channel_efficiency += channel.airtime_data["Gnb {}".format(i)]

        normalized_channel_occupancy_time = channel_occupancy_time / time
        normalized_channel_efficiency = channel_efficiency / time


        result_adder.writerow(
            [seed, number_of_gnb, normalized_channel_occupancy_time, normalized_channel_efficiency])