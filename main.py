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
    C_H = 8_500 #m

    #? Mass of the Earth
    C_M_EARTH =  5.972 * 10**24 #kg

    #? Radius of the earth
    C_R_EARTH = 6.371 * 10**6 #m

    #? Gravitational Constant
    C_GAMMA = 6.67e-11

    #? Euler constant
    C_Euler = 2.71828

    C_SECONDS_IN_YEAR = 365 * 86_400


    def __init__(self):
        #? Starting time
        self.T = 0.

        #? time step
        self.dt = 10000. #s
        
        #? Starting x coordinate of the satelite
        self.x = 0.

        #? Starting height of the satelite (y coordinate)
        self.h = 200_000 #m

        #? Starting distance from the center of the Earth 
        self.y = self.h + self.C_R_EARTH #m

        #? Starting orbital speed of the satelite (x component of the speed)
        self.vx = np.sqrt(self.C_GAMMA * self.C_M_EARTH * (self.C_R_EARTH + self.y))
        
        #? starting y component of the speed
        self.vy = 0.

        #? Starting speed
        self.v = self.vx + self.vy

    def main_loop(self, end_time):
        """
        Calculates the trajectory of a satelite in 2D space.
        Simulation is run until end_time is achieved.

        Function returns 2 arrays. One for the height change, second with the time stamps
        """
        print("Before loop")
        print("self.y: ", self.y)
        print("self.x: ", self.x)
        print("C_GAMMA", self.C_GAMMA)
        print("C_M_EARTH", self.C_M_EARTH)


        heights = []
        time_stamps = []

        while(self.T < end_time):
            print("Time passed:", self.T)
            
            e_coef = -(self.h / self.C_H)
            #? Calculate current atmosphere density
            Ro = self.C_Ro * self.C_Euler ** e_coef
            print("Ro: ", Ro)

            #? Calculate Drag force without the velocity
            Fd = 1/2 * Ro * self.C_Cd * self.C_Area
            print("Fd: ", Fd)

            ay = -self.C_GAMMA * self.C_M_EARTH * (self.x**2 + self.y**2)**(-3 / 2) * self.y - Fd * self.vy
            ax = -self.C_GAMMA * self.C_M_EARTH * (self.x**2 + self.y**2)**(-3 / 2) * self.x - Fd * self.vx

            print("ay: ", ay)
            print("ax: ", ax)
            
            #? Update y coordinate and y-axis speed component
            self.y = self.y + ay * (self.dt**2 / 2)
            self.vy = self.vy + ay * self.dt

            print("self.y: ", self.y)
            print("self.vy: ", self.vy)

            #? Update x coordinate and x-axis speed component
            self.x = self.x + ax * (self.dt**2 / 2)
            self.vx = self.vx + ax * self.dt
            
            print("self.x: ", self.x)
            print("self.vx: ", self.vx)

            #? Calculate current speed
            v = self.vx + self.vy
            print("v: ", v)

            self.T = self.T + self.dt

            distance = np.sqrt(self.x*self.x + self.y*self.y) - self.C_R_EARTH

            time_stamps.append(self.T)
            heights.append(distance)
        
        #! FIXME
        self._plot_2D(time_stamps, heights)
    
    
    def _plot_2D(self, time, height):
        """
        Plots the 2D graph
        """
        plt.plot(time, height)
        #plt.axis('equal')
        plt.xlabel("time (s)")
        plt.ylabel("height (m)")
        plt.show()

def main():
    op = OrbitalParadox()
    op.main_loop(OrbitalParadox.C_SECONDS_IN_YEAR)


if __name__ == "__main__":
    main()