import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit

current_directory = os.getcwd()

width = 0.01 #Width of quantisation bins for histogram plots

def percentage_stopped(stops):
    stopped = 0
    number = len(stops)
    for x in stops:
        if x != 0:
            stopped += 1
    percentage = stopped / number * 100
    return percentage

def number_stopped(stops):
    stopped = 0
    for x in stops:
        if x != 0:
            stopped += 1
    
    return stopped

def rest_lifetimes(x):
    muon_lifetime = 22000
    y = np.exp(-x/muon_lifetime)

    return y

def exponential_decay(t, N_0, tau):
    return N_0 * np.exp(-t/tau)

def get_folding_time(times, remaining_muons):
    x = times
    print(f'Remaining muons matrix in folding time fxn: {remaining_muons}')
    #y = N_0 * exp(-t/tau)
    #ln(y) = ln(N_0) - t/tau = ln(N_0) + lmbda*t
    padding = 1e-5
    coeffs = np.polyfit(x, np.log(np.add(remaining_muons, padding)), 1)
    N_0 = np.exp(coeffs[1])
    lmbda = coeffs[0] 
    
    tau_estimate = 1 / abs(lmbda)
    return tau_estimate

                     
def graph_ages(ages):
    """Graphs the population number for stationary muons in the array as a function of time spent stationary in the array"""

    lifetimes = [] #Collects all muons which have self.age != 1, i.e. decayed inside the matrix
    
    for x in ages:
        if x != 0: 
            lifetimes.append(x)

    if len(lifetimes) > 0:

        initial_population = len(lifetimes) #Initial number of muons which are stationary, i.e. population at t=0
        max_lifetime = np.max(lifetimes) #Maximum age of muons in the array

        bin_width = width
        bins = np.arange(0, max_lifetime + bin_width, bin_width)
        frequencies, edges = np.histogram(lifetimes, bins=bins)
        bin_centers = 0.5 * (edges[:-1] + edges[1:])

        decayed = np.cumsum(frequencies)
        remaining_muons = initial_population - decayed

        x = np.linspace(np.min(lifetimes), np.max(lifetimes))

        plt.scatter(bin_centers, remaining_muons, label = 'Observed Lifetimes in Array')
        plt.plot(x, initial_population * rest_lifetimes(x), label = 'Expected distribution for muons at rest', color='m')
        plt.legend()
        plt.title(f'Population graph of muons in array after each time, for {initial_population} muons.')
        plt.xlabel('Lifetime of muons in array / microseconds')
        plt.ylabel('Muon Population / total number')
        plt.grid(True)
        plt.savefig(current_directory+f'\\population graphs\Muon_Pop_v_time{initial_population}.png')
        plt.show()

    else:
        print("No muons decayed in simulation")    


def return_hist(ages, tmax):
    """Graphs the population number for stationary muons in the array as a function of time spent stationary in the array"""

    lifetimes = [] #Collects all muons which have self.age != 1, i.e. decayed inside the matrix
    
    for x in ages:
        if x != 0: 
            lifetimes.append(x)

    if len(lifetimes) > 0:

        initial_population = len(lifetimes)

        bins = len(ages)
        frequencies, edges = np.histogram(lifetimes, bins=bins)
        bin_centers = 0.5 * (edges[:-1] + edges[1:])

        remaining_muons = [0]

        decayed = np.cumsum(frequencies)

        for i in range(len(lifetimes)):
            remaining_muons = [initial_population - decayed[i+1] for i in range(len(decayed))]

        folding_time = get_folding_time(remaining_muons, tmax)

        #Returns the histrogram bin centre points, the number of surviving muons at each point, and the estimate of folding time, tau
        return bin_centers, remaining_muons, folding_time

    
    else:
        print("No muons decayed in simulation")


def plot_reduced_samples(ages):
    """Uses alternative method to graph ages of muons for sample sizes of less than 6 muon decays"""
    init_pop = len(ages)
    times = [0]
    population = [init_pop]

    for age in sorted(ages):
        times.append(age)

    for i in range(len(ages)):
        population.append(init_pop - (i+1))

    tau = get_folding_time(times, population)
    
    return times, population

def plot_reduced_samples_no_tau(ages):
    """Uses alternative method to graph ages of muons for sample sizes of less than 6 muon decays"""
    init_pop = len(ages)
    times = [0]
    population = [init_pop]

    for age in sorted(ages):
        times.append(age)

    for i in range(len(ages)):
        population.append(init_pop - (i+1))
    
    return times, population

# x = sorted([0,29856.470952521082, 7278.5805228244135, 3319.319442473883, 13997.699152302692, 35052.17123487241, 2833.6204762179104, 25272.912532584724, 43533.81012882453, 4105.307235359445, 45749.42530479566, 51960.91109054334, 26613.229481986244, 66058.93332211625, 21836.551906449327, 10526.942507710415, 9330.08435213552, 10932.957992298245, 21402.459909788788, 2450.321705174714, 14879.425304795663, 30430.453445279694, 7351.857489576128, 19892.791799076746, 2583.4285065690838, 1143.7482687751578, 3646.3372651487666, 76420.64654796182, 52587.824825099015, 8056.079035336175, 625.6312989926677, 35132.79648010837, 37838.735422818754, 36598.24516401929, 16725.611164961738, 6636.740962372215, 15744.692678735639, 6233.893907244066, 11834.912343132131, 9705.566166376737, 22824.77878005471, 8637.086160112805, 60854.283370758625, 21828.28052366389, 20835.883839985436, 60280.96262542227, 45929.0487994139, 20481.55123275422, 21794.367780580284, 5008.310755318906, 7661.055783324562, 8725.581824688026, 364.92903099285326, 32749.459909788788, 11602.723733418507, 11426.638974758791])
# y = [len(x) - i for i in range(len(x))]

# plt.plot(x,y, label=f'Energy Range: {110}-{200} MeV', color = 'r')

# x_rest = np.linspace(0, 100000, 1000)
# y_rest = rest_lifetimes(x_rest) #Expected graph for muons at rest

# #Make sure to rescale the rest-frame curve to keep it in line with the initial maximum population
# plt.scatter(x_rest, len(x)*y_rest, color='b', label='Expected distribution for muons at rest', marker='x', linewidths=0.1)

# plt.xlabel('Lifetime in array / 100ps')
# plt.ylabel('Muon population')
# plt.legend()
# plt.title(f'Muon Population Decay, {len(x)} decayed muons')
# #plt.savefig('Multiple energy maxima.png')
# plt.show()