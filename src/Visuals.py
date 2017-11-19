import pygame
import numpy as np

import src.assets.menu

def display_initial_menu(menu):
    menu.menu_entries = src.assets.menu.initial_menu 
    menu.display_menu()
    return

def display_building_menu(available_building, menu):
    menu.clear_menu()

    for _, building in available_building.iteritems():
        if building['Build Key']:
            text = building["Name"]
            menu.add_entry(text, building['Build Key'])
    menu.add_entry("Cancel", "c")
    menu.display_menu()
    return

def display_soldier_menu(menu):
    menu.menu_entries = src.assets.menu.soldier_menu 
    menu.display_menu()
    return


class Menu(object):
    def __init__(self, 
                 window_size,
                 map_window_size,
                 game_screen,
                 margin=5,
                 color=(255, 255, 255),
                 font_size=20):

        self.menu_coordinates = (map_window_size[0],
                                 int(window_size[1]/2),
                                 window_size[0] - map_window_size[0],
                                 int(window_size[1]/2))
        self.font_size = font_size
        self.color = color
        self.margin = margin
        self.menu_entries = [] 
        self.game_screen = game_screen

    def clear_menu(self):
        rectangle = self.menu_coordinates
        pygame.draw.rect(self.game_screen, (0, 0, 0), rectangle, 0)
        self.menu_entries = []
        return

    def add_entry(self, text, key):
        entry = {"key": key, "text":text}
        self.menu_entries.append(entry)
        return
    
    def display_menu(self):

        font = pygame.font.SysFont('Comic Sans MS', self.font_size)
        top_y = self.menu_coordinates[1] + self.margin
        top_x = self.menu_coordinates[0] + self.margin

        for i, entry in enumerate(self.menu_entries):
            text_position = (top_x, top_y + i*(self.font_size+5))
            text = font.render("(" + entry['key'] + ') ' + entry["text"], True, self.color)
            self.game_screen.blit(text, text_position)

        pygame.display.update()
        return



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

        # display black when not visible
        self.black_unvisible(map_visible) 

        # black background for right panel
        self.display_black_panel()

        return

    def display_black_panel(self):
        """
        Display the right panel black background
        """
        

        rectangle = (self.map_window_size[0],
                     0,
                     self.window_size[0] - self.map_window_size[0],
                     self.window_size[1]) 
        pygame.draw.rect(self.game_screen, (0,0,0), rectangle, 0)
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

