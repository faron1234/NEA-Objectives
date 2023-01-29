from static import Colours
import pygame
from math import pi


class PortalSprite(pygame.sprite.Sprite):
    def __init__(self, colour):
        super().__init__()
        self.orientation = None
        self.portalX = None
        self.portalY = None
        self.colour = colour
        self.width = 32
        self.height = 32
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()

    def setPos(self, newX, newY):
        self.portalX = newX
        self.portalY = newY

    def update(self, screen):
        if not self.portalX and not self.portalY:
            return
        self.rect.center = (self.portalX, self.portalY)
        self.drawPortal(screen)

    # draws the portal with a specific colour to the screen where the projectile hits
    def drawPortal(self, screen):
        if not self.portalX and not self.portalY:
            return
        pygame.draw.circle(screen, self.colour, [self.portalX, self.portalY], 16, 3)
