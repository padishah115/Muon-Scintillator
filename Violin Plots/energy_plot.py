import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('C:\\Users\\hayde\\Desktop\\Muon Scintillator\\Violin Plots\\angles_and_energies.csv')

energies = df['Energies / MeV']
muon_num = len(energies)

plt.figure(figsize=(10,6))
sns.violinplot(energies)
plt.ylabel('Energies / MeV')
plt.title(f'Energy Distribution, {muon_num} Muons')
plt.show()


print(energies)
