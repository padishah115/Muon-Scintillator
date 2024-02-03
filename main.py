import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from muon import Muon


"""
TO DO:
    Calculate the stopping power of the array and use this to determine whether the muon comes to a stop inside of the
        array.
    Have a purple trajectory line follow the muon through the array


A note on units: we need to be careful with units. So far, the units of t, as well as
the velocity, are undefined.

For a muon at sea level, expect an energy of 4 GeV. This translates to a beta*gamma of about 38 

"""

#Setting duration of the simulation. The program will run from t=0 to t=tmax. Increments are in the ballpark of about 200ps
t = 0
t_max = 20

#Dimensions of the scintillator array- DO NOT CHANGE THIS
array_dimension = 5

#Properties of the detector. The values here will affect the energy loss of the muon inside of the array

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

#Setting up the parameters of the simulation.
efficiency = 0.99 #Encode the quantum efficiency of the SiPMs
stopping_probability = 0.1 #Probability that the muon will come to a complete rest inside the array

muon_lifetime = 2 #Mean lifetime, i.e. time taken for the muon population to decrease by a factor of e
#NB- this should be like 2.2ms, i.e. many, many picoseconds, so the value 2 is not realistic.

muon_age = 0 #How long the muon is alive after stopping.


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
    if z == 0:
        if x == 0:
            a = 1
        if x == 1:
            a = 2
        if x == 2:
            a = 3
        if x == 3:
            a = 4
        if x == 4:
            a = 5
    if z == 1:
        if x == 0:
            a = 6
        if x == 1:
            a = 7
        if x == 2:
            a = 8
        if x == 3:
            a = 9
        if x == 4:
            a = 10
    if z == 2:
        if x == 0:
            a = 11
        if x == 1:
            a = 12
        if x == 2:
            a = 13
        if x == 3:
            a = 14
        if x == 4:
            a = 15
    if z == 3:
        if x == 0:
            a = 16
        if x == 1:
            a = 17
        if x == 2:
            a = 18
        if x == 3:
            a = 19
        if x == 4:
            a = 20
    if z == 4:
        if x == 0:
            a = 21
        if x == 1:
            a = 22
        if x == 2:
            a = 23
        if x == 3:
            a = 24
        if x == 4:
            a = 25
    
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
            chance_stop = np.random.random()
            if chance_stop <= stopping_probability:
                muon1.velocity = np.array([0,0,0])
                muon1.in_motion = False
                print("Muon has stopped inside of the array.")

        muon1.position = np.add(muon1.position, muon1.velocity)
        muon1.position = np.rint(muon1.position).astype(int)

    elif not muon1.in_motion and not muon1.decayed and muon1.in_matrix:
        #Check to see whether the muon, having stopped in the array, decays
        muon_age += 1
        exponent = np.exp(-muon_age/muon_lifetime)

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
plt.title('0 is max height, 4 is bottom of array')
ax.set_xlim(0,array_dimension)
ax.set_ylim(0,array_dimension)
ax.set_zlim(0,2)
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
plt.show()