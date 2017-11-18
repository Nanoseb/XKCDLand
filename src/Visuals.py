import pygame

import numpy as np


class Display(object):
    """
    Class that handle all the display
        map(background, buildings, visibility etc.), ressources
    """
    def __init__(self,
                 a_position,
                 cell_size, 
                 window_size,
                 map_window_size,
                 map_background_img):

        self.cell_size = cell_size
        self.window_size = window_size
        self.map_window_size = map_window_size
        self.a_position = a_position
        self.map_background_img = map_background_img

        self.game_screen = pygame.display.set_mode(self.window_size)

    
    def update_display(self, a_position, all_ressources, map_visible):

        # update a_position
        self.a_position = a_position

        # display background map
        self.backgound_map()
        
        # display buildings
        for building in all_ressources.Buildings:
            self.display_building(building)
        
        # display A
        self.display_A()


        # 
        self.black_unvisible(map_visible) 
        return


    def cell_to_px(self, cell_position):
        """ 
            Convert a cell position (i,j) in the grid to a pixel position on the screen
            return the (x,y) tuple of the top left corner of the square
            /!\ px coordinates and cell coordinates are inverted
        """
        
        a_px_position = (int(self.window_size[0]/2 - self.cell_size/2),
                         int(self.window_size[1]/2 - self.cell_size/2))

        cell_px_position = ((cell_position[1] - self.a_position[1])*self.cell_size +
                                a_px_position[0],
                            (cell_position[0] - self.a_position[0])*self.cell_size + 
                                a_px_position[1])
    #     if cell_px_position[0] < -cell_size or \
    #        cell_px_position[1] < -cell_size or \
    #        cell_px_position[0] > window_size[0] or \
    #        cell_px_position[1] > window_size[1]:
    #         return (None, None)

        return cell_px_position


    def backgound_map(self):
        """
        Display the background image at the right location on the screen
        """
        self.game_screen.fill((0,0,0))
        
        origin_position = self.cell_to_px((0,0),)

        self.game_screen.blit(self.map_background_img.convert(), origin_position)
        return


    def display_A(self):
        """
        Display A cell
        """
        
        font = pygame.font.SysFont('Comic Sans MS', 30)

        cell_px_position = self.cell_to_px(self.a_position)

        text = font.render("A", True, (0,0,0))
        self.game_screen.blit(text, cell_px_position)

        rectangle = cell_px_position + (self.cell_size, self.cell_size)
        pygame.draw.rect(self.game_screen, (0,0,0), rectangle, 2)
        return





    def display_building(self, building):
        """
        Display the building given in argument on the right cell on the screen
        For now, only display its name and a rectangle around the cell
        """
        
        font = pygame.font.SysFont('Comic Sans MS', 15)

        cell_px_position = self.cell_to_px(building.Position)

        text = font.render(building.Name, True, (0,0,0))
        self.game_screen.blit(text, cell_px_position)

        rectangle = cell_px_position + (self.cell_size, self.cell_size)
        pygame.draw.rect(self.game_screen, (0,0,0), rectangle, 2)
        return



    def black_unvisible(self, map_visible):
        """
        Black out unvisible cells of the screen
        """

        N, M = np.shape(map_visible)
        for i in range(N):
            for j in range(M):
                if not map_visible[i,j]:
                    cell_px_position = self.cell_to_px((i,j),)
                    rectangle = cell_px_position + (self.cell_size, self.cell_size)
                    pygame.draw.rect(self.game_screen, (0,0,0), rectangle, 0)

        return

