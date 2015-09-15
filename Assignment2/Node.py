class Node(object):
    def __init__(self, position, distance = None, parent = None):
        if not isinstance(position, tuple):
            raise TypeError("Posittion must be of type tuple.")
        if distance is not None and not isinstance(distance, int):
            raise TypeError("Distance must be of type int.")
        if parent is not None and not isinstance(parent, Node):
            raise TypeError("Parent must be of type Node.")
        self.position = position
        self.distance = distance
        self.parent = parent

    # Returns a tuple of coordinates
    def getPosition(self):
        return self.position

    def getDistance(self):
        return self.distance

    def getParent(self):
        return self.parent

    def setDistance(self, distance):
        self.distance = distance

    def setParent(self, parent):
        if not isinstance(parent, Node):
            raise TypeError("Parent must be of type Node.")
        self.parent = parent

    def __str__(self):
        return (str(self.position) + " with cost " + str(self.distance))

    def __cmp__(self, other):
        if self.distance is None:
            if other.distance is None:
                return 0
            else:
                return -1
        if other.distance is None:
            return 1
        if self.distance > other.distance:
            return 1
        elif self.distance < other.distance:
            return -1
        return 0

if __name__ == '__main__':
    testNode = Node((1, 2))
    print "Try printing the node..."
    print testNode
    print "Try printing the node's parent..."
    print testNode.getParent()
    print "Set distance and parent and repeat..."
    testNode.setDistance(100)
    testNode.setParent(Node((1,1)))
    print testNode
    print testNode.getParent()
