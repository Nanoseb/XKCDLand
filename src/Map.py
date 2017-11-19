import numpy as np
import pygame

import textwrap


def calculate_next_position(new_key, a_position, map_size):
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

    return tuple(new_position), has_moved


def update_visible_map(a_position, map_visible):
    """
    based on a position, check if new area has become visible,
    and if so, update the visibility map
    return new visibility map
    """

    visibility_template = """
      #
     ###
    ##x##
     ###
      #
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


def update_border_state(a_position, map_borders):
    """
    check if a border attack occurs at the current position
    return True if an attack occurs
    """
    attack_flag = False
    return attack_flag
