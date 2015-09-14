class Node(object):
    def __init__(self, x, y, distance, parent):
        self.x = x
        self.y = y
        self.distance = distance
        self.parent = parent

    # Returns a tuple of coordinates
    def getPosition(self):
        return (self.x, self.y)

    def getDistance(self):
        return self.distance

    def getParent(self):
        return self.parent

    def setDistance(self, distance):
        self.distance = distance

    def setParent(self, parent):
        self.parent = parent
