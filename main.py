"""
A game for the 2017 xkcd ludum dare
"""

import pygame
import random
import numpy as np
from src.assets.buildings import available_buildings
import src.assets.maps
import src.assets.display
import src.Map as mp
import src.Resources as rs
import src.Visuals as vs

pygame.init()
pygame.key.set_repeat(500, 100)
pygame.font.init() 

FRAME_RATE = 30
RESOURCE_TIME_STEP = 2   # seconds per resource update
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)

building_keys = ['h'] #rs.get_building_keys()

def handle_building_menu():
    building_menu = True
    while building_menu is True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                building_menu = False
                if pygame.key.name(event.key) in building_keys:
                    return available_buildings['Home']


if __name__ == "__main__":
    sprites_list = pygame.sprite.Group()
    pygame.display.set_caption("XKCD World")
    game_running = True

    # loading map file
    map_visible = src.assets.maps.map_visible
    map_size = src.assets.maps.map_size
    map_borders = src.assets.maps.map_borders
    map_background_img = src.assets.maps.map_background_img
    cell_size = src.assets.maps.cell_size
    a_position = src.assets.maps.start_position

    # loading display properties
    game_window_size = src.assets.display.game_window_size
    map_window_size = src.assets.display.map_window_size

    display = vs.Display(a_position,
                         cell_size,
                         game_window_size,
                         map_window_size,
                         map_background_img) 
    menu = vs.Menu(game_window_size,
                   map_window_size,
                   display.game_screen)
    vs.display_initial_menu(menu)


    # loading ressources
    all_resources = rs.AllResource(a_position)

    attack_flag = False
    clock = pygame.time.Clock()
    resource_timer = 0
    while game_running:
       
        key_pressed = None
        for event in pygame.event.get():
            # quit when on klicking x or pressing the x key
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    game_running = False
                else:
                    key_pressed = event.key
        
        #keys = pygame.key.get_pressed()
        # movement:
        # calculate next position
        a_position, has_moved = mp.calculate_next_position(key_pressed, a_position, map_size)
        if has_moved:
            #   check if space needs to be made visible in map_visible
            map_visible = mp.update_visible_map(a_position, map_visible)
            #   check if border was attacked in map_borders
            #attack_flag = mp.check_attack(a_position, map_borders) 
            pass

        if attack_flag:
            # TODO:
            # calculate results
            pass

        # building action:
        #   add/upgrade building in buildings_list 
        if key_pressed == pygame.K_b:
            vs.display_building_menu(available_buildings, menu)
            new_building = handle_building_menu()
            if new_building:
                output_text = all_resources.add_building(a_position, new_building)
                print(output_text)

        # soldier action:
        #   add/upgrade building in buildings_list 
        if key_pressed == pygame.K_s:
            vs.display_soldier_menu(menu)
            # TODO do something with the key presses

        # calculate next time step resources
        if resource_timer > (FRAME_RATE * RESOURCE_TIME_STEP):
            all_resources.calculate_next(a_position)
            resource_timer = 0
        resource_timer += 1

        # update screen
        display.update_display(a_position, all_resources, map_visible)
        vs.display_initial_menu(menu)

        # display right panel
        # TODO


        pygame.display.update()
        clock.tick(FRAME_RATE)

    pygame.quit()
