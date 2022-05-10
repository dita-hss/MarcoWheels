# import the modules and files
import pygame
import map
import sprites
import powerups

# loads the image that will be used for the background
background = pygame.image.load('Images/track.png')
# loads the image that will be used for collisions
border = pygame.image.load('Images/border.png')
# makes a mask for the border (ignores transparent pixels)
borderMask = pygame.mask.from_surface(border)
# loads the image that will be used for off-road slowing down
dirt = pygame.image.load('Images/dirt.png')
# makes a mask for the dirt on the track (ignores transparent pixels)
dirtMask = pygame.mask.from_surface(dirt)

background_rect = background.get_rect()
screenHeight = 850
screenWidth = 850
# frames per second
FPS = 60

# initializes pygame screen with its set caption
pygame.init()
screen = pygame.display.set_mode([screenWidth, screenHeight])
pygame.display.set_caption("Marco's Wheels")
font = pygame.font.Font(pygame.font.get_default_font(), 20)
clock = pygame.time.Clock()

# groups
player = sprites.PlayerCar(2, 2)
mapMove = map.MapMovement()

# coin placement and image
coin_image = pygame.image.load('Images/Coin_power.png')
coinMask = pygame.mask.from_surface(coin_image)
coins = [pygame.Rect(50, 100, 41, 50), pygame.Rect(100, 100, 41, 50), pygame.Rect(150, 100, 41, 50),
         pygame.Rect(250, 100, 41, 50)]

def main():
    # game loop

    running = True
    coin_score = 0
    while running:
        # keeps the loop running at the same speed in any device used
        clock.tick(FPS)
        for event in pygame.event.get():
            # ends the code when the pygame window is closed or if the escape key is pressed
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        # each time the loop runs, and there is no movement after previous movement, de acceleration is activated
        moving = False

        keys = pygame.key.get_pressed()
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
        # takes perfect pixel collision, the overlapping of the border and the visible pixels of the player's car
        # if it detects a point of intersection(POI), a collision occurs
        if player.collisions(borderMask, 0, 0) is not None:
            player.collide()
        # if the car starts driving on the dirt, the car will slow down
        elif player.collisions(dirtMask, 0, 0) is not None:
            player.offroad()

        # when a player touches a coin, that coin is removed from the list and erased from the screem
        for coin in coins:
            # checks for player/coin collision
            if player.collisions(coinMask, coin[0], coin[1]) is not None:
                coins.remove(coin)
                coin_score += 1

        # draws the background
        screen.blit(background, background_rect)
        # draws the coins in place
        for coin in coins:
            screen.blit(coin_image, (coin[0], coin[1]))
        # draws the players car
        player.draw(screen)
        # HUD
        coin_display = font.render('Coins: ' + str(coin_score), True, (0, 0, 0))
        coin_rect = coin_display.get_rect()
        coin_rect.x = 10
        coin_rect.y = 10
        screen.blit(coin_display, coin_rect)
        # updates the players screen to keep it from getting messy
        pygame.display.update()


# runs the main code
main()
