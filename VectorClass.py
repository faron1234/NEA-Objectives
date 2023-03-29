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
    def limit(self, component):
        if component == "i":
            if vel.i > terminalVel.i > 0:
                self.i = terminalVel.i
            elif vel.i < -terminalVel.i < 0:
                terminalVel.reverse('i')
                self.i = terminalVel.i
                terminalVel.reverse('i')
        elif component == "j":
            self.j = terminalVel.j

    def setVec(self, newI, newJ):
        self.i = newI
        self.j = newJ


gravity = Vector(0, 1)
vel = Vector(0, 0)
posVec = Vector(1000, 400)
acceleration = Vector(0.7, 0)
deceleration = Vector(0.7, 0)
terminalVel = Vector(8, 10)
