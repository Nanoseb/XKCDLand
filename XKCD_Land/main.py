"""
A game for the 2017 xkcd ludum dare
"""

import pygame
import numpy as np
from .src.assets.buildings import available_buildings
from .src.assets import maps
from .src.assets import display
from .src.assets import border
from .src import Map as mp
from .src import Borders as br
from .src import Resources as rs
from .src import Visuals as vs

pygame.init()
pygame.key.set_repeat(500, 100)
pygame.font.init()

FRAME_RATE = 30
RESOURCE_TIME_STEP = 2   # seconds per resource update
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)

building_keys = rs.get_building_keys()

def handle_building_menu():
    building_menu = True
    while building_menu is True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                building_menu = False
                new_key = pygame.key.name(event.key)
                if new_key in building_keys:
                    name = building_keys[new_key]
                    return available_buildings[name]

def handle_soldier_menu(main_display, all_resources):
    soldier_menu = True
    while soldier_menu is True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                new_key = pygame.key.name(event.key)
                soldier_msg = None
                if new_key == 'b':
                    soldier_menu = False
                if new_key == 's':
                    soldier_msg = all_resources.add_soldier(-1)
                if new_key == 't':
                    soldier_msg = all_resources.add_soldier(+1)
                if soldier_msg:
                    main_display.add_message(soldier_msg)
            main_display.display_messages()
            pygame.display.update()



def xkcdmain():
    pygame.display.set_caption("XKCD Land")
    game_running = True


    # loading map file
    map_visible = maps.map_visible
    map_cell_size = maps.map_cell_size
    map_background_img = maps.map_background_img
    cell_size = maps.cell_size
    a_position = maps.start_position

    # Loading borders
    map_border = border.border_map

    # loading display properties
    game_window_size = display.game_window_size
    map_window_size = display.map_window_size

    main_display = vs.Display(a_position,
                              cell_size,
                              game_window_size,
                              map_window_size,
                              map_cell_size,
                              map_background_img)
    menu = vs.Menu(game_window_size,
                   map_window_size,
                   main_display.game_screen)
    vs.display_initial_menu(menu)


    # loading ressources
    all_resources = rs.AllResource(a_position)

    attack_flag = False
    clock = pygame.time.Clock()
    resource_timer = 0

    map_visible = mp.update_visible_map(a_position, map_visible, initial_reveal=True)

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
        new_a_position, has_moved = mp.calculate_next_position(
            key_pressed,
            a_position,
            map_cell_size,
            resources=all_resources,
        )

        if has_moved:
            #   check if border was attacked in map_borders
            attack_flag, movement_border = br.is_on_border(new_a_position, map_border)
        else:
            attack_flag = False

        if attack_flag:
            new_soldiers, border_defeated = movement_border.attack(all_resources.ResourceDict["soldiers"])
            main_display.display_battle(new_a_position, a_position, all_resources, map_visible, map_border, clock, FRAME_RATE)
            if border_defeated:
                map_border = br.desactivate_border(movement_border.border_id, map_border)
                a_position = new_a_position
                main_display.add_message("You won the battle !")
            else:
                has_moved = False
                main_display.add_message("you lost " + str(all_resources.ResourceDict["soldiers"] - max(0,new_soldiers)) + " soldiers")
                all_resources.ResourceDict["soldiers"] = max(0,new_soldiers)
        else:
            a_position = new_a_position
            movement_border = None


        if has_moved:
            #   check if space needs to be made visible in map_visible
            map_visible = mp.update_visible_map(a_position, map_visible)




        # building action:
        # add building in buildings_list
        if key_pressed == pygame.K_b:
            vs.display_building_menu(available_buildings, menu)
            new_building = handle_building_menu()
            if new_building:
                output_text = all_resources.add_building(a_position, new_building)
                main_display.add_message(output_text)

        # add building in buildings_list
        if key_pressed == pygame.K_u:
            output_text = all_resources.upgrade_building(a_position)
            main_display.add_message(output_text)

        # soldier action:
        #   add/upgrade building in buildings_list
        if key_pressed == pygame.K_s:
            vs.display_soldier_menu(menu)
            new_soldiers = handle_soldier_menu(main_display, all_resources)

        # calculate next time step resources
        if resource_timer > (FRAME_RATE * RESOURCE_TIME_STEP):
            all_resources.calculate_next(a_position)
            resource_timer = 0
        resource_timer += 1

        # update screen
        main_display.update_display(a_position, all_resources, map_visible, map_border)
        vs.display_initial_menu(menu)



        pygame.display.update()
        clock.tick(FRAME_RATE)

    pygame.quit()
