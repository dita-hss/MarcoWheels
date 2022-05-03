
import pygame
import sprites

screenHeight = 1024
screenWidth = 1024
FPS = 30

#groups
mySprites = pygame.sprite.Group()
player = sprites.Player()
mySprites.add(player)

# initializes pygame screen with its set caption
pygame.init()
screen = pygame.display.set_mode([screenWidth, screenHeight])
pygame.display.set_caption("Marco's Wheels")
clock = pygame.time.Clock()
background = pygame.image.load('Track.png')
background_rect = background.get_rect()

def main():
    # game loop
    running = True
    while running:
        # keeps the loop running at the specified time
        clock.tick(FPS)
        for event in pygame.event.get():
            # ends the code when the pygame window is closed
            if event.type == pygame.QUIT:
                running = False

        # updates the players screen to keep it from getting messy
        mySprites.update()

        # draws the screen as black and then flips the screen
        screen.fill((0, 0, 0))
        screen.blit(background, background_rect)
        mySprites.draw(screen)
        pygame.display.flip()


main()
