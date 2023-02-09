class Text:
    def __init__(self, font, colour, name, x, y):
        self.name = name
        self.text = font.render(self.name, True, colour)
        self.colour = colour
        self.x = x
        self.y = y
        self.width = self.text.get_width()
        self.height = self.text.get_height()

    # renders the text then draws text to the screen
    def write(self, screen):
        screen.blit(self.text, (self.x, self.y))

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
