from static import Colours
import pygame


class Map:
    def __init__(self):
        self.lines = {}

    # add objects to self.lines
    def addObj(self, *objs):
        for iteration, obj in enumerate(objs):
            if obj.name is None:
                obj.name = iteration
            self.lines[obj.name] = obj

    # draw all shapes in self.lines
    def drawMap(self, screen):
        for shape in self.lines:
            self.lines[shape].draw(screen)


class Draw:
    def __init__(self, colour, objType, coord, thickness=0, name=None):
        self.colour = colour
        self.coord = coord
        self.objType = objType
        self.thickness = thickness
        self.drawing = None
        self.name = name
        self.doDraw = True

    # create drawing for types of object
    def draw(self, screen):
        if not self.doDraw:
            return
        if self.objType == "line":
            self.drawing = pygame.draw.line(screen, self.colour, [self.coord[0][0], self.coord[0][1]],
                                            [self.coord[1][0], self.coord[1][1]],
                                            self.thickness)
        if self.objType == "rect":
            self.drawing = pygame.draw.rect(screen, self.colour,
                                            [self.coord[0][0], self.coord[0][1], self.coord[1][0], self.coord[1][1]], self.thickness)


def createBackground(screenW, screenH):
    # add all drawings for background screen
    backgroundDrawing.addObj(
        # fill in background colours
        Draw(Colours.darkGrey, "rect", [[0, 0], [screenW, screenH]]),
        # x button
        Draw(Colours.red, "line", [[screenW, 0], [screenW - 20, 20]], 2),
        Draw(Colours.red, "line", [[screenW - 20, 0], [screenW, 20]], 2),
        Draw(Colours.black, "rect", [[screenW - 25, 0], [25, 25]], 2, "xButton"),

        # start button
        Draw(Colours.black, "rect", ([100, screenH/2], [400, 100]), 2, "startButton"),
        # scores button
        Draw(Colours.black, "rect", ([screenW-500, screenH / 2], [400, 100]), 2, "scoresButton"),
    )


backgroundDrawing = Map()
