from static import Colours
from math import inf, dist
import pygame
from TextClass import Text


class Node:
    def __init__(self, X, Y, name=None, colour=Colours.black, gCost=inf, hCost=inf, fCost=inf, closestNode=None):
        self.name = name
        self.fCost = fCost
        self.gCost = gCost
        self.hCost = hCost
        self.X = X
        self.Y = Y
        self.colour = colour
        self.adjNodes = {}
        self.closestNode = closestNode

    def setFCost(self):
        self.fCost = self.gCost + self.hCost

    # sets H cost to the heuristic distance from the node to the destination
    def setHCost(self, finalNode):
        self.hCost = dist((self.X, self.Y), (finalNode.X, finalNode.Y))

    def setGCost(self, val):
        self.gCost = val

    # finds the distance between two nodes
    def findDist(self, finalNode):
        return dist((self.X, self.Y), (finalNode.X, finalNode.Y))

    # draws nodes to the screen and changes their colour to red
    # draws lines between each node and red lines between the nodes in the path
    def drawNode(self, screen, font, Path):
        # pygame.draw.circle(screen, self.colour, [self.X, self.Y], 10)
        for adjNode in self.adjNodes:
            if Path.shortestPath and adjNode in Path.shortestPath and self in Path.shortestPath:
                pygame.draw.aaline(screen, Colours.red, [self.X, self.Y], [adjNode.X, adjNode.Y], 2)
                continue
            pygame.draw.aaline(screen, Colours.black, [self.X, self.Y], [adjNode.X, adjNode.Y], 2)

        # writes the name for each node on top
        nameText = Text(font, Colours.red, self.name, self.X, self.Y)
        nameText.write(screen)

    # sets the coordinates of a node to a new coordinate
    def setCoord(self, newCoord):
        self.X = newCoord[0]
        self.Y = newCoord[1]

    # rests the cost for each node and sets the colour back to black
    # runs every time a new path is created
    def reset(self):
        self.fCost = inf
        self.gCost = inf
        self.hCost = inf
        self.colour = Colours.black

    # used to add an adjacent node
    def addAdj(self, nodes):
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
        self.addAdj((self.closestNode,))
        print(self.adjNodes)

    @classmethod
    def dynamicNodes(cls, screenW, screenH):
        # nodesMap = []
        # previousNode = None
        # for xPixel in range(screenW):
        #     if xPixel % 500 != 0:
        #         continue
        #     for yPixel in range(screenH):
        #         if yPixel % 500 != 0:
        #             continue
        #         newNode = Node(xPixel, yPixel)
        #         nodesMap.append(newNode)
        #         if previousNode:
        #             newNode.addAdj((previousNode,))
        #         previousNode = newNode
        return nodesMap


class AStar:
    def __init__(self, nodes, firstNode, finalNode, iteration):
        self.previousNode = None
        self.shortestPath = None
        self.graph = None
        self.shortest = None
        self.firstNode = firstNode
        self.finalNode = finalNode
        self.iteration = iteration
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
        self.shortestPath = []
        self.previousNode = {}
        self.firstNode.X = player.x
        self.firstNode.Y = player.y
        self.graph = self.nodes.copy()
        for node in self.graph:
            node.reset()
            node.setHCost(self.finalNode)
            node.setFCost()
        self.firstNode.setGCost(0)
        self.firstNode.findAdj(self.graph)
        print(self.nodes, self.firstNode)

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

#
# A = Node(50*3, 150*3, "A")
# B = Node(150*3, 75*3, "B")
# C = Node(150*3, 225*3, "C")
# D = Node(250*3, 75*3, "D")
# E = Node(250*3, 225*3, "E")
# F = Node(350*3, 150*3, "F")
# G = Node(340*3, 275*3, "G")
#
# nodesMap = [A, B, C, D, E, F, G]
#
# A.addAdj(nodesMap)
# B.addAdj((C, D))
# C.addAdj((B, E))
# D.addAdj((E, F))
# E.addAdj((C, D, F, G))
# F.addAdj((D, E, G))
# G.addAdj((F,))
#
# Path = AStar(nodesMap, A, G, 0)


def createNodes(screenW, screenH):
    # nodesMap = Node.dynamicNodes(screenW, screenH)
    A = Node(0, 0, "A")
    B = Node(150*3, 75*3, "B")
    C = Node(150*3, 225*3, "C")
    D = Node(250*3, 75*3, "D")
    E = Node(250*3, 225*3, "E")
    F = Node(350*3, 150*3, "F")
    G = Node(340*3, 275*3, "G")

    nodesMap = [A, B, C, D, E, F, G]

    A.addAdj(nodesMap)
    B.addAdj((C, D))
    C.addAdj((B, E))
    D.addAdj((E, F))
    E.addAdj((C, D, F, G))
    F.addAdj((D, E, G))
    G.addAdj((F,))
    Path = AStar(nodesMap, A, nodesMap[-1], 0)
    return Path, nodesMap
