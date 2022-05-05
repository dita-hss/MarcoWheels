import pygame


# move the map with the player
class MapMovement:
    def __init__(self):
        self.x = 0
        self.y = 0

    def left(self, screen, background):
        self.x += 5
        screen.blit(background, (self.x, self.y))

    def right(self, screen, background):
        self.x -= 5
        screen.blit(background, (self.x, self.y))

    def up(self, screen, background):
        self.y -= 5
        screen.blit(background, (self.x, self.y))

    def down(self, screen, background):
        self.y += 5
        screen.blit(background, (self.x, self.y))
