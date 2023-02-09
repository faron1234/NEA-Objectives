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
        Draw(Colours.white, "rect", [[30, 30], [screenW - 30 * 2, screenH - 30 * 2]], 40),
        Draw(Colours.darkGrey, "rect", [[0, 0], [screenW, screenH]], 30),
        Draw(Colours.darkGrey, "rect", [[70, 70], [screenW - 70 * 2, screenH - 70 * 2]]),

        # draw borderlines
        Draw(Colours.black, "rect", [[30, 30], [screenW - 30 * 2, screenH - 30 * 2]], 3),
        Draw(Colours.black, "rect", [[70, 70], [screenW - 70 * 2, screenH - 70 * 2]], 3),

        # draw diagonal lines
        Draw(Colours.black, "line", [[32, 32], [72, 72]], 5),
        Draw(Colours.black, "line", [[32, screenH - 32], [72, screenH - 72]], 5),
        Draw(Colours.black, "line", [[screenW - 32, 32], [screenW - 72, 72]], 5),
        Draw(Colours.black, "line", [[screenW - 32, screenH - 32], [screenW - 72, screenH - 72]], 5),

        # left door
        Draw(Colours.black, "line", [[35, screenH - 35], [35, screenH - 130]], 3),
        Draw(Colours.black, "line", [[35, screenH - 130], [66, screenH - 161]], 4),
        Draw(Colours.black, "line", [[67, screenH - 67], [67, screenH - 162]], 3),

        # right door
        Draw(Colours.black, "line", [[screenW - 36, screenH - 131], [screenW - 36, screenH - 35]], 3),
        Draw(Colours.black, "line", [[screenW - 67, screenH - 162], [screenW - 37, screenH - 132]], 4),
        Draw(Colours.black, "line", [[screenW - 67, screenH - 162], [screenW - 67, screenH - 67]], 3),

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
