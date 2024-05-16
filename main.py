import simulation_package.simulation as simulation


#Number of times the simulation is run
simulation_number = 500
#Max time step in each iteration of the simulation- tmax in 100s of picoseconds
tmax = 100000

tmax_in_microseconds = ((tmax*100) * 10 **-12) / (1 * 10**-6) 

#Energy parameters
max_muon_energy = 200
min_muon_energy = 110 #110 MeV

array_dimension = 5
sipms_per_scintillator = 2
atomic_no = 64
mass_no = 118.17
excitation_energy = 64.7 #In eV, based on light of wavelength 425nm
rho = 1.023 #density in g/cm^3
dead_time_sipms_ns = 48 #48 ns dead time for sipms from broadcom data sheet
plot=True
return_energy = False

#graph_ages(ages)

simulation.run_simulation(plot, return_energy, tmax, sipms_per_scintillator, array_dimension, dead_time_sipms_ns, atomic_no, mass_no, excitation_energy, rho, max_muon_energy)
print(f'Simulation ran for {tmax_in_microseconds} microseconds')