import numpy as np

"""
                TO DO AND DESIRED FUNCTIONALITY FOR THE SIPM AND ARRAY CLASSES
                -Each array should have a cubic matrix representation used to store values
                -Eventually want a way of declaring explicitly how many SiPMs we want per scintillator

                Structure:
                    Each array has a list of Scintillators
                    Each scintillator itself has a list of SIPMS


"""

mean_efficiency = 0.8 #Modal/median/mean efficiency of the SiPMs
sigma_eff = 0.05 #Standard deviation of the efficiencies of the SiPMs


class Array:
        """Generates a square matrix of appropriate dimension for the muons to travel through. Takes the array dimension as an input."""

        def __init__(self, dimension, sipms_per_scintillator):
            
            #array dimension
            self.dimension = dimension 
            
            #number of scintillators. Equal to dimension**2 as one of the axes of the matrix is along the axis of the scintillator
            self.scintillator_no = dimension**2 

            #Number of SiPMs to be put in each scintillator
            self.sipms_per_scintillator = sipms_per_scintillator
            
            #Gives us the array representation as a cubic matrix
            self.matrix = self.initialise_matrix() 

            #Generates a list of scintillator objects in the array
            self.scintillators = self.initialise_N_scintillators() 
            

            
        def initialise_matrix(self):
            """Generates the matrix representation, with the second dimension "y" being the axis of the scintillating bars"""
             
            matrix = np.zeros((self.dimension, self.dimension, self.dimension))

            return matrix
        

        def initialise_N_scintillators(self):
            """Creates a list of scintillators for the array based on the dimensions of the """
            scintillator_list = []

            for i in range(self.scintillator_no):
                  scintillator_list.append(Scintillator(self.sipms_per_scintillator))

            return scintillator_list




class Scintillator:
    """Scintillator Class. Takes, as arguments, the no. of SiPMs in each scintillator."""

    def __init__(self, sipm_per_scintillator = 1):
        #Default number of SiPMs per scintillator is 1

        self.sipm_per_scintillator = sipm_per_scintillator

        self.sipms = self.initialise_sipms()

        #Creates an array, which tracks the number of detections per SiPM per scintillator
        self.detections = np.zeros((sipm_per_scintillator, 1))
        

    def initialise_sipms(self):
        sipms = []

        for i in range(self.sipm_per_scintillator):
             sipms.append(SIPM())

        return sipms
    
    def get_detections_or(self):
        """Uses or logic to see whether any of the SiPMs in the scintillator have produced a positive signal"""

        if any(self.detections):
             return True
        else:
             return False
         


class SIPM:
    """SiPM class with associated quantum efficiency and photoelectron modes. Also probabilistically generates an efficiency for each SiPM"""
    
    def __init__(self):
        #Quantum efficiency of the SiPM
        self.efficiency = self.generate_efficiency() 

        #Detection list to be plotted against time
        self.detections = [] 

    
    def generate_efficiency(self):
        """Uses a gaussian distribution to randomly generate SiPM efficiencies"""

        x_bar = mean_efficiency #Currently, the mean_efficiency is hard-coded at the top of this file

        eff = np.random.normal(x_bar, sigma_eff)

        return eff
    
    def caught_light(self):
        """Checks to see whether the SiPM catches the light of the scintillator."""
        chance = np.random.random()
        if chance <= self.efficiency:
             return True
        else:
             return False
