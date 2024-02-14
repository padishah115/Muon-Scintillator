import numpy as np


def check_stop(energy, stppow, rho, distance_travelled_in_array):
    """Pass the muon energy, stopping power in MeV and density in grams cm-3"""

    R = energy / (stppow * rho) #Expected stopping distance as calculated in 

    equiv_R = np.ceil(R/5) #One unit in the matrix corresponds to a real-world distance of 50mm or 5 cm

    stopping_curve = np.exp(-distance_travelled_in_array/equiv_R) #Population number vs time. Exponential decay curve

    chance = np.random.random()

    if chance >= stopping_curve:
        return True
    else:
        return False
    

