from static import Colours
import pygame


def Intersection(lines, screen):
    s1X = lines[0][2] - lines[0][0]
    s1Y = lines[0][3] - lines[0][1]
    s2X = lines[1][2] - lines[1][0]
    s2Y = lines[1][3] - lines[1][1]

    if -s2X * s1Y + s1X * s2Y != 0:

        s = (-s1Y * (lines[0][0] - lines[1][0]) + s1X * (lines[0][1] - lines[1][1])) / (-s2X * s1Y + s1X * s2Y)
        t = (s2X * (lines[0][1] - lines[1][1]) - s2Y * (lines[0][0] - lines[1][0])) / (-s2X * s1Y + s1X * s2Y)

        if 0 <= s <= 1 and 0 <= t <= 1:
            iX = lines[0][0] + (t * s1X)
            iY = lines[0][1] + (t * s1Y)
            pygame.draw.circle(screen, Colours.red, [iX, iY], 10)
            return iX, iY
        else:
            return None

    else:
        return None