"""
A game for the 2017 xkcd ludum dare
"""

import pygame
import random
import numpy as np
import src.assets.buildings
import src.assets.maps
import src.Map as mp
import src.Resources as rs
import src.Visuals as vs

pygame.init()
pygame.font.init() 
myfont = pygame.font.SysFont('Comic Sans MS', 30)

CELL_SIZE = 25 # size in px of the grid cells squares
START_POSITION = (0, 0)
GAME_WINDOW_SIZE = (700, 500)
FRAME_RATE = 10
RESOURCE_TIME_STEP = 2   # seconds per resource update
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)

# def has_moved(keys):
#     """
#     return true if a key for movement was pressed
#     """
#     movement = (keys[pygame.K_LEFT] or
#                 keys[pygame.K_RIGHT] or
#                 keys[pygame.K_UP] or
#                 keys[pygame.K_DOWN])
#     return movement

def has_built(keys):
    """
    return true if a key for a building action was pressed
    """
    built = (keys[pygame.K_b] or
             keys[pygame.K_u])
    return built



if __name__ == "__main__":
    game_screen = pygame.display.set_mode(GAME_WINDOW_SIZE)
    sprites_list = pygame.sprite.Group()
    pygame.display.set_caption("XKCD World")
    game_running = True
    a_position = START_POSITION
    map_visible = src.assets.maps.map_visible
    map_size = src.assets.maps.map_size
    map_borders = src.assets.maps.map_borders
    all_resources = rs.AllResource(START_POSITION)
    attack_flag = False
    clock = pygame.time.Clock()
    resource_timer = 0
    while game_running:
        for event in pygame.event.get():
            # quit when on klicking x or pressing the x key
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    game_running = False
        
        keys = pygame.key.get_pressed()
        # movement:
        # calculate next position
        a_position, has_moved = mp.calculate_next_position(keys, a_position, map_size)
        if has_moved:
            print(a_position)
            #   check if space needs to be made visible in map_visible
            #map_visible = mp.update_visible_map(a_position, map_visible)
            #   check if border was attacked in map_borders
            #attack_flag = mp.check_attack(a_position, map_borders) 
            pass

        if attack_flag:
            # TODO:
            # calculate results
            pass

        # building action:
        #   add/upgrade building in buildings_list 

        # calculate next time step resources
        if resource_timer > (FRAME_RATE * RESOURCE_TIME_STEP):
            all_resources.calculate_next(a_position)
            resource_timer = 0
        resource_timer += 1

        # update screen
        # print X at cell 5,5
        game_screen.fill(BLACK)
        text = myfont.render("X", True, WHITE)
        game_screen.blit(text,vs.cell_to_px((5,5), a_position, CELL_SIZE, GAME_WINDOW_SIZE))


        pygame.display.update()
        clock.tick(FRAME_RATE)

    pygame.quit()
