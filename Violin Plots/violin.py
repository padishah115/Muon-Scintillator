import seaborn as sns
import matplotlib.pyplot as plt
from muon import Muon
import pandas as pd

#Number of muons generated in order to make violin plots
muon_number = 100000

#Maximum and minimum energies to be included
min_energy = 110
max_energy= 300000

array_dim = 5

#Stores the angles in radians
angles = []

#Stores the energy in MeV
energies = []


#Generate some values of muon angle and energy
for i in range(muon_number):
    muon1 = Muon(array_dim, max_energy, min_energy)
    angles.append(muon1.theta)
    energies.append(muon1.energy)

data = pd.DataFrame({'Zenith Angles / Radians': angles, 'Energies / MeV': energies})

plt.figure(figsize=(10,6))
sns.violinplot(angles, y='Zenith Angles / Radians')
plt.title(f'Zenith Angles, {muon_number} Muons')
plt.show()

plt.figure(figsize=(10,6))
sns.violinplot(energies, y='Energies / MeV')
plt.title(f'Muon Energies, {muon_number} Muons')
plt.show()

