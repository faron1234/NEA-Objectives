from math import sin, cos, atan, pi, ceil, floor
from static import Colours
import pygame
from VectorClass import posVec


# def addImages(image):


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.SpritesRight = []
        self.SpritesLeft = []
        self.index = 0
        self.counter = 0
        for i in range(0, 5):
            imageRight = pygame.image.load(f'SpriteImages/SpritesRunRight/adventurer-run-{i}.png')
            imageRight = pygame.transform.scale(imageRight, (imageRight.get_width() * 2.5, imageRight.get_height() * 2.5))
            imageLeft = pygame.transform.flip(imageRight, True, False)
            self.SpritesRight.append(imageRight)
            self.SpritesLeft.append(imageLeft)
        self.image = self.SpritesRight[self.index]
        self.x = x
        self.y = y
        self.facingAngle = 0
        self.xChange = None
        self.yChange = None
        self.canJump = True
        self.movingRight = False
        self.movingLeft = False
        self.lastMoved = None
        self.col = Colours.black
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        animationCooldown = 10

        if not self.x and not self.y:
            return
        self.rect.center = (self.x, self.y)

        # animation
        self.counter += 1
        if self.counter <= animationCooldown:
            return

        self.counter = 0
        self.index += 1

        if not self.movingRight and not self.movingLeft:
            self.index = 2
            if self.lastMoved == "right":
                self.image = self.SpritesRight[self.index]
            elif self.lastMoved == "left":
                self.image = self.SpritesLeft[self.index]
            return

        if self.movingRight:
            if self.index >= len(self.SpritesRight):
                self.index = 0
            self.image = self.SpritesRight[self.index]
        if self.movingLeft:
            if self.index >= len(self.SpritesLeft):
                self.index = 0
            self.image = self.SpritesLeft[self.index]

    def setPos(self, newX, newY):
        self.x, self.y = newX, newY

    def drawPlayer(self, screen):
        screen.blit(self.image, self.rect)

    def objectCollide(self, sprites, vel):
        for spriteGroup in sprites:
            for sprite in spriteGroup:
                if sprite.objType == "polygon":
                    print(sprite.rect1, sprite.rect2)
                if vel.i > 0:
                    if sprite.rect.colliderect(self.rect.x + ceil(vel.i), self.rect.y, self.width, self.height):
                        vel.i = 0
                elif vel.i <= 0:
                    if sprite.rect.colliderect(self.rect.x + floor(vel.i), self.rect.y, self.width, self.height):
                        vel.i = 0
                if sprite.rect.colliderect(self.rect.x, self.rect.y + vel.j, self.width, self.height):
                    self.canJump = True
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


playerSprites = pygame.sprite.Group()
player = PlayerSprite(posVec.i, posVec.j)
playerSprites.add(player)
