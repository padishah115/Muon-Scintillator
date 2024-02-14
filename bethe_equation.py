import numpy as np

kappa = 1 #Coefficient of Bethe Equation
m_e = 0.511 #mass of electron

def bethe_equation(atomic_no, mass_no, gamma, excitation_energy, W_max):
    """Computes explicit form of the Bethe Equation using natural units and assumption that beta = 1"""

    bethe = kappa * atomic_no/mass_no * (1/2 * np.log(abs(2*m_e*gamma**2*W_max/excitation_energy**2) - 1))

    return bethe