import numpy as np
from array_scintillator_sipm import *
from muon import Muon
from scintillator_label import *

array_dimension = 5
sipms_per_scintillator = 2

t = 0
tmax = 20

array = Array(array_dimension, sipms_per_scintillator)

muon1 = Muon(array_dimension)


in_matrix = False
in_motion = False
decayed = False

while t < tmax:
    print(muon1.position)
    
    #Check to see whether the muon has decayed

    #Check to see whether the muon is in the array
    in_matrix = muon1.is_contained()
    #Check to see whether the muon is in motion
    in_motion = muon1.is_in_motion()    
    #Logs whether there were any detection events during the time slice of interest
    detection_status = 0 
   #Determines which scintillator was triggered.
    a = get_scintillator_label(muon1.position, array_dimension) 
    scintillator_index = a - 1

    if in_motion:
        #Calculate what happens if the muon is in motion
        
        if not in_matrix:
            #Muon is in motion and OUTSIDE the array.
            pass

        else:
            #Muon is in motion and INSIDE the array.
            
            # 1: Check to see whether the SiPMs in the current scintillator detect the light or not
            if a == 0:
                print('Error- muon said to be inside matrix but returning scintillator label outside of the matrix')
            else:
                scintillator = array.scintillators[scintillator_index] #This calls the relevant scintillator object
                for i, sipm in enumerate(scintillator.sipms):
                    if sipm.caught_light:
                        #If the SIPM caught the signal from the scintillator flash, update the corresponding slot in the scintillator detections matrix.
                        scintillator.detections[i] += 1

            # 2: Calculate the energy loss due to the stopping power of the array.
            
    
    else:
        #Muon not in motion!
        
        if not in_matrix:
            #Should be impossible:
            print('Error- stationary muon outside of array.')
        
        else:


        
    
    #MAKE SURE TO UPDATE GAMMA AND VELOCITY BEFORE THIS. THIS SHOULD BE THE VERY LAST STEP.
    muon1.update_position()

    t += 1

    print(a)

# while t < tmax:
