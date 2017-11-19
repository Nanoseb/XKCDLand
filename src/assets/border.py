from PIL import Image
import os.path
from ..Borders import Border_cell
import numpy as np


force_coeficient = 0.2

def is_border(colour):
    return colour[1] < 128

def load_border_map():
    root_file = os.path.join(
        os.path.dirname(__file__),
        'images',
        'border_cell.png',
    )


    with Image.open(root_file) as f:
        accessor = f.load()
        
        border_map = np.ndarray(shape=(f.size[1], f.size[0]), dtype=object)
        for y in range(f.size[1]):
            for x in range(f.size[0]):
                if is_border(accessor[x, y]):
                    border_map[y,x] = Border_cell(accessor[x,y][0], force_coeficient)
                else:
                    border_map[y,x] = Border_cell(0, force_coeficient)

    return border_map


border_map = load_border_map()

