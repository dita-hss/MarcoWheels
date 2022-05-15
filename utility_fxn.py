import pygame

# helps to scale images without having to repeat the code every time
def scaling_factor(images, factor):
    scale = (images.get_width() * factor), (images.get_height() * factor)
    return pygame.transform.scale(images, scale)