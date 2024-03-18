#RETURNS THE LABEL OF THE SCINTILLATOR WHICH THE MUON IS CURRENTLY LOCATED IN, BASED ON THE POSITION ARRAY OF THE MUON
import numpy as np
from simulation_package.muon import Muon

def get_scintillator_index(muon:Muon):
    """LABELLING THE SCINTILLATOR WHICH THE MUON IS IN in order to append the detection event to the correct scintillator
    
    ARGS:
    -----------------------------------------------------
    muon (muon): Takes the simulated muon object as input

    RETURNS:
    -------------------------------------------------------------------------------------------------------------------------------------
    scintillator index (integer): Returns the index of the scintillator containing the muon. Returns -1 if the muon has exited the array.
    
    """
    x = muon.position[0]
    y = muon.position[1]
    z = muon.position[2]

    array_dimension = muon.array_dimension

    if muon.is_contained():
        a = array_dimension*np.floor(z) + np.floor(x)
        return int(a)
            
    return -1
