import pygame
import math
from utility_fxn import scaling_factor

# loads the images that will be used for SPRITES
MARCO_CAR = pygame.image.load('Images/PlayerAnimation/SportsRacingCar_0.png')
GREEN_CAR = scaling_factor(pygame.image.load('Images/green-car.png'), 0.4)


# template that features the basic characteristic of ALL car movement and actions found in this game
class BaseCarPlayer:
    # initializes sprite
    def __init__(self, maxSpeed, rotVelocity):
        # set and load the sprite image
        self.image = self.IMG
        # set the rectangle/box that will enclose the image: just the image box here
        self.rect = self.image.get_rect()
        # set the starting speed, angle, and acceleration
        self.speed = 0
        self.angle = 0
        self.acceleration = 0.05
        # xy position of a car
        self.x, self.y = self.xy
        # max velocity
        self.maxSpeed = maxSpeed
        self.rotVelocity = rotVelocity
        self.box = None

    def reset(self, maxSpeed, rotVelocity):
        self.x = 32
        self.y = 465
        self.speed = 0
        self.angle = 0
        self.acceleration = 0.05
        self.maxSpeed = maxSpeed
        self.rotVelocity = rotVelocity

    def playerPicture(self, number):
        animation = [pygame.image.load('Images/PlayerAnimation/SportsRacingCar_0.png'),
                     pygame.image.load('Images/PlayerAnimation/SportsRacingCar_1.png'),
                     pygame.image.load('Images/PlayerAnimation/SportsRacingCar_2.png'),
                     pygame.image.load('Images/PlayerAnimation/SportsRacingCar_3.png'),
                     pygame.image.load('Images/PlayerAnimation/SportsRacingCar_4.png'),
                     pygame.image.load('Images/PlayerAnimation/SportsRacingCar_5.png'),
                     pygame.image.load('Images/PlayerAnimation/SportsRacingCar_6.png'),
                     pygame.image.load('Images/PlayerAnimation/SportsRacingCar_7.png')]
        self.image = animation[number]

    def changeMaxPU(self):
        self.maxSpeed = self.maxSpeed + 0.1

    # coin advantage, more coins will grant a higher maximum speed
    def changeMax(self, coin_score):
        self.maxSpeed = self.maxSpeed + coin_score * 0.015

    # tells the car how to accelerate everytime that the up button is pushed/held
    def accelerate_for(self):
        # add acceleration to the previously recorded speed value
        self.speed += self.acceleration
        # if speed becomes greater than the allowed max speed, then speed goes back down to the allowed max speed
        if self.speed > self.maxSpeed:
            self.speed = self.maxSpeed
        # accelerates in the direction that the car is facing
        self.direction()

    def accelerate_back(self):
        # add acceleration to the previously recorded speed value
        self.speed -= (self.acceleration / 2)
        # if speed becomes greater than the allowed max speed, then speed goes back down to the allowed max speed
        if self.speed > self.maxSpeed:
            self.speed = self.maxSpeed
        # accelerates in the direction that the car is facing
        self.direction()

    # tells the car how to slow down when the up key is no longer being pressed
    def de_accelerate(self):
        # speed is reduced by subtracting acceleration to the last recorded speed
        self.speed -= (self.acceleration + 0.05)
        # if speed becomes less than zero, then speed goes back to 0
        if self.speed < 0:
            self.speed = 0
        # de accelerates in the direction that the car is facing
        self.direction()

    # tells the car how to rotate when pressing left or right
    def steering(self, left=False, right=False):
        # if left is true, rotate by the given rotating speed
        if left:
            self.angle += self.rotVelocity
        # if right is true, rotate by the given rotating speed
        if right:
            self.angle -= self.rotVelocity

    def direction(self):
        # converts the current player angle from degrees to radians
        radians = math.radians(self.angle)
        # determines the direction that the image will be in
        y_change = math.cos(radians) * self.speed
        x_change = math.sin(radians) * self.speed
        self.y -= y_change
        self.x -= x_change

    # draws the player on the screen based on the x,y, direction from previous functions
    def draw(self, screen):
        rotCenter(screen, self.image, (self.x, self.y), self.angle)