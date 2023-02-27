from math import sin, cos
import pygame


class ProjectileSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.angle = None
        self.x = None
        self.y = None
        self.colour = None
        self.xi = None
        self.yi = None
        self.intersectionLine = None
        self.image = pygame.Surface([5, 5])
        self.rect = self.image.get_rect()

    # returns a specific attribute of the projectile
    def getAttr(self, attribute):
        return self.__getattribute__(attribute)

    def update(self):
        if not self.x and not self.y:
            return
        self.rect.center = (self.x, self.y)

    # sets the initial angle of motion
    def setAngle(self, newAngle):
        self.angle = newAngle

    # draws the portal to the screen and calls the update position method, passing in a speed
    def drawProjectile(self, speedCoefficient, screen):
        if not self.x and not self.y:
            return
        self.updatePos(speedCoefficient)
        pygame.draw.rect(screen, self.colour, self.rect, 2)
        pygame.draw.circle(screen, self.colour, [self.x, self.y], 5)

    def setAttributes(self, angle, x, y, col, intersectionLine):
        self.angle = angle
        self.x = x
        self.y = y
        self.colour = col
        self.intersectionLine = intersectionLine

    # updates the position of the projectile on the y and x-axis
    def updatePos(self, speedCoefficient):
        if self.angle is not None:
            self.y -= sin(self.angle) * speedCoefficient
            self.x += cos(self.angle) * speedCoefficient

    # detects for collisions
    def collision(self, *sprites):
        for spriteGroup in sprites:
            if pygame.sprite.spritecollide(self, spriteGroup, False):
                self.x, self.y = None, None
                return True


projectileSprites = pygame.sprite.Group()
projectile = ProjectileSprite()
projectile2 = ProjectileSprite()
