import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#Setting duration of the simulation. The program will run from t=0 to t=tmax
t = 0
t_max = 20

#Dimensions of the scintillator array
array_dimension = 5

#These are two matrices for plotting "pulse" vs time.
detection_array = []
times = []


#Setting up the parameters of the simulation.
efficiency = 0.6 #Encode the quantum efficiency of the SiPM
stopping_probability = 0.1 #Probability that the muon will come to a complete rest inside the array
muon_lifetime = 2 #Mean lifetime, i.e. time taken for the muon population to decrease by a factor of e
muon_age = 0 #How long the muon is alive after stopping.


i = np.random.randint(0,array_dimension) #X coordinate
j = np.random.randint(0,array_dimension) #Y coordinate- call this the depth of the scintillator array. All along the Y axis, we will have it set to 1 when there is a detection event
k = 0 #Z coordinate. We assume the muon arrives from above, so have it enter from the top of the array.

#Initial velocity parameters
vi = np.random.randint(0,2)
vj = np.random.randint(0,2)
vk = 1 #Always will have a downwards velocity

#Position and velocity arrays for the muon as it travels through the scintillating array
position = np.array([i, j, k])
velocity = np.array([vi, vj, vk])

#The physical scintillator matrix.
matrix = np.zeros((array_dimension,array_dimension,array_dimension))

#Initial position of the muon.
print(position)


#Boolean values to help handle different events in the array.
in_matrix = True
in_motion = True
decayed = False

while t < t_max:
    """Main loop- the muon starts at the top of the array and then passes through the scintillators."""
    detection_num = 0 #Number of detection events

    for i in range (0,3):
        if position[i] >= array_dimension:
            in_matrix = False
    
    x = position[0]
    y = position[1]
    z = position[2]

    if in_motion:
        chance_sipm = np.random.random()
        if chance_sipm <= efficiency and in_matrix:
            matrix[x, :, z] += 1
            print("Detection event")
            detection_num += 1
        else:
            detection_num += 1
        
        if in_matrix:
            chance_stop = np.random.random()
            if chance_stop <= stopping_probability:
                velocity = np.array([0,0,0])
                in_motion = False

        position = np.add(position, velocity)

    if not in_motion and not decayed and in_matrix:
        muon_age += 1
        exponent = np.exp(-muon_age/muon_lifetime)

        chance_decay = np.random.random()

        if chance_decay >= exponent:
            decayed = True
            print("Muon has decayed")
            matrix[x, :, z] += 1
            detection_num += 1


    detection_array.append(detection_num)
    times.append(t)
    t += 1

    print(position)
    print(f"Time is {t}")



detection_plane = matrix[:, 0, :]
print(detection_plane)

#Generating Meshgrids- X is the horizontal dimenion, Y is 
X, Y = np.meshgrid(np.arange(array_dimension), np.arange(array_dimension))
X_flatten = X.flatten()
Y_flatten = Y.flatten()
detection_flatten = detection_plane.flatten()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i, k, detection in zip(X_flatten, Y_flatten, detection_flatten):
    if detection > 0:
        ax.bar3d(i, k, 0, 1, 1, detection, color='r', alpha=0.8)

plt.ylabel('Horizonal axis (i)')
plt.xlabel('Height (k)')
plt.title('0 is max height, 4 is bottom of array')
ax.set_xlim(0,array_dimension)
ax.set_ylim(0,array_dimension)
ax.set_zlim(0,2)
plt.show()


plt.plot(times, detection_array)
plt.xlabel('Time stamp')
plt.ylabel('Output signal')
plt.title(f'Quantum efficiency: {efficiency}, Stopping probability: {stopping_probability}')
plt.show()
