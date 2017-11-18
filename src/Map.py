import pygame
import numpy as np
    

def calculate_next_position(keys, a_position, map_size):
    """ 
    update a position based on the key press
    return new position tuple and a boolean expressing if a has moved
    """
    new_position = list(a_position)
    if keys[pygame.K_LEFT] and a_position[1] != 0:
        new_position[1] -= 1

    elif keys[pygame.K_RIGHT] and a_position[1] != map_size[1]:
        new_position[1] += 1

    elif keys[pygame.K_UP] and a_position[0] != 0:
        new_position[0] -= 1

    elif keys[pygame.K_DOWN] and a_position[0] != map_size[0]:
        new_position[0] += 1
    has_moved = (new_position != list(a_position))

    return tuple(new_position), has_moved


def update_visible_map(a_position, map_visible):
    """
    based on a position, check if new area has become visible,
    and if so, update the visibility map
    return new visibility map
    """
    a = a_position
    # todo move that somewhere else
#     visibility_area = np.array([[0, 0, 1, 0, 0],
#                                 [0, 1, 1, 1, 0],
#                                 [1, 1, 1, 1, 1],
#                                 [0, 1, 1, 1, 0],
#                                 [0, 0, 1, 0, 0]])
#     newly_visible_map = np.zeros_like(map_visible)
#     newly_visible_map[a_position-2:a_position+3, 
#                       a_position-2:a_position+3] = visibility_area
#     
#     new_visible = numpy.logical_or(newly_visible_map, map_visible)
    # todo test extensvely...
    N, M = np.shape(map_visible)
    for i in range(N):
        for j in range(M):
            if (i == a[0] and j >= a[1]-2 and  j <= a[1]+2) or \
                    (j == a[1] and i >= a[0]-2 and  i <= a[0]+2) or \
                    (i >= a[0]-1 and i <= a[0]+1 and  j >= a[1]-1 and j <= a[1]+1):
                map_visible[i,j] = 1

    return map_visible

def update_border_state(a_position, map_borders):
    """
    check if a border attack occurs at the current position
    return True if an attack occurs
    """
    attack_flag = False
    return attack_flag
