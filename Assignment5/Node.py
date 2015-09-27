UP_DIRECTION = "U"
DOWN_DIRECTION = "D"
LEFT_DIRECTION = "L"
RIGHT_DIRECTION = "R"
NO_DIRECTION = "X"
ARRIVAL = "*"
directions = [UP_DIRECTION, DOWN_DIRECTION, LEFT_DIRECTION,
        RIGHT_DIRECTION, NO_DIRECTION, ARRIVAL]

class Node(object):
    def __init__(self, position, obstacle):
        if not isinstance(position, tuple):
            raise TypeError("Posittion must be of type tuple.")
        self.position = position
        self.obstacle = obstacle
        if obstacle == 0 or obstacle == 2:
            self.reward = 0
        elif obstacle == 1:
            self.reward = -1
        elif obstacle == 3:
            self.reward = -2
        elif obstacle == 4:
            self.reward = 1
        else:
            self.reward = obstacle
        if obstacle == 50:
            self.optimalDirection = ARRIVAL
            self.utility = 50
        else:
            self.optimalDirection = NO_DIRECTION
            self.utility = 0

    # Returns a tuple of coordinates
    def getPosition(self):
        return self.position

    def getObstacle(self):
        return self.obstacle

    def getUtility(self):
        return self.utility

    def setUtility(self, utility):
        self.utility = utility

    def getReward(self):
        return self.reward

    def getDirection(self):
        return self.optimalDirection

    def setDirection(self, direction):
        if direction not in directions:
            raise TypeError("Direction must be a valid direction")
        self.optimalDirection = direction

    def __str__(self):
        if self.optimalDirection == NO_DIRECTION:
            return (str(self.position) + " with utility " + str(self.utility)
                    + " and no direction.")
        return (str(self.position) + " with utility " + str(self.utility)
                + " in direction " + self.optimalDirection)

    def __cmp__(self, other):
        if self.utility is None:
            if other.utility is None:
                return 0
            else:
                return -1
        if other.utility is None:
            return 1
        if self.utility > other.utility:
            return 1
        elif self.utility < other.utility:
            return -1
        return 0

if __name__ == '__main__':
    testNode = Node((1, 2), 4)
    print "Try printing the node..."
    print testNode
    print "Set utility..."
    testNode.setUtility(100)
    print testNode
    print "Set direction..."
    testNode.setDirection(DOWN_DIRECTION)
    print testNode
