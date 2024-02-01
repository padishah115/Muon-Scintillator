import numpy as np
from velocity_distribution import *
from energy_distribution import *

class Muon:
    """The goal of the simulation is to correctly model the passage of a muon of a particular
    energy through the array of scintillators. This means we need to calculate the stopping probability
    for the muon at each point in the array"""

    def __init__(self, position):
        self.position = np.array(position)
        #self.energy = generate_energy() #Generate the muon energy given our information about the cosmic ray spectrum
        #self.v = v_from_energy(self.energy) #Absolute magnitude of velocity
        #self.velocity = generate_velocity(self.v)
        self.in_matrix = True 
        self.in_motion = True
        self.decayed = False   



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

        return 0