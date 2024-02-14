import numpy as np
from velocity_distribution import *
#from energy_distribution import *

class Muon:
    """The goal of the simulation is to correctly model the passage of a muon of a particular
    energy through the array of scintillators. This means we need to calculate the stopping probability
    for the muon at each point in the array"""

    def __init__(self, array_dim):
        self.array_dimension = array_dim
        
        #Mean muon energy is 4GeV, meaning v is about c
        #Set c = 1
        self.velocity = generate_velocity(1) #Returns velocity array 
        self.position = np.array(self.generate_position())

        

        #Start the simulation with the muon inside of the matrix at t = 0, not decayed, and in motion.
        self.in_matrix = True #Is the muon still inside of the scintillating array?
        self.in_motion = True #Is the muon in motion?
        self.decayed = False #Has the muon decayed?

        self.distance_travelled_in_array = 1 #At beginning of simulation, all muons have already entered the array and hence travelled 1 block
        self.energy = self.generate_energy() #Energy in MeV

        self.gamma = self.get_gamma()

        self.lifetime = 2.2
        self.age = 0


    def generate_position(self):
        """Generates the initial position of the muon given the velocity."""
        
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
    

    def generate_energy(self):
        """Generates a random energy between 1 and 10 Gev in steps of 1, using the paper
        https://arxiv.org/pdf/1606.06907.pdf"""

        energy = 4000 #default value is 4000 MeV

        energies = np.arange(1,11) #Energies between 1 and 10 GeV
        energies_mev = np.multiply(energies, 1000) #Convert to MeV

        normalisation_factor = 0

        for e in energies_mev:
            #Calculate the normalisation factor by summing over energies in the range
            normalisation_factor += ((4290 + e)**-3.01) * (1 + e/854)**-1

        ready = False

        while not ready:

            chance = np.random.random()
            energy_choice = np.random.choice(energies_mev) #try random energy from the MeV matrix
            energy_probability = (1/normalisation_factor) *  (((4290 + energy_choice)**-3.01) * (1 + energy_choice/854)**-1) #Calculate probability

            if chance <= energy_probability: #Accept reject
                energy = energy_choice
                ready = True

        return energy

def get_gamma(self):
    e = self.energy #Energy in MeV
    m = 206 * 0.511 #Mass in MeV
    gamma = e / m

    return gamma

