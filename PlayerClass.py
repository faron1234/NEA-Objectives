from math import sin, cos, atan, pi
from static import Colours
import pygame


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.facingAngle = 1
        self.xChange = 1
        self.yChange = 1
        self.col = Colours.black

    def drawPlayer(self):
        pass
        # pygame.draw.rect(screen, self.col, [self.x - characterWidth / 2, self.y - characterWidth / 2,
        # characterWidth, characterHeight * 3 / 2])

    def changeCol(self, newCol):
        self.col = newCol

    # draw players pointer
    def facingLine(self, length, screen):
        self.yChange = -sin(self.facingAngle) * length
        self.xChange = cos(self.facingAngle) * length
        pygame.draw.aaline(screen, Colours.black, [self.x, self.y],
                           [self.x + self.xChange, self.y + self.yChange], 3)

    # updates the players position
    def updatePos(self, newX, newY):
        self.x = newX
        self.y = newY

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


class SpritesClass(pygame.sprite.Sprite):
    def __init__(self, imagePath):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale((pygame.image.load(imagePath)), (100, 100))

    def update(self, x, y):
        self.rect.center = (x - 40, y - 40)


playerSprite = SpritesClass("SpriteImages/Stationary.xcf")
playerRight = ()
allSprites = pygame.sprite.Group()
allSprites.add(playerSprite)
