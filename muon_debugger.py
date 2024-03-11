from simulation_package.muon import Muon
import numpy as np

array_dim = 5
min_energy = 110
max_energy = 300000

muon1 = Muon(array_dim, max_energy, min_energy)

muon1.plot_energy_distribution()