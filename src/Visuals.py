from __future__ import division

import numpy as np
import pygame
import src.assets.menu
from src.assets.fonts import get_xkcd_font
from src.assets.water import WATER_TILES
from src.assets import cheats
from .Rainfall import Rainfall


def display_initial_menu(menu):
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

        self.cell_size = cell_size
        self.window_size = window_size
        self.map_window_size = map_window_size
        self.a_position = a_position
        self.map_cell_size = map_cell_size
        self.map_background_img = map_background_img

        self.game_screen = pygame.display.set_mode(self.window_size)

        self.rainfall = Rainfall(*self.window_size)

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

        # rain
        self.display_rain()

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

    def cell_to_px(self, cell_position):
        """
            Convert a cell position (i,j) in the grid to a pixel position on the screen
            return the (x,y) tuple of the top left corner of the square
            /!\ px coordinates and cell coordinates are inverted
        """

        a_px_position = (int(self.window_size[0] / 2 - self.cell_size / 2),
                         int(self.window_size[1] / 2 - self.cell_size / 2))

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

    def display_A(self):
        """
        Display A cell
        """

        font = get_xkcd_font(30)

        cell_px_position, _ = self.cell_to_px(self.a_position)

        text = font.render("A", True, (0, 0, 0))
        self.game_screen.blit(text, cell_px_position)

        rectangle = cell_px_position + (self.cell_size, self.cell_size)
        pygame.draw.rect(self.game_screen, (0, 0, 0), rectangle, 2)
        return

    def display_building(self, building):
        """
        Display the building given in argument on the right cell on the screen
        For now, only display its name and a rectangle around the cell
        """

        font = get_xkcd_font(15)

        cell_px_position, is_on_screen = self.cell_to_px(building.Position)

        if is_on_screen:
            text = font.render(building.Name, True, (0, 0, 0))
            self.game_screen.blit(text, cell_px_position)

            rectangle = cell_px_position + (self.cell_size, self.cell_size)
            pygame.draw.rect(self.game_screen, (0, 0, 0), rectangle, 2)
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

        for drop in self.rainfall.drops():
            pixel_value = int(255 * drop.alpha)
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
