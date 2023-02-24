from static import Colours
import pygame
from CollisionClass import Line


class ObstacleSprite(pygame.sprite.Sprite):
    def __init__(self, coord, corners, draw=True, objType="rect"):
        super().__init__()
        self.x = coord[0]
        self.y = coord[1]
        self.draw = draw
        self.objType = objType
        if objType == "rect" or objType == "temp":
            self.width = corners[0]
            self.height = corners[1]
            self.image = pygame.Surface((self.width, self.height))
            if not self.draw:
                invisibleSprites.add(self)
            else:
                objectSprites.add(self)
            self.rect = self.image.fill(Colours.white)
            self.rect = self.image.get_rect()
            self.rect.topleft = coord

        if self.objType == "polygon":
            self.width, self.height = corners[0][0], corners[0][1]
            self.width1, self.height1 = corners[2][0], corners[2][1]
            self.x1, self.y1 = self.x + corners[1][0], self.y + corners[1][1]
            ObstacleSprite((self.x, self.y), (self.width, self.height), True, "temp")
            ObstacleSprite((self.x1, self.y1), (self.width1, self.height1), True, "temp")

        obstacles.append(self)

    @classmethod
    def drawObstacle(cls, objects, screen):
        objectSprites.draw(screen)
        for obstacle in objects:
            if not obstacle.draw:
                continue
            if obstacle.objType == "polygon":
                pygame.draw.polygon(screen, Colours.black, [(obstacle.x, obstacle.y),
                                                            (obstacle.x + obstacle.width, obstacle.y),
                                                            (obstacle.x + obstacle.width, obstacle.y + obstacle.height1),
                                                            (obstacle.x1 + obstacle.width1, obstacle.y1),
                                                            (obstacle.x1 + obstacle.width1, obstacle.y + obstacle.height + obstacle.height1),
                                                            (obstacle.x1, obstacle.y + obstacle.height + obstacle.height1),
                                                            (obstacle.x1, obstacle.y1),
                                                            (obstacle.x, obstacle.y1),
                                                            (obstacle.x, obstacle.y)], 2)
            if obstacle.objType == "rect":
                pygame.draw.rect(screen, Colours.darkGrey, [obstacle.x + 30, obstacle.y + 30, obstacle.width - 60, obstacle.height - 60])
                pygame.draw.rect(screen, Colours.black, [obstacle.x, obstacle.y, obstacle.width, obstacle.height], 3)
                pygame.draw.rect(screen, Colours.black, [obstacle.x + 30, obstacle.y + 30, obstacle.width - 60, obstacle.height - 60], 3)
                pygame.draw.line(screen, Colours.black, [obstacle.x + 2, obstacle.y + 2], [obstacle.x + 30, obstacle.y + 30], 3)
                pygame.draw.line(screen, Colours.black, [obstacle.x + obstacle.width - 2, obstacle.y + 2], [obstacle.x + obstacle.width - 32, obstacle.y + 32], 3)
                pygame.draw.line(screen, Colours.black, [obstacle.x + 2, obstacle.y + obstacle.height - 2], [obstacle.x + 32, obstacle.y + obstacle.height - 32], 3)
                pygame.draw.line(screen, Colours.black, [obstacle.x + obstacle.width - 2, obstacle.y + obstacle.height - 2], [obstacle.x + obstacle.width - 32, obstacle.y + obstacle.height - 32], 3)


objectSprites, invisibleSprites = pygame.sprite.Group(), pygame.sprite.Group()
collisionObj, obstacles = [], []


def createObstacles(screenW, screenH, depth):
    ObstacleSprite((500, 450), (200, 300))
    ObstacleSprite((900, 750), (100, 300))
    ObstacleSprite((1000, 1000), (100, 100))
    ObstacleSprite((0, 0), ((400, 200), (200, 200), (200, 200)), True, "polygon")
    ObstacleSprite((900, 0), ((400, 200), (0, 200), (200, 200)), True, "polygon")
    ObstacleSprite((0, -200), (screenW, 200 + depth), False)
    ObstacleSprite((0, 0), (depth, screenH - depth), False)
    ObstacleSprite((screenW - depth, 0), (screenW - depth, screenH - depth), False)
    ObstacleSprite((0, screenH - depth), (screenW, screenH), False)
    for obj in obstacles:
        if obj.objType == "polygon":
            continue
        collisionObj.append(Line(obj.x, obj.y, obj.x + obj.width, obj.y))
        collisionObj.append(Line(obj.x, obj.y, obj.x, obj.y + obj.height))
        collisionObj.append(Line(obj.x, obj.y + obj.height, obj.x + obj.width, obj.y + obj.height))
        collisionObj.append(Line(obj.x + obj.width, obj.y, obj.x + obj.width, obj.y + obj.height))
