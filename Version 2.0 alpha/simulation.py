import numpy as np
from array_scintillator_sipm import *
from muon import Muon
from scintillator_label import *
from bethe_equation import *

array_dimension = 5
sipms_per_scintillator = 2

atomic_no = 29
mass_no = 63.5
excitation_energy = 3 #In eV, based on light of wavelength 425nm
rho = 8.96 #density in g/cm^3

t = 0
tmax = 20
dx = 5 #Distance across each element, in 5cm

no_of_decays = 0

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
                    if sipm.caught_light():
                        #If the SIPM caught the signal from the scintillator flash, update the corresponding slot in the scintillator detections matrix.
                        scintillator.detections[i] += 1
                        print('A scintillator flashed!')

            # 2: Calculate the energy loss due to the stopping power of the array.
            rho_de_dx = abs(bethe_equation(atomic_no, mass_no, muon1.get_gamma(), muon1.get_beta(), muon1.mass, excitation_energy, rho))
            de = abs(rho_de_dx * dx)

            #Decrease the energy of the muon appropriately
            muon1.energy -= de
            muon1.update_gamma()
            muon1.update_velocity()

            if muon1.get_gamma() == 1:
                print('Muon has stopped inside of the array!')
    
    else:
        #Muon not in motion! Let's explicitly set the velocity to 0 just in case, though this should have already been taken care of.
        muon1.velocity = np.array([0,0,0])
        
        if not in_matrix:
            #Should be impossible: muon shouldn't be stationary outside the matrix
            print('Error- stationary muon outside of array.')
        
        else:
            #Muon stationary and inside of the matrix
            if muon1.decayed:
                #Muon has already decayed. Nothing to see here.
                pass
            else:
                #Check to see whether the muon now decays
                if muon1.decays():
                    #The muon has decayed!
                    no_of_decays += 1
                    print('Muon has decayed inside of the array!')
                else:
                    #The muon lives to fight another day. Update his age inside of the matrix
                    muon1.age += 1

        
    
    #MAKE SURE TO UPDATE GAMMA AND VELOCITY BEFORE THIS. THIS SHOULD BE THE VERY LAST STEP.
    muon1.update_position()

    t += 1

    print(a)


print(f'Age of muon: {muon1.age}')
