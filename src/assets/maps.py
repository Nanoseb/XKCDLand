import os

import numpy as np
import pygame

start_position = (5,5)
# map_background_img = os.path.abspath("src/assets/images/background_map.png")
map_background_img = pygame.image.load(os.path.abspath("src/assets/images/background_map.png"))
map_background_img = pygame.transform.scale2x(map_background_img)
x,y = map_background_img.get_rect().size
cell_size = 25 # size in px of the grid cells squares


map_size = (int(y/cell_size), int(x/cell_size))

map_visible = np.zeros((map_size[0], map_size[1]),)  
map_borders = ["a"]
