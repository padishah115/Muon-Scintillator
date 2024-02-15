import numpy as np

class Muon:
    """The goal of the simulation is to correctly model the passage of a muon of a particular
    energy through the array of scintillators. This means we need to calculate the stopping probability
    for the muon at each point in the array"""

    def __init__(self, array_dim):
        self.array_dimension = array_dim
        
        #Mean muon energy is 4GeV, meaning v is about c
        #Set c = 1
        self.velocity = self.generate_velocity(1) #Returns velocity array 
        self.position = self.generate_position()

        self.mass = 206 * 0.511 #Muon mass in MeV

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
        https://arxiv.org/pdf/1606.06907.pdf as my reference"""

        energy = 4000 #default value is 4000 MeV

        energies = np.arange(self.mass, 10000, 1) #Energies between 105 MeV and 10000 MeV, increments of 1 MeV

        normalisation_factor = 0

        for e in energies:
            #Calculate the normalisation factor by summing over energies in the range
            normalisation_factor += ((4290 + e)**-3.01) * (1 + e/0.854)**-1

        ready = False

        while not ready:

            chance = np.random.random()
            energy_choice = np.random.choice(energies) #try random energy from the MeV matrix
            energy_probability = (1/normalisation_factor) *  (((4290 + energy_choice)**-3.01) * (1 + energy_choice/0.854)**-1) #Calculate probability

            if chance <= energy_probability: #Accept reject
                energy = energy_choice
                ready = True

        return energy

    def get_gamma(self):
        
        e = self.energy #Energy in MeV
        m = 206 * 0.511 #Muon Mass in MeV
        gamma = e / m

        return gamma

    def update_gamma(self):
        if self.energy > 105:
            e = self.energy #Energy in MeV
            m = 206 * 0.511 # Muon Mass in MeV
            gamma = e / m
        
        elif self.energy <= 105:
            #Ensure that gamma never less than 1
            #Make the muon stationary
            self.velocity = np.array([0,0,0])
            gamma = 1

        self.gamma = gamma

    # def update_velocity(self):
    #     return 0

    def generate_theta(self):
        """The muon cosmic ray spectrum is proportional to cos^2(theta)
        This function generates values of zenith angle, theta, given this distribution
        """

        ready = False #We keep looping until we beat the game of chance

        theta = 0 #default theta is directly downwards

        while not ready:
            theta_random = (np.pi / 2) * np.random.random() #Generate random phase between 0 and pi/2
            c2 = (np.cos(theta_random))**2
            chance = np.random.random()
            
            if chance < c2 and theta_random < 45/180 * np.pi: #reject anything above 45 degrees, as this is when cos^2 drops to 1/4
                theta = theta_random
                ready = True #we are ready to exit

        return theta


    def generate_velocity(self, v):
        """Generate a velocity given a value of zenith angle and velocity
            Requires you to pass the absolute magnitude of the velocity, which is given by 
            the muon momentum

            returns velocity and theta

            We need the returned velocity matrix to contain only integer values...
        """

        theta = self.generate_theta()

        v_z = v * np.cos(theta) #Project out the z component
        v_s = v * np.sin(theta) #Projects onto the x-y plane

        phi = np.random.random() * np.pi #Generate a random azimuthal angle

        v_x = v_s * np.cos(phi)
        v_y = v_s * np.sin(phi)

        velocity = np.array([v_x, v_y, v_z])

        return velocity
