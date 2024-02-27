from simulation import *
from lifetime_processing import *

#Number of times the simulation is run
simulation_number = 2000
#Max time step in each iteration of the simulation
tmax = 22000 #22000 * 100 picoseconds = 2.2 microseconds
tmax_in_microseconds = ((tmax*100) * 10 **-12) / (1 * 10**-6) 

array_dimension = 5
sipms_per_scintillator = 2
atomic_no = 64
mass_no = 118.17
excitation_energy = 3 #In eV, based on light of wavelength 425nm
rho = 1.081 #density in g/cm^3

max_energies = [1000, 2500, 5000, 10000] #Maximum energies for the distribution in units of MeV
master_pop = [] #Maximum lifetimes for each of the max energy values


for max_e in max_energies:
    ages = []
    stops = []

    colors = ['r', 'g', 'b', 'm', 'y', 'k', 'c']
    styles = ['o', 'v', 's', '*']
    
    for i in range(simulation_number):
        #Run the simulation a number of times equivalent to the simulation number, each time returning an age and a BOOLEAN as to whether the muon has stopped
        age, stopped = run_simulation(tmax, sipms_per_scintillator, array_dimension, atomic_no, mass_no, excitation_energy, rho, max_e)
        ages.append(age)
        stops.append(stopped) #"STOPPED" is a Boolean value, taking 0 for NOT STOPPED and 1 for STOPPED

    #Returns the x values (lifetime), y values (muon population remaining after each time), and TAU, the folding length
    x, y, tau = return_hist(ages)

    #Appends the initial population for each energy range to the master_pop list, which will be used to rescale the rest-frame distribution
    master_pop.append(np.max(y))

    #Plot the graph of muon population against rest frame lifetime
    plt.scatter(x,y, label=f'Max Energy: {max_e/1000} GeV, folding time {tau:.2f} microseconds, {percentage_stopped(stops):.2f}% stopped', color = np.random.choice(colors), marker=np.random.choice(styles))
   
    print(f'Percentage of muons stopped for max energy {max_e/1000} GeV: {percentage_stopped(stops):.2f} % ({number_stopped(stops)} muons total)')

print(f'Each simulation ran for {tmax_in_microseconds} microseconds')

x_rest = np.linspace(0, np.max(ages))
y_rest = rest_lifetimes(x_rest)

#Make sure to rescale the rest-frame curve to keep it in line with the initial maximum population
plt.plot(x_rest, np.max(master_pop) * y_rest, color='m', label='Expected distribution for muons at rest')

plt.xlabel('Lifetime in array / microseconds')
plt.ylabel('Muon population')
plt.legend()
plt.title('Population of muons at different energy ranges in PVT scintillator')
plt.savefig('Multiple energy maxima.png')
plt.show()

#graph_ages(ages)

#run_simulation_and_plot(tmax, sipms_per_scintillator, array_dimension, atomic_no, mass_no, excitation_energy, rho)