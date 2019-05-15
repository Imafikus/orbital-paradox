import matplotlib.pyplot as plt
import numpy as np
import pygame

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

        #? tracks the current height and current time
        self.heights = []
        self.time_stamps = []
        
        #? tracks the current coordinates of the satelite
        self.xs = []
        self.ys = []

    def main_loop(self, end_time, adjust_height = False):
        """
        Calculates the trajectory of a satelite in 2D space.
        Simulation is run until end_time is achieved.

        Function fills 4 arrays.

        xs, ys are the coordinates of the satelite
        time_stamps and heights are current time and height of the satelite

        adjust_height indicates if satelite speeds up, in order not to fall
        
        adjust_height defaluts to false, we only need to explicitly state that 
        we want do height adjustment
        """
        
        distance = np.sqrt(self.x*self.x + self.y*self.y) - self.C_R_EARTH
        print("distance: ", distance)

        speed_adjustment = 0

        while(self.T < end_time):
            
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

            #? Update x coordinate and x-axis speed component
            self.x = self.x + self.vx * self.dt + ax * (self.dt**2 / 2)
            self.vx = self.vx + ax * self.dt

            #!FIXME#? Calculate current speed
            # if distance < self.C_CRITICAL_HEIGHT and adjust_height:
            #     self.vy = self.vy + self.C_SPEED_ADJUSTMENT

            v = self.vx + self.vy

            self.T = self.T + self.dt

                
            #? If we have hit the surface, we don't want to run simulation anymore
            if distance < 0 :
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


def arrays_scaled_to_fit_screen(positions_x, positions_y):
    scaled_xs = []; scaled_ys = []
    min_x = min(positions_x)
    max_x = max(positions_x)
    for value in positions_x:
        scaled_xs.append(1280*(value-min_x)/(max_x-min_x))

    min_y = min(positions_y)
    max_y = max(positions_y)
    for value in positions_y:
        scaled_ys.append(720 - 720*(value-min_y)/(max_y-min_y))

    return scaled_xs, scaled_ys
        

def compress_arrays(positions_x, positions_y):
    compressed_xs = []; compressed_ys = []
    i = 0
    while i < len(positions_x):
        compressed_xs.append(positions_x[i])
        compressed_ys.append(positions_y[i])
        i+=50

    return compressed_xs, compressed_ys



def main():
    op = OrbitalParadox()
    time_period = op.C_SECONDS_IN_YEAR
    op.main_loop(time_period, False)
    
    #op.plot_coordinates()
    #op.plot_height_through_time()

    x, y = op.get_coordinates_arrays()
    x, y = compress_arrays(x, y)
    x, y = arrays_scaled_to_fit_screen(x, y)

    pygame.init()
    clock = pygame.time.Clock()

    white = (255,255,255)
    black = (0,0,0)

    gameDisplay = pygame.display.set_mode((1280,720))
    pygame.display.set_caption('Orbital paradox')

    position_x = 0
    position_y = 0

    i = 0
    gameExit = False
    while not gameExit:
        gameDisplay.fill(white)
        pygame.draw.circle(gameDisplay, black, [position_x, position_y], 10)
        i = (i + 1) % len(x)
        position_x = int(x[i])
        position_y = int(y[i])
        # print('x:' + str(position_x))
        # print('y:' + str(position_y))
        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()