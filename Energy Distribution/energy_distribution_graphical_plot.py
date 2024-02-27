import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Energy_Distribution:

    def __init__(self, emin, emax):
        """Takes energy values in units of GeV"""
        self.emin = emin
        self.emax = emax
        self.e_vals = np.linspace(self.emin, self.emax)
        self.p_values = self.get_p_values()

        self.fig, self.ax = plt.subplots()
        
    def get_p_values(self):
        """Returns the associated probabilities for each of the muons in the distributions"""
        p = (((4.290 + self.e_vals)**-3.01) / ((1 + self.e_vals/854)))
        p = p / np.sum(p)

        return p
    
    def get_mean_energy(self):
        """Returns the mean energy of the distribution"""
        p_times_e = np.multiply(self.e_vals, self.p_values)
        e_X = np.sum(p_times_e)
        return e_X

    
    def plot_distribution(self):
        plt.plot(self.e_vals, self.p_values, label = f'Mean energy = {self.get_mean_energy():.2f} GeV')
        plt.legend()
        plt.title(f'Energy Probability Function. Min: {self.emin:.2f} GeV. Max: {self.emax:.2f} GeV')
        plt.xlabel('Energy / GeV')
        plt.ylabel('Probability of Energy')
        plt.savefig(f'energy_distribution_graph_{self.emin:.2f}_{self.emax:.2f}_GeV.png')
        plt.show()
        

        


e_min = 0.1 #100 MeV
e_max = 300 #300 GeV

distribution1 = Energy_Distribution(e_min, e_max)
distribution1.plot_distribution()



