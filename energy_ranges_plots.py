#Import simulation library governing the passage and behaviour of muons in the scintillating array, including time dilation etc.
from simulation import *

#Library designed to produce useful graphs from the data returned by the simulation code.
from lifetime_processing import *

"""
                PLOTS OF LIFETIME OF MUONS IN ARRAY AS A FUNCTION OF ENERGY IN THE ENERGY DISTRIBUTION- RANGING FROM MIN TO MAX ENERGY
"""

#Number of muons per run of simulation. Each simulation generates muons up to and including a certain energy value.
muon_number = 100
#Max time step in each iteration of the simulation
tmax = 22000 #Time in 100s of picoseconds. 22000 * 100 picoseconds = 2.2 microseconds
tmax_in_microseconds = ((tmax*100) * 10 **-12) / (1 * 10**-6) #Converting explicitly to microseconds

array_dimension = 5
sipms_per_scintillator = 2
atomic_no = 64
mass_no = 118.17
excitation_energy = 3 #In eV, based on light of wavelength 425nm
rho = 1.081 #density in g/cm^3

#ENERGY RANGES
min_energies = [110, 200, 300, 400, 500, 600, 700, 800, 900] #Minimum energies for the energy distribution in MeV
max_energies = [200, 300, 400, 500, 600, 700, 800, 900, 1000] #Maximum energies for the distribution in units of MeV. Muons are generated with energies between rest mass and this value


#Maximum lifetimes for each of the different simulation runs. The dimension of this array should necessarily be the same as the max_energies array.
max_lifes = [] 

#Percentage of muons stopped for each pass of the simulation. 
percent_stopped = [] 


##########################
# RUNNING THE SIMULATION #
##########################

for j, max_e in enumerate(max_energies):
    #OVERALL LOOP FOR EACH MAX ENERGY VALUE

    min_e = min_energies[j]

    ages = [] #Ages of muons of those which have decayed. Muons which have not decayed will not have their values appended.
    stops = [] #For each generated muon, it will either stop or not stop. If it has stopped, a value of 1 is appened to the array. Otherwise, 0 is appended.

    colors = ['r', 'g', 'b', 'm', 'y', 'k', 'c']
    styles = ['o', 'v', 's', '*']
    
    for i in range(muon_number):
        #Run the simulation a number of times equivalent to the simulation number, each time returning a muon age and a BOOLEAN as to whether the muon has stopped
        age, stopped = run_simulation(tmax, sipms_per_scintillator, array_dimension, atomic_no, mass_no, excitation_energy, rho, max_e, min_muon_energy=min_e)
        if age != 0:
            ages.append(age)
        stops.append(stopped) #"STOPPED" is a Boolean value, taking 0 for NOT STOPPED and 1 for STOPPED

    #print(ages)

    if np.size(ages) != 0:
        #Only enter this block if some of the muons were actually stopped.
        #Returns the x values (lifetime), y values (muon population remaining after each time), and TAU, the folding length
        x, y, tau = return_hist(ages)

        #Appends the initial population for each energy range to the master_pop list, which will be used to rescale the rest-frame distribution
        max_lifes.append(np.max(y))

        #Plot the graph of muon population against rest frame lifetime using the histogram return_hist function
        plt.scatter(x,y, label=f'Energy Range: {min_e/1000}-{max_e/1000} GeV, folding time {tau:.2f} microseconds', color = np.random.choice(colors), marker=np.random.choice(styles))

        print(f'Percentage of muons stopped for {min_e/1000}-{max_e/1000} GeV: {percentage_stopped(stops):.2f} % ({number_stopped(stops)} muons total)')

    else:
        print(f'No muons stopped for energy range {min_e/1000}-{max_e/1000} GeV')

    #Calculates which percentage of muons were stopped using values in the 'stops' array
    percent_stopped.append(percentage_stopped(stops))


print(f'Each simulation ran for {tmax_in_microseconds} simulated microsecondsseconds')


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
plt.title(f'Population of muons at different energy ranges in PVT scintillator for {muon_number} muons')
plt.savefig('Multiple energy maxima.png')
plt.show()

#################################################################
# PLOTS OF PERCENTAGE % OF MUONS STOPPED VS MAXIMUM ENERGY      #
# Plots the maximum energy values in GeV against the percentage #
# of muons stopped in each case.                                #
#################################################################

#Convert original values which were in MeV to GeV
min_energies_gev = np.multiply(min_energies, 1/1000)
max_energies_gev = np.multiply(max_energies, 1/1000)

#Stores the energy range values as strings in order to be placed on the x-axis
labels = [] 

for i, percent in enumerate(percent_stopped):
    min_energy = min_energies_gev[i]
    max_energy = max_energies_gev[i]

    #Make an appropriate label based on the minimum and maximum energies
    label = str(min_energy) + '-' + str(max_energy)
    labels.append(label)

plt.bar(labels, percent_stopped)
plt.xlabel('Energy Range / GeV')
plt.ylabel('Stopped in array %')
plt.title(f'Percentage of Muons Stopped for {muon_number} muons')
plt.savefig('stopped_in_array.png')
plt.show()