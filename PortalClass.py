from static import Colours
import pygame
from math import pi


class PortalSprite(pygame.sprite.Sprite):
    def __init__(self, portalX, portalY, colour):
        super().__init__()
        self.angle = None
        self.orientation = None
        self.portalX = portalX
        self.portalY = portalY
        self.colour = colour
        self.width = 32
        self.height = 32
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(Colours.white)
        self.rect = self.image.get_rect()

    def update(self, screen):
        self.rect.center = (self.portalX, self.portalY)
        self.drawPortal(screen)

    # draws the portal with a specific colour to the screen where the projectile hits
    def drawPortal(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)
        pygame.draw.circle(screen, self.colour, [self.portalX, self.portalY], 16, 3)
