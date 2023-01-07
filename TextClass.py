class Text:
    def __init__(self, font, name=None, x=None, y=None):
        self.name = name
        self.x = x
        self.y = y
        self.font = font

    # renders the text then draws text to the screen
    def write(self, screen, col):
        text = self.font.render(self.name, True, col)
        screen.blit(text, (self.x, self.y))

    # updates what the text says
    def updateText(self, text):
        self.name = str(text)

    # adds string to the end of the text
    def addText(self, text):
        self.name += text

    # removes text from the end
    def deleteText(self):
        self.name = self.name[:-1]

    # updates the position of the text
    def updatePos(self, x, y):
        self.x = x
        self.y = y
