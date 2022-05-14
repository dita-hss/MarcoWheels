import pygame

# helps to scale images without having to repeat the code every time
def scaling_factor(img, factor):
    size = (img.get_width() * factor), (img.get_height() * factor)
    return pygame.transform.scale(img, size)