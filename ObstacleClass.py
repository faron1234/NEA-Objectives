from static import Colours
import pygame


class ObstacleSprite(pygame.sprite.Sprite):
    def __init__(self, obstacleX, obstacleY, width, height):
        super().__init__()
        self.obstacleX = obstacleX
        self.obstacleY = obstacleY
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.fill(Colours.white)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = (self.obstacleX+self.width/2, self.obstacleY+self.height/2)

    def drawObstacle(self, screen):
        pygame.draw.rect(screen, Colours.darkGrey, [self.obstacleX+30, self.obstacleY+30, self.width-60, self.height-60])
        pygame.draw.rect(screen, Colours.black, [self.obstacleX, self.obstacleY, self.width, self.height], 3)
        pygame.draw.rect(screen, Colours.black, [self.obstacleX+30, self.obstacleY+30, self.width-60, self.height-60], 3)

        pygame.draw.line(screen, Colours.black, [self.obstacleX+2, self.obstacleY+2], [self.obstacleX+30, self.obstacleY+30], 3)
        pygame.draw.line(screen, Colours.black, [self.obstacleX + self.width-2, self.obstacleY+2], [self.obstacleX + self.width-32, self.obstacleY+32], 3)
        pygame.draw.line(screen, Colours.black, [self.obstacleX+2, self.obstacleY+self.height-2], [self.obstacleX+32, self.obstacleY+self.height-32], 3)
        pygame.draw.line(screen, Colours.black, [self.obstacleX + self.width-2, self.obstacleY+self.height-2], [self.obstacleX + self.width-32, self.obstacleY+self.height-32], 3)
