# import the modules
import pygame
import time
# import supporting files
import sprites
import powerups
import buttons
from utility_fxn import scaling_factor


# initializes pygame
pygame.init()
# loads the image that will be used for the background
background = scaling_factor(pygame.image.load('Images/track.png'), 0.9)
# loads the image that will be used for the background
finishLine = scaling_factor(pygame.image.load('Images/finishline.png'), 0.9)
# makes a mask for the border (ignores transparent pixels)
finishLineMask = pygame.mask.from_surface(finishLine)
# loads the sound that will be used for the picking up coins
coin_sound = pygame.mixer.Sound('Sounds/Coin.wav')
# loads the sound that will be used for slipping on oil
oil_sound = pygame.mixer.Sound('Sounds/Oil.wav')
# loads the background for the rules page
black = pygame.image.load('Images/black.webp')
# loads the image that will be used for collisions
border = scaling_factor(pygame.image.load('Images/border.png'), 0.9)
# makes a mask for the border (ignores transparent pixels)
borderMask = pygame.mask.from_surface(border)
# loads the image that will be used for off-road slowing down
dirt = scaling_factor(pygame.image.load('Images/dirt.png'), 0.9)
# makes a mask for the dirt on the track (ignores transparent pixels)
dirtMask = pygame.mask.from_surface(dirt)
# pictures for the powerups
mushroomPic = pygame.image.load('Images/Mushroom.png')
bananaPic = pygame.image.load('Images/banana.png')
bananaMask = pygame.mask.from_surface(bananaPic)
coinPic = pygame.image.load('Images/CoinAnimation/Coin1.png')
none = pygame.image.load('Images/None.png')
background_rect = background.get_rect()
finishLine_rect = finishLine.get_rect()
screenWidth = background.get_width()
screenHeight = background.get_height()

# initializes pygame screen with its set caption
screen = pygame.display.set_mode([screenWidth, screenHeight])
pygame.display.set_caption("Marco's Wheels")
font = pygame.font.Font(pygame.font.get_default_font(), 20)
clock = pygame.time.Clock()

button = buttons.Button
# coin placement and image
coinList = [pygame.image.load('Images/CoinAnimation/Coin1.png'),
            pygame.image.load('Images/CoinAnimation/Coin2.png'),
            pygame.image.load('Images/CoinAnimation/Coin3.png'),
            pygame.image.load('Images/CoinAnimation/Coin4.png'),
            pygame.image.load('Images/CoinAnimation/Coin5.png')]
coinAnimation = powerups.Animation(coinList)
coinMask = pygame.mask.from_surface(coinList[1])
# oil puddle placement and image
oil_image = pygame.image.load('Images/oil.png')
oilMask = pygame.mask.from_surface(oil_image)
oil = [pygame.Rect(208, 39, 41, 50), pygame.Rect(400, 246, 41, 50), pygame.Rect(676, 59, 41, 50),
       pygame.Rect(461, 450, 41, 50), pygame.Rect(700, 663, 41, 50), pygame.Rect(80, 714, 41, 50)]
# mystery box placement and image
random_image = pygame.image.load('Images/Random.png')
randomMask = pygame.mask.from_surface(random_image)

# set points the computer car will follow
PATH = [(51, 163), (77, 91), (208, 39), (293, 159),
        (357, 238), (483, 192), (516, 74), (641, 38),
        (720, 167), (682, 304), (322, 387), (301, 473),
        (647, 472), (723, 582), (643, 691), (530, 696),
        (435, 613), (328, 631), (202, 727), (73, 655), (63, 325)]
# frames per second
FPS = 60
# groups
player = sprites.PlayerCar(4, 2)
computer = sprites.ComputerCar(2, 10, PATH)


def main_menu():
    # load the menu background
    menuBackground = pygame.image.load('Images/menubackground.png')
    screen.blit(menuBackground, (-310, 0))
    running1 = True
    # loads the menu music to play nonstop and lowers its volume
    pygame.mixer.music.load('Sounds/Menu.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    while running1:
        # creates the start button
        startButton = button("START", pygame.image.load("Images/button.png"),
                             390, 395, pygame.font.Font(pygame.font.get_default_font(), 20), (255, 255, 255))
        # creates the rules button
        rulesButton = button("RULES", pygame.image.load("Images/button.png"),
                             390, 435, pygame.font.Font(pygame.font.get_default_font(), 20), (255, 255, 255))
        # creates the quit button
        quitButton = button("QUIT", pygame.image.load("Images/button.png"),
                            390, 475, pygame.font.Font(pygame.font.get_default_font(), 20), (255, 255, 255))

        # the buttons are placed into a vector
        buttons = [startButton, rulesButton, quitButton]
        # the position of the mouse is defined as mouse
        mouse = pygame.mouse.get_pos()
        # the buttons are drawn onto the screen (image and then text)
        for b in buttons:
            screen.blit(b.image, b.rect)
            screen.blit(b.text, b.text_rect)

        for event in pygame.event.get():
            # ends the code when the escape key is pressed
            if event.type == pygame.QUIT:
                running1 = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running1 = False
            # checks if the mouse click is within one of the buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                if startButton.buttonPosition(mouse):
                    # starts the game
                    running1 = False
                    countdownStart()
                if rulesButton.buttonPosition(mouse):
                    # goes to rules screen
                    running1 = False
                    rules()
                if quitButton.buttonPosition(mouse):
                    # closes window
                    running1 = False
        # writes the title and updates the screen
        header = pygame.font.SysFont(None, 100)
        text = "MARCO'S WHEELS"
        rule_display = header.render(text, True, (0, 0, 0))
        screen.blit(rule_display, (65, 150))
        pygame.display.update()


def game():
    # game loop
    # places the coins
    coins = [pygame.Rect(30, 284, 41, 50), pygame.Rect(54, 284, 41, 50), pygame.Rect(78, 284, 41, 50),
             pygame.Rect(30, 202, 41, 50), pygame.Rect(54, 202, 41, 50), pygame.Rect(78, 202, 41, 50),
             pygame.Rect(164, 24, 41, 50), pygame.Rect(164, 68, 41, 50), pygame.Rect(237, 82, 41, 50),
             pygame.Rect(320, 205, 41, 50), pygame.Rect(308, 220, 41, 50), pygame.Rect(297, 235, 41, 50),
             pygame.Rect(595, 38, 41, 50), pygame.Rect(595, 62, 41, 50), pygame.Rect(670, 285, 41, 50),
             pygame.Rect(690, 305, 41, 50), pygame.Rect(300, 400, 41, 50), pygame.Rect(270, 435, 41, 50),
             pygame.Rect(300, 470, 41, 50), pygame.Rect(620, 450, 41, 50), pygame.Rect(620, 485, 41, 50),
             pygame.Rect(455, 695, 41, 50), pygame.Rect(476, 686, 41, 50), pygame.Rect(497, 677, 41, 50),
             pygame.Rect(174, 710, 41, 50), pygame.Rect(174, 740, 41, 50), pygame.Rect(66, 622, 41, 50)]

    # places the mystery boxes
    random = [pygame.Rect(30, 139, 41, 50), pygame.Rect(70, 139, 41, 50), pygame.Rect(160, 42, 41, 50),
              pygame.Rect(428, 207, 41, 50), pygame.Rect(448, 227, 41, 50), pygame.Rect(690, 175, 41, 50),
              pygame.Rect(715, 175, 41, 50), pygame.Rect(666, 300, 41, 50), pygame.Rect(266, 402, 41, 50),
              pygame.Rect(266, 465, 41, 50), pygame.Rect(600, 464, 41, 50), pygame.Rect(380, 585, 41, 50),
              pygame.Rect(380, 615, 41, 50), pygame.Rect(30, 550, 41, 50), pygame.Rect(70, 550, 41, 50)]
    # players box where powerups are stored
    box = []
    # keeps track of how many times the player/computer makes contact with the finish line
    player_count = 0
    computer_count = 0
    # keeps track of the last powerup that the player picked up
    last_powerup = none
    # every time the game function is called, the computer's car is reset to its starting position
    sprites.BaseCarPlayer.reset(player, 2, 2)
    running = True
    # keeps track of players coin score
    coin_score = 0
    # loads background music nonstop
    pygame.mixer.music.load('Sounds/background2.mp3')
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)
    # keeps track of the banana
    pos_x_y = (-10, -10)

    while running:
        # keeps the loop running at the same speed in any device used
        clock.tick(FPS)
        # enable animation for the coin
        coinAnimation.update()
        for event in pygame.event.get():
            # ends the code when the pygame window is closed or if the escape key is pressed
            if event.type == pygame.QUIT:
                running = False
                main_menu()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # starts the computer cars movement following the points set in PATH
        computer.accelerate_for()

        # each time the loop runs, and there is no movement after previous movement, de acceleration is activated
        moving = False
        keys = pygame.key.get_pressed()
        # when player presses down on the left arrow key, the car rotates towards the left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.steering(left=True)
            # changes player animation (wheels turn left)
            player.playerPicture(4)
        # when player presses down on the right arrow key, the car rotates towards the right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.steering(right=True)
            # changes player animation (wheels turn right)
            player.playerPicture(6)
        # when player presses down on the up key, the car begins accelerating forward
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            moving = True
            player.accelerate_for()
            if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
                # changes player animation (wheels turn right)
                player.playerPicture(4)
            elif keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
                # changes player animation (exhaust turns on)
                player.playerPicture(6)
            else:
                # changes player animation (plain car)
                player.playerPicture(1)
        # when player presses down on the up key, the car begins accelerating backwards
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            moving = True
            player.accelerate_back()

        # release and activation of powerups
        if keys[pygame.K_SPACE]:
            # if there are no powerups in store, nothing happens
            if len(box) == 0:
                pass
            elif box[0] == 'mushroom':
                player.changeMaxPU()
                mushroom_sound = pygame.mixer.Sound('Sounds/mushroom.mp3')
                mushroom_sound.play()
                last_powerup = none
                # box is emptied
                box = []
            elif box[0] == 'coin':
                coin_score += 1
                coin_sound.play()
                last_powerup = none
                # box is emptied
                box = []
            elif box[0] == 'banana':
                pos_x_y = player.position()
                banana_sound = pygame.mixer.Sound('Sounds/banana.wav')
                banana_sound.play()
                last_powerup = none
                # box is emptied
                box = []

        # otherwise, the car begins de-accelerating
        if not moving:
            player.de_accelerate()
            if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                player.playerPicture(0)

        # if the car hits the border of the map, the car will get speed backwards at a fraction of its prior speed
        if player.collisions(borderMask, 0, 0) is not None:
            player.collide()
            border_sound = pygame.mixer.Sound('Sounds/Collision.wav')
            border_sound.play()
            # coin balance is lowered due to collisions
            coin_score -= 1
            # prevents the coin score from going into a negative balance which would result into a negative velocity
            if coin_score < 0:
                coin_score = 0

        # if the car hits a banana, the car will rotate 180
        if player.collisions(bananaMask, 0, 0) is not None:
            bananas_sound = pygame.mixer.Sound('Sounds/bananaslip.mp3')
            bananas_sound.play()
            pos_x_y = (-10, -10)
            player.banana_and_oil_slip()
        # if the car starts driving on the dirt, the car will slow down
        if player.collisions(dirtMask, 0, 0) is not None:
            player.offroad()

        # if the car hits a banana, the computer car will speed to its last point
        if computer.collisions(bananaMask, 0, 0) is not None:
            computer.bananaSlip()
            bananas_sound = pygame.mixer.Sound('Sounds/bananaslip.mp3')
            bananas_sound.play()
            pos_x_y = (-10, -10)

        # if the player car hits the finish line 20 times at 60 fps, player wins
        if player.collisions(finishLineMask, 0, 0) is not None:
            player_count += 1
            if player_count == 20:
                end_gamePlayerWin()
                break

        # if the computer car hits the finish line 20 times at 60 fps, the computer car wins
        if computer.collisions(finishLineMask, 0, 0) is not None:
            computer_count += 1
            if computer_count == 20:
                end_gamePlayerLose()
                break

        for r in random:
            # when players hits a random box
            if player.collisions(randomMask, r[0], r[1]) is not None:
                # the player is randomly assigned a powerup
                player_powerup = powerups.random()
                # the powerup is placed into the box and a picture is displayed for the player to see
                if player_powerup == 'coin':
                    box = []
                    last_powerup = coinPic
                    box.append('coin')
                elif player_powerup == 'mushroom':
                    box = []
                    last_powerup = mushroomPic
                    box.append('mushroom')
                elif player_powerup == 'banana':
                    box = []
                    last_powerup = bananaPic
                    box.append('banana')
                random.remove(r)
                # the box is removed from the screen when player touches it
            # when computer hits a random box, the box is removed from the screen
            if computer.collisions(randomMask, r[0], r[1]) is not None:
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
            # when computer hits a coin, the coin is removed from the screen
            if computer.collisions(coinMask, coin[0], coin[1]) is not None:
                coins.remove(coin)

        for oi in oil:
            if player.collisions(oilMask, oi[0], oi[1]) is not None:
                oil_sound.play()
                coin_score = 0
                player.offroad()
                player.banana_and_oil_slip()

        screen.blit(background, background_rect)
        # draws the coins in place with animation
        for coin in coins:
            coinAnimation.draw(screen, coin[0], coin[1])
        # draws the oil puddles in place
        for o in oil:
            screen.blit(oil_image, (o[0], o[1]))
        # draws the mystery boxes in place
        for r in random:
            screen.blit(random_image, (r[0], r[1]))
        screen.blit(bananaPic, pos_x_y)
        # draws the players car
        player.draw(screen)
        # draws the computer's car
        computer.draw(screen)

        # HUD
        coin_display = font.render('Coins: ' + str(coin_score), True, (0, 0, 0))
        coin_rect = coin_display.get_rect()
        coin_rect.x = 10
        coin_rect.y = 10
        screen.blit(coin_display, coin_rect)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(15, 38, 38, 38))
        screen.blit(last_powerup, (26, 51))
        # updates the players screen to keep it from getting messy
        pygame.display.update()


def rules():
    screen.blit(black, (0, 0))
    running2 = True
    while running2:
        for event in pygame.event.get():
            # ends the code when the pygame window is closed or if the escape key is pressed
            if event.type == pygame.QUIT:
                running2 = False
                main_menu()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running2 = False
            keys2 = pygame.key.get_pressed()
            if keys2[pygame.K_m]:
                running2 = False
                main_menu()


        # SCREEN TEXT
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

        text3 = 'Traps: Oil puddles make you lose all of your coins'
        rule_display3 = font.render(text3, True, (255, 200, 0))
        screen.blit(rule_display3, (33, 193))

        text3_1 = 'and reset your maximum speed.'
        rule_display3_1 = font.render(text3_1, True, (255, 200, 0))
        screen.blit(rule_display3_1, (122, 213))

        text3_2 = 'Hitting borders make you lose one coin.'
        rule_display3_2 = font.render(text3_2, True, (255, 200, 0))
        screen.blit(rule_display3_2, (100, 233))

        text_4 = 'Press m to go back to Main Menu'
        rule_display4 = font.render(text_4, True, (255, 0, 0))
        screen.blit(rule_display4, (200, 600))
        pygame.display.update()


def countdownStart():
    running3 = True
    pygame.mixer.music.stop()
    computer.reset()
    while running3:
        screen.blit(black, (450, 450))
        for event in pygame.event.get():
            # ends the code when the pygame window is closed or if the escape key is pressed
            if event.type == pygame.QUIT:
                running3 = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running3 = False
        screen.fill((0, 0, 0))
        text = 'ARE YOU READY?'
        ready_display = font.render(text, True, (255, 255, 255))
        screen.blit(ready_display, (290, 370))
        pygame.display.update()
        start_sound = pygame.mixer.Sound('Sounds/racestart.wav')
        start_sound.play()
        time.sleep(3.5)
        break
    game()


def end_gamePlayerWin():
    running4 = True
    pygame.mixer.music.stop()
    win_sound = pygame.mixer.Sound('Sounds/win.wav')
    win_sound.play()
    while running4:
        for event in pygame.event.get():
            # ends the code when the pygame window is closed or if the escape key is pressed
            if event.type == pygame.QUIT:
                running4 = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running4 = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running4 = False
                countdownStart()


        screen.fill((0, 0, 0))
        text = 'WOW YOU BEAT MARCO'
        ready_display = font.render(text, True, (255, 255, 255))
        screen.blit(ready_display, (260, 370))
        text1 = 'press space to restart or esc to quit'
        ready_display1 = font.render(text1, True, (255, 255, 255))
        screen.blit(ready_display1, (220, 570))
        pygame.display.update()


def end_gamePlayerLose():
    running4 = True
    pygame.mixer.music.stop()
    lose_sound = pygame.mixer.Sound('Sounds/lose.wav')
    lose_sound.play()
    while running4:
        for event in pygame.event.get():
            # ends the code when the pygame window is closed or if the escape key is pressed
            if event.type == pygame.QUIT:
                running4 = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running4 = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running4 = False
                countdownStart()

        screen.fill((0, 0, 0))
        text = 'YOU LOSE'
        ready_display = font.render(text, True, (255, 255, 255))
        screen.blit(ready_display, (315, 370))
        text1 = 'press space to restart or esc to quit'
        ready_display1 = font.render(text1, True, (255, 255, 255))
        screen.blit(ready_display1, (220, 570))
        pygame.display.update()


main_menu()
