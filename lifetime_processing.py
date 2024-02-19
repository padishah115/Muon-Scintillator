import numpy as np
import matplotlib.pyplot as plt

def percentage_stopped(ages):
    stopped = 0
    number = len(ages)
    for x in ages:
        if x != 0:
            stopped += 1
    percentage = stopped / number * 100
    return percentage

def number_stopped(ages):
    stopped = 0
    for x in ages:
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

        values = np.arange(0, max_lifetime+1) #Values of lifetimes
        frequencies = np.zeros_like(values) #Number of muons at each lifetime

        
        frequencies[0] = 0 #Zero muons decay after 0 time

        for time in lifetimes:
            frequencies[time] += 1


        decayed = np.cumsum(frequencies) #Cumulative sum of how many have decayed using the ages matrix
        remaining_muons = np.zeros_like(frequencies)

        for i in range (len(decayed)):
            remaining_muons[i] = initial_population - decayed[i]


        plt.scatter(values, remaining_muons)
        plt.title(f'Population graph of muons in array after each time, for {len(lifetimes)} muons.')
        plt.xlabel('Lifetime of muons in array')
        plt.ylabel('Muon Population')
        plt.savefig('Muon_Pop_v_time.png')
        plt.show()

    else:
        print("No muons decayed in simulation")

    