import os
import numpy as np

map_size = (10, 20)
map_background_img = os.path.abspath("src/assets/images/background_map.png")
map_visible = np.zeros((map_size[0], map_size[1]),)  
map_borders = ["a"]

