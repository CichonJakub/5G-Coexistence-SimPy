# A Wi-Fi and NR-U Coexistence Channel Access Simulator based on the Python SimPy Library

## Intro
Simulator created for master thesis `Jakub_Cichon_Master_s_Thesis.pdf` by Jakub Cichoń, based on two existing implementations:
* [Wi-Fi simulator](https://github.com/ToporPawel/DCF-Simpy)
* [NR-U simulator](https://github.com/marekzajac97/nru-channel-access)

## Installation

- (Optional) Launch virtual env: `python3 -m venv env && source env/bin/activate`
- Install requirements : `pip install -r requirements.txt`

## Structure

Main program is located in `coexistanceSimpy` module.

`singleRun.py` and `changingNodesNumber.py` - scripts used for running simulations scenarios

`validation.py` and `resultAnalysis.py` - scripts used for plotting obtained results 


## Usage

This project is using `click` library to execute the program with pre defined simulation scenarios. For each of the possible scenarios there is a help function.

### Single run
Running single run of simulation with desired parameters. In default repeated 10 times (runs).

```bash
python singleRun.py --help
Usage: singleRun.py [OPTIONS]

Options:
  -r, --runs INTEGER              Number of simulation runs
  --seed INTEGER                  Seed for simulation
  --ap-number INTEGER             Number of Wi-Fi stations  [required]
  --gnb-number INTEGER            Number of NR-U gNBs  [required]
  -t, --simulation-time FLOAT     Duration of the simulation per stations
                                  number in s
  --wifi_cw_min INTEGER           Size of Wi-Fi cw min
  --wifi_cw_max INTEGER           Size of Wi-Fi cw max
  --nru_cw_min INTEGER            Size of NR-U cw min
  --nru_cw_max INTEGER            Size of NR-U cw max
  --wifi_r_limit INTEGER          Number of failed transmissions in a row
  -m, --mcs-value INTEGER         Value of mcs
  -syn_slot, --synchronization_slot_duration INTEGER
                                  Synchronization slot length in mikrosecounds
  -max_des, --max_sync_slot_desync INTEGER
                                  Max value of gNB desynchronization
  -min_des, --min_sync_slot_desync INTEGER
                                  Min value of gNB desynchronization
  -nru_obser_slots, --nru_observation_slot INTEGER
                                  amount of observation slots for NR_U
  --mcot INTEGER                  Max channel occupancy time for NR-U (ms)
  --help                          Show this message and exit.

```
##### Usage
```bash
python singleRun.py --ap-number 2 --gnb-number 2 -t 10 -r 1
SEED = 1 N_stations:=2 N_gNB:=2  CW_MIN = 15 CW_MAX = 63 WiFi pcol:=0.1217 WiFi cot:=0.8879164 WiFi eff:=0.88074 gNB pcol:=0.0000 gNB cot:=0.0354 gNB eff:=0.0354  all cot:=0.9233164 all eff:=0.91614
 Wifi succ: 1631 fail: 226
 NR succ: 59 fail: 0
fairness: 0.5398053473945499
joint: 0.4984111300570852
```



### Changing number of nodes

Running simulations in which number of Wi-Fi nodes (AP) is equal to number of NR-U nodes (gNB), and is increasing in every step from start to the end value (can be repeated with different seeds)

```bash
python changingNodesNumber.py --help
Usage: changingNodesNumber.py [OPTIONS]

Options:
  -r, --runs INTEGER              Number of simulation runs
  --seed INTEGER                  Seed for simulation
  --start_node_number INTEGER     Starting number of Wi-Fi and NR-U nodes
                                  [required]
  --end_node_number INTEGER       Ending number of Wi-Fi and NR-U nodes
                                  [required]
  -t, --simulation-time FLOAT     Duration of the simulation per stations
                                  number in s
  --wifi_cw_min INTEGER           Size of Wi-Fi cw min
  --wifi_cw_max INTEGER           Size of Wi-Fi cw max
  --nru_cw_min INTEGER            Size of NR-U cw min
  --nru_cw_max INTEGER            Size of NR-U cw max
  --wifi_r_limit INTEGER          Number of failed transmissions in a row
  -m, --mcs-value INTEGER         Value of mcs
  -syn_slot, --synchronization_slot_duration INTEGER
                                  Synchronization slot length in mikrosecounds
  -max_des, --max_sync_slot_desync INTEGER
                                  Max value of gNB desynchronization
  -min_des, --min_sync_slot_desync INTEGER
                                  Min value of gNB desynchronization
  -nru_obser_slots, --nru_observation_slot INTEGER
                                  amount of observation slots for NR_U
  --mcot INTEGER                  Max channel occupancy time for NR-U (ms)
  --help                          Show this message and exit.

```

##### Usage
```bash
python changingNodesNumber.py --start_node_number 1 --end_node_number 2 -t 10 -r 1
SEED = 1 N_stations:=1 N_gNB:=1  CW_MIN = 15 CW_MAX = 63 WiFi pcol:=0.0006 WiFi cot:=0.955422 WiFi eff:=0.9477 gNB pcol:=0.0244 gNB cot:=0.024 gNB eff:=0.024  all cot:=0.979422 all eff:=0.9717
 Wifi succ: 1755 fail: 1
 NR succ: 40 fail: 1
fairness: 0.5251039493099016
joint: 0.5142983602410024
SEED = 1 N_stations:=2 N_gNB:=2  CW_MIN = 15 CW_MAX = 63 WiFi pcol:=0.1217 WiFi cot:=0.8879164 WiFi eff:=0.88074 gNB pcol:=0.0000 gNB cot:=0.0354 gNB eff:=0.0354  all cot:=0.9233164 all eff:=0.91614
 Wifi succ: 1631 fail: 226
 NR succ: 59 fail: 0
fairness: 0.5398053473945499
joint: 0.4984111300570852
```



