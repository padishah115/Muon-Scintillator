"""Probability test"""

import numpy as np
import matplotlib.pyplot as plt

class Probability_Distribution:
    def __init__(self, times, tau):
        self.times = times
        self.tau = tau

    def plot_distribution(self):
        y = np.exp(-self.times/self.tau)
        plt.plot(self.times, y)
        plt.show()

times_coarse = np.linspace(0,6,6)
times_fine = np.linspace(0,6,100000)
tau = 2.2

prob1 = Probability_Distribution(times_coarse, tau)
prob2 = Probability_Distribution(times_fine, tau)

print(1e-5)

prob1.plot_distribution()
prob2.plot_distribution()
        