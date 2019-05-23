import pygame

class Simulation:
    
    COMPRESSION_STEP = 50

    def __init__(self):
        pass
    
    def arrays_scaled_to_fit_screen(self, positions_x, positions_y):
        """
        First we normalize the array to fit the [0, 1] segment and then stretch it
        to fit our 1280x720 screen;
        Since pygame has it's y coordinates upside down, we too have to inverse our y coords.
        """
        scaled_xs = []; scaled_ys = []
        min_x = min(positions_x)
        max_x = max(positions_x)
        for value in positions_x:
            scaled_xs.append(1280 * (value-min_x) / (max_x-min_x))

        min_y = min(positions_y)
        max_y = max(positions_y)
        for value in positions_y:
            scaled_ys.append(720 - 720 * (value-min_y) / (max_y-min_y))

        return scaled_xs, scaled_ys
    
    def compress_arrays(self, positions_x, positions_y):
        """
        Reduces the arrays by preserving 1 out of every 4 frames
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
        pygame.init()
        clock = pygame.time.Clock()

        white = (255,255,255)
        black = (0,0,0)

        game_display = pygame.display.set_mode((1280,720))
        pygame.display.set_caption('Orbital paradox')

        position_x = 0
        position_y = 0

        i = 0
        simulation_exit = False
        while not simulation_exit:
            game_display.fill(black)
            pygame.draw.circle(game_display, white, [position_x, position_y], 10)
            
            i = (i + 1) % len(x)
            
            position_x = int(x[i])
            position_y = int(y[i])
            
            pygame.display.update()
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    simulation_exit = True

        pygame.quit()
        quit()