from math import sin, cos
import pygame


class Projectile:
    def __init__(self, angle, x, y, col, xi, yi):
        self.angle = angle
        self.x = x
        self.y = y
        self.col = col
        self.xi = xi
        self.yi = yi

    # returns a specific attribute of the projectile
    def getAttr(self, attribute):
        return self.__getattribute__(attribute)

    # sets the initial angle of motion
    def setAngle(self, newAngle):
        self.angle = newAngle

    # draws the portal to the screen and calls the update position method, passing in a speed
    def drawProjectile(self, speedCoefficient, screen):
        self.updatePos(speedCoefficient)
        pygame.draw.circle(screen, self.col, [self.x, self.y], 5)

    # updates the position of the projectile on the y and x-axis
    def updatePos(self, speedCoefficient):
        if self.angle is not None:
            self.y -= sin(self.angle) * speedCoefficient
            self.x += cos(self.angle) * speedCoefficient

    # detects for collisions
    def collision(self, depth, screenW, screenH):
        if self.x < depth or self.x > screenW - depth or self.y < depth or self.y > screenH - depth:
            return True
