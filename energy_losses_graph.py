import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import simulation_package.lifetime_processing as life

current_directory = 'C:\\Users\\hayde\\Desktop\\Muon Scintillator\\Energy Losses\\'
entries = os.listdir(current_directory)
files = [f for f in entries if os.path.isfile(os.path.join(current_directory, f))]
files_csv = []
files_sanitised = []



df = pd.read_csv('C:\\Users\\hayde\\Desktop\\Muon Scintillator\\Energy Losses\\energy_losses_min110_max100000_distance25.00000000000111.csv')

initial_energies = df['initial energies / MeV']
final_energies = df['final energies / MeV']
energy_losses = df['energy losses / MeV']

kinetic_energies = np.add(initial_energies, -105.658)
fraction_of_ke_lost = np.multiply(energy_losses, 1/kinetic_energies)


print(initial_energies)
plt.scatter(initial_energies, fraction_of_ke_lost)
plt.title('Kinetic Energy Loss as a Function of Initial Energy \n for 1000 Simulated Muons')
plt.ylabel('Fraction of Kinetic Energy Lost')
plt.xlabel('Initial Energy / Mev')
#plt.xticks(rotation = 90)
#plt.ylim(0,100)
plt.xlim(0,250)
plt.show()


 

