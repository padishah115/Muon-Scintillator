import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from muon import Muon
from array_stopping_power import *
from bethe_equation import *


"""Make sure that the simulation and run sim/plot methods are actually doing the same thing"""

def run_simulation_and_plot(stppw, rho, t_max, array_dimension, efficiency):

    t = 0 #Initialise time

    #These are two matrices for plotting "pulse" vs time.
    detection_array = [] #Overall signal master array
    times = []

    #25 Scintillators
    """
        1  2  3  4  5
        6  7  8  9  10
        11 12 13 14 15
        16 17 18 19 20
        21 22 23 24 25

    """

    scintillator_detections = {
        #Stores detection events for each of the 25 scintillators in the array

        'det1': [],
        'det2': [],
        'det3': [],
        'det4':[],
        'det5': [],
        'det6': [],
        'det7': [],
        'det8': [],
        'det9': [],
        'det10': [],
        'det11': [],
        'det12': [],
        'det13': [],
        'det14': [],
        'det15': [],
        'det16': [],
        'det17': [],
        'det18': [],
        'det19': [],
        'det20': [],
        'det21': [],
        'det22': [],
        'det23': [],
        'det24': [],
        'det25': []

    }


    muon1 = Muon(array_dimension)


    #The physical scintillator matrix.
    matrix = np.zeros((array_dimension,array_dimension,array_dimension))

    #Initial position of the muon.
    print(muon1.position)
    print(muon1.velocity)

    while t < t_max:
        """Main loop- the muon starts at the top of the array and then passes through the scintillators."""
        detection_status = 0 #Prevents double detection
        a = 0 #Determines which scintillator was triggered

        for i in range (0,3):
            #Check to see whether the muon is still inside of the scintillating array
            if muon1.position[i] >= array_dimension or muon1.position[i] < 0:
                muon1.in_matrix = False
        
        x = muon1.position[0]
        y = muon1.position[1]
        z = muon1.position[2]

        """LABELLING THE SCINTILLATOR WHICH THE MUON IS IN in order to append the detection event to the correct scintillator"""
        if z <= 4 and x <= 4:
            a = 5*z + x + 1
        
        elif z > 4 or x > 4:
            a = 0 #a is 0 if Not in array at all


        if muon1.in_motion:
            chance_sipm = np.random.random() #Check to see whether SiPM picks up the signal based on efficiency
            if chance_sipm <= efficiency and muon1.in_matrix and muon1.in_motion:
                #Check against quantum efficiency
                matrix[x, :, z] += 1
                print("Detection event")
                if detection_status == 0:
                    detection_array.append(1)
                    detection_status = 1
            else:
                if detection_status == 0:
                    detection_array.append(0)
            
            if muon1.in_matrix:
                #Check to see whether the muon stops inside of the array
                if check_stop(muon1.energy, stppw, rho, muon1.distance_travelled_in_array):
                    muon1.velocity = np.array([0,0,0])
                    muon1.in_motion = False
                    print("Muon has stopped inside of the array.")

            muon1.position = np.add(muon1.position, muon1.velocity)
            muon1.position = np.rint(muon1.position).astype(int)
            if not muon1.velocity.all(0) and muon1.in_matrix:
                muon1.distance_travelled_in_array += 1


        elif not muon1.in_motion and not muon1.decayed and muon1.in_matrix:
            #Check to see whether the muon, having stopped in the array, decays
            muon1.age += 1 #Lifetime after stopping
            exponent = np.exp(-muon1.age/muon1.lifetime)

            chance_decay = np.random.random()

            if chance_decay >= exponent:
                #Check against a random variable to see whether decay has occurred
                muon1.decayed = True
                print("Muon has decayed")
                matrix[x, :, z] += 1
                if detection_status == 0:
                    detection_array.append(1)
                    detection_status = 1
            
        
        for i in range(len(scintillator_detections)):
            #Append 0 in any case, and then replace this with 1 if there is a detection. 
            #Ensures that the dimensions of the scintillator detections arrays are correct.
            scintillator_detections[f'det{i+1}'].append(0)

        if detection_status == 1 and a != 0:
            scintillator_detections[f'det{a}'][-1] = 1

        times.append(t)
        t += 1

        #Sanity-check output on the console
        print(muon1.position)
        print(f"Time is {t}")



    detection_plane = matrix[:, 0, :]

    #Prints the "detection plane", i.e. slices of constant Y, to give quick visual check in the console window
    print(detection_plane)

    #Generating Meshgrids- X is the horizontal dimenion, Y is 
    X, Y = np.meshgrid(np.arange(array_dimension), np.arange(array_dimension))
    X_flatten = X.flatten()
    Y_flatten = Y.flatten()
    detection_flatten = detection_plane.flatten()

    #Generate 3D graph
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i, k, detection in zip(X_flatten, Y_flatten, detection_flatten):
        if detection > 0:
            ax.bar3d(i, k, 0, 1, 1, detection, color='r', alpha=0.8)


    #3D Bar graph which graphically displays detection events
    plt.ylabel('Horizonal axis (i)')
    plt.xlabel('Height (k)')
    plt.title('0 is max height, 5 is bottom of array')
    ax.set_xlim(0,array_dimension)
    ax.set_ylim(0,array_dimension)
    ax.set_zlim(0,2)
    plt.savefig('detection_bars.png')
    plt.show()

    #Plots for all scintillators
    fig, axs = plt.subplots(array_dimension, array_dimension, figsize = (20, 20))

    a_count = 1
    x = times

    #Populate the 25 graphs with the signals from each scintillator
    for i in range(array_dimension):
        for j in range(array_dimension):
            y = scintillator_detections[f'det{a_count}']
            axs[i,j].plot(x,y)
            axs[i,j].set_title(f'{a_count}')
            #axs[i,j].set_xlabel('Time')

            if j == 0:
                #Only add y axis labels to leftmost column in order to conserve space
                axs[i,j].set_ylabel('Signal Output')
            if j != 0 :
                #Remove the ticks from the y axis if the graph is not in the leftmost column
                axs[i,j].tick_params(labelleft=False)
            a_count += 1

    plt.tight_layout()
    plt.savefig('pulse graphs')
    plt.show()

def run_simulation_and_return_age(t_max, array_dimension, efficiency, rho, a_no, m_no, exc_energy): 
    """Removes all graphical displays or printed values. Takes as arguments: t_max of simulation, dimension for the square array, atomic number of the material,
    average excitation energy, W_max as max transfer of energy in collision"""

    t = 0 #Initialise time

    #These are two matrices for plotting "pulse" vs time.
    detection_array = [] #Overall signal master array
    times = []

    #25 Scintillators
    """
        1  2  3  4  5
        6  7  8  9  10
        11 12 13 14 15
        16 17 18 19 20
        21 22 23 24 25

    """

    scintillator_detections = {
        #Stores detection events for each of the 25 scintillators in the array

        'det1': [],
        'det2': [],
        'det3': [],
        'det4':[],
        'det5': [],
        'det6': [],
        'det7': [],
        'det8': [],
        'det9': [],
        'det10': [],
        'det11': [],
        'det12': [],
        'det13': [],
        'det14': [],
        'det15': [],
        'det16': [],
        'det17': [],
        'det18': [],
        'det19': [],
        'det20': [],
        'det21': [],
        'det22': [],
        'det23': [],
        'det24': [],
        'det25': []

    }



    muon1 = Muon(array_dimension)


    #The physical scintillator matrix.
    matrix = np.zeros((array_dimension,array_dimension,array_dimension))

    #Initial position of the muon.
    #print(muon1.position)
    #print(muon1.velocity)

    while t < t_max:
        """Main loop- the muon starts at the top of the array and then passes through the scintillators."""
        detection_status = 0 #Prevents double detection
        a = 0 #Determines which scintillator was triggered

        for i in range (0,3):
            #Check to see whether the muon is still inside of the scintillating array
            if muon1.position[i] >= array_dimension or muon1.position[i] < 0:
                muon1.in_matrix = False
        
        x = muon1.position[0]
        y = muon1.position[1]#Scintillator bar axis
        z = muon1.position[2]

        """LABELLING THE SCINTILLATOR WHICH THE MUON IS IN in order to append the detection event to the correct scintillator"""
        if z <= 4 and x <= 4:
            a = 5*z + x + 1
        
        elif z > 4 or x > 4:
            a = 0 #a is 0 if Not in array at all


        if muon1.in_motion:
            chance_sipm = np.random.random() #Check to see whether SiPM picks up the signal based on efficiency
            if chance_sipm <= efficiency and muon1.in_matrix and muon1.in_motion:
                #Check against quantum efficiency
                matrix[x, :, z] += 1
                #print("Detection event")
                if detection_status == 0:
                    detection_array.append(1)
                    detection_status = 1
            else:
                if detection_status == 0:
                    detection_array.append(0)
            
            if muon1.in_matrix:
                #Stoppping power calculation

                de = abs(rho * bethe_equation(a_no, m_no, muon1.gamma, exc_energy) * 5) #5 cm steps from scintillator to scintillator 
                muon1.energy -= de #Reduces the energy of the muon in line with the Bethe equation
                #print(muon1.energy)
                muon1.update_gamma()
                #muon1.update_velocity()

                # if check_stop(muon1.energy, stppw, rho, muon1.distance_travelled_in_array):
                #     muon1.velocity = np.array([0,0,0])
                #     muon1.in_motion = False
                #     #print("Muon has stopped inside of the array.")

            muon1.position = np.add(muon1.position, muon1.velocity)
            muon1.position = np.rint(muon1.position).astype(int)
            # if not muon1.velocity.all(0) and muon1.in_matrix:
            #     muon1.distance_travelled_in_array += 1


        elif not muon1.in_motion and not muon1.decayed and muon1.in_matrix:
            #Check to see whether the muon, having stopped in the array, decays
            muon1.age += 1 #Lifetime after stopping
            exponent = np.exp(-muon1.age/muon1.lifetime)

            chance_decay = np.random.random()

            if chance_decay >= exponent:
                #Check against a random variable to see whether decay has occurred
                muon1.decayed = True
                #print("Muon has decayed")
                matrix[x, :, z] += 1
                if detection_status == 0:
                    detection_array.append(1)
                    detection_status = 1
            
        if muon1.energy <= 0:
            #If energy falls to 0 then the muon cannot be in motion
            muon1.in_motion = False
        
        for i in range(len(scintillator_detections)):
            #Append 0 in any case, and then replace this with 1 if there is a detection. 
            #Ensures that the dimensions of the scintillator detections arrays are correct.
            scintillator_detections[f'det{i+1}'].append(0)

        if detection_status == 1 and a != 0:
            scintillator_detections[f'det{a}'][-1] = 1

        times.append(t)
        t += 1

        #Sanity-check output on the console
        #print(muon1.position)
        #print(f"Time is {t}")



    #detection_plane = matrix[:, 0, :]

    #Prints the "detection plane", i.e. slices of constant Y, to give quick visual check in the console window
    #print(detection_plane)

    return(muon1.age)