import logging
import threading
from typing import Dict, List, Optional, Tuple

from coexistanceSimpy.Coex2 import *


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
    airtime_data = {"Station {}".format(i): 0 for i in range(1, stations_number + gnb_number+ 1)}
    airtime_control = {"Station {}".format(i): 0 for i in range(1, stations_number + gnb_number + 1)}
    run_simulation(stations_number, gnb_number, seeds, simulation_time, Config(payload_size, cw_min, cw_max, r_limit, mcs_value),
                   backoffs, airtime_data, airtime_control)





if __name__ == "__main__":
    #  running diferent scenarios of simulation

    #run_changing_stations(runs=5, seed=128, stations_start=1, stations_end=10, simulation_time=100, payload_size=1472, cw_min=15, cw_max=1023, r_limit=7, mcs_value=7)

    single_run(seeds=121, stations_number=0, gnb_number=2, simulation_time=10, payload_size=1472, cw_min=15, cw_max=1023, r_limit=7, mcs_value=7)
