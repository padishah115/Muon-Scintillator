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


# def get_folding_time(lifetimes):
#     lifetimes_sorted = sorted(lifetimes)
#     init_pop = len(lifetimes_sorted)

#     one_over_e_pop = init_pop / np.exp(1)

#     index = int(np.floor(one_over_e_pop) - 1)
#     print(index)

#     return lifetimes_sorted[index]


def get_folding_time(remaining_muons, tmax):
    x = np.linspace(0, tmax, len(remaining_muons))

    #y = Nexp(-t/tau)
    #ln(y) = ln(N_0) - t/tau = ln(N_0) + lmbda*t
    coeffs = np.polyfit(x, np.log(remaining_muons), 1)
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
    values = [] #Time spent stationary in matrix
    
    for x in ages:
        if x != 0: 
            lifetimes.append(x)

    if len(lifetimes) > 0:

        initial_population = len(lifetimes) #Initial number of muons which are stationary, i.e. population at t=0
        max_lifetime = np.max(lifetimes) #Maximum age of muons in the array

        bin_width = width
        #bins = np.arange(0, max_lifetime + bin_width, bin_width)
        bins = len(ages)
        frequencies, edges = np.histogram(lifetimes, bins=bins)
        bin_centers = 0.5 * (edges[:-1] + edges[1:])

        decayed = np.cumsum(frequencies)
        remaining_muons = initial_population - decayed

        folding_time = get_folding_time(remaining_muons, tmax)

        #Returns the histrogram bin centre points, the number of surviving muons at each point, and the estimate of folding time, tau
        return bin_centers, remaining_muons, folding_time

    
    else:
        print("No muons decayed in simulation")
