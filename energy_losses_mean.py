import simulation_package.simulation as simulation
import pandas as pd

#Number of times the simulation is run
simulation_number = 1000
#Max time step in each iteration of the simulation- tmax in 100s of picoseconds
tmax = 100000

tmax_in_microseconds = ((tmax*100) * 10 **-12) / (1 * 10**-6) 

#Energy parameters
max_muon_energy = 300000 #300GeV
min_muon_energy = 110 #110 MeV

array_dimension = 5
sipms_per_scintillator = 2
atomic_no = 64
mass_no = 118.17
excitation_energy = 3 #In eV, based on light of wavelength 425nm
rho = 1.081 #density in g/cm^3
dead_time_sipms_ns = 48 #48 ns dead time for sipms from broadcom data sheet
plot=False
return_energy = True

#graph_ages(ages)

initial_energies = []
final_energies = []
energy_losses = []

for i in range(simulation_number):
    age, stopped, initial_energy, final_energy = simulation.run_simulation(plot, return_energy, tmax, sipms_per_scintillator, array_dimension, dead_time_sipms_ns, atomic_no, mass_no, excitation_energy, rho, max_muon_energy)
    print(f'Simulation ran for {tmax_in_microseconds} microseconds')
    print(f'Initial energy: {initial_energy} / Mev')
    print(f'Final energy: {final_energy} / Mev')

    initial_energies.append(initial_energy)
    final_energies.append(final_energy)
    energy_losses.append(initial_energy - final_energy)

energy_losses_dataframe = pd.DataFrame({
    'initial energies / MeV' : initial_energies,
    'final energies / MeV' : final_energies,
    'energy losses / MeV' : energy_losses
    
    })

energy_losses_dataframe.to_csv(f'C:\\Users\\hayde\\Desktop\\Muon Scintillator\\Energy Losses\\energy_losses_min{min_muon_energy}_max{max_muon_energy}_muon_num{simulation_number}.csv', index=False)