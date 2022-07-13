import click
from coexistanceSimpy.Coexistence import *


@click.command()
@click.option("-r", "--runs", "runs", default=10, help="Number of simulation runs")
@click.option("--seed", "seed", default=1, help="Seed for simulation")
@click.option(
    "--start_node_number",
    "start_node_number",
    type=int,
    required=True,
    help="Starting number of Wi-Fi and NR-U nodes",
)
@click.option(
    "--end_node_number",
    "end_node_number",
    type=int,
    required=True,
    help="Ending number of Wi-Fi and NR-U nodes",
)
@click.option(
    "-t",
    "--simulation-time",
    "simulation_time",
    default=100.0,
    help="Duration of the simulation per stations number in s",
)
@click.option("--wifi_cw_min", "wifi_cw_min", default=15, help="Size of Wi-Fi cw min")
@click.option("--wifi_cw_max", "wifi_cw_max", default=63, help="Size of Wi-Fi cw max")
@click.option("--nru_cw_min", "nru_cw_min", default=15, help="Size of NR-U cw min")
@click.option("--nru_cw_max", "nru_cw_max", default=63, help="Size of NR-U cw max")
@click.option(
    "--wifi_r_limit", "wifi_r_limit", default=7, help="Number of failed transmissions in a row",
)
@click.option("-m", "--mcs-value", "mcs_value", default=7, help="Value of mcs")
@click.option("-syn_slot", "--synchronization_slot_duration", default=1000, help="Synchronization slot length in mikrosecounds")
@click.option("-max_des", "--max_sync_slot_desync", default=1000, help="Max value of gNB desynchronization")
@click.option("-min_des", "--min_sync_slot_desync", default=0, help="Min value of gNB desynchronization")
@click.option("-nru_obser_slots", "--nru_observation_slot", default=3, help="amount of observation slots for NR_U")
@click.option("--mcot", default=6, help="Max channel occupancy time for NR-U (ms)")
def changing_number_nodes(
        runs: int,
        seed: int,
        start_node_number: int,
        end_node_number: int,
        simulation_time: int,
        wifi_cw_min: int,
        wifi_cw_max: int,
        wifi_r_limit: int,
        mcs_value: int,

        nru_cw_min: int,
        nru_cw_max: int,
        synchronization_slot_duration: int,
        max_sync_slot_desync: int,
        min_sync_slot_desync: int,
        nru_observation_slot: int,
        mcot: int,
):

    for node_number in range(start_node_number, end_node_number + 1):


        backoffs = {key: {node_number: 0} for key in range(wifi_cw_max + 1)}
        airtime_data = {"Station {}".format(i): 0 for i in range(1, node_number + 1)}
        airtime_control = {"Station {}".format(i): 0 for i in range(1, node_number + 1)}
        airtime_data_NR = {"Gnb {}".format(i): 0 for i in range(1, node_number + 1)}
        airtime_control_NR = {"Gnb {}".format(i): 0 for i in range(1, node_number + 1)}

        for i in range(0, runs):
            curr_seed = seed + i
            run_simulation(node_number, node_number, curr_seed, simulation_time,
                           Config(1472, wifi_cw_min, wifi_cw_max, wifi_r_limit, mcs_value),
                           Config_NR(16, 9, synchronization_slot_duration, max_sync_slot_desync, min_sync_slot_desync,  nru_observation_slot, nru_cw_min, nru_cw_max, mcot),
                           backoffs, airtime_data, airtime_control, airtime_data_NR, airtime_control_NR)

if __name__ == "__main__":
    changing_number_nodes()

