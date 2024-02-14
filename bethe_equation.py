import numpy as np

kappa = 0.3 #Coefficient of Bethe Equation
m_e = 0.511 #mass of electron
M = 206 * m_e #Mass of muon

def bethe_equation(atomic_no, mass_no, gamma, excitation_energy):
    """Computes explicit form of the Bethe Equation using natural units and assumption that beta = 1"""

    W_max = (2 * m_e * gamma ** 2) / (1 + (2*gamma*m_e/M) + (m_e/M)**2)

    arg = 2*m_e*gamma**2*W_max/excitation_energy**2

    bethe = kappa * atomic_no/mass_no * (1/2 * np.log(abs(arg)) - 1)

    return bethe

#print(bethe_equation(29,63,38,3))