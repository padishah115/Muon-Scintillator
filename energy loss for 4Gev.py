import numpy as np
import simulation_package.bethe_equation as bethe

rest_mass = 0.105658
max_energy = 300
sample_number = 10000


class energy_distribution_function:

    def __init__(self, min_energy:float, max_energy:float, sample_no:int):
        """Takes the minimum and maximum energies (GeV) of the distribution as argument, as well as the number of samples to be taken"""
        
        self.energies = np.linspace(min_energy, max_energy, sample_no)

        self.normalisation_factor = np.sum(((4.290 + self.energies)**-3.01) * (1 + self.energies/854)**-1)

    def get_pdf_value(self, energy:float):
        """Returns the value of the PDF for an energy in GeV"""

        numerator = ((4.290 + energy)**-3.01) * (1 + energy/854)**-1

        return numerator / self.normalisation_factor
    

energy_distribution_function(rest_mass, max_energy, sample_number)

c = 30 #cm/ns
distance_travelled_cm = 0
energy = 4 #4 GeV
energy_lost = 0

dx = 1e-5

while distance_travelled_cm < 5 and energy > rest_mass:
    #Energy lost when travelling through 25cm of PVT

    gamma = energy / rest_mass
    beta = np.sqrt(1-1/gamma**2)

    de_dx = bethe.bethe_equation(64, 118.170, gamma, beta, rest_mass, 64.7, 1.023)
    
    de = abs(de_dx * dx)

    energy_lost = energy_lost + abs(de)

    energy = energy - abs(de)
    distance_travelled_cm = distance_travelled_cm + dx

print(f'Energy lost: {energy_lost} MeV over {distance_travelled_cm} cm')
