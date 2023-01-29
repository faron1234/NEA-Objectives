from math import sin, cos, atan, pi, ceil, floor
from static import Colours
import pygame


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, imagePath, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.facingAngle = 0
        self.xChange = None
        self.yChange = None
        self.canJump = True
        self.col = Colours.black
        self.image = pygame.Surface([10, 10])
        self.image = pygame.image.load(imagePath)
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        if not self.x and not self.y:
            return
        self.rect.center = (self.x, self.y)

    def setPos(self, newX, newY):
        self.x, self.y = newX, newY

    def drawPlayer(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, self.col, self.rect, 2)

    def objectCollide(self, sprites, vel):
        for sprite in sprites:
            if vel.i > 0:
                if sprite.rect.colliderect(self.rect.x + ceil(vel.i), self.rect.y, self.width, self.height):
                    vel.i = 0
            elif vel.i <= 0:
                if sprite.rect.colliderect(self.rect.x + floor(vel.i), self.rect.y, self.width, self.height):
                    vel.i = 0
            if sprite.rect.colliderect(self.rect.x, self.rect.y + vel.j, self.width, self.height):
                if vel.j < 0:
                    vel.j = sprite.rect.bottom - self.rect.top
                elif vel.j >= 0:
                    vel.j = sprite.rect.top - self.rect.bottom

    def portalCollide(self, sprites):
        for sprite in sprites:
            if sprite.rect.colliderect(self.rect.x, self.rect.y, self.width, self.height):
                return sprite

    def changeCol(self, newCol):
        self.col = newCol

    # draw players pointer
    def facingLine(self, length, screen):
        self.yChange = -sin(self.facingAngle) * length
        self.xChange = cos(self.facingAngle) * length
        pygame.draw.aaline(screen, Colours.black, [self.x, self.y],
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
