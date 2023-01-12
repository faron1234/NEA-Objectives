from static import Colours
import pygame
from math import pi


class Portal:
    def __init__(self, portalX, portalY, colour):
        self.angle = None
        self.orientation = None
        self.portalX = portalX
        self.portalY = portalY
        self.colour = colour

    # draws the portal with a specific colour to the screen where the projectile hits
    def drawPortal(self, screen):
        pygame.draw.circle(screen, self.colour, [self.portalX, self.portalY], 16, 3)
        pygame.draw.arc(screen, Colours.black, [self.portalX-16, self.portalY-16, 32, 32], 0, pi, 2)
