import numpy as np

mean_efficiency = 0.55 #Modal/median/mean photon detection efficiency of the SiPMs
sigma_eff = 0.05 #Standard deviation of the efficiencies of the SiPMs


class Array:
        """Generates a square matrix of appropriate dimension for the muons to travel through. Takes the array dimension as an input."""

        def __init__(self, dimension, sipms_per_scintillator, dead_time_sipms_ns):
            
            #array dimension
            self.dimension = dimension 
            
            #number of scintillators. Equal to dimension**2 as one of the axes of the matrix is along the axis of the scintillator
            self.scintillator_no = dimension**2 

            #Number of SiPMs to be put in each scintillator
            self.sipms_per_scintillator = sipms_per_scintillator

            #Dead time of SiPMs nanoseconds
            self.dead_time_sipms_ns = dead_time_sipms_ns
            
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
                  scintillator_list.append(Scintillator(self.dead_time_sipms_ns, self.sipms_per_scintillator))

            return scintillator_list
        
        ####################
        # DETECTION PLANES #
        ####################
                
        def return_detection_plane(self):
            """This function should return a multidimensional array. Each slice in the x-direction should be the SiPM counts from a different scintillator."""
            
            detection_array = np.zeros((self.sipms_per_scintillator, self.dimension, self.dimension))

            for i in range(self.dimension):
                 for j in range(self.dimension):
                      for k in range(self.sipms_per_scintillator):
                           index = i* self.dimension + j
                           flash_no = self.scintillators[index].detections[k][0]
                           detection_array[k][i][j] += flash_no

            return detection_array
        
        # def return_OR_detection_plane(self):
        #     """Returns signals from the array if SiPMs used in conjunction with OR logic"""
        #     detection_array_OR = np.zeros((self.dimension, self.dimension))
            
        #     for i in range(self.dimension):
        #          for j in range(self.dimension):
        #               index = i*self.dimension + j
        #               if self.scintillators[index].any_sipms_flashed():
        #                    detection_array_OR[i][j] += 1

        #     return detection_array_OR    

        
        def return_AND_detection_plane(self):
            """Returns signals for the array if SiPMs used in conjucntion with AND logic"""
            detection_array_and = np.zeros((self.dimension, self.dimension))
            
            for i in range(self.dimension):
                 for j in range(self.dimension):
                      index = i*self.dimension + j
                      detection_array_and[i][j] += self.scintillators[index].AND_sipms_flashed()

            return detection_array_and


        ################
        # SIPM METHODS #
        ################

        def reset_SIPMS(self):
             """Resets all SIPMS to unflashed state"""
             for scintillator in self.scintillators:
                  for sipm in scintillator.sipms:
                       sipm.flashed = False

        def update_sipms(self):
             """if the SIPMS have not flashed, append 0 values to each SIPMS"""
             for i in range(self.dimension):
                for j in range(self.dimension):
                    index = i * self.dimension + j
                    scintillator = self.scintillators[index]
                    for k in range(self.sipms_per_scintillator):
                        sipm = scintillator.sipms[k]
                        if sipm.flashed:
                            sipm.detections.append(1)
                        else:
                            sipm.detections.append(0)






class Scintillator:
    """Scintillator Class. Takes, as arguments, the no. of SiPMs in each scintillator."""

    def __init__(self, dead_time_sipms_ns, sipm_per_scintillator = 1):
        """Takes the dead time of SiPMs in ns and the number of sipms per scintillator as arguments"""
        #Default number of SiPMs per scintillator is 1

        self.sipm_per_scintillator = sipm_per_scintillator
        self.dead_time_sipms_ns = dead_time_sipms_ns

        self.sipms = self.initialise_sipms()

        #Creates an array, which tracks the number of detections per SiPM per scintillator
        self.detections = np.zeros((sipm_per_scintillator, 1))
        

    def initialise_sipms(self):
        sipms = []

        for i in range(self.sipm_per_scintillator):
             sipms.append(SIPM(self.dead_time_sipms_ns))

        return sipms
    
    def AND_sipms_flashed(self):
        """Returns number of events for which at least two sipms flashed"""
        event_no = 0

        for i, sipm1 in enumerate(self.sipms):
             for j, sipm2 in enumerate(self.sipms):
                flash_times1 = sipm1.flash_times
                flash_times2 = sipm2.flash_times
                if i < j:    
                    for time1 in flash_times1:
                        for time2 in flash_times2:
                            if time1 == time2:
                                event_no = event_no + 1
        
        return event_no


class SIPM:
    """SiPM class with associated quantum efficiency and photoelectron modes. Also probabilistically generates an efficiency for each SiPM"""
    
    def __init__(self, dead_time_ns):
        """Takes the dead time in ns as an argument"""
        #Quantum efficiency of the SiPM
        self.efficiency = self.generate_efficiency() 

        #Detection list to be plotted against time
        self.detections = [] 
        

        self.flashed = False

        #Stores time and location at which the SiPM flashed. This is for use in generating and/or graphs
        self.flash_times = []
        
        
        self.dead_time = (dead_time_ns * 10**-9) / (100*10**-12)
        self.last_flashed_time = 0

    
    def generate_efficiency(self):
        """Uses a gaussian distribution to randomly generate SiPM efficiencies"""

        x_bar = mean_efficiency #Currently, the mean_efficiency is hard-coded at the top of this file

        eff = np.random.normal(x_bar, sigma_eff)

        return eff
    
    def caught_light(self, t):
        """Checks to see whether the SiPM catches the light of the scintillator."""
        chance = np.random.random()
        if self.last_flashed_time == 0:
             #First flash
             self.last_flashed_time = t+1e-5 #Prevents edge case of flash occuring at t = 0 and then last_flashed time being set to 0
             return True
        if chance < self.efficiency and t - self.last_flashed_time > self.dead_time and self.last_flashed_time !=0:
             #Not the first flash
             self.last_flashed_time = t
             return True
        else:
             return False
