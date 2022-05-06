# import the modules and files
import pygame
import map
import sprites

# loads the image that will be used for the background
background = pygame.image.load('Images/track.png')
# loads the image that will be used for collisions
border = pygame.image.load('Images/border.png')
# makes a mask for the border (ignores transparent pixels)
borderMask = pygame.mask.from_surface(border)
background_rect = background.get_rect()
screenHeight = 850
screenWidth = 850
# frames per second
FPS = 60

# initializes pygame screen with its set caption
pygame.init()
screen = pygame.display.set_mode([screenWidth, screenHeight])
pygame.display.set_caption("Marco's Wheels")
clock = pygame.time.Clock()

# groups
player = sprites.PlayerCar(4, 2)
mapMove = map.MapMovement()

def main():
    # game loop
    running = True
    while running:
        # keeps the loop running at the same speed in any device used
        clock.tick(FPS)
        for event in pygame.event.get():
            # ends the code when the pygame window is closed or if the escape key is pressed
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        # each time the loop runs, and there is no movement after previous movement, de acceleration is activated
        moving = False
        # when player presses down on the left arrow key, the car rotates towards the left
        if keys[pygame.K_LEFT]:
            player.steering(left=True)
        # when player presses down on the right arrow key, the car rotates towards the left
        if keys[pygame.K_RIGHT]:
            player.steering(right=True)
        # when player presses down on the up key, the car begins accelerating forward
        if keys[pygame.K_UP]:
            moving = True
            player.accelerate_for()
        # when player presses down on the up key, the car begins accelerating backwards
        if keys[pygame.K_DOWN]:
            moving = True
            player.accelerate_back()
        # otherwise, the car begins de-accelerating
        if not moving:
            player.de_accelerate()
        # if the car hits the border of the map, the car will get pushed back at a fraction of its speed (for aesthetic)
        # takes perfect pixel collision, the overlapping of the border and the visible pixels of the players car
        # if it detects a point of intersection(POI), a collision occurs
        if player.collisions(borderMask) is not None:
            player.collide()

        # draws the background
        screen.blit(background, background_rect)
        # draws the players car
        player.draw(screen)
        # updates the players screen to keep it from getting messy
        pygame.display.update()


# runs the main code
main()
