from __future__ import division

import time
import numpy as np
import pygame
import src.assets.menu
from src.assets.fonts import get_xkcd_font
from src.assets.water import WATER_TILES
from src.assets.sprite import image_dict
from src.assets.sprite import frame_speed
from src.assets import cheats
from .Rainfall import Rainfall



def display_initial_menu(menu):
    menu.clear_menu()
    menu.menu_entries = src.assets.menu.initial_menu
    menu.display_menu()
    return


def display_building_menu(available_building, menu):
    menu.clear_menu()

    for _, building in available_building.items():
        if building['Build Key']:
            text = building["Name"]
            menu.add_entry(text, building['Build Key'])
    menu.add_entry("Cancel", "c")
    menu.display_menu()
    return


def display_soldier_menu(menu):
    menu.clear_menu()
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
                                 int(window_size[1] / 2),
                                 window_size[0] - map_window_size[0],
                                 int(window_size[1] / 2))
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
        entry = {"key": key, "text": text}
        self.menu_entries.append(entry)
        return

    def display_menu(self):

        font = get_xkcd_font(self.font_size)
        top_y = self.menu_coordinates[1] + self.margin
        top_x = self.menu_coordinates[0] + self.margin

        for i, entry in enumerate(self.menu_entries):
            text_position = (top_x, top_y + i * (self.font_size + 5))
            text = font.render(
                "-" + entry['key'] + '- ' + entry["text"],
                True,
                self.color)
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
                 map_cell_size,
                 map_background_img):

        self.frame_nb = 1
        self.cell_size = cell_size
        self.window_size = window_size
        self.map_window_size = map_window_size
        self.a_position = a_position
        self.map_cell_size = map_cell_size
        self.map_background_img = map_background_img
        self.rainfall = Rainfall(*self.window_size)
        self.message_list = []

        self.game_screen = pygame.display.set_mode(self.window_size)
        self.font_size = 20

    def update_display(self, a_position, all_resources, map_visible, map_border):
        self.frame_nb += 1

        # update a_position
        self.a_position = a_position

        # display background map
        self.backgound_map()

        # display buildings
        for building in all_resources.Buildings:
            self.display_building(building)

        # display A
        self.display_A()

        # display border map
        self.display_borders(map_border)

        # rain
        self.display_rain()

        # display black when not visible
        self.black_unvisible(map_visible)


        # black background for right panel
        self.display_black_panel()

        self.display_resources(all_resources.ResourceDict)
        
        self.display_messages()

        return

    def display_messages(self):
        i = 0
        font = get_xkcd_font(self.font_size)
        top_x = int(self.map_window_size[0]/2)
        top_y = int(self.map_window_size[1]/2 + 30)
        for message_dict in self.message_list:
            if message_dict["frame"] >= 90:
                self.message_list.remove(message_dict)
            else:
                i += 1
                message_dict["frame"] += 1
                text_position = (top_x, top_y + i * (self.font_size + 5))
                text = font.render(message_dict["message"],
                                   True,
                                   (128, 128, 128))
                self.game_screen.blit(text, text_position)


    def add_message(self, message):
        self.message_list.append({"frame":0, "message": message})
        return
        

    def display_black_panel(self):
        """
        Display the right panel black background
        """

        rectangle = (self.map_window_size[0],
                     0,
                     self.window_size[0] - self.map_window_size[0],
                     self.window_size[1])
        pygame.draw.rect(self.game_screen, (0, 0, 0), rectangle, 0)
        return


    def display_resources(self, all_resources):

        font = get_xkcd_font(self.font_size)
        top_y = 25
        top_x = self.map_window_size[0] + 5
        
        list_text = ["Corners:", "   " + str(all_resources['corners']),
                     "Money:",   "   " + str(all_resources['money']),
                     "Food:",    "   " + str(all_resources['food']),
                     "Soldiers:","   " + str(all_resources['soldiers'])]


        for i, text in enumerate(list_text):
            text_position = (top_x, top_y + i * (self.font_size + 5))
            text = font.render(text,
                               True,
                               (255,255,255))
            self.game_screen.blit(text, text_position)

        pygame.display.update()
        return



    def cell_to_px(self, cell_position):
        """
            Convert a cell position (i,j) in the grid to a pixel position on the screen
            return the (x,y) tuple of the top left corner of the square
            /!\ px coordinates and cell coordinates are inverted
        """

        a_px_position = (int(self.map_window_size[0] / 2 - self.cell_size / 2),
                         int(self.map_window_size[1] / 2 - self.cell_size / 2))

        cell_px_position = (
            (cell_position[1] - self.a_position[1]) * self.cell_size + a_px_position[0],
            (cell_position[0] - self.a_position[0]) * self.cell_size + a_px_position[1])
        is_on_screen = not (cell_px_position[0] < -self.cell_size or \
                            cell_px_position[1] < -self.cell_size or \
                            cell_px_position[0] > self.window_size[0] or \
                            cell_px_position[1] > self.window_size[1])

        return cell_px_position, is_on_screen

    def get_visible_cells(self):
        I = int(self.window_size[1] / self.cell_size) + 2
        J = int(self.window_size[0] / self.cell_size) + 2
        min_i = max(0,-int(I/2) + self.a_position[0])
        min_j = max(0,-int(J/2) + self.a_position[1])
        max_i = min(self.map_cell_size[0], int(I/2) + self.a_position[0])
        max_j = min(self.map_cell_size[1], int(J/2) + self.a_position[1])

        return (min_i, max_i, min_j, max_j)


    def _converted_map_background_image(self):
        if not hasattr(self, '_converted_map_background_img'):
            self._converted_map_background_img = \
                self.map_background_img.convert()
        return self._converted_map_background_img

    def backgound_map(self):
        """
        Display the background image at the right location on the screen
        """
        self.game_screen.fill((0, 0, 0))

        origin_position, _ = self.cell_to_px((0, 0),)

        self.game_screen.blit(
            self._converted_map_background_image(),
            origin_position)
        return

    def get_image_name(self, prefix, nbframe):
        if nbframe == 1:
            return prefix + ".png"
        else:
            return prefix + str((int(self.frame_nb*frame_speed) % nbframe) +1) + ".png"

    def display_A(self):
        """
        Display A cell
        """

        if self.a_position in  WATER_TILES:
            name = self.get_image_name("AinBoat", 4)
        else:
            name = self.get_image_name("ASquare", 4)


        A_square_img = image_dict[name].convert_alpha()

        cell_px_position, _ = self.cell_to_px(self.a_position)
        self.game_screen.blit(A_square_img, cell_px_position)
        return
    
    def display_battle(self, battle_position, 
                       a_position, 
                       all_resources,
                       map_visible, 
                       map_border,
                       clock,
                       frame_rate):
        cell_px_position, _ = self.cell_to_px(battle_position)
        import time
        self.frame_nb = 0
        for i in range(9):
            self.frame_nb += 1
            name = self.get_image_name("battle", 9)
            img = image_dict[name].convert_alpha()

            self.update_display(a_position, all_resources, map_visible, map_border)
            self.game_screen.blit(img, cell_px_position)
            pygame.display.update()

            clock.tick(frame_rate)


    def display_building(self, building):
        """
        Display the building given in argument on the right cell on the screen
        """
        cell_px_position, is_on_screen = self.cell_to_px(building.Position)

        if is_on_screen:
            if building.Frame != 0:
                name = self.get_image_name(building.Name, building.Frame)
                img = image_dict[name].convert_alpha()

                self.game_screen.blit(img, cell_px_position)
            else:

                font = get_xkcd_font(15)

                text = font.render(building.Name, True, (0, 0, 0))
                self.game_screen.blit(text, cell_px_position)

                rectangle = cell_px_position + (self.cell_size, self.cell_size)
                pygame.draw.rect(self.game_screen, (0, 0, 0), rectangle, 2)
        return


    def display_borders(self, map_border):
        s = pygame.Surface(self.window_size)
        s.set_alpha(60)
        (min_i, max_i, min_j, max_j) = self.get_visible_cells()
        for i in range(min_i, max_i+1):
            for j in range(min_j, max_j + 1):
                if map_border[i,j].active:
                    cell_px_position, is_on_screen = self.cell_to_px((i, j),)
                    if is_on_screen:
                        s = pygame.Surface((self.cell_size, self.cell_size))  # the size of your rect
                        s.set_alpha(58) 
                        s.fill((255,0,0))
                        self.game_screen.blit(s,cell_px_position)   

        return





    def black_unvisible(self, map_visible):
        """
        Black out unvisible cells of the screen
        """

        N, M = np.shape(map_visible)
        (min_i, max_i, min_j, max_j) = self.get_visible_cells()
        for i in range(min_i, max_i+1):
            for j in range(min_j, max_j + 1):
                if not map_visible[i, j] and not cheats.NO_FOG_OF_WAR:
                    cell_px_position, is_on_screen = self.cell_to_px((i, j),)
                    if is_on_screen:
                        rectangle = cell_px_position + \
                            (self.cell_size, self.cell_size)
                        pygame.draw.rect(self.game_screen, (0, 0, 0), rectangle, 0)
                elif cheats.SHOW_WATER and (i, j) in WATER_TILES:
                    cell_px_position, is_on_screen = self.cell_to_px((i, j),)
                    if is_on_screen:
                        rectangle = cell_px_position + \
                            (self.cell_size, self.cell_size)
                        pygame.draw.rect(self.game_screen, (0, 0, 255), rectangle, 0)

        return

    def display_rain(self):
        """Rainfall"""

        rain_surface = pygame.Surface(self.window_size)

        rainfall_level = np.sin(time.time() / 60.0) ** 2
        for drop in self.rainfall.drops():
            pixel_value = int(255 * drop.alpha * rainfall_level)
            shifted_x = (drop.x + (self.a_position[0] * 25)) % self.window_size[0]
            pygame.draw.line(
                rain_surface,
                (pixel_value, pixel_value, pixel_value),
                (drop.x, drop.y - drop.tail),
                (drop.x, drop.y),
            )

        self.game_screen.blit(
            rain_surface,
            (0, 0, self.window_size[0], self.window_size[1]),
            special_flags=pygame.BLEND_SUB,
        )

        self.rainfall.update(1 / 30)
