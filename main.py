from simulation import *
from lifetime_processing import *

#Number of times the simulation is run
simulation_number = 500
#Max time step in each iteration of the simulation
tmax = 20

#Energy parameters
max_muon_energy = 10000

array_dimension = 5
sipms_per_scintillator = 2
atomic_no = 64
mass_no = 118.17
excitation_energy = 3 #In eV, based on light of wavelength 425nm
rho = 1.081 #density in g/cm^3

#graph_ages(ages)

run_simulation_and_plot(tmax, sipms_per_scintillator, array_dimension, atomic_no, mass_no, excitation_energy, rho, max_muon_energy)