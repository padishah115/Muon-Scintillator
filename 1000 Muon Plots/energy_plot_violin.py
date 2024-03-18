import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('C:\\Users\\hayde\\Desktop\\Muon Scintillator\\Violin Plots\\angles_and_energies.csv')

bin_no = 1000
energies = df['Energies / MeV']
muon_num = len(energies)

#violin plot
plt.figure(figsize=(10,6))
sns.violinplot(energies)
plt.ylabel('Energies / MeV')
plt.title(f'Energy Distribution, {muon_num} Muons')
plt.show()

plt.hist(energies, bin_no)
plt.title(f'Histogram Plot of Energies, {muon_num} Muons, {bin_no} Bins')
plt.xlabel('Energies / MeV')
plt.show()


print(energies)
