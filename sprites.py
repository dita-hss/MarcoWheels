import pygame, math


# the players sprite
class Player(pygame.sprite.Sprite):
    # initializes sprites
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # set and load the sprite image
        self.image = pygame.image.load('Untitled-1.png')
        # set the rectangle/box that will enclose the image: just the image box here
        self.rect = self.image.get_rect()
        # set where the player will start on the screen
        self.rect.center = (97, 450)
        # set the starting speed
        self.speedx = 0
        self.speedy = 0

    def update(self):
        # with every update, the player will have zero speed in both x and y directions
        self.speedx = 0
        self.speedy = 0
        keys = pygame.key.get_pressed()

        # describes what will happen if one presses down, up, left, right
        # x direction
        if keys[pygame.K_LEFT]:
            self.speedx = -5
        if keys[pygame.K_RIGHT]:
            self.speedx = 5
        # y direction
        if keys[pygame.K_DOWN]:
            self.speedy = 5
        if keys[pygame.K_UP]:
            self.speedy = -5
        self.rect.y += self.speedy
        self.rect.x += self.speedx
