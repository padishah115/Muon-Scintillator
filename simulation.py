import numpy as np
from array_scintillator_sipm import *
from muon import Muon
from scintillator_label import *
from bethe_equation import *
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
#import datetime

current_directory = os.getcwd()

def run_simulation(tmax, sipms_per_scintillator, array_dimension, atomic_no, mass_no, excitation_energy, rho, max_muon_energy, min_muon_energy=200, dx=5):
    """Runs the simulation and returns the decayed muon ages (muon age of 0 indicates that the muon did not decay inside of the array), and whether the
    muon was stopped in the array as a 0 or 1 value"""

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
                muon1.age += 1 / muon1.get_gamma()
                
        
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
                        muon1.age += 1
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
        print(f'Position: {muon1.position}')
        print(f'Velocity: {muon1.velocity}')

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
                muon1.age += 1 / muon1.get_gamma()
                
        
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
                        muon1.age += 1
        else:
            print('Error- neither in motion nor not in motion')

        #Updates sipm detections list based on whether the sipm.flashed value is true or false
        array.update_sipms()
        
        #MAKE SURE TO UPDATE GAMMA AND VELOCITY BEFORE THIS. THIS SHOULD BE THE VERY LAST STEP.
        muon1.update_position()

        t += 1

    #RECALL- WE ARE NO LONGER STORING SCINTILLATOR FLASHES WITHIN THE MATRIX ELEMENT. 
    #WE ARE NOW INSTEAD STORING THEM IN A MULTIDIMENSIONAL ARRAY INSIDE OF EACH SCINTILLATOR CLASS


    detection_plane = array.return_detection_plane()
    #print(detection_plane)

    #Generating Meshgrids
    X, Y = np.meshgrid(np.arange(array_dimension), np.arange(array_dimension))
    X_flatten = X.flatten()
    Y_flatten = Y.flatten()


    # #Generate 3D graph
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #List of colours
    colors = ['r', 'g', 'b', 'c', 'y', 'k', 'w', 'm']

    max_height = 1

    for x in range(array.sipms_per_scintillator):
        #Generate z values for each slice of the detection plane, i.e. for each sipm
        detection_flatten = detection_plane[x, :, :].flatten()
        color1 = colors[x % len(colors)] #Make sure each sipm gets its own color

        if x != 0:
            height = np.max(detection_plane[x-1,:,:])
        else:
            height = 0
        
        max_height += height

        for i, k, detection in zip(X_flatten, Y_flatten, detection_flatten):
            if detection > 0:
                ax.bar3d(k, i, max_height, 1, 1, detection, color=color1, alpha=0.8, label=f'SiPM{x}')
                


    #3D Bar graph which graphically displays detection events
    plt.ylabel('Horizonal axis (i)')
    plt.xlabel('Height (k)')
    plt.title(f'0 is max height, 5 is bottom of array. Muon energy: {muon1.energy/1000:.2f} GeV')
    ax.set_xlim(0,array_dimension)
    ax.set_ylim(0,array_dimension)
    ax.set_zlim(0,max_height)
    plt.savefig(current_directory+f'\\bar graphs\detection_bars_energy_{muon1.energy:.2f}.png')
    plt.show()
    
    

    #Plots for all scintillators
    fig, axs = plt.subplots(array_dimension, array_dimension, figsize = (20, 20))

    x = np.arange(0, tmax+1)

    #List of styles
    styles = ['-', '--', '-.', ':', ',', 'o', '^']

    #Populate the dim*dim graphs with the signals from each scintillator
    for i in range(array_dimension):
         for j in range(array_dimension):
            #Initialise graph for each scintillator in the array
            scintillator_index = i*array_dimension + j
            sipm_number = array.sipms_per_scintillator
            scintillator = array.scintillators[scintillator_index]

            for k in range(sipm_number):
                #One plot per scintillator graph per SiPM
                y = scintillator.sipms[k].detections
                axs[i,j].plot(x,y, label=f'SiPM {k+1}', color=colors[k % len(colors)], linestyle=styles[k % len(styles)])
                axs[i,j].legend()

            axs[i,j].set_title(f'{scintillator_index+1}')
            axs[i,j].set_xlabel('Time')

            if j == 0:
                #Only add y axis labels to leftmost column in order to conserve space
                axs[i,j].set_ylabel('Signal Output')
            if j != 0 :
                #Remove the ticks from the y axis if the graph is not in the leftmost column
                axs[i,j].tick_params(labelleft=False)

    plt.tight_layout()
    plt.savefig(current_directory+f'\\Pulse graphs\pulse graphs energy {muon1.energy:.2f}.png')
    plt.show()
    
    
    
