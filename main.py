import matplotlib.pyplot as plt
import numpy as np

class OrbitalParadox():
    """
    Class used to describe Orbital Paradox
    """

    #? Air densisty
    C_Ro = 1.23 #kg/m3

    #? Drag coefficient for satelites
    C_Cd = 2.2

    #? Cross-section area of the satelite (bus size used)
    C_Area = 10 * 3 #m2

    #? Starting height, used for calculating changing density of the atmosphere
    C_H = 8_500 #m

    #? Mass of the Earth
    C_M_EARTH =  5.972 * 10**24 #kg

    #? Radius of the earth
    C_R_EARTH = 6_371_000.#m

    #? Gravitational Constant
    C_GAMMA = 6.67e-11

    #? Euler constant
    C_Euler = 2.71828

    C_SECONDS_IN_YEAR = 365 * 86_400

    #? indicates if the satelite needs height adjustment
    C_CRITICAL_HEIGHT = 160_000.

    C_SPEED_ADJUSTMENT = 1_000. #m/s

    def __init__(self):
        #? Starting time
        self.T = 0.

        #? time step
        self.dt = 1. #s
        
        #? Starting x coordinate of the satelite
        self.x = 0.

        #? Starting height of the satelite (y coordinate) from the Earth surface
        self.h = 200_000 #m

        #? Starting distance from the center of the Earth 
        self.y = self.h + self.C_R_EARTH #m

        #? Starting orbital speed of the satelite (x component of the speed)
        self.vx = np.sqrt(self.C_GAMMA * self.C_M_EARTH / (self.y))
        
        #? starting y component of the speed
        self.vy = 0.

        #? Starting speed
        self.v = self.vx + self.vy

        self.heights = []
        self.time_stamps = []
        self.xs = []
        self.ys = []

    def main_loop(self, end_time, adjust_height = False):
        """
        Calculates the trajectory of a satelite in 2D space.
        Simulation is run until end_time is achieved.

        Function fills 4 arrays.

        xs, ys are the coordinates of the satelite
        time_stamps and heights are current time and height of the satelite

        adjust_height indicates if satelite need to speed up, in order not to fall
        """
        print("Before loop")
        print("self.y: ", self.y)
        print("self.x: ", self.x)
        print("C_GAMMA", self.C_GAMMA)
        print("C_M_EARTH", self.C_M_EARTH)

        distance = np.sqrt(self.x*self.x + self.y*self.y) - self.C_R_EARTH
        print("distance: ", distance)
        print("critical height: ", self.C_CRITICAL_HEIGHT)

        while(self.T < end_time):
            
            speed_was_adjusted = False
            if distance < self.C_CRITICAL_HEIGHT and adjust_height:
                print("Speed adjusted")
                self.v = self.v + 300
                speed_was_adjusted = True

            #? If we have hit the surface, we don't want to run simulation anymore
            if distance < 0 and not speed_was_adjusted:
                break

            print("Time passed:", self.T)
            
            e_coef = -(self.h / self.C_H)
            #? Calculate current atmosphere density
            Ro = self.C_Ro * self.C_Euler ** e_coef
            print("Ro: ", Ro)

            #? Calculate Drag force 
            Fd = 1/2 * Ro * self.C_Cd * self.C_Area * np.sqrt(self.vx**2 + self.vy**2)
            print("Fd: ", Fd)

            ay = -self.C_GAMMA * self.C_M_EARTH * (self.x**2 + self.y**2)**(-3 / 2) * self.y - Fd * self.vy
            ax = -self.C_GAMMA * self.C_M_EARTH * (self.x**2 + self.y**2)**(-3 / 2) * self.x - Fd * self.vx

            print("ay: ", ay)
            print("ax: ", ax)
            
            #? Update y coordinate and y-axis speed component
            self.y = self.y + self.vy * self.dt + ay * (self.dt**2 / 2)
            self.vy = self.vy + ay * self.dt

            print("self.y: ", self.y)
            print("self.vy: ", self.vy)

            #? Update x coordinate and x-axis speed component
            self.x = self.x + self.vx * self.dt + ax * (self.dt**2 / 2)
            self.vx = self.vx + ax * self.dt
            
            print("self.x: ", self.x)
            print("self.vx: ", self.vx)

            #? Calculate current speed
            v = self.vx + self.vy
            print("v: ", v)

            self.T = self.T + self.dt

            distance = np.sqrt(self.x*self.x + self.y*self.y) - self.C_R_EARTH
            print("distance: ", distance)

            self.time_stamps.append(self.T)
            self.heights.append(distance)
            
            self.xs.append(self.x)
            self.ys.append(self.y)
        
        #self._plot_coordinates(xs, ys)
    
    def reset_arrays(self):
        """
        Reset arrays all arrays to be empty
        """
        self.heights = []
        self.time_stamps = []
        self.xs = []
        self.ys = []
    
    def get_coordinates_arrays(self):
        """
        returns arrays for x and y coordinates of the satelite
        """
        return self.xs, self.ys


    def plot_coordinates(self):
        """
        Plots the position of the satelite  
        """
        #plt.xkcd()
        #plt.axis('equal')
        plt.plot(self.xs, self.ys)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()
        

    def plot_height_through_time(self):
        """
        Plots the height change through time
        """ 
        plt.plot(self.time_stamps, self.heights)
        plt.xlabel("time (s)")
        plt.ylabel("height (m)")
        plt.show()
    

def main():
    op = OrbitalParadox()
    time_period = op.C_SECONDS_IN_YEAR
    print(time_period)
    
    op.main_loop(10_000, True)
    
    op.plot_coordinates()
    op.plot_height_through_time()


if __name__ == "__main__":
    main()