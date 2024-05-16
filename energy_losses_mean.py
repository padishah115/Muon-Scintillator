import simulation_package.simulation as simulation
import pandas as pd
import simulation_package.bethe_equation as bethe
import numpy as np
import simulation_package.muon as muon
import matplotlib.pyplot as plt

#Energy parameters
max_muon_energy = 100000 #
min_muon_energy = 110 #110 MeV

atomic_no = 64
mass_no = 118.17
excitation_energy =  64.7 #Excitation energy of PVT in eV
rho = 1.023 #density of PVT in g/cm^3
muon_mass = 105.658

dx = 1e-2

#graph_ages(ages)

initial_energies = np.linspace(110, 100000, 50000) #Energies between 110 MeV and 100 GeV
final_energies = []
energy_losses = []
percentage_lost = [] #Percentage of KE lost

gammas = np.divide(initial_energies, muon_mass)
betas = np.sqrt(1-1/gammas**2)

de_dxs = de_dx = abs(bethe.bethe_equation(atomic_no,mass_no, gammas, betas, muon_mass, excitation_energy, rho))

for i, initial_energy in enumerate(initial_energies):
    final_energy = initial_energy
    distance_travelled_cm = 0

    while distance_travelled_cm < 25 and final_energy > muon_mass:
        #Energy lost when travelling through 25cm of PVT

        gamma = final_energy / muon_mass
        beta = np.sqrt(1-1/gamma**2)

        #Dx in cm

        de_dx = bethe.bethe_equation(atomic_no,mass_no, gamma, beta, muon_mass, excitation_energy, rho)
        
        de = abs(de_dx * dx)

        final_energy = final_energy - de
        distance_travelled_cm = distance_travelled_cm + dx


    if final_energy > muon_mass:
        final_energies.append(final_energy)
        energy_lost = initial_energy - final_energy
        energy_losses.append(energy_lost)

        kinetic_energy = initial_energy - muon_mass
        percentage_lost.append((energy_lost/kinetic_energy)*100)
        

    else:
        final_energies.append(muon_mass)
        energy_lost = initial_energy - final_energy
        energy_losses.append(energy_lost)
        
        kinetic_energy = initial_energy - muon_mass
        percentage_lost.append(100)


for i, lost in enumerate(percentage_lost):
    if i < len(percentage_lost):
        if percentage_lost[i] < 100 and percentage_lost[i-1] == 100:
            final_stopped = initial_energies[i-1]
    

# print(initial_energies)
# print(final_energies)
print(percentage_lost)


plt.plot(initial_energies, percentage_lost)
plt.title('Kinetic Energy Lost by Muon in Array\n as a Function of Initial Energy \n(Simulated)')
plt.ylabel('Percentage of Kinetic Energy Lost %')
plt.xlabel('Energy / MeV')
plt.vlines(final_stopped, label=f'Highest Energy Muon Stopped in Array: {final_stopped:.1f} MeV', ymin=-5, ymax=110, ls='--', color='r')
plt.vlines(4000, label='4 GeV', ymin=-5, ymax = 5, ls='--', color='g')
#plt.yscale('log')
plt.xscale('log')
plt.legend()
plt.show()


energy_losses_dataframe = pd.DataFrame({
    'initial energies / MeV' : initial_energies,
    'final energies / MeV' : final_energies,
    'energy losses / MeV' : energy_losses
    
    })

energy_losses_dataframe.to_csv(f'C:\\Users\\hayde\\Desktop\\Muon Scintillator\\Energy Losses\\energy_losses_min{min_muon_energy}_max{max_muon_energy}_distance{distance_travelled_cm}.csv', index=False)