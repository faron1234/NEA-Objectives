from static import Colours
from math import inf, dist
import pygame
from TextClass import Text
import numpy as np


class Node:
    def __init__(self, X, Y, name=None, colour=Colours.black, gCost=inf, hCost=inf, fCost=inf, closestNode=None):
        self.name = name
        self.fCost = fCost
        self.gCost = gCost
        self.hCost = hCost
        self.x = X
        self.y = Y
        self.colour = colour
        self.adjNodes = {}
        self.closestNode = closestNode

    def setFCost(self):
        self.fCost = self.gCost + self.hCost

    # sets H cost to the heuristic distance from the node to the destination
    def setHCost(self, finalNode):
        self.hCost = dist((self.x, self.y), (finalNode.x, finalNode.y))

    def setGCost(self, val):
        self.gCost = val

    # finds the distance between two nodes
    def findDist(self, finalNode):
        return dist((self.x, self.y), (finalNode.x, finalNode.y))

    # draws nodes to the screen and changes their colour to red
    # draws lines between each node and red lines between the nodes in the path
    def drawNode(self, screen, font, Path, last):
        # pygame.draw.circle(screen, self.colour, [self.X, self.Y], 10)
        for adjNode in self.adjNodes:
            if Path.shortestPath and adjNode in Path.shortestPath and self in Path.shortestPath:
                pygame.draw.aaline(screen, Colours.red, [self.x, self.y], [adjNode.x, adjNode.y], 2)
                continue
            pygame.draw.aaline(screen, Colours.black, [self.x, self.y], [adjNode.x, adjNode.y], 2)
        pygame.draw.circle(screen, Colours.red, [self.x, self.y], 5)
        pygame.draw.circle(screen, Colours.blue, [last.x, last.y], 10)
        # writes the name for each node on top
        nameText = Text(font, Colours.red, self.name, self.x, self.y)
        nameText.write(screen)

    # sets the coordinates of a node to a new coordinate
    def setCoord(self, newCoord):
        self.x = newCoord[0]
        self.y = newCoord[1]

    # rests the cost for each node and sets the colour back to black
    # runs every time a new path is created
    def reset(self):
        self.fCost = inf
        self.gCost = inf
        self.hCost = inf
        self.colour = Colours.black

    # used to add an adjacent node
    def addAdj(self, *nodes):
        for item in nodes:
            self.adjNodes.update({item: self.findDist(item)})

    # creates a dictionary of adjacent nodes and adds these to itself
    def findAdj(self, nodes):
        self.adjNodes = {}
        for item in nodes:
            if self.closestNode is None or self.closestNode is nodes[0]:
                self.closestNode = item
            if self.findDist(item) < self.findDist(self.closestNode):
                self.closestNode = item
        self.addAdj(self.closestNode)

    @classmethod
    def dynamicNodes(cls, screenW, screenH):
        nodesMap = []
        tempArray = np.empty(((screenH // 100) + 0, (screenW // 100) + 0), dtype=object)
        previousNode = None
        playerNode = Node(0, 0, "A")
        tempArray[0, 0] = playerNode
        nodesMap.append(playerNode)

        for i in range((screenH // 100) + 0):
            for j in range((screenW // 100) + 0):
                newNode = Node((j * 100) + 0, (i * 100) + 0)
                tempArray[i, j] = newNode
                if previousNode:
                    newNode.addAdj(previousNode)
                    previousNode.addAdj(newNode)

                    # top-left diagonal
                    if i > 0 and j > 0 and tempArray[i - 1, j - 1]:
                        newNode.addAdj(tempArray[i - 1, j - 1])
                    # top-right diagonal
                    if i > 0 and j < tempArray.shape[1] - 1 and tempArray[i - 1, j + 1]:
                        newNode.addAdj(tempArray[i - 1, j + 1])
                    # bottom-left diagonal
                    if i < tempArray.shape[0] - 1 and j > 0 and tempArray[i + 1, j - 1]:
                        newNode.addAdj(tempArray[i + 1, j - 1])
                        # bottom-right diagonal
                    if i < tempArray.shape[0] - 1 and j < tempArray.shape[1] - 1 and tempArray[i + 1, j + 1]:
                        newNode.addAdj(tempArray[i + 1, j + 1])

                previousNode = newNode
            previousNode = None

        for i in range(tempArray.shape[0]):
            for j in range(tempArray.shape[1]):
                if j < tempArray.shape[1] - 1:
                    tempArray[i, j].addAdj(tempArray[i, j + 1])
                if i < tempArray.shape[0] - 1:
                    tempArray[i, j].addAdj(tempArray[i + 1, j])
                nodesMap.append(tempArray[i, j])
        return nodesMap, playerNode


class AStar:
    def __init__(self, nodes, firstNode):
        self.previousNode = None
        self.shortestPath = None
        self.graph = None
        self.shortest = None
        self.firstNode = firstNode
        self.finalNode = None
        self.iteration = 0
        self.nodes = nodes

    def findClosestNode(self):
        self.shortest = None
        for node in self.graph:
            if self.shortest is None:
                self.shortest = node
            elif node.fCost < self.shortest.fCost:
                self.shortest = node

    # finds the path between two given nodes
    def findPath(self, player):
        self.graph = self.nodes.copy()
        self.shortestPath = []
        self.previousNode = {}
        self.finalNode = self.graph[-1]
        self.firstNode.x = player.x
        self.firstNode.y = player.y
        for node in self.graph:
            node.reset()
            node.setHCost(self.finalNode)
            node.setFCost()
        self.firstNode.setGCost(0)
        self.firstNode.findAdj(self.graph)

        while self.finalNode in self.graph:
            self.iteration += 1
            self.findClosestNode()
            for adjNode in self.shortest.adjNodes:
                if adjNode not in self.graph or self.shortest.adjNodes[adjNode] + self.shortest.gCost + adjNode.hCost > adjNode.fCost:
                    continue
                adjNode.gCost = self.shortest.adjNodes[adjNode] + self.shortest.gCost
                adjNode.setFCost()
                self.previousNode.update({adjNode: self.shortest})

            self.graph.remove(self.shortest)
        node = self.finalNode
        self.firstNode.colour = Colours.red
        while node != self.firstNode:
            node.colour = Colours.red
            self.shortestPath.insert(0, node)
            node = self.previousNode[node]
        self.shortestPath.insert(0, self.firstNode)


def createNodes(screenW, screenH):
    nodesMap, playerNode = Node.dynamicNodes(screenW, screenH)
    Path = AStar(nodesMap, playerNode)
    return Path, nodesMap
