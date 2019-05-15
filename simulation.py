import pygame

class Simulation:
    
    def __init__(self):
        pass
    
    def arrays_scaled_to_fit_screen(self, positions_x, positions_y):
        """
        Scale arrays to fit the screen
        #TODO needs better comments
        """
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
    
    def compress_arrays(self, positions_x, positions_y):
        """
        Reduces the arrays to better fit the screen
        """
        compressed_xs = []; compressed_ys = []
        i = 0
        while i < len(positions_x):
            compressed_xs.append(positions_x[i])
            compressed_ys.append(positions_y[i])
            i+=50

        return compressed_xs, compressed_ys

    def start_loop(self, x, y):
        """
        Starts the simulation given the x and y arrays of coordinates
        """
        pygame.init()
        clock = pygame.time.Clock()

        white = (255,255,255)
        black = (0,0,0)

        gameDisplay = pygame.display.set_mode((1280,720))
        pygame.display.set_caption('Orbital paradox')

        position_x = 0
        position_y = 0

        i = 0
        simulationExit = False
        while not simulationExit:
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
                    simulationExit = True

        pygame.quit()
        quit()