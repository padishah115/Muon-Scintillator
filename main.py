import numpy as np
import matplotlib.pyplot as plt

t = 0
t_max = 20

detection_array = []
times = []

efficiency = 0.6 #Encode the quantum efficiency of the SiPM
stopping_probability = 0.1 #Probability that the muon will come to a complete rest inside the array
muon_lifetime = 2 #Mean lifetime, i.e. time taken for the muon population to decrease by a factor of e

muon_age = 0

i = np.random.randint(0,5)
j = np.random.randint(0,5)
k = 0

vi = np.random.randint(0,2)
vj = np.random.randint(0,2)
vk = 1

position = np.array([i, j, k])
velocity = np.array([vi, vj, vk])

matrix = np.zeros((5,5,5))

print(position)

in_matrix = True
in_motion = True
decayed = False

while t < t_max:

    detection_status = 0

    for i in range (0,3):
        if position[i] > 4:
            in_matrix = False
    
    x = position[0]
    y = position[1]
    z = position[2]

    if in_motion:
        chance_sipm = np.random.random()
        if chance_sipm <= efficiency and in_matrix:
            matrix[x][y][z] += 1
            print("Detection event")
            if detection_status == 0:
                detection_array.append(1)
                detection_status = 1
        else:
            if detection_status == 0:
                detection_array.append(0)
                detection_status = 1
        
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
            matrix[x][y][z] += 1
            if detection_status == 0:
                detection_array.append(1)
                detection_status = 1
        
        else:
            if detection_status == 0:
                detection_array.append(0)
                detection_status =1
    
    elif detection_status == 0:
        detection_array.append(0)
        detection_status = 1


    times.append(t)
    t += 1

    print(position)
    print(f"Time is {t}")

plt.plot(times, detection_array)
plt.xlabel('Time stamp')
plt.ylabel('Output signal')
plt.title(f'Quantum efficiency: {efficiency}')
plt.show()
