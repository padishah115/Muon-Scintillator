import numpy as np
from velocity_distribution import *
#from energy_distribution import *

class Muon:
    """The goal of the simulation is to correctly model the passage of a muon of a particular
    energy through the array of scintillators. This means we need to calculate the stopping probability
    for the muon at each point in the array"""

    def __init__(self, array_dim):
        self.array_dimension = array_dim
        
        #self.energy = generate_energy() #Generate the muon energy given our information about the cosmic ray spectrum
        #self.v = v_from_energy(self.energy) #Absolute magnitude of velocity


        #Mean muon energy is 4GeV, meaning v is about c
        #Set c = 1
        self.velocity = np.array(generate_velocity(1)) #Returns velocity array
        

        self.position = np.array(self.generate_position())

        

        #Start the simulation with the muon inside of the matrix at t = 0, not decayed, and in motion.
        self.in_matrix = True #Is the muon still inside of the scintillating array?
        self.in_motion = True #Is the muon in motion?
        self.decayed = False #Has the muon decayed?


    def generate_position(self):
        #Generates the initial position of the muon given the velocity.
        
        if self.velocity[0] > 0 and self.velocity[1] > 0:
            i = 0
            j = 0
            k = np.random.randint(0,self.array_dimension)

        if self.velocity[0] > 0 and self.velocity[1] < 0:
            i = 0
            j = self.array_dimension - 1
            k = np.random.randint(0,self.array_dimension)
        
        if self.velocity[0] < 0 and self.velocity[1] > 0:
            i = self.array_dimension - 1
            j = 0
            k = np.random.randint(0,self.array_dimension)

        if self.velocity[0] < 0 and self.velocity[1] < 0:
            i = self.array_dimension -1
            j = self.array_dimension -1 
            k = np.random.randint(0,self.array_dimension)

        if self.velocity[0] == 0 and self.velocity[1] == 0:
                #Comes from vertically downwards
                i = np.random.randint(0, self.array_dimension)
                j = np.random.randint(0, self.array_dimension)
                k = 0
        
        if self.velocity[0] == 0 and self.velocity[1] != 0:
            if self.velocity[1] > 0:
                i = np.random.randint(0,self.array_dimension)
                j = 0
                k = np.random.randint(0,self.array_dimension)
            if self.velocity[1] < 0:
                i = np.random.randint(0,self.array_dimension)
                j = self.array_dimension - 1
                k = np.random.randint(0,self.array_dimension)


        if self.velocity [0] != 0 and self.velocity[1] == 0:
            if self.velocity[0] > 0:
                j = np.random.randint(0,self.array_dimension)
                i = 0
                k = np.random.randint(0,self.array_dimension)
            if self.velocity[0] < 0:
                j = np.random.randint(0,self.array_dimension)
                i = self.array_dimension - 1
                k = np.random.randint(0,self.array_dimension)
        

        return np.array([i,j,k])

    def stopping_probability(self, dx, n_e, Z, A):
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