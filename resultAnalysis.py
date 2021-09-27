import pandas as pd
import matplotlib.pyplot as plt

def print_collision_prob():
    # read data from csv
    data = pd.read_csv('results.csv', delimiter=',')
    data2 = pd.read_csv('results2.csv', delimiter=',')

    # group by number of stations and calculate mean colision proob
    data = data.groupby(['Stations'])['Colisions'].mean()
    data2 = data2.groupby(['Stations'])['Colisions'].mean()

    # plotting
    # 5G _ JC
    ax = data.plot(title='5G_Coexistance vs DCF simulators', marker='o', legend=True, ylim=(0, 40))
    ax.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="Collision probability")

    # DCF - PT
    ax2 = data2.plot(title='5G_Coexistance vs DCF simulators', marker='x', legend=True, ylim=(0, 40))
    ax2.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="Collision probability")
    ax2.legend(['5G-Coexistance-Simpy', 'DCF-Simpy'])

    # Save to file
    plt.tight_layout()
    plt.savefig('colisonERRROR2.png')

def print_airtime_34():
    # read data from csv
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
    ax.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="% of time")
    ax2 = data3.plot(title='Airtime 5G-Coexistance-Simpy vs DCF-Simpy', marker='x', legend=True, ylim=(0, 1))
    ax2.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="% of time")
    #ax2.legend(['Normalized Channel Occupancy', 'Channel Efficiency'])

    ax3 = data2dcf.plot(title='Airtime 5G-Coexistance-Simpy vs DCF-Simpy', marker='o', legend=True, ylim=(0, 1))
    ax4 = data3dcf.plot(title='Airtime 5G-Coexistance-Simpy vs DCF-Simpy', marker='x', legend=True, ylim=(0, 1))
    ax3.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="% of time")
    ax4.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="% of time")
    ax2.legend(['5G - Normalized Channel Occupancy', '5G - Channel Efficiency','DCF - Normalized Channel Occupancy', 'DCF - Channel Efficiency' ])


    # # DCF - PT
    # ax2 = data2.plot(title='5G_Coexistance vs DCF simulators', marker='x', legend=True, ylim=(0, 40))
    # ax2.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="Collision probability")
    # ax2.legend(['5G-Coexistance-Simpy', 'DCF-Simpy'])

    # Save to file
    plt.tight_layout()
    plt.savefig('airtime34.png')

def print_airtime_per_station():
    # read data from csv
    data = pd.read_csv('airtime12.csv', delimiter=',')
    # data2 = pd.read_csv('results2.csv', delimiter=',')

    # group by number of stations and calculate mean colision proob
    data2 = data.groupby(['Stations'])['PerStation'].mean()


    # plotting
    # 5G _ JC
    ax = data2.plot(title='Time of airtime per station', marker='o', legend=True, ylim=(0, 20))
    ax.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="time in secounds")
    # ax.legend(['Normalized Channel Occupancy', 'Channel Efficiency'])
    # # DCF - PT
    # ax2 = data2.plot(title='5G_Coexistance vs DCF simulators', marker='x', legend=True, ylim=(0, 40))
    # ax2.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="Collision probability")
    # ax2.legend(['5G-Coexistance-Simpy', 'DCF-Simpy'])

    # Save to file
    plt.tight_layout()
    plt.savefig('airtime1.png')

def print_airtime_norm_per_station():
    # read data from csv
    data = pd.read_csv('airtime12.csv', delimiter=',')
    # data2 = pd.read_csv('results2.csv', delimiter=',')

    # group by number of stations and calculate mean colision proob
    data2 = data.groupby(['Stations'])['NormPerStation'].mean()

    # plotting
    # 5G _ JC
    ax = data2.plot(title='Normalized time of airtime per station', marker='o', legend=True, ylim=(0, 0.15))
    ax.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="% of time")
    # ax.legend(['Normalized Channel Occupancy', 'Channel Efficiency'])
    # # DCF - PT
    # ax2 = data2.plot(title='5G_Coexistance vs DCF simulators', marker='x', legend=True, ylim=(0, 40))
    # ax2.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="Collision probability")
    # ax2.legend(['5G-Coexistance-Simpy', 'DCF-Simpy'])

    # Save to file
    plt.tight_layout()
    plt.savefig('airtime2.png')


if __name__ == "__main__":
    #print_collision_prob()
    #print_airtime_34()
    print_airtime_per_station()
    print_airtime_norm_per_station()
