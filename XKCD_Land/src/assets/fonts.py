"""Font accessors."""

import os

import pygame.font

XKCD_FONT = {}

def get_xkcd_font(font_size):
    """Get or open the XKCD font in the given size."""

    try:
        return XKCD_FONT[font_size]
    except KeyError:
        pass

    root_path = os.path.join(
        os.path.dirname(__file__),
        'xkcd.ttf',
    )

    new_font = pygame.font.Font(root_path, font_size)

    XKCD_FONT[font_size] = new_font
    return new_font
