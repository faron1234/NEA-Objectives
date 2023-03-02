import static
from static import Colours
import pygame
from CollisionClass import Line
import numpy as np


objectSprites, invisibleSprites = pygame.sprite.Group(), pygame.sprite.Group()
collisionObj = []


class ObstacleSprite(pygame.sprite.Sprite):
    def __init__(self, coord, cell, obstacleType):
        super().__init__()
        self.x1 = coord[0]
        self.y1 = coord[1]
        self.width = gameMap.blockSize[0]
        self.height = gameMap.blockSize[1]
        self.x2 = self.x1 + self.width
        self.y2 = self.y1 + self.height
        self.cell = cell
        self.offsets = []
        self.adjacencyMatrix = np.zeros((3, 3), dtype=int)
        self.adjacencyMatrix[1, 1] = 1
        self.obstacleType = obstacleType
        self.image = pygame.Surface((self.width, self.height))
        objectSprites.add(self)
        self.rect = self.image.fill(Colours.white)
        self.rect = pygame.rect.Rect(self.x1, self.y1, self.width, self.height)
        self.center = self.rect.center

    @classmethod
    def createLines(cls, objects):
        for obstacle in objects:
            left, right, up, down = 0, 0, 0, 0
            if (-1, 0) in obstacle.offsets:
                up = 30
            if (0, -1) in obstacle.offsets:
                left = 30
            if (0, 1) in obstacle.offsets:
                right = 30
            if (1, 0) in obstacle.offsets:
                down = 30
            if not up:
                collisionObj.append(Line(obstacle.x1 + 15 - left, obstacle.y1 + 15, obstacle.x2 - 15 + right, obstacle.y1 + 15, 1))
            if not left:
                collisionObj.append(Line(obstacle.x1 + 15, obstacle.y1 + 15 - up, obstacle.x1 + 15, obstacle.y2 - 15 + down, 4))
            if not down:
                collisionObj.append(Line(obstacle.x1 + 15 - left, obstacle.y2 - 15, obstacle.x2 - 15 + right, obstacle.y2 - 15, 3))
            if not right:
                collisionObj.append(Line(obstacle.x2 - 15, obstacle.y1 + 15 - up, obstacle.x2 - 15, obstacle.y2 - 15 + down, 2))

    @classmethod
    def drawObstacle(cls, objects, screen):
        objectSprites.draw(screen)
        for obstacle in objects:
            adjacencyList = obstacle.adjacencyMatrix.tolist()
            name = "["
            for row in adjacencyList:
                name += "[{} {} {}] ".format(row[0], row[1], row[2])
            name = name[:-1] + "]"
            image = pygame.image.load(f'ObstacleImages/{name}.xcf')
            screen.blit(image, (obstacle.x1, obstacle.y1))

    def getNeighbors(self, gameGrid):
        # calculate what neighbors each cell has
        offsets = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if (i, j) != (0, 0)]
        for offset in offsets:
            row = self.cell[0] + offset[0]
            col = self.cell[1] + offset[1]
            if 0 <= row < gameGrid.height and 0 <= col < gameGrid.width and gameGrid.grid[row, col] == 1:
                self.offsets.append(offset)


class Map:
    def __init__(self, blockSize, width, height):
        self.blockSize = blockSize
        self.width = width
        self.height = height
        self.grid = np.zeros((self.height, self.width), dtype=int)
        self.grid[0, :] = 1
        self.grid[-1, :] = 1
        self.grid[:, 0] = 1
        self.grid[:, -1] = 1
        self.obstacles = []

    def addObstacle(self, obstacleType, *cells):
        for cell in cells:
            x1, y1 = cell[0] * self.blockSize[0], cell[1] * self.blockSize[1]
            self.obstacles.append(ObstacleSprite((x1, y1), (cell[1], cell[0]), obstacleType))
            self.grid[cell[1], cell[0]] = obstacleType

    def createObstacles(self):
        # Create obstacles based on the game map
        for row, col in zip(*self.grid.nonzero()):
            # Create an obstacle at the current cell
            self.addObstacle(1, (col, row))
        for obstacle in self.obstacles:
            obstacle.getNeighbors(self)
        for obstacle in self.obstacles:
            for offset in obstacle.offsets:
                obstacle.adjacencyMatrix[offset[0] + 1, offset[1] + 1] = 1


gameMap = Map((101, 108), 19, 10)
gameMap.addObstacle(1, (3, 3), (6, 1), (5, 4), (5, 5), (5, 6), (4, 5), (6, 5))
gameMap.grid[5, 0] = 0
gameMap.grid[8, 0] = 0
gameMap.createObstacles()

ObstacleSprite.createLines(gameMap.obstacles)
