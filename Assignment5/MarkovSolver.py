import Node
from WorldBuilder import WorldBuilder
GAMMA = 0.9

class MarkovSolver(object):
    def __init__(self, world, epsilon):
        self.world = world
        self.epsilon = epsilon

    def findPolicy(self):
        pass

    # calculates utility at a node and sets the direction and utility
    def calculateUtility(self, node):
        if node.getObstacle() == 2:
            return
        posn = node.getPosition()
        expectedValues = []
        if posn[1] - 1 < 0:
            topUtility = 0
        else:
            topUtility = self.world[posn[1] - 1][posn[0]].getUtility()
        if posn[0] - 1 < 0:
            leftUtility = 0
        else:
            leftUtility = self.world[posn[1]][posn[0] - 1].getUtility()
        if posn[0] + 1 > 9:
            rightUtility = 0
        else:
            rightUtility = self.world[posn[1]][posn[0] + 1].getUtility()
        if posn[1] + 1 > 7:
            downUtility = 0
        else:
            downUtility = self.world[posn[1] + 1][posn[0]].getUtility()
        # go top
        expectedValues.append(((0.8 * topUtility + 0.1 * leftUtility
                + 0.1 * rightUtility), Node.UP_DIRECTION))
        expectedValues.append(((0.8 * leftUtility + 0.1 * topUtility
                + 0.1 * downUtility), Node.LEFT_DIRECTION))
        expectedValues.append(((0.8 * rightUtility + 0.1 * topUtility
                + 0.1 * downUtility), Node.RIGHT_DIRECTION))
        expectedValues.append(((0.8 * downUtility + 0.1 * leftUtility
                + 0.1 * rightUtility), Node.DOWN_DIRECTION))
        maxExpectation = max(expectedValues)
        node.setUtility(int(node.getUtility() + GAMMA * maxExpectation[0]))
        node.setDirection(maxExpectation[1])

    def printSolution(self):
        pass

if __name__ == '__main__':
    wb = WorldBuilder()
    w = wb.readWorld()
    ms = MarkovSolver(w, 0.5)
    ms.calculateUtility(w[1][1])
    print w[1][1]
