from static import Colours
import pygame
from math import pi


class PortalSprite(pygame.sprite.Sprite):
    def __init__(self, colour):
        super().__init__()
        self.direction = None
        self.x = None
        self.y = None
        self.colour = colour
        self.width = 27
        self.height = 80
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.intersectionLine = None

    def setPos(self, projectile):
        if projectile.colour == Colours.blue:
            self.x = projectile.intersectionLine.xi1
            self.y = projectile.intersectionLine.yi1
        elif projectile.colour == Colours.orange:
            self.x = projectile.intersectionLine.xi2
            self.y = projectile.intersectionLine.yi2

    def setLine(self, line):
        self.intersectionLine = line
        self.direction = self.intersectionLine.direction

    def update(self, screen):
        if not self.x and not self.y:
            return
        self.rect.center = (self.x, self.y)
        self.drawPortal(screen)

    # draws the portal with a specific colour to the screen where the projectile hits
    def drawPortal(self, screen):
        if not self.x and not self.y:
            return
        if self.intersectionLine.direction == "up" or self.intersectionLine.direction == "down":
            pygame.draw.ellipse(screen, self.colour, [self.x - 30, self.y - 13, self.height, self.width], 4)
        if self.intersectionLine.direction == "left" or self.intersectionLine.direction == "right":
            pygame.draw.ellipse(screen, self.colour, [self.x - 13, self.y - 30, self.width, self.height], 4)


portalSprites = pygame.sprite.Group()
portal = PortalSprite(Colours.blue)
portal2 = PortalSprite(Colours.orange)
portalSprites.add(portal)
portalSprites.add(portal2)
