import numpy as np
from array_scintillator_sipm import *
from muon import Muon
from scintillator_label import *
from bethe_equation import *
import os
from graphing_functions import *
#import datetime

current_directory = os.getcwd()

def run_simulation(tmax, sipms_per_scintillator, array_dimension, atomic_no, mass_no, excitation_energy, rho, max_muon_energy, min_muon_energy=200, dx=5):
    """Runs the simulation and returns the decayed muon ages (muon age of 0 indicates that the muon did not decay inside of the array), and whether the
    muon was stopped in the array as a 0 or 1 value
    Note that muon age is no longer being updated once the muon leaves the array"""

    t = 0

    #Initialise array
    array = Array(array_dimension, sipms_per_scintillator)

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
        a = get_scintillator_label(muon1.position, array_dimension) 
        scintillator_index = a - 1
        #Reset all sipms to FALSE for flashed
        array.reset_SIPMS()

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
                                    sipm.flashed = True
                                    #print('A SiPM pinged! a')

                # 2: Check chance of decay
                
                if muon1.decays():
                    #The muon has decayed!
                    muon1.decayed = True
                    if a == 0:
                            print('Error- muon decay not occuring within the matrix d')
                    else:
                        scintillator = array.scintillators[scintillator_index] #This calls the relevant scintillator object
                        for i, sipm in enumerate(scintillator.sipms):
                            if sipm.caught_light():
                                #If the SIPM caught the signal from the scintillator flash, update the corresponding slot in the scintillator detections matrix.
                                scintillator.detections[i] += 1 #Update corresponding scintillator array
                                sipm.flashed = True
                                #print('A SiPM pinged! e')
                        #print('Muon has decayed inside of the array! f')


                # 3: Calculate the energy loss due to the stopping power of the array.
                rho_de_dx = abs(bethe_equation(atomic_no, mass_no, muon1.get_gamma(), muon1.get_beta(), muon1.mass, excitation_energy, rho))
                de = abs(rho_de_dx * dx)


                #Decrease the energy of the muon appropriately
                muon1.energy -= de
                muon1.update_gamma()
                muon1.update_velocity()

                #Update muon rest-frame lifetime, accounting for time dilation
                muon1.age += 0.0001 / muon1.get_gamma()
                
        
        elif not in_motion:
            #Muon not in motion! Let's explicitly set the velocity to 0 just in case, though this should have already been taken care of.
            muon1.velocity = np.array([0,0,0])
            
            if not in_matrix:
                #Should be impossible: muon shouldn't be stationary outside the matrix
                print('Error- stationary muon outside of array. c')
            
            else:
                #Muon stationary and inside of the matrix
                if decayed:
                    #Muon has already decayed. Nothing to see here.
                    pass

                else:
                    #Check to see whether the muon now decays
                    if muon1.decays():
                        #The muon has decayed!
                        muon1.decayed = True
                        if a == 0:
                            print('Error- muon decay not occuring within the matrix d')
                        else:
                            scintillator = array.scintillators[scintillator_index] #This calls the relevant scintillator object
                            for i, sipm in enumerate(scintillator.sipms):
                                if sipm.caught_light():
                                    #If the SIPM caught the signal from the scintillator flash, update the corresponding slot in the scintillator detections matrix.
                                    scintillator.detections[i] += 1 #Update corresponding scintillator array
                                    sipm.flashed = True
                                    #print('A SiPM pinged! e')
                        #print('Muon has decayed inside of the array! f')
                    else:
                        #The muon lives to fight another day. Update his age inside of the matrix
                        muon1.age += 0.0001
        else:
            print('Error- neither in motion nor not in motion')

        #Updates sipm detections list based on whether the sipm.flashed value is true or false
        array.update_sipms()
        
        #MAKE SURE TO UPDATE GAMMA AND VELOCITY BEFORE THIS. THIS SHOULD BE THE VERY LAST STEP.
        muon1.update_position()

        t += 1

    #RETURN VALUES OF THE SIMULATION:
        #Two values returned: the age (float) and whether the muon was stopped (boolean)

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


def run_simulation_and_plot(tmax, sipms_per_scintillator, array_dimension, atomic_no, mass_no, excitation_energy, rho, max_muon_energy, min_muon_energy=200, dx=5):
    """Runs the simulation and plots graphs showing detection events for each scintillator"""

    t = 0

    #Initialise array
    array = Array(array_dimension, sipms_per_scintillator)

    #Initialise muon
    muon1 = Muon(array_dimension, max_muon_energy, min_muon_energy)

    in_matrix = False
    in_motion = False

    while t <= tmax:
        #print(f'Position: {muon1.true_position}')
        #print(f'Velocity: {muon1.velocity}')

        #Check to see whether the muon is in the array
        in_matrix = muon1.is_contained()
        #Check to see whether the muon is in motion
        in_motion = muon1.is_in_motion()    
        #Check to see whether the muon has decayed
        decayed = muon1.decayed
        #Determines which scintillator was triggered.
        a = get_scintillator_label(muon1.position, array_dimension) 
        scintillator_index = a - 1
        #Reset all sipms to FALSE for flashed
        array.reset_SIPMS()

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
                                    sipm.flashed = True
                                    print('A SiPM pinged! a')

                # 2: Check chance of decay
                
                if muon1.decays():
                    #The muon has decayed!
                    muon1.decayed = True
                    if a == 0:
                            print('Error- muon decay not occuring within the matrix d')
                    else:
                        scintillator = array.scintillators[scintillator_index] #This calls the relevant scintillator object
                        for i, sipm in enumerate(scintillator.sipms):
                            if sipm.caught_light():
                                #If the SIPM caught the signal from the scintillator flash, update the corresponding slot in the scintillator detections matrix.
                                scintillator.detections[i] += 1 #Update corresponding scintillator array
                                sipm.flashed = True
                                print('A SiPM pinged! e')
                        print('Muon has decayed inside of the array! f1')


                # 3: Calculate the energy loss due to the stopping power of the array.
                rho_de_dx = abs(bethe_equation(atomic_no, mass_no, muon1.get_gamma(), muon1.get_beta(), muon1.mass, excitation_energy, rho))
                de = abs(rho_de_dx * dx)


                #Decrease the energy of the muon appropriately
                muon1.energy -= de
                muon1.update_gamma()
                muon1.update_velocity()

                #Update muon rest-frame lifetime, accounting for time dilation
                muon1.age += 0.0001 / muon1.get_gamma()
                
        
        elif not in_motion:
            #Muon not in motion! Let's explicitly set the velocity to 0 just in case, though this should have already been taken care of.
            muon1.velocity = np.array([0,0,0])
            
            if not in_matrix:
                #Should be impossible: muon shouldn't be stationary outside the matrix
                print('Error- stationary muon outside of array. c')
            
            else:
                #Muon stationary and inside of the matrix
                if decayed:
                    #Muon has already decayed. Nothing to see here.
                    pass

                else:
                    #Check to see whether the muon now decays
                    if muon1.decays():
                        #The muon has decayed!
                        muon1.decayed = True
                        if a == 0:
                            print('Error- muon decay not occuring within the matrix d')
                        else:
                            scintillator = array.scintillators[scintillator_index] #This calls the relevant scintillator object
                            for i, sipm in enumerate(scintillator.sipms):
                                if sipm.caught_light():
                                    #If the SIPM caught the signal from the scintillator flash, update the corresponding slot in the scintillator detections matrix.
                                    scintillator.detections[i] += 1 #Update corresponding scintillator array
                                    sipm.flashed = True
                                    print('A SiPM pinged! e')
                        print('Muon has decayed inside of the array! f2')
                    else:
                        #The muon lives to fight another day. Update his age inside of the matrix
                        muon1.age += 0.0001
        else:
            print('Error- neither in motion nor not in motion')

        #Updates sipm detections list based on whether the sipm.flashed value is true or false
        array.update_sipms()
        
        #MAKE SURE TO UPDATE GAMMA AND VELOCITY BEFORE THIS. THIS SHOULD BE THE VERY LAST STEP.
        muon1.update_position()

        t += 1

    #RECALL- WE ARE NO LONGER STORING SCINTILLATOR FLASHES WITHIN THE MATRIX ELEMENT. 
    #WE ARE NOW INSTEAD STORING THEM IN A MULTIDIMENSIONAL ARRAY INSIDE OF EACH SCINTILLATOR CLASS

    print(f'Initial position: {muon1.initial_poisiton}')
    print(f'Final position: {muon1.final_position}')
    print(f'Time muon spent in array: {muon1.time_in_array}')
    generate_scintillator_graphs(array, muon1, tmax)
    #generate_muon_graph(muon1, muon1.initial_poisiton, muon1.final_position)
    
    
    
    
