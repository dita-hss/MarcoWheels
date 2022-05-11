# import the modules and files
import pygame
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

# coin placement and image
coin_image = pygame.image.load('Images/Coin_power.png')
coinMask = pygame.mask.from_surface(coin_image)
coins = [pygame.Rect(38, 284, 41, 50), pygame.Rect(62, 284, 41, 50), pygame.Rect(85, 284, 41, 50),
         pygame.Rect(38, 202, 41, 50), pygame.Rect(62, 202, 41, 50), pygame.Rect(85, 202, 41, 50),
         pygame.Rect(164, 29, 41, 50), pygame.Rect(164, 73, 41, 50), pygame.Rect(248, 82, 41, 50),
         pygame.Rect(360, 228, 41, 50), pygame.Rect(348, 243, 41, 50), pygame.Rect(337, 258, 41, 50),
         pygame.Rect(648, 38, 41, 50), pygame.Rect(649, 62, 41, 50), pygame.Rect(667, 339, 41, 50),
         pygame.Rect(674, 369, 41, 50), pygame.Rect(378, 443, 41, 50), pygame.Rect(343, 473, 41, 50),
         pygame.Rect(357, 506, 41, 50), pygame.Rect(679, 502, 41, 50), pygame.Rect(680, 530, 41, 50),
         pygame.Rect(487, 715, 41, 50), pygame.Rect(508, 706, 41, 50), pygame.Rect(528, 695, 41, 50),
         pygame.Rect(194, 788, 41, 50), pygame.Rect(194, 816, 41, 50), pygame.Rect(60, 617, 41, 50)]
# oil puddle placement and image
oil_image = pygame.image.load('Images/oil.png')
oilMask = pygame.mask.from_surface(oil_image)
oil = [pygame.Rect(85, 300, 41, 50)]
# mystery box placement and image
random_image = pygame.image.load('Images/Random.png')
randomMask = pygame.mask.from_surface(random_image)
random = [pygame.Rect(85, 350, 41, 50)]

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print(pos)
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
            # coin balance is lowered due to collisions
            coin_score -= 1
        # if the car starts driving on the dirt, the car will slow down
        elif player.collisions(dirtMask, 0, 0) is not None:
            player.offroad()
        # when a player touches a coin, that coin is removed from the list and erased from the screem
        for coin in coins:
            # checks for player/coin collision
            if player.collisions(coinMask, coin[0], coin[1]) is not None:
                # if there was a collision with a coin, the coin is removed from the screen
                coins.remove(coin)
                # coin balance is raised
                coin_score += 1
                # maximum speed is updated
                player.changeMax(coin_score)
        # draws the background
        screen.blit(background, background_rect)
        # draws the coins in place
        for coin in coins:
            screen.blit(coin_image, (coin[0], coin[1]))
        # draws the oil puddles in place
        for o in oil:
            screen.blit(oil_image, (o[0], o[1]))
        # draws the mystery boxes in place
        for r in random:
            screen.blit(random_image, (r[0], r[1]))
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
