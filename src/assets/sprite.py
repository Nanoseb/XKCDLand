import os
from os.path import basename
import pygame
import glob
image_dict = {}
frame_speed = 0.3

folder = "src/assets/images/"
for image_file in glob.iglob(folder + '*.png'):
    img_file = os.path.abspath(image_file)
    image_dict[basename(image_file)] = pygame.image.load(img_file)



