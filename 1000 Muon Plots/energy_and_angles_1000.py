import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('C:\\Users\\hayde\\Desktop\\Muon Scintillator\\1000 Muon Plots\\angles_and_energies_1000.csv')

angles = df['Zenith Angles / Radians']
energies = df['Energies / MeV']

muon_number = len(angles)
mean_energy = np.mean(energies)

radians = np.linspace(0, np.pi / 2, 1000)

def normalised_cos_squared(x):
    """Generates a normalised cos^2 graph, which serves as a probability density"""

    y = (np.cos(x))**2

    normalisation_factor = np.trapz(y, x)

    y_normalised = (1/normalisation_factor) * y

    return y_normalised


#Angular Distribution
plt.hist(angles, label=f'Simulated muon angles', bins=25, density=True)
plt.plot(radians, normalised_cos_squared(radians), label='Normalised cos squared graph')
plt.title(f'Density Histogram of Generated Zenith Angles for {muon_number} Simulated Muons')
plt.ylabel('Frequency')
plt.xlabel('Zenith Angle / Radians')
plt.legend()
plt.show()

#Energy Distribution
plt.hist(energies, label=f'Simulated muon energies. Mean energy: {mean_energy/1000:.2f} GeV', bins=500)
plt.title(f'Histogram of Generated Energies for {muon_number} Simulated Muons')
plt.ylabel('Frequency')
plt.xlabel('Energy / MeV')
plt.legend()
plt.show()