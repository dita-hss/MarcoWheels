import pygame
import random as r

class Animation:
    def __init__(self, imageList):
        self.imageList = imageList
        self.index = 0
        self.timer = 0
        self.speed = 10

    def update(self):
        self.timer += 1
        if self.timer >= self.speed:
            self.index += 1
            self.timer = 0
            if self.index > len(self.imageList) - 1:
                self.index = 0

    def draw(self, screen, x, y):
        screen.blit(self.imageList[self.index], (x, y))


def random():
    choices = ['mushroom', 'coin']
    x = r.randint(0, 1)
    powerup = choices[x]
    return powerup



