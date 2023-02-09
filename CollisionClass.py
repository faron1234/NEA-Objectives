from static import Colours
import pygame


class Line:
    def __init__(self, x1=None, y1=None, x2=None, y2=None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def setCoord(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def intersection(self, L2, screen):
        s1X = self.x2 - self.x1
        s1Y = self.y2 - self.y1
        s2X = L2.x2 - L2.x1
        s2Y = L2.y2 - L2.y1

        if -s2X * s1Y + s1X * s2Y == 0:
            return None

        s = (-s1Y * (self.x1 - L2.x1) + s1X * (self.y1 - L2.y1)) / (-s2X * s1Y + s1X * s2Y)
        t = (s2X * (self.y1 - L2.y1) - s2Y * (self.x1 - L2.x1)) / (-s2X * s1Y + s1X * s2Y)

        if 1 < s or s < 0 or 1 < t or t < 0:
            return None

        iX = self.x1 + (t * s1X)
        iY = self.y1 + (t * s1Y)
        pygame.draw.circle(screen, Colours.red, [iX, iY], 10)
        return iX, iY


L1 = Line()
