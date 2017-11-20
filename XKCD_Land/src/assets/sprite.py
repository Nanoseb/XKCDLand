import os.path
import pygame
import glob
image_dict = {}
frame_speed = 0.3

folder = os.path.join(
    os.path.dirname(__file__),
    'images',
)
for image_file in glob.iglob(folder + '/*.png'):
    img_file = os.path.abspath(image_file)
    image_dict[os.path.basename(image_file)] = pygame.image.load(img_file)
