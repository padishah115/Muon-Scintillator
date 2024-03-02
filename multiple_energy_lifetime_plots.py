#Import simulation library governing the passage and behaviour of muons in the scintillating array, including time dilation etc.
from simulation import *

#Library designed to produce useful graphs from the data returned by the simulation code.
from lifetime_processing import *

"""
                PLOTS OF LIFETIME OF MUONS IN ARRAY AS A FUNCTION OF ENERGY IN THE ENERGY DISTRIBUTION
                The purpose of this piece of the code is to see the effects of time dilation/lifetime in the array.
                Currently, this seems to generate unexpected curve shapes, and so this code is not currently stable.

                The simulation is called for a certain muon_number (i.e. how many muons are generated during each pass of the simulation)

                Each run of the simulation generates muons up to a certain energy. These different energy maxima are stored below inside of the 
                max_energies array.




"""

#Number of muons per run of simulation. Each simulation generates muons up to and including a certain energy value.
muon_number = 2000
#Max time step in each iteration of the simulation
tmax = 22000 #22000 * 100 picoseconds = 2.2 microseconds
tmax_in_microseconds = ((tmax*100) * 10 **-12) / (1 * 10**-6) 

array_dimension = 5
sipms_per_scintillator = 2
atomic_no = 64
mass_no = 118.17
excitation_energy = 3 #In eV, based on light of wavelength 425nm
rho = 1.081 #density in g/cm^3

max_energies = [50000, 75000, 100000, 20000] #Maximum energies for the distribution in units of MeV. Muons are generated with energies between rest mass and this value
max_lifes = [] #Maximum lifetimes for each of the different simulation runs. The dimension of this array should necessarily be the same as the max_energies array.

percent_stopped = [] #Percentage of muons stopped for each pass of the simulation. 


##########################
# RUNNING THE SIMULATION #
##########################

for max_e in max_energies:
    ages = []
    stops = []

    colors = ['r', 'g', 'b', 'm', 'y', 'k', 'c']
    styles = ['o', 'v', 's', '*']
    
    for i in range(muon_number):
        #Run the simulation a number of times equivalent to the simulation number, each time returning a muon age and a BOOLEAN as to whether the muon has stopped
        age, stopped = run_simulation(tmax, sipms_per_scintillator, array_dimension, atomic_no, mass_no, excitation_energy, rho, max_e)
        ages.append(age)
        stops.append(stopped) #"STOPPED" is a Boolean value, taking 0 for NOT STOPPED and 1 for STOPPED

    #Returns the x values (lifetime), y values (muon population remaining after each time), and TAU, the folding length
    x, y, tau = return_hist(ages)

    #Appends the initial population for each energy range to the master_pop list, which will be used to rescale the rest-frame distribution
    max_lifes.append(np.max(y))

    #Plot the graph of muon population against rest frame lifetime
    plt.scatter(x,y, label=f'Max Energy: {max_e/1000} GeV, folding time {tau:.2f} microseconds, {percentage_stopped(stops):.2f}% stopped', color = np.random.choice(colors), marker=np.random.choice(styles))
   
    print(f'Percentage of muons stopped for max energy {max_e/1000} GeV: {percentage_stopped(stops):.2f} % ({number_stopped(stops)} muons total)')

    percent_stopped.append(percentage_stopped(stops))

print(f'Each simulation ran for {tmax_in_microseconds} microseconds')


#########################################################################
# PLOTS OF MUON POPULATION AGAINST LIFETIME FOR DIFFERENT ENERGY RANGES #
#########################################################################

#Check that the dimensions of the master_population array is the same as the max_energies array.

if len(max_energies) != len(max_lifes):
    raise ValueError('Error: master_pop array storing maximum lifetimes does not have same dimensions as max_energies array.')

x_rest = np.linspace(0, np.max(ages))
y_rest = rest_lifetimes(x_rest) #Expected graph for muons at rest

#Make sure to rescale the rest-frame curve to keep it in line with the initial maximum population
plt.plot(x_rest, np.max(max_lifes) * y_rest, color='m', label='Expected distribution for muons at rest')

plt.xlabel('Lifetime in array / microseconds')
plt.ylabel('Muon population')
plt.legend()
plt.title('Population of muons at different energy ranges in PVT scintillator')
plt.savefig('Multiple energy maxima.png')
plt.show()

#################################################################
# PLOTS OF PERCENTAGE % OF MUONS STOPPED VS MAXIMUM ENERGY      #
# Plots the maximum energy values in GeV against the percentage #
# of muons stopped in each case.                                #
#################################################################

#Convert original values which were in MeV to GeV
max_energies_gev = np.multiply(max_energies, 1/1000)

plt.plot(max_energies_gev, percent_stopped)
plt.xlabel('Maximum energy in distribution / GeV')
plt.ylabel('stopped in array %')
plt.title('Percentage of Muons Stopped in Array As Function of Cutoff Energy')
plt.show()


#graph_ages(ages)

#run_simulation_and_plot(tmax, sipms_per_scintillator, array_dimension, atomic_no, mass_no, excitation_energy, rho)