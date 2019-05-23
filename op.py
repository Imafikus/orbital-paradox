import matplotlib.pyplot as plt
import numpy as np

class OrbitalParadox():
    """
    Class used to describe Orbital Paradox
    """
    def __init__(self):
        #? Air densisty
        self.C_Ro = 1.2255 #kg/m3

        #? Drag coefficient for satelites
        self.C_Cd = 2.0

        #? Cross-section area of the satelite (bus size used)
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

        #? indicates if the satelite needs height adjustment
        self.C_CRITICAL_HEIGHT = 160_000.

        self.C_SPEED_ADJUSTMENT = 1_000. #m/s

        #? Starting time
        self.T = 0.

        #? time step
        self.dt = 1. #s

        ###
        
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
            self.y = self.y + self.vy * self.dt
            self.vy = self.vy + ay * self.dt

            #? Update x coordinate and x-axis speed component
            self.x = self.x + self.vx * self.dt
            self.vx = self.vx + ax * self.dt

            #!FIXME#? Calculate current speed
            # if distance < self.C_CRITICAL_HEIGHT and adjust_height:
            #     self.vy = self.vy + self.C_SPEED_ADJUSTMENT

            self.v = np.sqrt(self.vx**2 + self.vy**2)

            self.T = self.T + self.dt
                
            #? If we have hit the surface, we don't want to run simulation anymore
            if distance < 500:
                break

            distance = np.sqrt(self.x**2 + self.y**2) - self.C_R_EARTH
            print("distance: ", distance)

            self.time_stamps.append(self.T)
            self.heights.append(distance)
            
            self.xs.append(self.x)
            self.ys.append(self.y)
            self.speed.append(self.v)

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
    time_period = op.C_SECONDS_IN_YEAR / 100
    op.main_loop(time_period, include_drag_force = True)
    
    op.plot_coordinates()
    op.plot_height_through_time()
    op.plot_speed_through_time()

if __name__ == "__main__":
    main()