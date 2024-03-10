import numpy as np
import matplotlib.pyplot as plt

#Import simulation library governing the passage and behaviour of muons in the scintillating array, including time dilation etc.
import simulation as sim

#Library designed to produce useful graphs from the data returned by the simulation code.
import lifetime_processing as life

"""
                PLOTS OF LIFETIME OF MUONS IN ARRAY AS A FUNCTION OF ENERGY IN THE ENERGY DISTRIBUTION- RANGING FROM MIN TO MAX ENERGY
                Also generates a plot of percentage of muons stopped in the array for each energy range
"""

#Number of muons per run of simulation. Each simulation generates muons up to and including a certain energy value.
muon_number = 15
#Max time step in each iteration of the simulation
tmax = 100000 #Time in 100s of picoseconds. 44000 * 100 picoseconds = 4.4 microseconds
tmax_in_microseconds = ((tmax*100) * 10 **-12) / (1 * 10**-6) #Converting explicitly to microseconds

array_dimension = 5
sipms_per_scintillator = 2

#Using knowledge of the properties of the scintillator material
atomic_no = 64
mass_no = 118.17
excitation_energy = 3 #In eV, based on light of wavelength 425nm
rho = 1.081 #density in g/cm^3

plot = False #Don't want to plot
dead_time_sipms_ns = 10 #Dead time of the SiPMs in nanoseconds

#ENERGY RANGES
min_energies =  np.arange(110, 290, 10) #Minimum energies for the energy distribution in MeV
max_energies = np.add(10, min_energies) #Maximum energies for the distribution in units of MeV. Muons are generated with energies between rest mass and this value

#Maximum lifetimes for each of the different simulation runs.
init_pops = [] 

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

    colors = ['r', 'g', 'm', 'y', 'k', 'c']
    styles = ['o', 'v', 's', '*']
    
    for i in range(muon_number):
        #Run the simulation a number of times equivalent to the simulation number, each time returning a muon age and a BOOLEAN as to whether the muon has stopped
        age, stopped = sim.run_simulation(plot, tmax, sipms_per_scintillator, array_dimension, sipms_per_scintillator, atomic_no, mass_no, excitation_energy, rho, max_e, min_muon_energy=min_e)
        if age != 0:
            ages.append(age)
        stops.append(stopped) #"STOPPED" is a Boolean value, taking 0 for NOT STOPPED and 1 for STOPPED

    print(ages)

    if np.size(ages) != 0 and np.size(ages) > 5:
        #Only enter this block if some of the muons were actually stopped.
        #Returns the x values (lifetime), y values (muon population remaining after each time), and TAU, the folding length
        x, y = life.plot_reduced_samples(ages)

        #Appends the initial population for each energy range to the init_pops list, which will be used to rescale the rest-frame distribution
        init_pops.append(np.max(y))

        #Plot the graph of muon population against rest frame lifetime using the histogram return_hist function
        plt.plot(x,y, label=f'Energy Range: {min_e}-{max_e} MeV', color = np.random.choice(colors))

        print(f'Percentage of muons stopped for {min_e}-{max_e} MeV: {life.percentage_stopped(stops):.2f} % ({life.number_stopped(stops)} muons total)')

    elif np.size(ages) <=5:
        #Use alternative method to avoid lack of convergence in least-squares method
        times, pop = life.plot_reduced_samples_no_tau(ages)
        init_pops.append(np.max(y))
        plt.plot(x,y, label=f'Energy Range: {min_e}-{max_e} MeV', color = np.random.choice(colors))
        print(f'Percentage of muons stopped for {min_e}-{max_e} MeV: {life.percentage_stopped(stops):.2f} % ({life.number_stopped(stops)} muons total)')

    else:
        print(f'No muons stopped for energy range {min_e}-{max_e} MeV')

    #Calculates which percentage of muons were stopped using values in the 'stops' array
    percent_stopped.append(life.percentage_stopped(stops))


print(f'Each simulation ran for {tmax_in_microseconds} simulated microseconds')


#########################################################################
# PLOTS OF MUON POPULATION AGAINST LIFETIME FOR DIFFERENT ENERGY RANGES #
#########################################################################

#Check that the dimensions of the master_population array is the same as the max_energies array

x_rest = np.linspace(0, 100000, 1000)
y_rest = life.rest_lifetimes(x_rest) #Expected graph for muons at rest

#Make sure to rescale the rest-frame curve to keep it in line with the initial maximum population
for init_pop in init_pops:
    plt.scatter(x_rest, init_pop*y_rest, color='b', marker='x', s=0.15, label='Expected population')

plt.xlabel('Lifetime in array / microseconds')
plt.ylabel('Muon population')
plt.legend()
plt.title(f'Muon Population Decay')
#plt.savefig('Multiple energy maxima.png')
plt.show()

#################################################################
# PLOTS OF PERCENTAGE % OF MUONS STOPPED VS MAXIMUM ENERGY      #
# Plots the maximum energy values in GeV against the percentage #
# of muons stopped in each case.                                #
#################################################################

#Stores the energy range values as strings in order to be placed on the x-axis
labels = [] 

for i, percent in enumerate(percent_stopped):
    min_energy = min_energies[i]
    max_energy = max_energies[i]

    #Make an appropriate label based on the minimum and maximum energies
    label = str(min_energy) + '-' + str(max_energy)
    labels.append(label)

plt.bar(labels, percent_stopped)
plt.xlabel('Energy Range / MeV')
plt.ylabel('Stopped in array %')
plt.ylim(0,100)
plt.xticks(rotation=90)
plt.title(f'Percentage of Muons Stopped of {muon_number} Muons. Sim. Length: {tmax_in_microseconds} us')
#plt.savefig('stopped_in_array.png')
plt.show()