from static import Colours
import pygame


class Obstacle:
    def __init__(self, obstacleX, obstacleY, width, height):
        self.obstacleX = obstacleX
        self.obstacleY = obstacleY
        self.width = width
        self.height = height

    def drawObstacle(self, screen):
        pygame.draw.rect(screen, Colours.white, [self.obstacleX-30, self.obstacleY-30, self.width+60, self.height+30])
        pygame.draw.rect(screen, Colours.darkGrey, [self.obstacleX, self.obstacleY, self.width, self.height])
        pygame.draw.line(screen, Colours.black, [self.obstacleX, self.obstacleY], [self.obstacleX, self.obstacleY+self.height], 3)
        pygame.draw.line(screen, Colours.black, [self.obstacleX-30, self.obstacleY-30], [self.obstacleX-30, self.obstacleY + self.height-40], 3)


ob1 = Obstacle(500, 850, 100, 200)
ob2 = Obstacle(900, 750, 100, 300,)
obstacles = [ob1, ob2]