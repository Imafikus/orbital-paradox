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
    C_H = 5_500 #m

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

        #? tracks the current height and current time
        self.heights = []
        self.time_stamps = []
        
        #? tracks the current coordinates of the satelite
        self.xs = []
        self.ys = []
        self.speed = []

    def main_loop(self, end_time, include_drag_force, adjust_height = False):
        """
        Calculates the trajectory of a satelite in 2D space.
        Simulation is run until end_time is achieved.

        Function fills 4 arrays.

        xs, ys are the coordinates of the satelite
        time_stamps and heights are current time and height of the satelite

        include_drag_force just says whether we include the drag force, or not.
        It must be stated everytime

        adjust_height indicates if satelite speeds up, in order not to fall
        
        adjust_height defaluts to false, we only need to explicitly state that 
        we want do height adjustment
        """
        
        distance = np.sqrt(self.x*self.x + self.y*self.y) - self.C_R_EARTH
        # print("distance: ", distance)

        speed_adjustment = 0

        while(self.T < end_time):
            
            e_coef = -(self.h / self.C_H)
            #? Calculate current atmosphere density
            Ro = self.C_Ro * self.C_Euler ** e_coef

            #? Calculate Drag force 
            if(include_drag_force == True):
                Fd = 1/2 * Ro * self.C_Cd * self.C_Area * np.sqrt(self.vx**2 + self.vy**2)
            else:
                Fd = 0

            ay = -self.C_GAMMA * self.C_M_EARTH * (self.x**2 + self.y**2)**(-3 / 2) * self.y - Fd * self.vy
            ax = -self.C_GAMMA * self.C_M_EARTH * (self.x**2 + self.y**2)**(-3 / 2) * self.x - Fd * self.vx
            
            #? Update y coordinate and y-axis speed component
            self.y = self.y + self.vy * self.dt + ay * (self.dt**2 / 2)
            self.vy = self.vy + ay * self.dt

            #? Update x coordinate and x-axis speed component
            self.x = self.x + self.vx * self.dt + ax * (self.dt**2 / 2)
            self.vx = self.vx + ax * self.dt

            #!FIXME#? Calculate current speed
            # if distance < self.C_CRITICAL_HEIGHT and adjust_height:
            #     self.vy = self.vy + self.C_SPEED_ADJUSTMENT

            v = self.vx + self.vy
            self.speed.append(v)

            self.T = self.T + self.dt
                
            #? If we have hit the surface, we don't want to run simulation anymore
            if distance < 0:
                break

            distance = np.sqrt(self.x*self.x + self.y*self.y) - self.C_R_EARTH
            print("distance: ", distance)

            self.time_stamps.append(self.T)
            self.heights.append(distance)
            
            self.xs.append(self.x)
            self.ys.append(self.y)
        
    
    def reset_arrays(self):
        """
        Resets arrays all arrays to be empty
        """
        self.heights = []
        self.time_stamps = []
        self.xs = []
        self.ys = []
    
    def get_coordinates_arrays(self):
        """
        Returns arrays for x and y coordinates of the satelite
        """
        return self.xs, self.ys


    def plot_coordinates(self):
        """
        Plots the position of the satelite  
        """
        plt.plot(self.xs, self.ys)
        plt.axis("equal")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()
        

    def plot_height_through_time(self):
        """
        Plots the height change through time
        """ 
        plt.plot(self.time_stamps, self.heights)
        plt.axis("equal")
        plt.xlabel("time (s)")
        plt.ylabel("height (m)")
        plt.show()

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
    time_period = op.C_SECONDS_IN_YEAR / 500
    op.main_loop(time_period, False, False)
    
    op.plot_coordinates()
    op.plot_height_through_time()

if __name__ == "__main__":
    main()