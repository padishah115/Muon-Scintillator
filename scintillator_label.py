def get_scintillator_label(position, array_dimension):
    """LABELLING THE SCINTILLATOR WHICH THE MUON IS IN in order to append the detection event to the correct scintillator"""
    x = position[0]
    z = position[2]

    if z <= array_dimension-1 and x <= array_dimension-1:
        a = array_dimension*z + x + 1
        
    elif z >= array_dimension or x >= array_dimension:
        a = 0 #a is 0 if Not in array at all

    return a
