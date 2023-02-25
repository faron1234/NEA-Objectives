from static import Colours
import pygame


class Line:
    def __init__(self, x1=None, y1=None, x2=None, y2=None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    # used to set the coordinates of the line objects
    def setCoord(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    # used to find the intersection between two line segments
    def intersection(self, L2, screen):
        # used to calculate the direction vectors of both the lines
        s1X = self.x2 - self.x1
        s1Y = self.y2 - self.y1
        s2X = L2.x2 - L2.x1
        s2Y = L2.y2 - L2.y1

        # used to check if the lines are parallel,
        # if they are then there cannot be an intersection so None is returned
        if -s2X * s1Y + s1X * s2Y == 0:
            return None

        # calculates the position of intersection along the line for both the lines,
        # this should be between 0 and 1 because it represents a percentage of the line vector
        s = (-s1Y * (self.x1 - L2.x1) + s1X * (self.y1 - L2.y1)) / (-s2X * s1Y + s1X * s2Y)
        t = (s2X * (self.y1 - L2.y1) - s2Y * (self.x1 - L2.x1)) / (-s2X * s1Y + s1X * s2Y)

        # if s and t are not both between 0 and 1,
        # then the intersection can not occur between the two segments,
        # so the program returns None
        if 1 < s or s < 0 or 1 < t or t < 0:
            return None

        # this is used to find the actual coordinates of intersection,
        # by multiplying the percentage along the vector by the vector,
        # and adding the original position,
        # this calculates the exact coordinates of intersection for the two line segments
        iX = self.x1 + (t * s1X)
        iY = self.y1 + (t * s1Y)
        pygame.draw.circle(screen, Colours.red, [iX, iY], 10)
        return iX, iY


L1 = Line()
