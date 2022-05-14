# import the modules and files
import pygame
import sprites
import powerups
import Buttons
from utils import scale_image


# initializes pygame
pygame.init()
# loads the image that will be used for the background
background = scale_image(pygame.image.load('Images/track.png'), 0.9)
# loads the sound that will be used for the picking up coins
coin_sound = pygame.mixer.Sound('Sounds/Coin.wav')
# loads the sound that will be used for slipping on oil
oil_sound = pygame.mixer.Sound('Sounds/Oil.wav')
black = pygame.image.load('Images/black.webp')
# loads the image that will be used for collisions
border = scale_image(pygame.image.load('Images/border.png'), 0.9)
# makes a mask for the border (ignores transparent pixels)
borderMask = pygame.mask.from_surface(border)
# loads the image that will be used for off-road slowing down
dirt = scale_image(pygame.image.load('Images/dirt.png'), 0.9)
# makes a mask for the dirt on the track (ignores transparent pixels)
dirtMask = pygame.mask.from_surface(dirt)
mushroomPic = pygame.image.load('Images/Mushroom.png')
bananaPic = pygame.image.load('Images/banana.png')
coinPic = pygame.image.load('Images/CoinAnimation/Coin1.png')
none = pygame.image.load('Images/None.png')


background_rect = background.get_rect()
WIDTH, HEIGHT = background.get_width(), background.get_height()
#screenHeight = 850
#screenWidth = 850
# frames per second
FPS = 60

# initializes pygame screen with its set caption
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Marco's Wheels")
font = pygame.font.Font(pygame.font.get_default_font(), 20)
clock = pygame.time.Clock()

# groups
player = sprites.PlayerCar(2, 2)
computer =sprites.ComputerCar (2,2)
button = Buttons.Button
# coin placement and image
coinList = [pygame.image.load('Images/CoinAnimation/Coin1.png'),
            pygame.image.load('Images/CoinAnimation/Coin2.png'),
            pygame.image.load('Images/CoinAnimation/Coin3.png'),
            pygame.image.load('Images/CoinAnimation/Coin4.png'),
            pygame.image.load('Images/CoinAnimation/Coin5.png')]
coinAnimation = powerups.Animation(coinList)
coinMask = pygame.mask.from_surface(coinList[1])
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
oil = [pygame.Rect(107, 103, 41, 50), pygame.Rect(586, 59, 41, 50), pygame.Rect(461, 527, 41, 50),
       pygame.Rect(781, 725, 41, 50), pygame.Rect(166, 802, 41, 50), pygame.Rect(52, 657, 41, 50)]
# mystery box placement and image
random_image = pygame.image.load('Images/Random.png')
randomMask = pygame.mask.from_surface(random_image)
random = [pygame.Rect(40, 139, 41, 50), pygame.Rect(80, 139, 41, 50), pygame.Rect(160, 47, 41, 50),
          pygame.Rect(498, 213, 41, 50), pygame.Rect(513, 225, 41, 50), pygame.Rect(530, 235, 41, 50),
          pygame.Rect(764, 225, 41, 50), pygame.Rect(797, 225, 41, 50), pygame.Rect(666, 349, 41, 50),
          pygame.Rect(278, 452, 41, 50), pygame.Rect(279, 520, 41, 50), pygame.Rect(425, 541, 41, 50),
          pygame.Rect(631, 753, 41, 50), pygame.Rect(631, 784, 41, 50), pygame.Rect(37, 554, 41, 50),
          pygame.Rect(79, 554, 41, 50)]


def main_menu():
    menuBackground = pygame.image.load('Images/menubackground.png')
    screen.blit(menuBackground, (0, 0))
    running1 = True
    pygame.mixer.music.load('Sounds/Menu.mp3')
    pygame.mixer.music.play(-1)

    while running1:
        startButton = button("START", pygame.image.load("Images/button.png"),
                             405, 395, pygame.font.Font(pygame.font.get_default_font(), 20), (255, 255, 255))
        rulesButton = button("RULES", pygame.image.load("Images/button.png"),
                             405, 435, pygame.font.Font(pygame.font.get_default_font(), 20), (255, 255, 255))
        quitButton = button("QUIT", pygame.image.load("Images/button.png"),
                            405, 475, pygame.font.Font(pygame.font.get_default_font(), 20), (255, 255, 255))

        buttons = [startButton, rulesButton, quitButton]
        mouse = pygame.mouse.get_pos()
        for b in buttons:
            if b.image is not None:
                screen.blit(b.image, b.rect)
            screen.blit(b.text, b.text_rect)

        for event in pygame.event.get():
            # ends the code when the pygame window is closed or if the escape key is pressed
            if event.type == pygame.QUIT:
                running1 = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running1 = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if startButton.mouseInput(mouse):
                    countdownStart()
                    running1 = False
                if rulesButton.mouseInput(mouse):
                    rules()
                    running1 = False
                if quitButton.mouseInput(mouse):
                    running1 = False
        pygame.display.update()


def game():
    # game loop
    box = []
    last_powerup = none
    sprites.BaseCarPlayer.reset(player, 2, 2)
    running = True
    coin_score = 0
    # loads background music
    pygame.mixer.music.load('Sounds/Background.mp3')
    pygame.mixer.music.play(-1)
    while running:
        # keeps the loop running at the same speed in any device used
        clock.tick(FPS)
        coinAnimation.update()
        for event in pygame.event.get():
            # ends the code when the pygame window is closed or if the escape key is pressed
            if event.type == pygame.QUIT:
                main_menu()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        # each time the loop runs, and there is no movement after previous movement, de acceleration is activated
        moving = False
        keys = pygame.key.get_pressed()
        # when player presses down on the left arrow key, the car rotates towards the left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.steering(left=True)
            player.playerPicture(4)
        # when player presses down on the right arrow key, the car rotates towards the left
        if keys[pygame.K_RIGHT or keys[pygame.K_d]]:
            player.steering(right=True)
            player.playerPicture(6)
        # when player presses down on the up key, the car begins accelerating forward
        if keys[pygame.K_UP or keys[pygame.K_w]]:
            moving = True
            player.accelerate_for()
            if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
                player.playerPicture(4)
            elif keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
                player.playerPicture(6)
            else:
                player.playerPicture(1)
        # when player presses down on the up key, the car begins accelerating backwards
        if keys[pygame.K_DOWN]:
            moving = True
            player.accelerate_back()
        if keys[pygame.K_SPACE]:
            if len(box) == 0:
                pass
            elif box[0] == 'mushroom':
                player.changeMaxPU()
                last_powerup = none
                box = []
            elif box[0] == 'coin':
                coin_score += 1
                coin_sound.play()
                last_powerup = none
                box = []
            elif box[0] == 'banana':
                screen.blit(bananaPic, (player.position()))
                last_powerup = none
                box = []

        # otherwise, the car begins de-accelerating
        if not moving:
            player.de_accelerate()
            if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                player.playerPicture(0)

        # if the car hits the border of the map, the car will get pushed back at a fraction of its speed (for aesthetic)
        # takes perfect pixel collision, the overlapping of the border and the visible pixels of the player's car
        # if it detects a point of intersection(POI), a collision occurs
        if player.collisions(borderMask, 0, 0) is not None:
            player.collide()
            border_sound = pygame.mixer.Sound('Sounds/Collision.wav')
            border_sound.play()
            # coin balance is lowered due to collisions
            coin_score -= 1
            # prevents the coin score from going into a negative balance which would result into a negative velocity
            if coin_score < 0:
                coin_score = 0
        # if the car starts driving on the dirt, the car will slow down
        elif player.collisions(dirtMask, 0, 0) is not None:
            player.offroad()
        for r in random:
            if player.collisions(randomMask, r[0], r[1]) is not None:
                if powerups.random() == 'coin':
                    box = []
                    last_powerup = coinPic
                    box.append('coin')
                elif powerups.random() == 'mushroom':
                    box = []
                    last_powerup = mushroomPic
                    box.append('mushroom')
                elif powerups.random() == 'banana':
                    box = []
                    last_powerup = bananaPic
                    box.append('banana')
                random.remove(r)
        # when a player touches a coin, that coin is removed from the list and erased from the screem
        for coin in coins:
            # checks for player/coin collision
            if player.collisions(coinMask, coin[0], coin[1]) is not None:
                # if there was a collision with a coin, the coin is removed from the screen
                coins.remove(coin)
                coin_sound.play()
                # coin balance is raised
                coin_score += 1
                # maximum speed is updated
                player.changeMax(coin_score)
        # draws the background

        for oi in oil:
            if player.collisions(oilMask, oi[0], oi[1]) is not None:
                oil_sound.play()
                coin_score = 0
                player.offroad()

        screen.blit(background, background_rect)
        # draws the coins in place
        for coin in coins:
            coinAnimation.draw(screen, coin[0], coin[1])
        # draws the oil puddles in place
        for o in oil:
            screen.blit(oil_image, (o[0], o[1]))
        # draws the mystery boxes in place
        for r in random:
            screen.blit(random_image, (r[0], r[1]))
        # draws the players car
        player.draw(screen)
        computer.draw(screen)

        # HUD
        coin_display = font.render('Coins: ' + str(coin_score), True, (0, 0, 0))
        coin_rect = coin_display.get_rect()
        coin_rect.x = 10
        coin_rect.y = 10
        screen.blit(coin_display, coin_rect)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(20, 40, 40, 40))
        screen.blit(last_powerup, (33, 53))


        # updates the players screen to keep it from getting messy
        pygame.display.update()


def rules():
    screen.blit(black, (0, 0))
    running2 = True
    while running2:
        for event in pygame.event.get():
            # ends the code when the pygame window is closed or if the escape key is pressed
            if event.type == pygame.QUIT:
                main_menu()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running2 = False

        text = 'Player movement: You can use the arrow keys or WASD.'
        rule_display = font.render(text, True, (255, 100, 0))
        screen.blit(rule_display, (33, 53))

        text2 = 'Powerups: Mushrooms increase your maximum speed.'
        rule_display2 = font.render(text2, True, (255, 150, 0))
        screen.blit(rule_display2, (33, 93))

        text2_1 = 'Coins speed you up.'
        rule_display2_1 = font.render(text2_1, True, (255, 150, 0))
        screen.blit(rule_display2_1, (143, 113))

        text2_2 = 'Bananas make your opponent or yourself slip.'
        rule_display2_2 = font.render(text2_2, True, (255, 150, 0))
        screen.blit(rule_display2_2, (143, 133))

        text2_3 = 'Press the spacebar to redeem powerup.'
        rule_display2_2 = font.render(text2_3, True, (255, 150, 0))
        screen.blit(rule_display2_2, (143, 153))

        text3 = 'Traps: Oil puddles make you lose all of your coins and reset your maximum speed.'
        rule_display3 = font.render(text3, True, (255, 200, 0))
        screen.blit(rule_display3, (33, 193))

        text3_1 = 'Hitting borders make you lose one coin.'
        rule_display3_2 = font.render(text3_1, True, (255, 200, 0))
        screen.blit(rule_display3_2, (102, 213))
        pygame.display.update()


def countdownStart():
    running3 = True
    while running3:
        screen.blit(black, (450, 450))
        for event in pygame.event.get():
            # ends the code when the pygame window is closed or if the escape key is pressed
            if event.type == pygame.QUIT:
                running3 = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running3 = False
        start_sound = pygame.mixer.Sound('Sounds/racestart.wav')
        start_sound.play()
        break
    game()


main_menu()