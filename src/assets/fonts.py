"""Font accessors."""

import pygame.font

XKCD_FONT = {}

def get_xkcd_font(font_size):
    """Get or open the XKCD font in the given size."""

    try:
        return XKCD_FONT[font_size]
    except KeyError:
        pass

    new_font = pygame.font.SysFont('Comic Sans MS', font_size)

    XKCD_FONT[font_size] = new_font
    return new_font
