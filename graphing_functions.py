#This contains all of the necessary graphing functions. THis is designed to tidy up the simulation.py code

import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

current_directory = os.getcwd()

def generate_scintillator_graphs(array, muon, tmax):
    array_dimension = array.dimension
    detection_plane = array.return_detection_plane()

    """Produces bar graphs and pulse graphs for the scintillating array"""
    #Generating Meshgrids
    X, Y = np.meshgrid(np.arange(array_dimension), np.arange(array_dimension))
    X_flatten = X.flatten()
    Y_flatten = Y.flatten()


    #Generate 3D graph
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
                ax.bar3d(k, i, height, 1, 1, detection, color=color1, alpha=0.8, label=f'SiPM{x}')
                


    #3D Bar graph which graphically displays detection events
    plt.ylabel('Horizonal axis (i)')
    plt.xlabel('Height (k)')
    plt.title(f'0 is max height, 5 is bottom of array. Muon energy: {muon.energy/1000:.2f} GeV')
    ax.set_xlim(0,array_dimension)
    ax.set_ylim(0,array_dimension)
    ax.set_zlim(0,max_height)
    plt.savefig(current_directory+f'\\bar graphs\detection_bars_energy_{muon.energy/1000:.2f} GeV.png')
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
    plt.savefig(current_directory+f'\\Pulse graphs\pulse graphs energy {muon.energy/1000:.2f} GeV.png')
    plt.show()


def generate_muon_graph(muon):
    """Generates a 3D plot given the muon trajectory through the scintillator"""
    dimension = muon.array_dimension

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(f'Muon trajectory through the matrix for energy {muon.energy/1000:.2f} GeV')

    crosswise,scintwise,height = zip(*muon.position_history)

    ax.plot3D(height, crosswise, scintwise, color='m')

    ax.set_ylim(0,dimension)
    ax.set_xlim(0,dimension)
    ax.set_zlim(0,dimension)
    ax.set_xlabel('Height above ground')
    plt.savefig(current_directory+f'\\trajectories\\trajectory for {muon.energy/1000:.2f} GeV.png')
    plt.show()


