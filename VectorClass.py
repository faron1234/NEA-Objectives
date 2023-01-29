class Vector:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    # adds two vectors together
    def add(self, vec, component):
        if component == "i":
            self.i += vec.i
        elif component == "j":
            self.j += vec.j

    # takes one vector from another
    def subtract(self, vec, component):
        if component == "i":
            self.i -= vec.i
        elif component == "j":
            self.j -= vec.j

    # scales self with another vector
    def scale(self, vec, component):
        if component == "i":
            self.i *= vec.i
        if component == "j":
            self.j *= vec.j

    # applies an inverse coefficient to the vector
    def reverse(self, component):
        if component == "i":
            self.i *= -1
        elif component == "j":
            self.j *= -1

    # applies a limit to a vector, so it can't increase
    def limit(self, vec, component):
        if component == "i":
            self.i = vec.i
        elif component == "j":
            self.j = vec.j

    def setVec(self, newI, newJ):
        self.i = newI
        self.j = newJ

    def swapVec(self):
        tempI = self.i
        self.i = self.j
        self.j = tempI


gravity = Vector(0, 1)
vel = Vector(0, 0)
posVec = Vector(100, 100)
acceleration = Vector(0.25, 0)
deceleration = Vector(0.9, 0)
terminalVel = Vector(5, 10)
