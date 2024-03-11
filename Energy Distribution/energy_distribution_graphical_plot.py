import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()

x = np.arange(5,300, 1)
means = []

class Energy_Distribution:

    def __init__(self, emin, emax):
        """Takes energy values in units of GeV"""
        self.emin = emin
        self.emax = emax
        self.e_vals = np.linspace(self.emin, self.emax, 10000)
        self.p_values = self.get_p_values()
        self.mean = self.get_mean_energy()
        
    def get_p_values(self):
        """Returns the associated probabilities for each of the muons in the distributions"""
        p = (((4.290 + self.e_vals)**-3.01) / ((1 + self.e_vals/854)))
        p = np.multiply(p, 1/ np.sum(p))

        return p
    
    def get_mean_energy(self):
        """Returns the mean energy of the distribution"""
        p_times_e = np.multiply(self.e_vals, self.p_values)
        e_X = np.sum(p_times_e)
        return e_X

    
    def plot_distribution(self):
        ax.plot(self.e_vals, self.p_values, label = f'Mean energy = {self.mean:.2f} GeV')
        ax.legend()
        ax.set_xlabel('Energy / GeV')
        ax.set_ylabel('Probability of Energy')
        plt.title(f'Energy Probability Function. Min: {self.emin:.2f} GeV. Max: {self.emax:.2f} GeV')
        plt.show()
        

energy_dist = Energy_Distribution(0.110, 300)
energy_dist.plot_distribution()


# e_min = 0.1 #100 MeV

# e_maxes = [i for i in x]

# for emax in e_maxes:
#     distrib = Energy_Distribution(e_min, emax)
#     mean = distrib.mean
#     means.append(mean)

# plt.plot(x, means)
# plt.yticks(np.arange(np.min(means), np.max(means), 0.5))
# plt.title(f'Mean Energy as a Function of Maximum Energy. Min Energy: {e_min} GeV')
# plt.xlabel('Max Energy / GeV')
# plt.ylabel('Mean Energy / Gev')
# #plt.savefig('max_energy_vs_mean.png')
# plt.show()

# def animate(i):
#     ax.clear()
#     e_max = e_maxes[i]
#     distribution1 = Energy_Distribution(e_min, e_max)
#     distribution1.plot_distribution()
#     return 0

# anim = animation.FuncAnimation(fig, animate, frames = len(e_maxes), interval = 1000)

# plt.show()

# anim.save('energy_distribution_animation_2.gif')