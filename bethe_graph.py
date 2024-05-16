import simulation_package.bethe_equation as bethe
import numpy as np
import matplotlib.pyplot as plt

def beta_gamma_to_energy(beta_gamma):

    energy = 206*0.511 * np.sqrt((beta_gamma**2) + 1)

    return energy

def energy_to_beta_gamma(energy):

    beta_gamma = np.sqrt(((energy / (206*0.511))**2 - 1))

    return beta_gamma

print(beta_gamma_to_energy(1e-3))

atomic_no = 64
mass_no = 118.17
excitation_energy = 64.7 #In eV, based on light of wavelength 425nm
rho = 1.081 #density in g/cm^3
muon_mass = 105.658

eps = 1e-7

betas = np.linspace(0.000000001, 0.9999999999, 100)
gammas = 1/np.sqrt((1-betas**2))

y = bethe.bethe_equation(atomic_no, mass_no, gammas, betas, muon_mass, excitation_energy, rho)

fig, ax1 = plt.subplots()

ax1.plot(np.multiply(betas,gammas), abs(y), label = 'Simulated Bethe-Bloch')
ax1.set_xlabel('βγ')
ax1.set_xscale('log')
ax1.set_xlim(1e-3,1000)

ax1.set_ylabel('(-dE/dX) / MeVcm-1')
ax1.set_yscale('log')

secax = ax1.secondary_xaxis('top', functions=(beta_gamma_to_energy, energy_to_beta_gamma))
secax.set_xlabel('\nMuon Energy / MeV\n')

plt.axvline(0.1, color='g', ls='--', label = 'βγ = 0.1')
plt.axvline(100, color='r', ls='--', label = 'βγ = 1000')

plt.legend()
plt.title('Bethe-Bloch Formula Used in Simulation')
plt.show()