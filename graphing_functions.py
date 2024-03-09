#This contains all of the necessary graphing functions. THis is designed to tidy up the simulation.py code

import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

current_directory = os.getcwd()

def generate_scintillator_graphs(array, muon):
    """This generates the 3D bar graphs which show the pulses from each individual SiPM in the array."""
    array_dimension = array.dimension
    detection_plane = array.return_detection_plane()

    #########################################################################
    # BAR GRAPHS, 3D, SHOWING SIGNALS PRODUCED BY SiPMs IN THE ARRAY        #
    #########################################################################
    
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
    plt.ylabel('Horizonal axis')
    plt.xlabel('Height off ground')
    plt.title(f'Graph of SiPM signals. Muon energy: {muon.energy/1000:.2f} GeV')
    ax.set_zlabel('SiPM pulse number')
    ax.set_xlim(0,array_dimension)
    ax.set_ylim(0,array_dimension)
    ax.set_zlim(0,max_height*2)
    #plt.savefig(current_directory+f'\\bar graphs\detection_bars_energy_{muon.energy/1000:.2f} GeV.png')
    plt.show()
    

    #########################################################################
    # PULSE GRAPHS FOR EACH INDIVIDUAL SCINTILLATOR OUTPUT                  #
    #########################################################################

    fig, axs = plt.subplots(array_dimension, array_dimension, figsize = (20, 20))

    x = np.arange(0, muon.time_in_array)

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
                y = scintillator.sipms[k].detections[:muon.time_in_array]
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
    #plt.savefig(current_directory+f'\\Pulse graphs\pulse graphs energy {muon.energy/1000:.2f} GeV.png')
    plt.show()


def generate_muon_graph(muon, initial_pos, final_pos):
    """Generates a 3D plot given the muon trajectory through the scintillator"""
    dimension = muon.array_dimension

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ##################################################################################
    # PLOT INITIAL AND FINAL POSITIONS OF THE MUON DURING PASSAGE THROUGH ARRAY      #
    ##################################################################################

    #Intial position plus label
    ax.scatter(initial_pos[2], initial_pos[0], initial_pos[1], color='k')
    ax.text(initial_pos[2] + 0.1, initial_pos[0] + 0.1, initial_pos[1] +1, f'[{initial_pos[2]:.1f}, {initial_pos[0]:.1f}, {initial_pos[1]:.1f}]', color='blue')
    
    #Final position plus label
    ax.scatter(final_pos[2], final_pos[0], final_pos[1], color='k')
    ax.text(final_pos[2] + 0.1, final_pos[0] + 0.1, final_pos[1] +1, f'[{final_pos[2]:.1f}, {final_pos[0]:.1f}, {final_pos[1]:.1f}]', color='blue')


    #########################################################################
    # TRAJECTORY LINE FOR MUON PASSING THROUGH THE ARRAY                    #
    #########################################################################

    ax.set_title(f'Muon trajectory through the matrix for energy {muon.energy/1000:.2f} GeV')

    crosswise,scintwise,height = zip(*muon.position_history)

    ax.plot3D(height, crosswise, scintwise, color='m')

    ax.set_ylim(0,dimension)
    ax.set_xlim(0,dimension)
    ax.set_zlim(0,dimension)
    ax.set_xlabel('Height above ground')
    ax.set_ylabel('Perpendicular to scint. axis')
    ax.set_zlabel('Along axis of scint.')
    #plt.savefig(current_directory+f'\\trajectories\\trajectory for {muon.energy/1000:.2f} GeV.png')
    plt.show()

def generate_muon_graph_with_scintillators(muon, initial_pos, final_pos):
    """Generates a 3D plot given the muon trajectory through the scintillator"""
    dimension = muon.array_dimension

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ##################################################################################
    # PLOT INITIAL AND FINAL POSITIONS OF THE MUON DURING PASSAGE THROUGH ARRAY      #
    ##################################################################################

    #Intial position plus label
    ax.scatter(initial_pos[2], initial_pos[0], initial_pos[1], color='k')
    #ax.text(initial_pos[2] + 0.1, initial_pos[0] + 0.1, initial_pos[1] +1, f'[{initial_pos[2]:.1f}, {initial_pos[0]:.1f}, {initial_pos[1]:.1f}]', color='blue')
    
    #Final position plus label
    ax.scatter(final_pos[2], final_pos[0], final_pos[1], color='k')
    #ax.text(final_pos[2] + 0.1, final_pos[0] + 0.1, final_pos[1] +1, f'[{final_pos[2]:.1f}, {final_pos[0]:.1f}, {final_pos[1]:.1f}]', color='blue')


    #########################################################################
    # TRAJECTORY LINE FOR MUON PASSING THROUGH THE ARRAY                    #
    #########################################################################

    ax.set_title(f'Muon trajectory through the matrix for energy {muon.energy/1000:.2f} GeV')

    crosswise,scintwise,height = zip(*muon.position_history)

    ax.plot3D(height, crosswise, scintwise, color='m')

    colors = ['black', 'dimgray']

    for i in range(dimension):
        for j in range(dimension):
            color_index = (i+j) % 2
            ax.bar3d(i, j, 0, 1, 1, dimension, color=colors[color_index], edgecolor='w', alpha=0.01)

    ax.set_ylim(0,dimension)
    ax.set_xlim(0,dimension)
    ax.set_zlim(0,dimension)
    ax.set_xlabel('Height above ground')
    ax.set_ylabel('Perpendicular to scint. axis')
    ax.set_zlabel('Along axis of scint.')
    #plt.savefig(current_directory+f'\\trajectories\\trajectory for {muon.energy/1000:.2f} GeV.png')
    plt.show()


# def generate_OR_plot():
#     """Generates graph of SiPMs using OR combination logic"""
    
# def generate_AND_plot():
#     """Generates graph of SiPMs using AND combination logic"""


