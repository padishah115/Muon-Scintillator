import numpy as np

######################
# MUON CLASS LIBRARY #
######################

class Muon:
    """The goal of the simulation is to correctly model the passage of a muon of a particular
    energy through the array of scintillators. This means we need to calculate the stopping probability
    for the muon at each point in the array"""

    def __init__(self, array_dim, max_energy, min_energy):
        self.array_dimension = array_dim
        self.mass = 206 * 0.511 #Muon mass in MeV
        self.minimum_energy = np.max([self.mass, min_energy])
        self.max_angle_deg = 90 #Maximal zenith angle of the muons in units of degrees
        self.max_energy = max_energy #Maximum energy in distribution in MeV
        self.default_energy = 4000 #Default energy in MeV
        self.energies = np.linspace(self.minimum_energy, self.max_energy, 500) #Energies between 105 MeV and max MeV, 500 samples
        self.position_history = [] #For use later on in plotting the trajectories

        #First, generate energy using distribution. Use this to generate gamma. This, in turn, can be used to compute the velocity in natural units
        self.energy = self.generate_energy() #Energy in MeV
        self.gamma = self.get_gamma()
        
        #Mean muon energy is 4GeV, meaning v is about c
        #Set c = 1
        self.velocity = self.generate_velocity(1) #Returns velocity array 
        self.position = self.generate_position()
        self.true_position = self.position
        self.theta

        

        #Start the simulation with the muon inside of the matrix at t = 0, not decayed, and in motion.
        #self.in_matrix = True #Is the muon still inside of the scintillating array?
        #self.in_motion = True #Is the muon in motion?
        self.decayed = False #Has the muon decayed?

        self.distance_travelled_in_array = 1 #At beginning of simulation, all muons have already entered the array and hence travelled 1 block

        self.lifetime = 22000 #Characteristic decay time in 100s of picoseconds
        self.age = 0

        #These are for generating markers at the point of entry and point of exit in the array
        self.initial_poisiton = self.position #Sets the initial position 
        self.final_position = self.set_final_position() #Undefined until the muon exits the array
        self.time_in_array


    #GENERATORS

    def generate_position(self):
        """Generates the initial position of the muon given the velocity. """
        v_x = self.velocity[0]
        v_y = self.velocity[1]
        v_z = self.velocity[2]

        array_dim = self.array_dimension

        if abs(v_z) > abs(v_x) and abs(v_z) > abs(v_y):
            #if the vertical component is largest (this is the most likely case for muons as they have small zenith angles)
            k = 0 #Generate at the top of the array
            i = np.random.randint(0,array_dim)
            j = np.random.randint(0,array_dim)

        elif abs(v_x) > abs(v_y) and abs(v_x) > abs(v_z):
            if v_x > 0:
                i = 0
                k = np.random.randint(0,array_dim)
                j = np.random.randint(0,array_dim)
            elif v_x < 0:
                i = array_dim - 1
                j = np.random.randint(0,array_dim)
                k = np.random.randint(0,array_dim)

        elif abs(v_y) > abs(v_x) and abs(v_y) > abs(v_z):
            if v_y > 0:
                j = 0
                k = np.random.randint(0,array_dim)
                i = np.random.randint(0,array_dim)
            elif v_y < 0:
                j = array_dim - 1
                i = np.random.randint(0,array_dim)
                k = np.random.randint(0,array_dim)

        else:
            print(f'Muon velocity: {self.velocity}')
            raise ValueError('Invalid velocity direction when generating initial muon position')

        return np.array([i,j,k])
    

    def generate_energy(self):
        """Generates a random muon energy between 1 and 10 Gev in steps of 1, using the paper
        https://arxiv.org/pdf/1606.06907.pdf as my reference for the shape of the energy distribution.
        
        The original paper uses an experimental fit for the intensity of muons at different values of energy.

        I have used the shape of this intensity plot and used a normalisation proceduce below to turn this into a probability density.
        """

        energy = self.default_energy #default value is 4000 MeV

        normalisation_factor = sum(((4290 + e)**-3.01) * (1 + e/0.854)**-1 for e in self.energies)

        ready = False

        while not ready:
            
            chance = np.random.random()
            energy_choice = np.random.choice(self.energies) #try random energy from the MeV matrix
            energy_probability = (1/normalisation_factor) *  (((4290 + energy_choice)**-3.01) * (1 + energy_choice/0.854)**-1) #Calculate probability

            if chance <= energy_probability: #Accept reject
                energy = energy_choice
                ready = True

        return energy
    

    def calculate_theta(self):
        """The muon cosmic ray spectrum is proportional to cos^2(theta)
        This function generates values of zenith angle, theta, given this distribution, using an accept-reject method.
        """

        ready = False #We keep looping until we beat the game of chance

        theta = 0 #default theta is directly downwards

        while not ready:
            theta_random = (np.pi / 2) * np.random.random() #Generate random phase between 0 and pi/2
            c2 = (np.cos(theta_random))**2
            chance = np.random.random()
            
            if chance < c2 and theta_random < self.max_angle_deg/180 * np.pi: #reject anything above 45 degrees, as this is when cos^2 drops to 1/4
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

        theta = self.calculate_theta()
        self.theta = theta
        

        v_z = v * np.cos(theta) #Project out the z component
        v_s = v * np.sin(theta) #Projects onto the x-y plane

        phi = np.random.random() * np.pi #Generate a random azimuthal angle

        v_x = v_s * np.cos(phi)
        v_y = v_s * np.sin(phi)

        velocity = np.array([v_x, v_y, v_z])

        gamma = self.gamma
        beta = beta = np.sqrt(1-1/gamma**2)

        #c=1 so use beta to find overall value of velocity
        velocity = np.multiply(velocity, beta)


        return velocity
    
    #RETURNS

    def get_gamma(self):
        
        e = self.energy #Energy in MeV
        m = self.mass #Muon Mass in MeV
        gamma = e / m

        return gamma
    
    def get_beta(self):
        """Returns absolute magnitude of velocity as a fraction of c"""
        gamma = self.gamma
        beta = np.sqrt(1 - 1/gamma**2)

        return beta
    
    #MUTATORS

    def update_gamma(self):
        """Updates value of gamma based on energy loss. ALWAYS CALL THIS BEFORE UPDATING VELOCITY"""
        if self.energy > self.mass:
            e = self.energy #Energy in MeV
            m = self.mass # Muon Mass in MeV
            gamma = e / m
        
        elif self.energy <= self.mass:
            #Ensure that gamma never less than 1
            #Make the muon stationary
            self.velocity = np.array([0,0,0])
            gamma = 1

        self.gamma = gamma
    

    def update_velocity(self):
        """Updates velocity based on updated values of gamma. ALWAYS CALL THIS AFTER UPDATE_GAMMA"""
        gamma = self.gamma
        beta = np.sqrt(1-1/gamma**2)

        #Velocity init
        self.velocity = np.multiply(self.velocity, beta)


    def update_position(self):
        """Updates the position of the particle"""
        self.position_history.append(self.true_position)

        self.true_position = np.add(self.true_position, self.velocity)
        self.position = np.rint(self.true_position).astype(int) #Rounded to better fit in with the quantised array


    #LOGIC CHECKERS
        #Is the muon contained in the matrix?
        #Is the muon still in motion?
        #Does the muon decay?

    def is_contained(self):
        """Checks to see whether the muon is contained within the array matrix"""
        for i in range (0,3):
        #Check to see whether the muon is still inside of the scintillating array
            if self.position[i] >= self.array_dimension or self.position[i] < 0:
                return False
        return True

    def is_in_motion(self):
        """Checks to see whether the muon is still in motion"""
        if any(self.velocity):
            return True
        else:
            return False
        
    def decays(self):
        """Check to see whether the muon decays given its age. If it has decayed, set "decayed" to true"""
        chance = np.random.random()
        exp = np.exp(-self.age / self.lifetime)

        if chance < exp:
            return False
        else:
            self.decayed = True
            return True
    
    def set_final_position(self):
        """Takes the final position as input and updates the final position parameter accordingly"""
        pos = self.true_position
        tolerance = 10**-1
        step_size = 0.01

        ready = False
        k = 0

        while not ready:
            pos = np.add(pos, np.multiply(self.velocity, step_size))
            k += 1
            for i in range(3):
                if abs(pos[i] - self.array_dimension) <= tolerance:
                    self.time_in_array = int(np.ceil(k*step_size))
                    return pos

