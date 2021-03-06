import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import numpy as np

class OrbitalParadox():
    """
    Class used to describe Orbital Paradox
    """
    def __init__(self):
        #? Air densisty
        self.C_Ro = 1.2255 #kg/m3

        #? Drag coefficient for satellites
        self.C_Cd = 22.2

        #? Cross-section area of the satellite (bus size used)
        self.C_Area = 10 * 3 #m2

        #? Starting height, used for calculating changing density of the atmosphere
        self.C_H = 7_500 #m

        #? Mass of the Earth
        self.C_M_EARTH =  5.972 * 10**24 #kg

        #? Radius of the earth
        self.C_R_EARTH = 6_371_000.#m

        #? Gravitational Constant
        self.C_GAMMA = 6.67e-11

        #? Euler constant
        self.C_Euler = 2.71828

        self.C_SECONDS_IN_YEAR = 365 * 86_400

        #? Starting time
        self.T = 0.

        #? time step
        self.dt = 0.01 #s

        ###
        
        #? Starting x coordinate of the satellite
        self.x = 0.

        #? Starting height of the satellite (y coordinate) from the Earth surface
        self.h = 200_000 #m

        #? Starting distance from the center of the Earth 
        self.y = self.h + self.C_R_EARTH #m

        #? Starting orbital speed of the satellite (x component of the speed)
        self.vx = np.sqrt(self.C_GAMMA * self.C_M_EARTH / (self.y))
        
        #? starting y component of the speed
        self.vy = 0.

        #? Starting speed
        self.v = self.vx + self.vy

        #? tracks the current height and current time
        self.heights = []
        self.time_stamps = []
        
        #? tracks the current coordinates of the satellite
        self.xs = []
        self.ys = []
        self.speed = []

    def main_loop(self, end_time, include_drag_force, adjust_height = False):
        """
        Calculates the trajectory of a satellite in 2D space.
        Simulation is run until end_time is achieved.

        Function fills 4 arrays.

        xs, ys are the coordinates of the satellite
        time_stamps and heights are current time and height of the satellite

        include_drag_force just says whether we include the drag force, or not.
        It must be stated everytime

        adjust_height indicates if satellite speeds up, in order not to fall
        
        adjust_height defaluts to false, we only need to explicitly state that 
        we want do height adjustment
        """
        
        distance = np.sqrt(self.x*self.x + self.y*self.y) - self.C_R_EARTH

        while(self.T < end_time):
            
            e_coef = -(self.h / self.C_H)
            #? Calculate current atmosphere density
            Ro = self.C_Ro * self.C_Euler ** e_coef

            #? Calculate Drag force 
            if(include_drag_force == True):
                Fd = 1/2 * Ro * self.C_Cd * self.C_Area * np.sqrt(self.vx**2 + self.vy**2)
            else:
                Fd = 0

            # Acceleration
            ay = -self.C_GAMMA * self.C_M_EARTH * (self.x**2 + self.y**2)**(-3 / 2) * self.y - Fd * self.vy
            ax = -self.C_GAMMA * self.C_M_EARTH * (self.x**2 + self.y**2)**(-3 / 2) * self.x - Fd * self.vx
            
            #? Update y coordinate and y-axis speed component
            self.y = self.y + self.vy * self.dt
            self.vy = self.vy + ay * self.dt

            #? Update x coordinate and x-axis speed component
            self.x = self.x + self.vx * self.dt
            self.vx = self.vx + ax * self.dt

            self.v = np.sqrt(self.vx**2 + self.vy**2)

            self.T = self.T + self.dt
                
            distance = np.sqrt(self.x**2 + self.y**2) - self.C_R_EARTH
            print("distance: ", distance)

            self.time_stamps.append(self.T)
            self.heights.append(distance)
            
            self.xs.append(self.x)
            self.ys.append(self.y)
            self.speed.append(self.v)

            #? If we have hit the surface, we don't want to run simulation anymore
            if distance < 0:
                break
    
    def get_coordinates_arrays(self):
        """
        Returns arrays for x and y coordinates of the satellite
        """
        return self.xs, self.ys

    def get_C_H(self):
        return self.C_H

    def set_C_H(self, val):
        self.C_H = val

    def get_h(self):
        return self.h

    def set_h(self, val):
        self.h = val

    def get_dt(self):
        return self.dt

    def set_dt(self, val):
        self.dt = val

    def get_C_Cd(self):
        return self.C_Cd

    def set_C_Cd(self, val):
        self.C_Cd = val
    
    def get_C_Area(self):
        return self.C_Area

    def set_C_Area(self, val):
        self.C_Area = val
    

    def plot_coordinates(self):
        """
        Plots the position of the satellite  
        """
        plt.plot(self.xs, self.ys)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()

    def plot_height_through_time(self):
        """
        Plot the height change through time
        """ 
        plt.plot(self.time_stamps, self.heights)
        plt.xlabel("time (s)")
        plt.ylabel("height (m)")
        plt.show()

    def plot_speed_through_time(self):
        """
        Plot the speed change through time
        """ 
        plt.plot(self.time_stamps, self.speed)
        plt.xlabel("time (s)")
        plt.ylabel("speed (m/s)")
        plt.show()

        print(min(self.speed))
        print(max(self.speed))

    def print_values():
        """
        Used to print all values of the variables which are used
        in the main loop function
        """    
        print("Time passed:", self.T)
        
        print("self.y: ", self.y)
        print("self.vy: ", self.vy)
        
        print("self.x: ", self.x)
        print("self.vx: ", self.vx)

def main():
    op = OrbitalParadox()
    time_period = op.C_SECONDS_IN_YEAR / 5000
    op.main_loop(time_period, include_drag_force = False)
    
    op.plot_coordinates()
    op.plot_height_through_time()
    op.plot_speed_through_time()

if __name__ == "__main__":
    main()