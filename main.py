import matplotlib.pyplot as plt
import numpy as np

class OrbitalParadox():
    """
    Class used to describe Orbital Paradox
    """

    #? Air densisty
    C_Ro = 1.23 #km/m3

    #? Drag coefficient for satelites
    C_Cd = 2.2

    #? Cross-section area of the satelite (bus size used)
    C_Area = 10 * 3 #m2

    #? Starting height, used for calculating changing density of the atmosphere
    C_H = 10_000 #m

    #? Mass of the Earth
    C_M_EARTH =  5.972 * 10**24 #kg

    #? Radius of the earth
    C_R_EARTH = 6.371 * 10**6 #m

    #? Gravitational Constant
    C_GAMMA = 6.67e-11


    def __init__(self):
        #? Starting height of the satelite
        self.h0 = 20_000 #m

        #? Starting orbital speed of the satelite
        self.vx0 = np.sqrt(C_GAMMA * C_M_EARTH * (C_R_EARTH + self.h0))







if __name__ == "__main__":
    op = OrbitalParadox()