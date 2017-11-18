import pygame

def calculate_next_position(keys, a_position, map_size):
    """ 
    update a position based on the key press
    return new position tuple and a boolean expressing if a has moved
    """
    new_position = a_position
    if keys[pygame.K_LEFT] and a_position[1] != 0:
        new_position[1] -= 1

    elif keys[pygame.K_RIGHT] and a_position[1] != map_size[1]:
        new_position[1] += 1

    elif keys[pygame.K_UP] and a_position[0] != 0:
        new_position[0] -= 1

    elif keys[pygame.K_DOWN] and a_position[0] != map_size[0]:
        new_position[0] += 1
    has_moved = (new_position != a_position)

    return new_position, has_moved

def update_visible_map(a_position, map_visible):
    """
    based on a position, check if new area has become visible,
    and if so, update the visibility map
    return new visibility map
    """
    # todo move that somewhere else
    visibility_map = numpy.array([[0, 0, 1, 0, 0],
                                  [0, 1, 1, 1, 0],
                                  [1, 1, 1, 1, 1],
                                  [0, 1, 1, 1, 0],
                                  [0, 0, 1, 0, 0]])
    return 

    

    




def calculate_next_position(keys, a_position, map_size):
    """ 
    update a position based on the key press
    return new position tuple and a boolean expressing if a has moved
    """
    new_position = a_position
    if keys[pygame.K_LEFT] and a_position[1] != 0:
        new_position[1] -= 1

    elif keys[pygame.K_RIGHT] and a_position[1] != map_size[1]:
        new_position[1] += 1

    elif keys[pygame.K_UP] and a_position[0] != 0:
        new_position[0] -= 1

    elif keys[pygame.K_DOWN] and a_position[0] != map_size[0]:
        new_position[0] += 1
    has_moved = (new_position != a_position)

    return new_position, has_moved

def update_visible_map(a_position, map_visible):
    """
    based on a position, check if new area has become visible,
    and if so, update the visibility map
    return new visibility map
    """
    new_visible = map_visible
    return new_visible

def update_border_state(a_position, map_borders):
    """
    check if a border attack occurs at the current position
    return True if an attack occurs
    """
    attack_flag = False
    return attack_flag



    new_visible = map_visible
    return new_visible

def update_border_state(a_position, map_borders):
    """
    check if a border attack occurs at the current position
    return True if an attack occurs
    """
    attack_flag = False
    return attack_flag
