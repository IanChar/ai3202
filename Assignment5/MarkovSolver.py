import Node
import sys
from WorldBuilder import WorldBuilder
GAMMA = 0.9

class MarkovSolver(object):
    def __init__(self, world, epsilon):
        self.world = world
        self.epsilon = epsilon

    def findPolicy(self):
        delta = float("inf")
        while not (delta < self.epsilon * (1 - GAMMA)/GAMMA):
            delta = -1 * float("inf")
            for row in reversed(self.world):
                for n in reversed(row):
                    possibleDelta = self.calculateUtility(n)
                    if possibleDelta > delta:
                        delta = possibleDelta
        self.printOptimalPath()
        self.printWorldInfo()

    # calculates utility at a node and sets the direction and utility
    def calculateUtility(self, node):
        if node.getObstacle() == 2 or node.getObstacle() == 50:
            return
        posn = node.getPosition()
        expectedValues = []
        # Note that top and down utilities switched since world is also switched
        if posn[1] - 1 < 0:
            downUtility = 0
        else:
            downUtility = self.world[posn[1] - 1][posn[0]].getUtility()
        if posn[0] - 1 < 0:
            leftUtility = 0
        else:
            leftUtility = self.world[posn[1]][posn[0] - 1].getUtility()
        if posn[0] + 1 > 9:
            rightUtility = 0
        else:
            rightUtility = self.world[posn[1]][posn[0] + 1].getUtility()
        if posn[1] + 1 > 7:
            topUtility = 0
        else:
            topUtility = self.world[posn[1] + 1][posn[0]].getUtility()
        expectedValues.append(((0.8 * topUtility + 0.1 * leftUtility
                + 0.1 * rightUtility), Node.UP_DIRECTION))
        expectedValues.append(((0.8 * leftUtility + 0.1 * topUtility
                + 0.1 * downUtility), Node.LEFT_DIRECTION))
        expectedValues.append(((0.8 * rightUtility + 0.1 * topUtility
                + 0.1 * downUtility), Node.RIGHT_DIRECTION))
        expectedValues.append(((0.8 * downUtility + 0.1 * leftUtility
                + 0.1 * rightUtility), Node.DOWN_DIRECTION))
        maxExpectation = max(expectedValues)
        tmp = node.getUtility()
        node.setUtility(float(node.getReward() + GAMMA * maxExpectation[0]))
        node.setDirection(maxExpectation[1])
        return abs(tmp - node.getUtility())

    def printWorldInfo(self):
        print "\n---------------------Map Policy---------------------"
        policyMatrix = [[n.getDirection() for n in row]
                for row in reversed(self.world)]
        for row in policyMatrix:
            print " ".join(row)
        print "-------------------Node Utilities-------------------"
        for row in reversed(self.world):
            for n in row:
                print n

    def printOptimalPath(self):
        print "\n---------------------Optimal Path---------------------"
        x = 0
        y = 0
        currNode = self.world[y][x]
        while currNode.getDirection() != '*':
            print currNode
            if currNode.getDirection() == 'U':
                y += 1
            elif currNode.getDirection() == 'D':
                y -= 1
            elif currNode.getDirection() == 'L':
                x -= 1
            if currNode.getDirection() == 'R':
                x += 1
            currNode = self.world[y][x]

if __name__ == '__main__':
    wb = WorldBuilder()
    try:
        w = wb.readWorld(sys.argv[1])
    except:
        w = wb.readWorld("World1MDP.txt")
    try:
        epsilon = float(sys.argv[2])
    except:
        epsilon = 0.5
    ms = MarkovSolver(w, epsilon)
    ms.findPolicy()
