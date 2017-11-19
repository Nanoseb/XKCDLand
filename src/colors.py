import matplotlib._color_data as mcd
import matplotlib.patches as mpatch


def torgb(strcolor):
    hexcolor = mcd.XKCD_COLORS["xkcd:" + strcolor].lstrip("#")
    rgbcolor = tuple(int(hexcolor[i:i + 2], 16) for i in (0, 2, 4))
    return rgbcolor
