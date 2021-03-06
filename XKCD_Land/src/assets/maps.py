import os

import numpy as np
import pygame

start_position = (39, 36)
map_background_img = pygame.image.load(os.path.join(os.path.dirname(__file__),
                                       'images',
                                       'background_map.png',)
                                       )


x,y = map_background_img.get_rect().size
cell_size = 25 # size in px of the grid cells squares


map_cell_size = (int(y/cell_size), int(x/cell_size))

map_visible = np.zeros((map_cell_size[0], map_cell_size[1]),)


