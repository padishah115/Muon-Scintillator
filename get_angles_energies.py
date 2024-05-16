import seaborn as sns
import matplotlib.pyplot as plt
from simulation_package import muon
import pandas as pd
import numpy as np

#Number of muons generated in order to make violin plots
muon_number = 1000

#Maximum and minimum energies to be included
min_energy = 110 #110 MeV
max_energy= 110000 #110 Gev

array_dim = 5

#Stores the angles in radians
angles = []

#Stores the energy in MeV
energies = []

#Generate some values of muon angle and energy
for i in range(muon_number):
    muon1 = muon.Muon(array_dim, max_energy, min_energy)
    angles.append(muon1.theta)
    energies.append(muon1.energy)
    print(muon1.energy)

data = pd.DataFrame({'Zenith Angles / Radians': angles, 'Energies / MeV': energies})
data.to_csv(f'angles_and_energies_{muon_number}.csv', index=False)

# plt.figure(figsize=(10,6))
# sns.violinplot(data=data, y='Zenith Angles / Radians')
# plt.title(f'Zenith Angles, {muon_number} Muons')
# plt.show()

# plt.figure(figsize=(10,6))
# sns.violinplot(data=data, y='Energies / MeV')
# plt.title(f'Muon Energies, {muon_number} Muons')
# plt.show()