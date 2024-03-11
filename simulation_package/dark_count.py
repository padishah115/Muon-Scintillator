import numpy as np

######################################################################
# File for handling the dark count of SiPMs based on the temperature #
######################################################################

def check_dark_count(ionisation_energy, temperature):
    """Takes ionisation input in Joules and temperature in Kelvin"""

    #Calculation of Boltzmann Constant
    k_b = 8.3145 / (6.023*(10**23))
    T = temperature
    E = ionisation_energy

    #Calculate the Boltzman factor
    exp = np.exp(-E/(k_b*T))

    #Random chance number for use in accept-reject method
    chance = np.random.random()

    #Determine whether dark count occured by comparing random value to the boltzmann factor
    if chance < exp:
        return True
    
    return False
