import pandas as pd
import matplotlib.pyplot as plt

#read data from csv
data = pd.read_csv('results.csv', delimiter=',')
data2 = pd.read_csv('results2.csv', delimiter=',')

#group by number of stations and calculate mean colision proob
data = data.groupby(['Stations'])['Colisions'].mean()
data2 = data2.groupby(['Stations'])['Colisions'].mean()

#plotting
#5G _ JC
ax = data.plot(title='5G_Coexistance vs DCF simulators', marker='o', legend=True, ylim=(0, 40))
ax.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="Collision probability")


#DCF - PT
ax2 = data.plot(title='5G_Coexistance vs DCF simulators', marker='x', legend=True, ylim=(0, 40))
ax2.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="Collision probability")
ax2.legend(['5G-Coexistance-Simpy', 'DCF-Simpy'])

# Save to file
plt.tight_layout()
plt.savefig('colisonProb3.png')