from array_stopping_power import *
from simulation import *
from lifetime_processing import *


"""
TO DO:
    Calculate the stopping power of the array and use this to determine whether the muon comes to a stop inside of the
        array.

    Make a graph showing the characteristic lifetime of muons which decay in the apparatus.


UNITS: MeV, cm, 100s of picoseconds

For a muon at sea level, expect an energy of 4 GeV. This translates to a beta*gamma of about 38 

"""

#Properties of the copper array
copper_rho = 8.96 #Density in g/cm^3
copper_atomic_number = 29
copper_atomic_mass = 63.5
excitation_energy = 3 #In eV, based on light of wavelength 425nm

#Quantum efficiency of SiPM
efficiency = 0.8

#Setting duration of the simulation. The program will run from t=0 to t=tmax. Increments are in the ballpark of about 200ps
t = 0
t_max = 20
sim_num = 1000

#Dimensions of the scintillator array- DO NOT CHANGE THIS
array_dimension = 5

ages = []

for x in range(sim_num):
    a = run_simulation_and_return_age(t_max, array_dimension, efficiency, copper_rho, copper_atomic_number, copper_atomic_mass, excitation_energy)
    ages.append(a) #a = 0 implies that the muon never stopped inside the array

print(ages)
print(f"{number_stopped(ages)} stopped in total")
print(f"{percentage_stopped(ages):.2f} % of muons stopped in the array") # prints the percentage of muons which were stopped in the array
graph_ages(ages)

#Nice to have a graph
#run_simulation_and_plot(t_max, array_dimension, efficiency, copper_rho, copper_atomic_number, copper_atomic_mass, excitation_energy)



