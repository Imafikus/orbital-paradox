import pygame
import numpy as np
from pygame.locals import *
from op import OrbitalParadox

class Simulation:
    
    COMPRESSION_STEP = int(24 * (1 / OrbitalParadox().dt))

    def __init__(self):
        pass
    
    def scale_arrays_to_fit_screen(self, positions_x, positions_y):
        """
        First we normalize the array to fit the [0, 1] segment and then stretch it
        to fit our 1280x720 screen;
        Since pygame has it's y coordinates upside down, we too have to inverse our y coords.
        """
        scaled_xs = []; scaled_ys = []
        min_x = min(positions_x)
        max_x = max(positions_x)

        for value in positions_x:
            scaled_xs.append(480 * (value-min_x) / (max_x-min_x))

        min_y = min(positions_y)
        max_y = max(positions_y)
        for value in positions_y:
            scaled_ys.append(480 - 480 * (value-min_y) / (max_y-min_y))

        # Scaled earth radius is equal to initial_distance * (r / (r + h0))
        # Import those numbers and calculate the initial distance
        r = OrbitalParadox().C_R_EARTH; h0 = OrbitalParadox().h
        self.scaled_earth_radius = (480 - 480 * (0-min_y) / (max_y-min_y) - scaled_ys[0]) * (r / (r+h0))

        # Translate earth and the satellite so that the center of earth is at [640, 360]
        self.scaled_earth_center_x = 480 * (0-min_x) / (max_x-min_x)
        self.scaled_earth_center_y = 480 - 480 * (0-min_y) / (max_y-min_y)
        i = 0
        tx = np.abs(self.scaled_earth_center_x - 640)
        ty = np.abs(self.scaled_earth_center_y - 360)
        while i < len(scaled_xs):
            scaled_xs[i] = scaled_xs[i] + tx
            scaled_ys[i] = scaled_ys[i] + ty
            i += 1

        self.scaled_earth_center_x = 640
        self.scaled_earth_center_y = 360

        return scaled_xs, scaled_ys
    
    def compress_arrays(self, positions_x, positions_y):
        """
        Reduces the arrays by preserving 1 out of every COMPRESSION_STEP frames
        """
        compressed_xs = []; compressed_ys = []
        i = 0
        while i < len(positions_x):
            compressed_xs.append(positions_x[i])
            compressed_ys.append(positions_y[i])
            i += self.COMPRESSION_STEP

        return compressed_xs, compressed_ys

    def start_loop(self, x, y):
        """"
        Starts the simulation given the x and y arrays of coordinates
        """

        x, y = self.compress_arrays(x, y)
        x, y = self.scale_arrays_to_fit_screen(x, y)

        pygame.init()
        clock = pygame.time.Clock() # This is used to set the framerate

        white = (255,255,255)
        black = (0,0,0)
        blue = (135,206,250)

        game_display = pygame.display.set_mode((1280,720), RESIZABLE)
        pygame.display.set_caption('Orbital paradox')

        position_x = int(x[0])
        position_y = int(y[0])
        i = 0
        simulation_exit = False
        while not simulation_exit:
            game_display.fill(black)
            pygame.draw.circle(game_display, white, [position_x, position_y], 5) # Satellite
            pygame.draw.circle(game_display, blue, [int(self.scaled_earth_center_x), int(self.scaled_earth_center_y)], int(self.scaled_earth_radius)) # Planet
            
            i = (i + 1) % len(x) # Loop through the arrays
            
            position_x = int(x[i])
            position_y = int(y[i])
            
            pygame.display.update()
            clock.tick(60) # Framerate set to 60fps
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    simulation_exit = True

        pygame.quit()
        quit()