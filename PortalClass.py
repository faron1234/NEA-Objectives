from static import Colours
import pygame


class PortalSprite(pygame.sprite.Sprite):
    def __init__(self, colour, name):
        super().__init__()
        self.direction = None
        self.x = None
        self.y = None
        self.name = name
        self.colour = colour
        self.width = 28
        self.height = 80
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.intersectionLine = None

    def setPos(self, projectile):
        if projectile.name == 1:
            self.x = projectile.intersectionLine.xi1
            self.y = projectile.intersectionLine.yi1
        elif projectile.name == 2:
            self.x = projectile.intersectionLine.xi2
            self.y = projectile.intersectionLine.yi2

    def setLine(self, line):
        self.intersectionLine = line
        self.direction = self.intersectionLine.direction

    def update(self, screen):
        if not self.x and not self.y:
            return
        self.rect.center = (self.x, self.y)
        pygame.draw.rect(screen, Colours.black, self.rect)
        self.drawPortal(screen)

    # draws the portal with a specific colour to the screen where the projectile hits
    def drawPortal(self, screen):
        if not self.x and not self.y:
            return
        if self.intersectionLine.direction == 1 or self.intersectionLine.direction == 3:
            pygame.draw.ellipse(screen, self.colour, [self.x - 30, self.y - 13, self.height, self.width], 4)
        if self.intersectionLine.direction == 4 or self.intersectionLine.direction == 2:
            pygame.draw.ellipse(screen, self.colour, [self.x - 13, self.y - 30, self.width, self.height], 4)


portalSprites = pygame.sprite.Group()
portal = PortalSprite(Colours.blue, 1)
portal2 = PortalSprite(Colours.orange, 2)
portalSprites.add(portal)
portalSprites.add(portal2)
