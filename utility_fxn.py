import pygame


def scaling_factor(img, factor):
    size = (img.get_width() * factor), (img.get_height() * factor)
    return pygame.transform.scale(img, size)