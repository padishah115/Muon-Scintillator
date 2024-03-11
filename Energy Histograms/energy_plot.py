import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('C:\\Users\\hayde\\Desktop\\Muon Scintillator\\Energy Histograms\\angles_and_energies.csv')

bin_no = 1000
energies = df['Energies / MeV']
muon_num = len(energies)

plt.hist(energies, bin_no)
plt.title(f'Histogram Plot of Energies, {muon_num} Muons, {bin_no} Bins')
plt.xlabel('Energies / MeV')
plt.show()


print(energies)
