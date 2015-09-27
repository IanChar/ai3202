UP_DIRECTION = "U"
DOWN_DIRECTION = "D"
LEFT_DIRECTION = "L"
RIGHT_DIRECTION = "R"
directions = [UP_DIRECTION, DOWN_DIRECTION, LEFT_DIRECTION, RIGHT_DIRECTION]

class Node(object):
    def __init__(self, position, obstacle):
        if not isinstance(position, tuple):
            raise TypeError("Posittion must be of type tuple.")
        self.position = position
        self.obstacle = obstacle
        if obstacle == 0 or obstacle == 2:
            self.utility = 0
        elif obstacle == 1:
            self.utility = -1
        elif obstacle == 3:
            self.utility = -2
        elif obstacle == 4:
            self.utility = 1
        else:
            self.utility = obstacle
        self.optimalDirection = None

    # Returns a tuple of coordinates
    def getPosition(self):
        return self.position

    def getObstacle(self):
        return self.obstacle

    def getUtility(self):
        return self.utility

    def setUtility(self, utility):
        if not isinstance(utility, int):
            raise TypeError("Utility must be of type int.")
        self.utiltiy = utility

    def getDirection(self):
        return self.optimalDirection

    def setDirection(self, direction):
        if direction not in directions:
            raise TypeError("Direction must be a valid direction")
        self.optimalDirection = direction

    def __str__(self):
        if self.optimalDirection is None:
            return (str(self.position) + " with utility " + str(self.utility)
                    + " and no direction.")
        return (str(self.position) + " with utility " + str(self.utility)
                + " in direction " + self.optimalDirection)

    def __cmp__(self, other):
        if self.optimal is None:
            if other.optimal is None:
                return 0
            else:
                return -1
        if other.optimal is None:
            return 1
        if self.optimal > other.optimal:
            return 1
        elif self.optimal < other.optimal:
            return -1
        return 0

if __name__ == '__main__':
    testNode = Node((1, 2), 0)
    print "Try printing the node..."
    print testNode
    print "Set utility..."
    testNode.setUtility(100)
    print testNode
    print "Set direction..."
    testNode.setDirection(DOWN_DIRECTION)
    print testNode