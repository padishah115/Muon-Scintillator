import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('C:\\Users\\hayde\\Desktop\\Muon Scintillator\\1000 Muon Plots\\angles_and_energies_1000.csv')

bin_no = 1000
energies = df['Energies / MeV']
muon_num = len(energies)
mean_energy_mev = np.sum(energies) / muon_num

mean_energy_gev = mean_energy_mev / 1000

plt.hist(energies, int(bin_no), label = f'Mean Energy: {mean_energy_gev:.2f} GeV')
plt.title(f'Histogram Plot of Energies, {muon_num} Muons, {int(bin_no)} Bins')
plt.xlabel('Energies / MeV')
plt.ylabel('Frequency')
plt.xscale('log')
plt.legend()
plt.show()


print(energies)
