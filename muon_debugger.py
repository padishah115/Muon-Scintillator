from muon import Muon
import numpy as np

array_dimension = 5
tests = 50

velocities = []
positions = []
energies = []
angles = []

for i in range(tests):
    muon1 = Muon(array_dimension)
    velocities.append(muon1.velocity)
    positions.append(muon1.position)
    energies.append(muon1.energy)
    angles.append(muon1.theta)

# print('Velocities: ')
# print(velocities)
# print('Positions: ')
# print(positions)
# print('Energies: ')
# print(energies)
# print('Angles: ')
# print(angles)

print(np.mean(energies))