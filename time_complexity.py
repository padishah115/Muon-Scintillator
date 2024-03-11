from simulation import *
from lifetime_processing import *
import time

###################################
# Measurements of Time Complexity #
###################################

#Maximum order polynomial used in polyfit function
maximum_order = 5

#Minimum and maximum simulated times in 100s of picoseconds
tmax_min = 100
tmax_max = 100000

#Number of sampling points
datapoint_no = 1000

#Number of times the simulation is run
simulation_number = 500
#Max time step in each iteration of the simulation- tmax in 100s of picoseconds
tmaxs = np.linspace(tmax_min, tmax_max, datapoint_no)
times_taken = []

tmaxs_microseconds = []


#Energy parameters
max_muon_energy = 300000 #300 GeV
min_muon_energy = 110 #110 MeV

array_dimension = 5
sipms_per_scintillator = 2
atomic_no = 64
mass_no = 118.17
excitation_energy = 3 #In eV, based on light of wavelength 425nm
rho = 1.081 #density in g/cm^3
dead_time_sipms_ns = 10 #10 ns dead time for sipms
plot=False

def fit_N_order_polynomial(x, y, n):
    """Fits a polynomial to data (x,y) of arbitrary order n"""
    z = np.polyfit(x, y, n)
    polynomial = np.poly1d(z)
    return polynomial



for tmax in tmaxs:
    start_time = time.time()
    run_simulation(plot, tmax, sipms_per_scintillator, array_dimension, dead_time_sipms_ns, atomic_no, mass_no, excitation_energy, rho, max_muon_energy)
    end_time = time.time()

    #Calculate the time taken to execute the simulation for each value of tmax
    dt = end_time - start_time
    times_taken.append(dt)
    print(f'Time taken for {tmax*100}ps: {dt}s')

    #Add the value of the simulated tmax value, in microseconds, to the tmax in microseconds array
    this_tmax_in_microseconds = ((tmax*100) * 10 **-12) / (1 * 10**-6) 
    tmaxs_microseconds.append(this_tmax_in_microseconds)
    print(f'Simulation ran for {this_tmax_in_microseconds} microseconds')


#Using polyfit up
for i in range(maximum_order):
    poly_N = fit_N_order_polynomial(tmaxs_microseconds, times_taken, i+1)
    plt.plot(tmaxs_microseconds, poly_N(tmaxs_microseconds), label=f'Order {i+1} polynomial')

plt.scatter(tmaxs_microseconds, times_taken, label='Data')
plt.xlabel('Simulated time / microseconds')
plt.ylabel('Real computation time / seconds')
plt.title(f'Sim. Complexity. Muon Energy:{min_muon_energy/1000}-{max_muon_energy/1000} GeV')
plt.legend()
plt.show()