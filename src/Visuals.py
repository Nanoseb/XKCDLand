import pygame

import numpy as np

def cell_to_px(cell_position, a_position, cell_size, window_size):
    """ 
        Convert a cell position (i,j) in the grid to a pixel position on the screen
        return the (x,y) tuple of the top left corner of the square
        /!\ px coordinates and cell coordinates are inverted
    """
    
    a_px_position = (int(window_size[0]/2 - cell_size/2),
                     int(window_size[1]/2 - cell_size/2))

    cell_px_position = ((cell_position[1] - a_position[1])*cell_size + a_px_position[0],
                        (cell_position[0] - a_position[0])*cell_size + a_px_position[1])
#     if cell_px_position[0] < -cell_size or \
#        cell_px_position[1] < -cell_size or \
#        cell_px_position[0] > window_size[0] or \
#        cell_px_position[1] > window_size[1]:
#         return (None, None)

    return cell_px_position


def display_backgound_map(a_position, cell_size, window_size, image, game_screen):
    """
    Display the background image at the right location on the screen
    """
    image = pygame.image.load(image).convert()
    
    origin_position = cell_to_px((0,0), a_position, cell_size, window_size)

    game_screen.blit(image, origin_position)
    return


def display_building(building, color, a_position, cell_size, window_size, game_screen):
    """
    Display the building given in argument on the right cell on the screen
    For now, only display its name and a rectangle around the cell
    """
    
    font = pygame.font.SysFont('Comic Sans MS', 15)
    i,j = building.position

    cell_px_position = cell_to_px(building.position, a_position, cell_size, window_size)

    text = font.render(building.name, True, color)
    game_screen.blit(text, cell_px_position)

    rectangle = cell_px_position + (cell_size, cell_size)
    pygame.draw.Rect(game_screen, color, rectangle, 2)

    return



# def black_unvisible(a_position, cell_size, window_size, map_visible, game_screen):
#     """
#     Black out unvisible cells of the screen
#     """

#     N, M = np.shape(map_visible)
#     for i in range(N):
#         for j in range(M):
#             if map_visible[i,j]:
#                 cell_px_position = cell_to_px((i,j), a_position, cell_size, window_size)
#                 rectangle = cell_px_position + (cell_size, cell_size)
#                 pygame.draw.Rect(game_screen, (0,0,0), rectangle, 0)

#     return

