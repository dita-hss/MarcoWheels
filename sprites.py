import pygame
import math

# loads the images that will be used for SPRITES
MARCO_CAR = pygame.image.load('Images/PlayerAnimation/SportsRacingCar_0.png')
GREEN_CAR = pygame.image.load('/Users/Jewel M/PycharmProjects/MarcoWheels/Images/green-car.png')
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
        self.maxSpeed = self.maxSpeed + coin_score*0.015

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

    # checks for any collision
    def collisions(self, mask, x, y):
        # creates a car mask (ignores transparent pixels)
        carMask = pygame.mask.from_surface(self.image)
        # checks the offset position of the car relative to the border
        offset = (int(self.x - x), int(self.y - y))
        # looks for a point of intersection between the car and the border
        poi = mask.overlap(carMask, offset)
        return poi

    # defines what to do in the case of a collision
    def collide(self):
        # the car is thrown backwards at the current speed
        self.speed = -self.speed

    # defines what to do in the case that the car goes off-road
    def offroad(self):
        # the car is reduced to a portion of the original speed
        self.speed = self.speed*0.97

# uses the base car template to create the player car
class PlayerCar(BaseCarPlayer):
    # sets the player's car image
    IMG = MARCO_CAR
    # sets the starting position of the player's car!
    xy = (37, 515)

# rotates an image around its center
def rotCenter(screen, image, top_left, angle):
    rotIMG = pygame.transform.rotate(image, angle)
    new_rect = rotIMG.get_rect(center=image.get_rect(topleft=top_left).center)
    screen.blit(rotIMG, new_rect.topleft)

class ComputerCar(BaseCarPlayer):
    #sets the computer's car image
    IMG = GREEN_CAR
    #sets the starting postion of the computer's car
    xy = (74, 515)

    #def __init__(self, , path=[]):
       # super().__init__(max_vel, rotation_vel)
       # self.rotVelocity = rotVelocity
       # self.path = path
        #self.current_point = 0
       # self.vel = max_vel

   # def draw_points(self, win):
       # for point in self.path:
            #pygame.draw.circle(win, (255, 0, 0), point, 5)

    #def draw(self, win):
       # super().draw(win)
       # self.draw_points(win)