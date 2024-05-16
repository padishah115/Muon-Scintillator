import numpy as np


def bethe_equation(atomic_no:float, mass_no:float, gamma:float, beta:float, muon_mass:float, excitation_energy:float, rho:float):
    """Computes explicit form of the Bethe Equation using natural units"""

    kappa = 0.307 #Coefficient of Bethe Equation
    m_e = 0.511 #mass of electron
    M = 105.658 #Mass of muon

    plasma_energy = np.sqrt(rho * atomic_no/mass_no) * 28.816

    #Density correction
    delta = np.log(plasma_energy / excitation_energy) + np.log(gamma*beta) - 0.5

    #Max energy transfer
    W_max = (2 * m_e * (gamma ** 2) * (beta**2)) / (1 + (2*gamma*m_e/muon_mass) + (m_e/muon_mass)**2)

    #Argument of logarithm
    arg = 2 * m_e * (gamma**2) * (beta**2) * W_max/(excitation_energy**2)

    #Bethe formula
    bethe = (kappa * (atomic_no/mass_no) * (1/(beta)**2) * (1/2 * np.log(arg) - beta**2 -delta)) * rho

    return bethe


    



