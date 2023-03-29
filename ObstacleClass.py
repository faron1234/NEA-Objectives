from static import Colours
import pygame
import numpy as np


objectSprites, invisibleSprites = pygame.sprite.Group(), pygame.sprite.Group()
collisionObj = []


class ObstacleSprite(pygame.sprite.Sprite):
    def __init__(self, coord, cell, obstacleType, addObjects):
        super().__init__()
        self.width = gameMap.blockSize[0]
        self.height = gameMap.blockSize[1]
        self.x1 = coord[0] - self.width
        self.y1 = coord[1] - self.height
        self.x2 = self.x1 + self.width
        self.y2 = self.y1 + self.height
        self.cell = cell
        self.offsets = []
        self.adjacencyMatrix = np.zeros((3, 3), dtype=int)
        self.adjacencyMatrix[1, 1] = 1
        self.obstacleType = obstacleType
        self.image = pygame.Surface((self.width - 15, self.height - 15))
        if addObjects:
            objectSprites.add(self)
        self.rect = self.image.fill(Colours.white)
        self.rect = pygame.rect.Rect(self.x1 + 15, self.y1 + 15, self.width - 30, self.height - 30)
        self.center = self.rect.center

    @classmethod
    def drawObstacle(cls, objects, screen):
        for obstacle in objects:
            if obstacle.cell[0] == 0 or obstacle.cell[1] == 0 or obstacle.cell[0] == gameMap.height - 1 or obstacle.cell[1] == gameMap.width - 1:
                continue
            adjacencyList = obstacle.adjacencyMatrix.tolist()
            name = "[" + " ".join(["[{} {} {}]".format(row[0], row[1], row[2]) for row in adjacencyList]) + "]"
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
    def __init__(self, blockSize, width, height, draw=True):
        self.blockSize = blockSize
        self.width = width
        self.height = height
        self.grid = np.zeros((self.height, self.width), dtype=int)
        self.grid[0, :] = 1
        self.grid[-1, :] = 1
        self.grid[:, 0] = 1
        self.grid[:, -1] = 1
        self.grid[1, :] = 1
        self.grid[-2, :] = 1
        self.grid[:, 1] = 1
        self.grid[:, -2] = 1
        self.obstacles = []
        self.draw = draw

    def setObstacle(self, obstacleType, *cells):
        for cell in cells:
            x1, y1 = cell[0] * self.blockSize[0], cell[1] * self.blockSize[1]
            if obstacleType >= 1:
                self.obstacles.append(ObstacleSprite((x1, y1), (cell[1], cell[0]), obstacleType, self.draw))
            self.grid[cell[1], cell[0]] = obstacleType

    def createObstacles(self):
        # Create obstacles based on the game map
        for row, col in zip(*self.grid.nonzero()):
            # Create an obstacle at the current cell
            self.setObstacle(1, (col, row))
        for obstacle in self.obstacles:
            obstacle.getNeighbors(self)
        for obstacle in self.obstacles:
            for offset in obstacle.offsets:
                obstacle.adjacencyMatrix[offset[0] + 1, offset[1] + 1] = 1
            corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
            for i, j in corners:
                if i == 0 and j == 0 and (obstacle.adjacencyMatrix[0, 1] + obstacle.adjacencyMatrix[1, 0]) < 2:
                    obstacle.adjacencyMatrix[i, j] = 0
                elif i == 0 and j == 2 and (obstacle.adjacencyMatrix[0, 1] + obstacle.adjacencyMatrix[1, 2]) < 2:
                    obstacle.adjacencyMatrix[i, j] = 0
                elif i == 2 and j == 0 and (obstacle.adjacencyMatrix[1, 0] + obstacle.adjacencyMatrix[2, 1]) < 2:
                    obstacle.adjacencyMatrix[i, j] = 0
                elif i == 2 and j == 2 and (obstacle.adjacencyMatrix[2, 1] + obstacle.adjacencyMatrix[1, 2]) < 2:
                    obstacle.adjacencyMatrix[i, j] = 0


gameMap = Map((101, 108), 21, 12)
gameMap.setObstacle(1, (3, 3), (6, 1), (5, 4), (5, 7), (5, 8), (5, 5), (5, 6), (4, 5), (6, 5), (8, 8))
gameMap.setObstacle(0, (1, 8), (19, 9))
gameMap.createObstacles()
