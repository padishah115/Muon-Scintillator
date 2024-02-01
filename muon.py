import numpy as np

class Muon:
    """The goal of the simulation is to correctly model the passage of a muon of a particular
    energy through the array of scintillators. This means we need to calculate the stopping probability
    for the muon at each point in the array"""

    def __init__(self, position, velocity):
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.in_matrix = True 
        self.in_motion = True
        self.decayed = False

        #The mean energy of muons at sea level is about 3 GeV. Eventually, I can turn this into a probabilistic distribution.
        self.energy = 4 #in GeV

    def set_velocity(self):
        """The probability distribution of muon angles at sea level is proportional to cos^2(theta) where theta is the zenith angle."""

        #Generate 
        costheta = np.random.random()

    def stopping_probability(self, dx, n_e):
        """Try and calculate the chance of a muon stopping inside of the scintillating array
        ARGUMENTS:
            dx = distance travelled in the array
            n_e = number density of the material it passes through
        """
        # if self.in_motion:
        #     #Only calculate the stopping probability of a muon which is in motion


        # else:
        #     pass 