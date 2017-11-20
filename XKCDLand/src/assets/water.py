from PIL import Image
import os.path

def is_water_tile(colour):
    return colour[0] < 128

def load_water_map():
    root_file = os.path.join(
        os.path.dirname(__file__),
        'images',
        'water_cell.png',
    )

    tiles = set()

    with Image.open(root_file) as f:
        accessor = f.load()

        for y in range(f.size[1]):
            for x in range(f.size[0]):
                if is_water_tile(accessor[x, y]):
                    tiles.add((y, x))

    return tiles

WATER_TILES = load_water_map()
