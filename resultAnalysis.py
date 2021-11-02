import pandas as pd
import matplotlib.pyplot as plt

import numpy as np
import matplotlib as mpl
from matplotlib import cm

import cycler

n = 4
color = mpl.cm.viridis(np.linspace(0.0, 1.0, n))


def viridis(a, b, color_amount):
    color = mpl.cm.viridis(np.linspace(a, b, n))
    mpl.rcParams['axes.prop_cycle'] = cycler.cycler('color', color)

def print_collision_prob():
    # read data from csv

    viridis(0.3, 1.0, 2)

    data = pd.read_csv('results.csv', delimiter=',')
    data2 = pd.read_csv('results2.csv', delimiter=',')

    # group by number of stations and calculate mean colision proob
    data = data.groupby(['Stations'])['Colisions'].mean()
    data2 = data2.groupby(['Stations'])['Colisions'].mean()

    # plotting
    # 5G _ JC
    ax = data.plot(title='5G_Coexistance vs DCF simulators', marker='o', legend=True, ylim=(0, 40))
    # DCF - PT
    ax2 = data2.plot(title='5G_Coexistance vs DCF simulators', marker='x', legend=True, ylim=(0, 40))
    ax2.legend(['5G-Coex-SimPy', 'DCF-SimPy'])
    ax.set_xlabel('Number of transmitting Wi-Fi stations', fontsize=14)
    ax.set_ylabel('Collision probability', fontsize=14)

    # Save to file
    plt.tight_layout()
    plt.savefig('results/colisonProbability.png')

def print_airtime_34():
    # read data from csv
    viridis(0.0, 1.0, 4)

    data = pd.read_csv('airtime34.csv', delimiter=',')
    data_dcf = pd.read_csv('DCF_airtime34.csv', delimiter=',')
    # data2 = pd.read_csv('results2.csv', delimiter=',')

    # group by number of stations and calculate mean colision proob
    data2 = data.groupby(['Stations'])['ChannelOccupancy'].mean()
    data3 = data.groupby(['Stations'])['ChannelEfficiency'].mean()

    data2dcf = data_dcf.groupby(['Stations'])['Occupancy'].mean()
    data3dcf = data_dcf.groupby(['Stations'])['Efficiency'].mean()
    # data2 = data2.groupby(['Stations'])['Colisions'].mean()

    # plotting
    # 5G _ JC
    ax = data2.plot(title='Airtime 5G-Coexistance-Simpy vs DCF-Simpy', marker='o', legend=True, ylim=(0, 1))
    ax2 = data3.plot(title='Airtime 5G-Coexistance-Simpy vs DCF-Simpy', marker='o', legend=True, ylim=(0, 1))

    ax3 = data2dcf.plot(title='Airtime 5G-Coexistance-Simpy vs DCF-Simpy', marker='x', legend=True, ylim=(0, 1), linestyle= '--')
    ax4 = data3dcf.plot(title='Airtime 5G-Coexistance-Simpy vs DCF-Simpy', marker='x', legend=True, ylim=(0, 1), linestyle= '--')

    ax2.legend(['5G-Coex-SimPy occupancy', '5G-Coex-SimPy efficiency', 'DCF-SimPy occupancy', 'DCF-SimPy efficiency' ])
    ax2.set_xlabel('Number of transmitting Wi-Fi stations', fontsize=14)
    ax2.set_ylabel('Normalized airtime', fontsize=14)

    # # DCF - PT
    # ax2 = data2.plot(title='5G_Coexistance vs DCF simulators', marker='x', legend=True, ylim=(0, 40))
    # ax2.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="Collision probability")
    # ax2.legend(['5G-Coexistance-Simpy', 'DCF-Simpy'])

    # Save to file
    plt.tight_layout()
    plt.savefig('results/airtime_efficiency_and_occupancy.png')


def print_channel_occupancy():
    viridis(0.2, 1.0, 2)

    # read data from csv
    data = pd.read_csv('airtime34.csv', delimiter=',')
    data_dcf = pd.read_csv('DCF_airtime34.csv', delimiter=',')
    # data2 = pd.read_csv('results2.csv', delimiter=',')

    # group by number of stations and calculate mean colision proob
    data2 = data.groupby(['Stations'])['ChannelOccupancy'].mean()
    data2dcf = data_dcf.groupby(['Stations'])['Occupancy'].mean()
    # plotting
    # 5G _ JC
    ax = data2.plot(title='Airtime 5G-Coexistance-Simpy vs DCF-Simpy', marker='o', legend=True, ylim=(0, 1))


    #ax2.legend(['Normalized Channel Occupancy', 'Channel Efficiency'])

    ax3 = data2dcf.plot(title='Airtime 5G-Coexistance-Simpy vs DCF-Simpy', marker='x', legend=True, ylim=(0, 1), linestyle= '--')


    ax.set_xlabel('Number of transmitting Wi-Fi stations', fontsize=14)
    ax.set_ylabel('Channel occupancy time', fontsize=14)
    ax3.set_xlabel('Number of transmitting Wi-Fi stations', fontsize=14)
    ax3.set_ylabel('Channel occupancy time', fontsize=14)

    ax3.legend(['5G-Coex-SimPy occupancy', 'DCF-SimPy occupancy'])
    # Save to file
    plt.tight_layout()
    plt.savefig('results/channel_occupancy.png')


def print_channel_efficency():
    viridis(0.2, 1.0, 2)

    # read data from csv
    data = pd.read_csv('airtime34.csv', delimiter=',')
    data_dcf = pd.read_csv('DCF_airtime34.csv', delimiter=',')
    # data2 = pd.read_csv('results2.csv', delimiter=',')

    # group by number of stations and calculate mean colision proob
    data3 = data.groupby(['Stations'])['ChannelEfficiency'].mean()
    data3dcf = data_dcf.groupby(['Stations'])['Efficiency'].mean()
    # data2 = data2.groupby(['Stations'])['Colisions'].mean()

    # plotting
    # 5G _ JC
    ax2 = data3.plot(title='Airtime 5G-Coexistance-Simpy vs DCF-Simpy', marker='o', legend=True, ylim=(0, 1))
    ax2.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="% of time")

    ax4 = data3dcf.plot(title='Airtime 5G-Coexistance-Simpy vs DCF-Simpy', marker='x', legend=True, ylim=(0, 1), linestyle= '--')

    ax4.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="Normalized airtime")
    ax2.legend(['5G-Coex-SimPy efficiency','DCF-SimPy efficiency'])

    ax2.set_xlabel('Number of transmitting Wi-Fi stations', fontsize=14)
    ax2.set_ylabel('Channel efficiency time', fontsize=14)
    ax4.set_xlabel('Number of transmitting Wi-Fi stations', fontsize=14)
    ax4.set_ylabel('Channel efficiency time', fontsize=14)

    # Save to file
    plt.tight_layout()
    plt.savefig('results/channel_efficiency.png')

def print_airtime_norm_per_station():
    viridis(0.5, 1.0, 10)
    # read data from csv
    data = pd.read_csv('airtime12_new2.csv', delimiter=',')
    # data2 = pd.read_csv('results2.csv', delimiter=',')

    # group by number of stations and calculate mean colision proob
    data2 = data.groupby(['Num'])['NormPerStation'].mean()

    # plotting
    # 5G _ JC
    ax = data2.plot.bar(title='Per station normalized airtime', legend=False, ylim=(0, 1))
    #ax.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="% of time")
    ax.set_xlabel('Number of transmitting Wi-Fi stations', fontsize=14)
    ax.set_ylabel('Mean normalized airtime', fontsize=14)

    # Save to file
    plt.tight_layout()
    plt.savefig('results/normalized_airtime_per_station.png')

def print_airtime_per_station():
    viridis(0.0, 1.0, 10)
    # read data from csv
    data = pd.read_csv('airtime12_new2.csv', delimiter=',')
    # data2 = pd.read_csv('results2.csv', delimiter=',')

    # group by number of stations and calculate mean colision proob
    data2 = data.groupby(['Num'])['PerStation'].mean()

    # plotting
    # 5G _ JC
    ax = data2.plot.bar(title='Per station airtime', legend=False, ylim=(0, 100))
    #ax.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="% of time")
    ax.set_xlabel('Number of transmitting Wi-Fi stations', fontsize=14)
    ax.set_ylabel('Mean airtime', fontsize=14)

    # Save to file
    plt.tight_layout()
    plt.savefig('results/airtime_per_station.png')


def print_nru_airtime():
    # read data from csv
    viridis(0.0, 1.0, 4)

    data = pd.read_csv('nru_airtime2.csv', delimiter=',')

    # group by number of stations and calculate mean colision proob
    data2 = data.groupby(['Gnb'])['ChannelOccupancy'].mean()
    data3 = data.groupby(['Gnb'])['ChannelEfficiency'].mean()



    # plotting
    # 5G _ JC
    ax = data2.plot(title='NR-U airtime', marker='o', legend=True, ylim=(0, 1))
    ax2 = data3.plot(title='NR-U airtime', marker='x', legend=True, ylim=(0, 1))



    ax2.legend(['NR-U occupancy', 'NR-U efficiency'])
    ax2.set_xlabel('Number of transmitting Gnbs', fontsize=14)
    ax2.set_ylabel('Normalized airtime', fontsize=14)

    # # DCF - PT
    # ax2 = data2.plot(title='5G_Coexistance vs DCF simulators', marker='x', legend=True, ylim=(0, 40))
    # ax2.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="Collision probability")
    # ax2.legend(['5G-Coexistance-Simpy', 'DCF-Simpy'])

    # Save to file
    plt.tight_layout()
    plt.savefig('results/nru_airtime4.png')

if __name__ == "__main__":
    #print_collision_prob()
    #print_airtime_34()
    #print_airtime_norm_per_station()
    #print_airtime_per_station()
    #print_channel_occupancy()
    #print_channel_efficency()

    print_nru_airtime()
