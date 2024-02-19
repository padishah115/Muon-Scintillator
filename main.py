from simulation import *
from lifetime_processing import *

#Number of times the simulation is run
simulation_number = 50
#Max time step in each iteration of the simulation
tmax = 20

array_dimension = 5
sipms_per_scintillator = 2
atomic_no = 29
mass_no = 63.5
excitation_energy = 3 #In eV, based on light of wavelength 425nm
rho = 8.96 #density in g/cm^3

# ages = []

# for i in range(simulation_number):
#     #Run the simulation a number of times equivalent to the simulation number, each time returning an age
#     age = run_simulation_and_return_age(tmax, sipms_per_scintillator, array_dimension, atomic_no, mass_no, excitation_energy, rho)
#     ages.append(age)

# print(f'Percentage of muons stopped in array: {percentage_stopped(ages)} % ({number_stopped(ages)} muons total)')

# graph_ages(ages)

run_simulation_and_plot(tmax, sipms_per_scintillator, array_dimension, atomic_no, mass_no, excitation_energy, rho)