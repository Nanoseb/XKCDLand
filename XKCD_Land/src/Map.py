import numpy as np
import pygame

import textwrap

from .assets.water import WATER_TILES


def calculate_next_position(new_key, a_position, map_size, resources):
    """
    update a position based on the key press
    return new position tuple and a boolean expressing if a has moved
    """
    new_position = list(a_position)
    if new_key == pygame.K_LEFT and a_position[1] != 0:
        new_position[1] -= 1

    elif new_key == pygame.K_RIGHT and a_position[1] != map_size[1]:
        new_position[1] += 1

    elif new_key == pygame.K_UP and a_position[0] != 0:
        new_position[0] -= 1

    elif new_key == pygame.K_DOWN and a_position[0] != map_size[0]:
        new_position[0] += 1
    has_moved = (new_position != list(a_position))

    if (
        tuple(new_position) in WATER_TILES and
        tuple(a_position) not in WATER_TILES
    ):
        # Block movement from land to water, unless there is a pontoon
        if resources.check_for_existing_building(a_position) != 'Pontoon':
            return a_position, False

    return tuple(new_position), has_moved


def update_visible_map(a_position, map_visible, initial_reveal=False):
    """
    based on a position, check if new area has become visible,
    and if so, update the visibility map
    return new visibility map
    """

    if initial_reveal:
        visibility_template = """
            ###
           #####
          #######
         #########
        ###########
        #####x#####
        ###########
         #########
          #######
           #####
            ###
        """
    else:
        visibility_template = """
         ###
        #####
        ##x##
        #####
         ###
        """

    visibility_mask = [
        [
            (index, character)
            for index, character in enumerate(line)
            if character != ' '
        ]
        for line in textwrap.dedent(visibility_template).splitlines()
        if line.strip()
    ]

    for line_number, line in enumerate(visibility_mask):
        for column_number, character in line:
            if character == 'x':
                template_offset = (-line_number, -column_number)
                break

    new_map_visible = np.copy(map_visible)

    for line_number, line in enumerate(visibility_mask):
        for column_number, _ in line:
            new_x = a_position[0] + template_offset[0] + line_number
            new_y = a_position[1] + template_offset[1] + column_number

            if new_x <= 0:
                continue
            if new_y <= 0:
                continue
            if new_x >= new_map_visible.shape[0]:
                continue
            if new_y >= new_map_visible.shape[1]:
                continue

            new_map_visible[new_x, new_y] = 1

    return new_map_visible


