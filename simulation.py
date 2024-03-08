import numpy as np
import array_scintillator_sipm as arr
from muon import Muon
import scintillator_label
import bethe_equation as bethe
import os
import graphing_functions
#import datetime

current_directory = os.getcwd()

if __name__ == '__main__':
    print('Accessing simulation')

def run_simulation(plot, tmax, sipms_per_scintillator, array_dimension, dead_time_sipms_ns, atomic_no, mass_no, excitation_energy, rho, max_muon_energy, min_muon_energy=200, dx=5):
    """Runs the simulation and plots graphs showing detection events for each scintillator"""

    t = 0

    #Initialise array
    array = arr.Array(array_dimension, sipms_per_scintillator, dead_time_sipms_ns)

    #Initialise muon
    muon1 = Muon(array_dimension, max_muon_energy, min_muon_energy)

    in_matrix = False
    in_motion = False

    while t <= tmax:
        #print(muon1.position)

        #Check to see whether the muon is in the array
        in_matrix = muon1.is_contained()
        #Check to see whether the muon is in motion
        in_motion = muon1.is_in_motion()    
        #Check to see whether the muon has decayed
        decayed = muon1.decayed
        #Determines which scintillator was triggered.
        scintillator_index = scintillator_label.get_scintillator_index(muon1) 
        
        #Reset all sipms to FALSE for flashed
        array.reset_SIPMS()

        if in_motion:
            #Calculate what happens if the muon is in motion
            
            if not in_matrix:
                #Muon is in motion and OUTSIDE the array.
                #print('a')
                muon1.age = muon1.age + (1/muon1.get_gamma())

            else:
                #Muon is in motion and INSIDE the array.
                
                # 1: Check to see whether the SiPMs in the current scintillator detect the light or not
                if scintillator_index < 0:
                    print('Error- muon said to be inside matrix but returning scintillator label outside of the matrix')
                    #print('b')
                else:
                    #print('c')
                    scintillator = array.scintillators[scintillator_index] #This calls the relevant scintillator object
                    for i, sipm in enumerate(scintillator.sipms):
                                if sipm.caught_light(t):
                                    #If the SIPM caught the signal from the scintillator flash, update the corresponding slot in the scintillator detections matrix.
                                    scintillator.detections[i] += 1
                                    sipm.flashed = True
                                    #print('A SiPM pinged! d')
                                    

                # 2: Check chance of decay
                
                if muon1.decays():
                    #print('d')
                    print(muon1.decay_exp)
                    print(muon1.chance)
                    #The muon has decayed!
                    muon1.decayed = True
                    if scintillator_index < 0:
                            print('Error- muon decay not occuring within the matrix d')
                    else:
                        scintillator = array.scintillators[scintillator_index] #This calls the relevant scintillator object
                        for i, sipm in enumerate(scintillator.sipms):
                            if sipm.caught_light(t):
                                #If the SIPM caught the signal from the scintillator flash, update the corresponding slot in the scintillator detections matrix.
                                scintillator.detections[i] += 1 #Update corresponding scintillator array
                                sipm.flashed = True
                                #print('A SiPM pinged! e')
                        #print('Muon has decayed inside of the array! f')

                if not decayed:
                    #print('e')
                    #Update muon rest-frame lifetime, accounting for time dilation
                    muon1.age = muon1.age + (1 / muon1.get_gamma())

                    # 3: Calculate the energy loss due to the stopping power of the array.
                    rho_de_dx = abs(bethe.bethe_equation(atomic_no, mass_no, muon1.get_gamma(), muon1.get_beta(), muon1.mass, excitation_energy, rho))
                    de = abs(rho_de_dx * dx)

                    #Decrease the energy of the muon appropriately
                    muon1.update_energy(de)
                    muon1.update_gamma()
                    muon1.update_velocity()
                
        
        elif not in_motion:
            #print('f')
            #Muon not in motion! Let's explicitly set the velocity to 0 just in case, though this should have already been taken care of.
            muon1.velocity = np.array([0,0,0])
            
            if not in_matrix:
                #Should be impossible: muon shouldn't be stationary outside the matrix
                print('Error- stationary muon outside of array. c')
            
            else:
                #Muon stationary and inside of the matrix
                if decayed:
                    #print('g')
                    #Muon has already decayed. Nothing to see here.
                    pass

                else:
                    #Check to see whether the muon now decays
                    if muon1.decays():
                        #print('h')
                        #print(muon1.decay_exp)
                        #print(muon1.chance)
                        #The muon has decayed!
                        muon1.decayed = True
                        if scintillator_index < 0:
                            print('Error- muon decay not occuring within the matrix d')
                        else:
                            scintillator = array.scintillators[scintillator_index] #This calls the relevant scintillator object
                            for i, sipm in enumerate(scintillator.sipms):
                                if sipm.caught_light(t):
                                    #If the SIPM caught the signal from the scintillator flash, update the corresponding slot in the scintillator detections matrix.
                                    scintillator.detections[i] += 1 #Update corresponding scintillator array
                                    sipm.flashed = True
                                    #print('A SiPM pinged! f')
                        #print('Muon has decayed inside of the array! f')
                    else:
                        #The muon lives to fight another day. Update his age inside of the matrix
                        muon1.age = muon1.age + 1
                        #print('i')
        else:
            raise ValueError('Error- neither in motion nor not in motion')

        #Updates sipm detections list based on whether the sipm.flashed value is true or false
        array.update_sipms()
        
        #MAKE SURE TO UPDATE GAMMA AND VELOCITY BEFORE THIS. THIS SHOULD BE THE VERY LAST STEP.
        muon1.update_position()

        t = t + 1

    if muon1.decayed:
        print('Muon has decayed inside of the matrix.')

    if plot:
        #RECALL- WE ARE NO LONGER STORING SCINTILLATOR FLASHES WITHIN THE MATRIX ELEMENT. 
        #WE ARE NOW INSTEAD STORING THEM IN A MULTIDIMENSIONAL ARRAY INSIDE OF EACH SCINTILLATOR CLASS
        print(muon1.position_history)
        print(f'Initial position: {muon1.initial_poisiton}')
        print(f'Final position: {muon1.final_position}')
        print(f'Time muon spent in array: {muon1.time_in_array}')
        graphing_functions.generate_scintillator_graphs(array, muon1)
        graphing_functions.generate_muon_graph(muon1, muon1.initial_poisiton, muon1.final_position)
        graphing_functions.generate_muon_graph_with_scintillators(muon1, muon1.initial_poisiton, muon1.final_position)
    else:
        #RETURN VALUES OF THE SIMULATION:
        #Two values returned: the age (float) and whether the muon was stopped (boolean)
        #print(f'Age at end: {muon1.age}')
        print(f'Energy at end: {muon1.energy:.2f} MeV')

        if muon1.decayed and in_motion:
            #Muon decayed but wasn't stopped
            return muon1.age, 0
        elif muon1.decayed and not in_motion:
            #Muon decayed and was stopped
            return muon1.age, 1
        elif not muon1.decayed and in_motion:
            #Muon neither decayed nor stopped
            return 0, 0
        else:
            #Muon stopped but not decayed
            return 0, 1

    
    
    
    
