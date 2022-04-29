import pandas as pd
import matplotlib.pyplot as plt

import numpy as np
import matplotlib as mpl
from matplotlib import cm

import cycler

import scipy.stats as st
# n = 4
# color = mpl.cm.viridis(np.linspace(0.0, 1.0, n))


def viridis(a, b, color_amount):
    color = mpl.cm.viridis(np.linspace(a, b, color_amount))
    mpl.rcParams['axes.prop_cycle'] = cycler.cycler('color', color)



def valid_wifi_pcol():
    viridis(0.0, 1.0, 3)

    coex5g = pd.read_csv('val/coex5g_wifi_63v2.csv', delimiter=',')
    matlab = pd.read_csv('val/matlab_wifi_63v2.csv', delimiter=',')
    dcf = pd.read_csv('val/DCF_valid_63v2.csv', delimiter=',')


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
    plt.savefig('val/wifi_pcol_63v2.svg')


def valid_wifi():
    viridis(0.0, 1.0, 8)

    coex5g = pd.read_csv('val/coex5g_wifi_1023.csv', delimiter=',')
    matlab = pd.read_csv('val/matlab_wifi_val_1023.csv', delimiter=',')
    dcf = pd.read_csv('val/DCF_valid_1023.csv', delimiter=',')

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
    plt.savefig('val/wifi_airtime_1023v2.svg')


def valid_nru_pcol():
    viridis(0.0, 1.0, 3)

    coex5g = pd.read_csv('val/coex5g_gap_63.csv', delimiter=',')
    matlab = pd.read_csv('val/matlab_gap_63.csv', delimiter=',')
    nru = pd.read_csv('val/nru_gap_63.csv', delimiter=',')


    coex5g_pcol = coex5g.groupby(['Gnb'])['PcolNR'].mean()
    matlab_pcol = matlab.groupby(['nLAA'])['pcLAA'].mean()
    nru_pcol = nru.groupby(['N_sta'])['pc'].mean()


    ax = coex5g_pcol.plot(marker="o", legend=True,  ylim=(0, 0.1))
    ax = matlab_pcol.plot(marker="x", legend=True,  ylim=(0, 0.1), linestyle='--')
    ax = nru_pcol.plot(marker="v", legend=True,  ylim=(0, 0.1), linestyle=':')

    ax.legend(['5G-Coex-SimPy', 'Matlab', 'NRU-SimPy'])
    ax.set_xlabel('Number of gNBs', fontsize=14)
    ax.set_ylabel('Collision probability', fontsize=14)

    plt.tight_layout()
    plt.savefig('val/gap_pcol_63.svg')

def valid_nru():
    viridis(0.0, 1.0, 7)

    coex5g = pd.read_csv('val/coex5g_rs_1023.csv', delimiter=',')
    matlab = pd.read_csv('val/matlab_rs_1023.csv', delimiter=',')
    nru = pd.read_csv('val/nru_rs_1023.csv', delimiter=',')
    coex5g2 = pd.read_csv('val/coex5g_rs_1023v2.csv', delimiter=',')

    coex5g_cot = coex5g.groupby(['Gnb'])['ChannelOccupancyNR'].mean()
    coex5g_eff = coex5g.groupby(['Gnb'])['ChannelEfficiencyNR'].mean()

    coex5g_cot2 = coex5g2.groupby(['Gnb'])['ChannelOccupancyNR'].mean()
    coex5g_eff2 = coex5g2.groupby(['Gnb'])['ChannelEfficiencyNR'].mean()

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

    ax = coex5g_cot2.plot(marker="o", legend=True, ylim=(0.6, 1))
    ax = coex5g_eff2.plot(marker="o", legend=True, ylim=(0.6, 1))

    ax.legend(['5G-Coex-SimPy cot', '5G-Coex-SimPy eff', 'Matlab cot', 'Matlab eff', 'NRU-SimPy eff', '5G-Coex-SimPy2 cot', '5G-Coex-SimPy2 eff'])
    ax.set_xlabel('Number of gNBs', fontsize=14)
    ax.set_ylabel('Channel occupation time', fontsize=14)

    plt.tight_layout()
    plt.savefig('val/rs_airtime_1023v2.svg')

def valid_nru_pcol_gap():
    viridis(0.0, 1.0, 3)

    coex5g = pd.read_csv('val/coex5g_gap_63v2.csv', delimiter=',')
    matlab = pd.read_csv('val/matlab_gap_63.csv', delimiter=',')
    nru = pd.read_csv('val/nru_gap_63.csv', delimiter=',')


    coex5g_pcol = coex5g.groupby(['Gnb'])['PcolNR'].mean()
    matlab_pcol = matlab.groupby(['nNR'])['pcNR'].mean()
    nru_pcol = nru.groupby(['N_sta'])['pc'].mean()


    ax = coex5g_pcol.plot(marker="o", legend=True,  ylim=(0, 0.1))
    ax = matlab_pcol.plot(marker="x", legend=True,  ylim=(0, 0.1), linestyle='--')
    ax = nru_pcol.plot(marker="v", legend=True,  ylim=(0, 0.1), linestyle=':')

    ax.legend(['5G-Coex-SimPy', 'Matlab', 'NRU-SimPy'])
    ax.set_xlabel('Number of gNBs', fontsize=14)
    ax.set_ylabel('Collision probability', fontsize=14)

    plt.tight_layout()
    plt.savefig('val/gap_pcol_63v2.svg')

def valid_nru_gap():
    viridis(0.0, 1.0, 3)

    coex5g = pd.read_csv('val/coex5g_gap_1023v2.csv', delimiter=',')
    matlab = pd.read_csv('val/matlab_gap_1023.csv', delimiter=',')
    nru = pd.read_csv('val/nru_gap_1023.csv', delimiter=',')

    coex5g_cot = coex5g.groupby(['Gnb'])['ChannelOccupancyNR'].mean()

    matalb_eff = matlab.groupby(['nNR'])['effNR'].mean()

    nru_eff = nru.groupby(['N_sta'])['eff'].mean()

    ax = coex5g_cot.plot(marker="o", legend=True,  ylim=(0.6, 1))
    ax = matalb_eff.plot(marker="x", legend=True, ylim=(0.6, 1), linestyle='--')
    #ax = nru_cot.plot(marker="v", legend=True, ylim=(0.6, 1), linestyle=':')
    ax = nru_eff.plot(marker="v", legend=True, ylim=(0.6, 1), linestyle=':')

    ax.legend(['5G-Coex-SimPy cot', 'Matlab cot', 'NRU-SimPy cot'])
    ax.set_xlabel('Number of gNBs', fontsize=14)
    ax.set_ylabel('Channel occupation time', fontsize=14)

    plt.tight_layout()
    plt.savefig('val/gap_airtime_1023v2.svg')


def calc():
    alpha = 0.05

    wifi = pd.read_csv('val/coex5g_gap_1023.csv', delimiter=',')

    std = wifi.groupby('Gnb').std().loc[:, 'ChannelOccupancyNR']
    var = wifi.groupby('Gnb').var().loc[:, 'ChannelOccupancyNR']
    n = wifi.groupby('Gnb').count().loc[:, 'ChannelOccupancyNR']
    # Calculate confidence intervals
    yerr = std / np.sqrt(n) * st.t.ppf(1 - alpha / 2, n - 1)


    print(std)
    print(var)
    print(yerr)


def coex():
    viridis(0.0, 1.0, 4)

    coex5g = pd.read_csv('val/coex5g_wifi_gap_1023.csv', delimiter=',')
    matlab = pd.read_csv('val/matlab_wifi_gap_1023.csv', delimiter=',')

    coex5g_cot = coex5g.groupby(['Gnb'])['ChannelOccupancyNR'].mean()
    matalb_cot = matlab.groupby(['nNR'])['cotNR'].mean()

    coex5g_cot2 = coex5g.groupby(['WiFi'])['ChannelOccupancyWiFi'].mean()
    matlab_cot2 = matlab.groupby(['nWifi'])['cotWifi'].mean()


    ax = coex5g_cot.plot(marker="o", legend=True, ylim=(0, 1))
    ax = coex5g_cot2.plot(marker="o", legend=True, ylim=(0, 1))
    ax = matalb_cot.plot(marker="x", legend=True, ylim=(0, 1), linestyle='--')
    ax = matlab_cot2.plot(marker="x", legend=True, ylim=(0, 1), linestyle='--')


    ax.legend(['5G-Coex-SimPy NR-U cot', '5G-Coex-SimPy Wi-Fi cot', 'Matlab NR-U cot', 'Matlab Wi-Fi cot'])
    #ax.legend(['5G-Coex-SimPy NR-U cot', '5G-Coex-SimPy Wi-Fi cot'])
    ax.set_xlabel('Number of gNBs/stations', fontsize=14)
    ax.set_ylabel('Channel occupation time', fontsize=14)

    plt.tight_layout()
    plt.savefig('val/coex_airtime_1023v2.svg')

def coex2():
    viridis(0.0, 1.0, 4)

    coex5g = pd.read_csv('val/coex5g_wifi_gap_1023.csv', delimiter=',')
    matlab = pd.read_csv('val/matlab_wifi_gap_1023.csv', delimiter=',')

    coex5g_cot = coex5g.groupby(['Gnb'])['ChannelEfficiencyNR'].mean()
    matalb_cot = matlab.groupby(['nNR'])['effNR'].mean()

    coex5g_cot2 = coex5g.groupby(['WiFi'])['ChannelEfficiencyWiFi'].mean()
    matlab_cot2 = matlab.groupby(['nWifi'])['effWifi'].mean()


    ax = coex5g_cot.plot(marker="o", legend=True, ylim=(0, 1))
    ax = coex5g_cot2.plot(marker="o", legend=True, ylim=(0, 1))
    ax = matalb_cot.plot(marker="x", legend=True, ylim=(0, 1), linestyle='--')
    ax = matlab_cot2.plot(marker="x", legend=True, ylim=(0, 1), linestyle='--')


    ax.legend(['5G-Coex-SimPy NR-U eff', '5G-Coex-SimPy Wi-Fi eff', 'Matlab NR-U eff', 'Matlab Wi-Fi eff'])
    #ax.legend(['5G-Coex-SimPy NR-U cot', '5G-Coex-SimPy Wi-Fi cot'])
    ax.set_xlabel('Number of gNBs/stations', fontsize=14)
    ax.set_ylabel('Channel occupation time', fontsize=14)

    plt.tight_layout()
    plt.savefig('val/coex_airtime_eff_1023v2.svg')


def coex_rs():
    viridis(0.0, 1.0, 4)

    coex5g = pd.read_csv('val/coex5g_wifi_rs_63.csv', delimiter=',')
    matlab = pd.read_csv('val/matlab_wifi_rs_63.csv', delimiter=',')

    coex5g_cot = coex5g.groupby(['Gnb'])['ChannelEfficiencyNR'].mean()
    matalb_cot = matlab.groupby(['nLAA'])['effLAA'].mean()

    coex5g_cot2 = coex5g.groupby(['WiFi'])['ChannelEfficiencyWiFi'].mean()
    matlab_cot2 = matlab.groupby(['nWifi'])['effWifi'].mean()


    ax = coex5g_cot.plot(marker="o", legend=True, ylim=(0, 1))
    ax = coex5g_cot2.plot(marker="o", legend=True, ylim=(0, 1))
    ax = matalb_cot.plot(marker="x", legend=True, ylim=(0, 1), linestyle='--')
    ax = matlab_cot2.plot(marker="x", legend=True, ylim=(0, 1), linestyle='--')


    ax.legend(['5G-Coex-SimPy NR-U eff', '5G-Coex-SimPy Wi-Fi eff', 'Matlab NR-U eff', 'Matlab Wi-Fi eff'])
    #ax.legend(['5G-Coex-SimPy NR-U cot', '5G-Coex-SimPy Wi-Fi cot'])
    ax.set_xlabel('Number of gNBs/stations', fontsize=14)
    ax.set_ylabel('Channel occupation time', fontsize=14)

    plt.tight_layout()
    plt.savefig('val/coex_airtime_rs_63.svg')


def coex_pcol():
    viridis(0.0, 1.0, 4)

    coex5g = pd.read_csv('val/coex5g_coex_1023.csv', delimiter=',')
    matlab = pd.read_csv('val/matlab_coexGap_1023.csv', delimiter=',')


    coex5g_pcol = coex5g.groupby(['Gnb'])['PcolNR'].mean()
    matlab_pcol = matlab.groupby(['nNR'])['pcNR'].mean()
    coex5g_pcol2 = coex5g.groupby(['WiFi'])['PcolWifi'].mean()
    matlab_pcol2 = matlab.groupby(['nWifi'])['pcWifi'].mean()

    ax = coex5g_pcol.plot(marker="o", legend=True, ylim=(0, 0.5))
    ax = coex5g_pcol2.plot(marker="o", legend=True, ylim=(0, 0.5))
    ax = matlab_pcol.plot(marker="x", legend=True, ylim=(0, 0.5), linestyle='--')
    ax = matlab_pcol2.plot(marker="x", legend=True, ylim=(0, 0.5), linestyle='--')


    ax.legend(['5G-Coex-SimPy NR-U','5G-Coex-SimPy Wi-Fi', 'Matlab NR-U', 'Matlab Wi-Fi'])
    # ax.legend(['5G-Coex-SimPy NR-U', '5G-Coex-SimPy Wi-Fi'])
    ax.set_xlabel('Number of gNBs/stations', fontsize=14)
    ax.set_ylabel('Collision probability', fontsize=14)

    plt.tight_layout()
    plt.savefig('val/coex_pcol_1023.svg')



def coexistence_rs():
        viridis(0.0, 1.0, 8)

        coex5g = pd.read_csv('val/coex/coex5g_coexistence_rs_63v4.csv', delimiter=',')
        #coex5g = pd.read_csv('val/coex/coex5g_coexistence_rs_63.csv', delimiter=',')
        matlab = pd.read_csv('val/coex/matlab_coexistence_rs_63_6ms.csv', delimiter=',')

        coex5g_eff_nru = coex5g.groupby(['Gnb'])['ChannelEfficiencyNR'].mean()
        matalb_eff_nru = matlab.groupby(['nLAA'])['effLAA'].mean()

        coex5g_eff_wifi = coex5g.groupby(['WiFi'])['ChannelEfficiencyWiFi'].mean()
        matlab_eff_wifi = matlab.groupby(['nWifi'])['effWifi'].mean()




        coex5g_cot_nru = coex5g.groupby(['Gnb'])['ChannelOccupancyNR'].mean()
        matalb_cot_nru = matlab.groupby(['nLAA'])['cotLAA'].mean()

        coex5g_cot_wifi = coex5g.groupby(['WiFi'])['ChannelOccupancyWiFi'].mean()
        matlab_cot_wifi = matlab.groupby(['nWifi'])['cotWifi'].mean()

        ax = coex5g_cot_nru.plot(marker="o", legend=True, ylim=(0, 1))
        ax = coex5g_cot_wifi.plot(marker="o", legend=True, ylim=(0, 1), linestyle='--')

        ax = coex5g_eff_nru.plot(marker="o", legend=True, ylim=(0, 1))
        ax = coex5g_eff_wifi.plot(marker="o", legend=True, ylim=(0, 1), linestyle='--')

        ax = matalb_cot_nru.plot(marker="x", legend=True, ylim=(0, 1))
        ax = matlab_cot_wifi.plot(marker="x", legend=True, ylim=(0, 1), linestyle='--')

        ax = matalb_eff_nru.plot(marker="x", legend=True, ylim=(0, 1))
        ax = matlab_eff_wifi.plot(marker="x", legend=True, ylim=(0, 1), linestyle='--')

        ax.legend(['5G-Coex-SimPy NR-U cot', '5G-Coex-SimPy Wi-Fi cot','5G-Coex-SimPy NR-U eff', '5G-Coex-SimPy Wi-Fi eff', 'Matlab NR-U cot', 'Matlab Wi-Fi cot', 'Matlab NR-U eff', 'Matlab Wi-Fi eff'])
        # ax.legend(['5G-Coex-SimPy NR-U cot', '5G-Coex-SimPy Wi-Fi cot'])
        ax.set_xlabel('Number of gNBs/stations', fontsize=14)
        ax.set_ylabel('Channel occupation time', fontsize=14)

        plt.tight_layout()
        plt.savefig('val/coex/coexistence_rs_63_6ms.svg')


def coexistence_rs_pcol():
    viridis(0.0, 1.0, 4)

    coex5g = pd.read_csv('val/coex/coex5g_coexistence_rs_63debuged.csv', delimiter=',')
    matlab = pd.read_csv('val/coex/matlab_coexistence_rs_63.csv', delimiter=',')

    coex5g_pc_nru = coex5g.groupby(['Gnb'])['PcolNR'].mean()
    matalb_pc_nru = matlab.groupby(['nLAA'])['pcLAA'].mean()

    coex5g_pc_wifi = coex5g.groupby(['WiFi'])['PcolWifi'].mean()
    matlab_pc_wifi = matlab.groupby(['nWifi'])['pcWifi'].mean()


    ax = coex5g_pc_nru.plot(marker="o", legend=True, ylim=(0, 1))
    ax = coex5g_pc_wifi.plot(marker="o", legend=True, ylim=(0, 1))

    ax = matalb_pc_nru.plot(marker="x", legend=True, ylim=(0, 1), linestyle='--')
    ax = matlab_pc_wifi.plot(marker="x", legend=True, ylim=(0, 1), linestyle='--')

    ax.legend(['5G-Coex-SimPy NR-U pcol', '5G-Coex-SimPy Wi-Fi pcol',
               'Matlab NR-U pcol', 'Matlab Wi-Fi pcol'])
    # ax.legend(['5G-Coex-SimPy NR-U cot', '5G-Coex-SimPy Wi-Fi cot'])
    ax.set_xlabel('Number of gNBs/stations', fontsize=14)
    ax.set_ylabel('Collision probability', fontsize=14)

    plt.tight_layout()
    plt.savefig('val/coex/coexistence_rs_63_pcol_ok.svg')

def coexistence_gap():
    viridis(0.0, 1.0, 6)

    coex5g = pd.read_csv('val/coex/coex5g_coexistence_gap_63.csv', delimiter=',')
    matlab = pd.read_csv('val/coex/matlab_coexistence_gap_63v2.csv', delimiter=',')


    coex5g_eff_wifi = coex5g.groupby(['WiFi'])['ChannelEfficiencyWiFi'].mean()
    matlab_eff_wifi = matlab.groupby(['nWifi'])['effWifi'].mean()

    coex5g_cot_nru = coex5g.groupby(['Gnb'])['ChannelOccupancyNR'].mean()
    matalb_cot_nru = matlab.groupby(['nNR'])['cotNR'].mean()

    coex5g_cot_wifi = coex5g.groupby(['WiFi'])['ChannelOccupancyWiFi'].mean()
    matlab_cot_wifi = matlab.groupby(['nWifi'])['cotWifi'].mean()

    ax = coex5g_cot_nru.plot(marker="o", legend=True, ylim=(0, 1))
    ax = coex5g_cot_wifi.plot(marker="o", legend=True, ylim=(0, 1), linestyle='--')

    ax = coex5g_eff_wifi.plot(marker="o", legend=True, ylim=(0, 1), linestyle='--')

    ax = matalb_cot_nru.plot(marker="x", legend=True, ylim=(0, 1),)
    ax = matlab_cot_wifi.plot(marker="x", legend=True, ylim=(0, 1), linestyle='--')

    ax = matlab_eff_wifi.plot(marker="x", legend=True, ylim=(0, 1), linestyle='--')

    ax.legend(['5G-Coex-SimPy NR-U cot', '5G-Coex-SimPy Wi-Fi cot', '5G-Coex-SimPy Wi-Fi eff',
               'Matlab NR-U cot', 'Matlab Wi-Fi cot', 'Matlab Wi-Fi eff'])
    # ax.legend(['5G-Coex-SimPy NR-U cot', '5G-Coex-SimPy Wi-Fi cot'])
    ax.set_xlabel('Number of gNBs/stations', fontsize=14)
    ax.set_ylabel('Channel occupation time', fontsize=14)

    plt.tight_layout()
    plt.savefig('val/coex/coexistence_gap_63.svg')

def coexistence_gap_pcol():
    viridis(0.0, 1.0, 4)

    coex5g = pd.read_csv('val/coex/coex5g_coexistence_gap_1023.csv', delimiter=',')
    matlab = pd.read_csv('val/coex/matlab_coexistence_gap_1023.csv', delimiter=',')

    coex5g_pc_nru = coex5g.groupby(['Gnb'])['PcolNR'].mean()
    matalb_pc_nru = matlab.groupby(['nNR'])['pcNR'].mean()

    coex5g_pc_wifi = coex5g.groupby(['WiFi'])['PcolWifi'].mean()
    matlab_pc_wifi = matlab.groupby(['nWifi'])['pcWifi'].mean()


    ax = coex5g_pc_nru.plot(marker="o", legend=True, ylim=(0, 1))
    ax = coex5g_pc_wifi.plot(marker="o", legend=True, ylim=(0, 1), linestyle='--')

    ax = matalb_pc_nru.plot(marker="x", legend=True, ylim=(0, 1))
    ax = matlab_pc_wifi.plot(marker="x", legend=True, ylim=(0, 1), linestyle='--')

    ax.legend(['5G-Coex-SimPy NR-U pcol', '5G-Coex-SimPy Wi-Fi pcol',
               'Matlab NR-U pcol', 'Matlab Wi-Fi pcol'])
    # ax.legend(['5G-Coex-SimPy NR-U cot', '5G-Coex-SimPy Wi-Fi cot'])
    ax.set_xlabel('Number of gNBs/stations', fontsize=14)
    ax.set_ylabel('Collision probability', fontsize=14)

    plt.tight_layout()
    plt.savefig('val/coex/coexistence_gap_1023_pcol.svg')

if __name__ == "__main__":
    #valid_wifi()
    #valid_nru()
    # calc()
    #coex_rs()
    coexistence_rs()


