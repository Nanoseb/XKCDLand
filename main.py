"""
A game for the 2017 xkcd ludum dare
"""

import pygame
import random
import numpy as np

pygame.init()

BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
game_window_size = (700, 500)

if __name__ == "__main__":
    game_screen = pygame.display.set_mode(game_window_size)
    sprites_list = pygame.sprite.Group()
    pygame.display.set_caption("XKCD World")
    game_running = True
    clock = pygame.time.Clock()
    while game_running:
        for event in pygame.event.get():
            # quit when on klicking x or pressing the x key
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    game_running = False

    clock.tick(10)

    pygame.quit()
