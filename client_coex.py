
from coexistanceSimpy.Coexistence import *


def single_run(
        seeds: int,
        stations_number: int,
        gnb_number: int,
        simulation_time: int,
        cw_min: int,
        cw_max: int,
        r_limit: int,
        payload_size: int,
        mcs_value: int,
):
    backoffs = {key: {stations_number: 0} for key in range(cw_max + 1)}
    airtime_data = {"Station {}".format(i): 0 for i in range(1, stations_number + 1)}
    airtime_control = {"Station {}".format(i): 0 for i in range(1, stations_number + 1)}
    airtime_data_NR = {"Gnb {}".format(i): 0 for i in range(1, gnb_number + 1)}
    airtime_control_NR = {"Gnb {}".format(i): 0 for i in range(1, gnb_number + 1)}
    # run_simulation(stations_number, gnb_number, seeds, simulation_time, Config(payload_size, cw_min, cw_max, r_limit, mcs_value),
    #                backoffs, airtime_data, airtime_control)
    run_simulation(stations_number, gnb_number, seeds, simulation_time,
                   Config(payload_size, cw_min, cw_max, r_limit, mcs_value),
                   backoffs, airtime_data, airtime_control, airtime_data_NR, airtime_control_NR)





if __name__ == "__main__":
    #  running diferent scenarios of simulation

    # performing single run
    number = 1
    single_run(seeds=145324
               , stations_number=number, gnb_number=number, simulation_time=10, payload_size=1472, cw_min=15, cw_max=63, r_limit=7, mcs_value=7)

    # performing multiple runs
    # list = []
    # for radn in range(1, 10):
    #     n = random.randint(1000, 10000)
    #     list.append(n)
    #
    # print(list)
    #
    # for var in list:
    #     #for k in range(2, 12):
    #     # k = 4
    #     single_run(seeds=var, stations_number=k, gnb_number=k, simulation_time=1, payload_size=1472, cw_min=15,
    #                    cw_max=1023, r_limit=7, mcs_value=7)