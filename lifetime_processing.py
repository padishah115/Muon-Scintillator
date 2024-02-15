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

def graph_ages(ages):
    lifetimes = []
    values = [] #Lifetime values

    for x in ages:
        if x != 0: 
            lifetimes.append(x)

    max_lifetime = np.max(lifetimes)

    for x in range(0, max_lifetime+1):
        values.append(x)

    frequencies = np.zeros_like(values) #Frequency of each value of lifetime

    for x in lifetimes:
        frequencies[x] += 1

    frequencies[0] = len(lifetimes) #Length of lifetimes array is the number of muons which have been stopped inside of the array

    #p = np.polyfit(values, np.log(frequencies), 1)

    #best_fit_freq = []

    # for value in values:
    #     i = np.exp(p[1] + p[0]*value)
    #     best_fit_freq.append(i)

    plt.scatter(values, frequencies)
    #plt.plot(values, best_fit_freq)
    plt.title('Population graph of muons in array after each time')
    plt.xlabel('Lifetime of muons in array')
    plt.ylabel('Frequency of lifetime')
    plt.savefig('Muon_Pop_v_time.png')
    plt.show()

    