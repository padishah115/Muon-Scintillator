import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from muon import Muon
from array_stopping_power import *
from simulation import *


"""
TO DO:
    Calculate the stopping power of the array and use this to determine whether the muon comes to a stop inside of the
        array.

    Make a graph showing the characteristic lifetime of muons which decay in the apparatus.

    Rewrite the code to run the simulation some arbitrary number of times. We're going to want to massively increase the number of time steps.


UNITS: MeV, cm, 100s of picoseconds

For a muon at sea level, expect an energy of 4 GeV. This translates to a beta*gamma of about 38 

"""

#Properties of the copper array
copper_stopping_power = 1.5 #MeV cm^2/g
copper_rho = 8.96 #Density in g/cm^3

#Setting duration of the simulation. The program will run from t=0 to t=tmax. Increments are in the ballpark of about 200ps
t = 0
t_max = 20

#Dimensions of the scintillator array- DO NOT CHANGE THIS
array_dimension = 5

run_simulation(copper_stopping_power, copper_rho, t_max, array_dimension)


