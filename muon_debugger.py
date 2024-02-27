from muon import Muon
import numpy as np

array_dimension = 5
tests = 150
min_energy = 107
max_energy = 10000

velocities = []
positions = []
energies = []
angles = []

for i in range(tests):
    muon1 = Muon(array_dimension, max_energy, min_energy)
    velocities.append(muon1.velocity)
    #positions.append(muon1.position)
    #energies.append(muon1.energy)
    angles.append(muon1.theta)

print(angles)
print(velocities)