from PlayerClass import Player
import pygame
import math
from TextClass import *
# test
pygame.init()

player = Player(500, 500)
fps = 60

clock = pygame.time.Clock()
size = pygame.display.Info()
screen = pygame.display.set_mode((size.current_w, size.current_h))

screenW = size.current_w
screenH = size.current_h

playerImage = pygame.image.load("Stationary.xcf")
font = pygame.font.Font("MainFont.otf", 15)


def Play():
    angleText = Text(font)
    while True:
        # statements every frame
        screen.fill((255, 255, 255))
        clock.tick(fps)
        mx, my = pygame.mouse.get_pos()
        player.drawPlayer(playerImage, screen)
        player.facingLine(20, screen)

        # check for events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()

        # find facing angle
        opposite = player.y - my
        adjacent = mx - player.y
        angle = player.findAngle(mx, my, opposite, adjacent)

        # draw angle
        angleText.updateText(round(math.degrees(angle)))
        angleText.updatePos(player.x + player.xChange, player.y + player.yChange)
        angleText.write(screen, (0, 0, 0))

        pygame.display.update()


if __name__ == '__main__':
    Play()
