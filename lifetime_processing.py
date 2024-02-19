import numpy as np
import matplotlib.pyplot as plt

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

def graph_ages(ages):
    """Graphs the population number for stationary muons in the array as a function of time spent stationary in the array"""

    lifetimes = [] #Collects all muons which have self.age != 1, i.e. decayed inside the matrix
    values = [] #Time spent stationary in matrix
    
    for x in ages:
        if x != 0: 
            lifetimes.append(x)

    if len(lifetimes) > 0:

        initial_population = len(lifetimes) #Initial number of muons which are stationary, i.e. population at t=0
        max_lifetime = np.max(lifetimes) #Maximum age of muons in the array

        bin_width = 0.1
        bins = np.arange(0, max_lifetime + bin_width, bin_width)

        frequencies, edges = np.histogram(lifetimes, bins=bins)
        bin_centers = 0.5 * (edges[:-1] + edges[1:])

        decayed = np.cumsum(frequencies)
        remaining_muons = initial_population - decayed

        plt.scatter(bin_centers, remaining_muons)
        plt.title(f'Population graph of muons in array after each time, for {initial_population} muons.')
        plt.xlabel('Lifetime of muons in array')
        plt.ylabel('Muon Population')
        plt.grid(True)
        plt.savefig('Muon_Pop_v_time.png')
        plt.show()

    else:
        print("No muons decayed in simulation")
    