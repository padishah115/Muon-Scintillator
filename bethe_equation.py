import numpy as np

kappa = 0.3 #Coefficient of Bethe Equation
m_e = 0.511 #mass of electron
M = 206 * m_e #Mass of muon

def bethe_equation(atomic_no, mass_no, gamma, beta, muon_mass, excitation_energy):
    """Computes explicit form of the Bethe Equation using natural units"""

    W_max = (2 * m_e * gamma ** 2 * beta**2) / (1 + (2*gamma*m_e/muon_mass) + (m_e/muon_mass)**2)

    arg = 2 * m_e * gamma**2 * beta**2 * W_max/excitation_energy**2

    bethe = kappa * atomic_no/mass_no * (1/2 * np.log(abs(arg)) - beta**2)

    return bethe

