from math import sin, cos, atan, pi
import pygame


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.facingAngle = 1
        self.xChange = 1
        self.yChange = 1
        self.col = (0, 0, 0)

    # draw player
    def drawPlayer(self, image, screen):
        screen.blit(image, (self.x - 47, self.y - 47))

    # draw players pointer
    def facingLine(self, length, screen):
        self.yChange = -sin(self.facingAngle) * length
        self.xChange = cos(self.facingAngle) * length
        pygame.draw.line(screen, (0, 0, 0), [self.x, self.y],
                         [self.x + self.xChange, self.y + self.yChange], 3)

    # finds what angle the player is facing
    def findAngle(self, mx, my, opposite, adjacent):
        # Northeast quadrant
        if mx > self.x and my < self.y:
            self.facingAngle = atan(opposite / adjacent)
        # Northwest quadrant and Southwest quadrant
        elif mx < self.x and my < self.y or mx < self.x and my > self.y:
            self.facingAngle = pi + atan(opposite / adjacent)
        # Southeast quadrant
        elif mx > self.x and my > self.y:
            self.facingAngle = pi * 2 + atan(opposite / adjacent)
        # North
        elif mx == self.x and my < self.y:
            self.facingAngle = pi / 2
        # South
        elif mx == self.x and my > self.y:
            self.facingAngle = 3 * pi / 2
        # East
        elif my == self.y and mx > self.x:
            self.facingAngle = 0
        # West
        elif my == self.y and mx < self.x:
            self.facingAngle = pi
        return self.facingAngle
