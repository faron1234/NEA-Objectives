from static import Colours
import pygame
from CollisionClass import Line


class ObstacleSprite(pygame.sprite.Sprite):
    def __init__(self, objType, coord, corners, draw=True):
        super().__init__()
        self.type = objType
        self.x = coord[0]
        self.y = coord[1]
        self.corners = corners
        self.draw = draw
        if self.type == "polygon":
            self.image = pygame.Surface((200, 150), pygame.SRCALPHA, 32)
            self.mask = pygame.mask.from_surface(self.image)
        elif self.type == "rect":
            self.width = corners[0]
            self.height = corners[1]
            self.image = pygame.Surface((self.width, self.height))
            self.rect = self.image.fill(Colours.white)
        self.rect = self.image.get_rect()
        self.rect.topleft = coord

    @classmethod
    def drawObstacle(cls, objects, screen):
        for obstacle in objects:
            if not obstacle.draw:
                return
            if obstacle.type == "rect":
                pygame.draw.rect(screen, Colours.darkGrey, [obstacle.x + 30, obstacle.y + 30, obstacle.width - 60, obstacle.height - 60])
                pygame.draw.rect(screen, Colours.black, [obstacle.x, obstacle.y, obstacle.width, obstacle.height], 3)
                pygame.draw.rect(screen, Colours.black, [obstacle.x + 30, obstacle.y + 30, obstacle.width - 60, obstacle.height - 60], 3)

                pygame.draw.line(screen, Colours.black, [obstacle.x + 2, obstacle.y + 2], [obstacle.x + 30, obstacle.y + 30], 3)
                pygame.draw.line(screen, Colours.black, [obstacle.x + obstacle.width - 2, obstacle.y + 2], [obstacle.x + obstacle.width - 32, obstacle.y + 32], 3)
                pygame.draw.line(screen, Colours.black, [obstacle.x + 2, obstacle.y + obstacle.height - 2], [obstacle.x + 32, obstacle.y + obstacle.height - 32], 3)
                pygame.draw.line(screen, Colours.black, [obstacle.x + obstacle.width - 2, obstacle.y + obstacle.height - 2], [obstacle.x + obstacle.width - 32, obstacle.y + obstacle.height - 32], 3)
            elif obstacle.type == "polygon":
                pygame.draw.polygon(screen, Colours.white, obstacle.corners)


objectSprites = pygame.sprite.Group()
collisionObj, obstacles = [], []


def createObstacles(screenW, screenH, depth):
    ob1 = ObstacleSprite("rect", (500, 450), (200, 300))
    ob2 = ObstacleSprite("rect", (900, 750), (100, 300))
    ob3 = ObstacleSprite("rect", (1000, 1000), (100, 100))
    ob4 = ObstacleSprite("polygon", (500, 500), ((200, 100), (400, 100), (400, 250), (300, 250), (300, 200), (200, 200), (200, 100)))
    roof = ObstacleSprite("rect", (0, 0), (screenW, depth), False)
    wall1 = ObstacleSprite("rect", (0, 0), (depth, screenH - depth), False)
    ground = ObstacleSprite("rect", (screenW - depth, 0), (screenW - depth, screenH - depth), False)
    wall2 = ObstacleSprite("rect", (0, screenH - depth), (screenW, screenH), False)
    obstacles.extend([ob1, ob2, ob3, ob4, roof, wall1, ground, wall2])
    for obj in obstacles:
        if obj.type == "polygon":
            corners = obj.corners
            for index in range(len(corners)-1):
                collisionObj.append(Line(corners[index][0], corners[index][1], corners[index+1][0], corners[index+1][1]))
        if obj.type == "rect":
            collisionObj.append(Line(obj.x, obj.y, obj.x + obj.width, obj.y))
            collisionObj.append(Line(obj.x, obj.y, obj.x, obj.y + obj.height))
            collisionObj.append(Line(obj.x, obj.y + obj.height, obj.x + obj.width, obj.y + obj.height))
            collisionObj.append(Line(obj.x + obj.width, obj.y, obj.x + obj.width, obj.y + obj.height))
        objectSprites.add(obj)
