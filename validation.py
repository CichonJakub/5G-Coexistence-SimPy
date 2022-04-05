import pandas as pd
import matplotlib.pyplot as plt

import numpy as np
import matplotlib as mpl
from matplotlib import cm

import cycler

# n = 4
# color = mpl.cm.viridis(np.linspace(0.0, 1.0, n))


def viridis(a, b, color_amount):
    color = mpl.cm.viridis(np.linspace(a, b, color_amount))
    mpl.rcParams['axes.prop_cycle'] = cycler.cycler('color', color)



def valid_wifi_pcol():
    viridis(0.0, 1.0, 3)

    coex5g = pd.read_csv('val/coex5g_wifi_63.csv', delimiter=',')
    matlab = pd.read_csv('val/matlab_wifi_val_63.csv', delimiter=',')
    dcf = pd.read_csv('val/DCF_valid_63.csv', delimiter=',')


    coex5g_pcol = coex5g.groupby(['WiFi'])['PcolWifi'].mean()
    matlab_pcol = matlab.groupby(['nWifi'])['pcWifi'].mean()
    dcf_pcol = dcf.groupby(['Stations'])['Pcol'].mean()


    ax = coex5g_pcol.plot(marker="o", legend=True,  ylim=(0, 0.5))
    ax = matlab_pcol.plot(marker="x", legend=True,  ylim=(0, 0.5), linestyle='--')
    ax = dcf_pcol.plot(marker="v", legend=True,  ylim=(0, 0.5), linestyle=':')

    ax.legend(['5G-Coex-SimPy', 'Matlab', 'DCF-SimPy'])
    ax.set_xlabel('Number of Wifi nodes', fontsize=14)
    ax.set_ylabel('Collision probability', fontsize=14)

    plt.tight_layout()
    plt.savefig('val/wifi_pcol_63.svg')


def valid_wifi():
    viridis(0.0, 1.0, 6)

    coex5g = pd.read_csv('val/coex5g_wifi_63.csv', delimiter=',')
    matlab = pd.read_csv('val/matlab_wifi_val_63.csv', delimiter=',')
    dcf = pd.read_csv('val/DCF_valid_63.csv', delimiter=',')

    coex5g_cot = coex5g.groupby(['WiFi'])['ChannelOccupancyWiFi'].mean()
    coex5g_eff = coex5g.groupby(['WiFi'])['ChannelEfficiencyWiFi'].mean()


    matlab_cot = matlab.groupby(['nWifi'])['cotWifi'].mean()
    matalb_eff = matlab.groupby(['nWifi'])['effWifi'].mean()

    dcf_cot = dcf.groupby(['Stations'])['Occupancy'].mean()
    dcf_eff = dcf.groupby(['Stations'])['Efficiency'].mean()

    ax = coex5g_cot.plot(marker="o", legend=True,  ylim=(0.6, 1))
    ax = coex5g_eff.plot(marker="o", legend=True, ylim=(0.6, 1))
    ax = matlab_cot.plot(marker="x", legend=True,  ylim=(0.6, 1), linestyle='--')
    ax = matalb_eff.plot(marker="x", legend=True, ylim=(0.6, 1), linestyle='--')
    ax = dcf_cot.plot(marker="v", legend=True, ylim=(0.6, 1), linestyle=':')
    ax = dcf_eff.plot(marker="v", legend=True, ylim=(0.6, 1), linestyle=':')

    ax.legend(['5G-Coex-SimPy cot', '5G-Coex-SimPy eff', 'Matlab cot', 'Matlab eff', 'DCF-SimPY cot', 'DCF-SimPy eff'])
    ax.set_xlabel('Number of Wifi nodes', fontsize=14)
    ax.set_ylabel('Channel occupation time', fontsize=14)

    plt.tight_layout()
    plt.savefig('val/wifi_airtime_63.svg')


def valid_nru_pcol():
    viridis(0.0, 1.0, 3)

    coex5g = pd.read_csv('val/coex5g_rs_1023.csv', delimiter=',')
    matlab = pd.read_csv('val/matlab_rs_1023.csv', delimiter=',')
    nru = pd.read_csv('val/nru_rs_1023.csv', delimiter=',')


    coex5g_pcol = coex5g.groupby(['Gnb'])['PcolNR'].mean()
    matlab_pcol = matlab.groupby(['nLAA'])['pcLAA'].mean()
    nru_pcol = nru.groupby(['N_sta'])['pc'].mean()


    ax = coex5g_pcol.plot(marker="o", legend=True,  ylim=(0, 0.5))
    ax = matlab_pcol.plot(marker="x", legend=True,  ylim=(0, 0.5), linestyle='--')
    ax = nru_pcol.plot(marker="v", legend=True,  ylim=(0, 0.5), linestyle=':')

    ax.legend(['5G-Coex-SimPy', 'Matlab', 'NRU-SimPy'])
    ax.set_xlabel('Number of gNBs', fontsize=14)
    ax.set_ylabel('Collision probability', fontsize=14)

    plt.tight_layout()
    plt.savefig('val/rs_pcol_1023.svg')

def valid_nru():
    viridis(0.0, 1.0, 5)

    coex5g = pd.read_csv('val/coex5g_rs_63.csv', delimiter=',')
    matlab = pd.read_csv('val/matlab_rs_63.csv', delimiter=',')
    nru = pd.read_csv('val/nru_rs_63.csv', delimiter=',')

    coex5g_cot = coex5g.groupby(['Gnb'])['ChannelOccupancyNR'].mean()
    coex5g_eff = coex5g.groupby(['Gnb'])['ChannelEfficiencyNR'].mean()


    matlab_cot = matlab.groupby(['nLAA'])['cotLAA'].mean()
    matalb_eff = matlab.groupby(['nLAA'])['effLAA'].mean()

    #nru_cot = nru.groupby(['N_sta'])['occ'].mean()
    nru_eff = nru.groupby(['N_sta'])['eff'].mean()

    ax = coex5g_cot.plot(marker="o", legend=True,  ylim=(0.6, 1))
    ax = coex5g_eff.plot(marker="o", legend=True, ylim=(0.6, 1))
    ax = matlab_cot.plot(marker="x", legend=True,  ylim=(0.6, 1), linestyle='--')
    ax = matalb_eff.plot(marker="x", legend=True, ylim=(0.6, 1), linestyle='--')
    #ax = nru_cot.plot(marker="v", legend=True, ylim=(0.6, 1), linestyle=':')
    ax = nru_eff.plot(marker="v", legend=True, ylim=(0.6, 1), linestyle=':')

    ax.legend(['5G-Coex-SimPy cot', '5G-Coex-SimPy eff', 'Matlab cot', 'Matlab eff', 'NRU-SimPy eff'])
    ax.set_xlabel('Number of gNBs', fontsize=14)
    ax.set_ylabel('Channel occupation time', fontsize=14)

    plt.tight_layout()
    plt.savefig('val/rs_airtime_63.svg')


if __name__ == "__main__":
    # valid_wifi_pcol()
    valid_nru_pcol()




