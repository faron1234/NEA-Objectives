from math import sin, cos, atan, pi, ceil, floor
from static import Colours
import pygame
from itertools import repeat


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.SpritesRight = []
        self.SpritesLeft = []
        self.SpritesIdle = []
        self.index = 0
        self.counter = 0
        for i in range(0, 5):
            imageRight = pygame.image.load(f'SpriteImages/SpritesRunRight/adventurer-run-{i}.png')
            imageRight = pygame.transform.scale(imageRight, (imageRight.get_width()*2, imageRight.get_height()*2))
            imageLeft = pygame.transform.flip(imageRight, True, False)
            self.SpritesRight.append(imageRight)
            self.SpritesLeft.append(imageLeft)
        for i in range(0, 2):
            imageIdle = pygame.image.load(f'SpriteImages/SpritesIdle/adventurer-idle-0{i}.png')
            imageIdle = pygame.transform.scale(imageIdle, (imageIdle.get_width() * 2, imageIdle.get_height() * 2))
            self.SpritesIdle.append(imageIdle)
            self.SpritesIdle.append(imageIdle)
        self.image = self.SpritesRight[self.index]
        self.x = x
        self.y = y
        self.facingAngle = 0
        self.xChange = None
        self.yChange = None
        self.canJump = True
        self.movingRight = False
        self.movingLeft = False
        self.col = Colours.black
        self.mask = pygame.mask.from_surface(self.image)
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

        if self.counter > animationCooldown:
            self.counter = 0
            self.index += 1
            if self.movingRight:
                if self.index >= len(self.SpritesRight):
                    self.index = 0
                self.image = self.SpritesRight[self.index]
            if self.movingLeft:
                if self.index >= len(self.SpritesLeft):
                    self.index = 0
                self.image = self.SpritesLeft[self.index]
            if not self.movingRight and not self.movingLeft:
                if self.index >= len(self.SpritesIdle):
                    self.index = 0
                self.image = self.SpritesIdle[self.index]

    def setPos(self, newX, newY):
        self.x, self.y = newX, newY

    def drawPlayer(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, self.col, self.rect, 2)

    def objectCollide(self, sprites, vel):
        for sprite in sprites:
            if sprite.type == "polygon":
                if pygame.sprite.collide_mask(sprite, self):
                    print("collision")

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
