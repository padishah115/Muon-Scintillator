import numpy as np

"""This module holds the functions which generate the velocity of the muons based on the cos^2 distribution"""


def generate_theta():
    """The muon cosmic ray spectrum is proportional to cos^2(theta)
       This function generates values of zenith angle, theta, given this distribution
    """

    ready = False #We keep looping until we beat the game of chance

    theta = 0 #default theta is directly downwards

    while not ready:
        theta_random = (np.pi / 2) * np.random.random() #Generate random phase between 0 and pi/2
        c2 = (np.cos(theta_random))**2
        chance = np.random.random()
        
        if chance < c2:
            theta = theta_random
            ready = True #we are ready to exit

    return theta



def generate_velocity(v):
    """Generate a velocity given a value of zenith angle and velocity
        Requires you to pass the absolute magnitude of the velocity, which is given by 
        the muon momentum
    """

    theta = generate_theta()

    v_z = v * np.cos(theta) #Project out the z component
    v_s = v * np.sin(theta) #Projects onto the x-y plane

    phi = np.random.random() * np.pi #Generate a random azimuthal angle

    v_x = v_s * np.cos(phi)
    v_y = v_s * np.sin(phi)

    velocity = np.array([v_x, v_y, v_z])

    return velocity
