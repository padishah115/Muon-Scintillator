from simulation_package.muon import Muon
import numpy as np
import matplotlib.pyplot as plt

import os

current_directory = os.getcwd()

muon_number = 500
array_dim = 5
max_energy = 10000 #10 GeV
min_energy = 107 #106 Mev- rest mass

bin_no = 100

step = 0.01

thetas = []
x = np.arange(0,np.pi/2, step) #X values in radians

for i in range(muon_number):
     muon1 = Muon(array_dim, max_energy, min_energy)
     theta1 = muon1.theta
     thetas.append(theta1)

cos_2x = np.power(np.cos(x), 2)
y, bin_edges = np.histogram(thetas, bins=bin_no, density=True)

integral = np.trapz(cos_2x, x)

bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
cos_2x_norm = cos_2x / integral

plt.plot(x, cos_2x_norm, label='Cos^2(x) PDF, normalised')
plt.scatter(bin_centers, y, color='r', label=f'Randomly Generated Theta Values, {bin_no} quantisation bins')
plt.legend()
plt.title(f'Simulation probability density function for zenith angle, {muon_number} muons')
plt.savefig(f'angular_distrib_graph_{bin_no}_bins.png')
plt.show()

