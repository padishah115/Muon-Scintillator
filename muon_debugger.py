from muon import Muon
import numpy as np

array_dimension = 5
tests = 500

velocities = []
positions = []
energies = []
angles = []

for i in range(tests):
    muon1 = Muon(array_dimension)
    #velocities.append(muon1.velocity)
    #positions.append(muon1.position)
    energies.append(muon1.energy)
    #angles.append(muon1.theta)

mean_energy = np.mean(energies)
print(mean_energy)