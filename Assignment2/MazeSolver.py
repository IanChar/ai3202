from WorldBuilder import WorldBuilder
from Node import Node
from NodeHeap import NodeHeap

class MazeSolver(object):
    # Prints solution of maze. Does not return anything.
    def solveMaze(self, start, end, world, heuristic):
        if not isinstance(start, tuple):
            raise TypeError("Start position must be of type tuple.")
        if not isinstance(end, tuple):
            raise TypeError("End position must be of type tuple.")
        heap = NodeHeap()
        heap.addOrUpdate(Node(start, 0))
        while not heap.isOpenEmpty():
            minNext = heap.pop()
            if minNext.getPosition() == end:
                self.readSolution(minNext, world)
                return
            else:
                self.addAdjacent(minNext, world, heuristic, heap)
        print "No solution found."

    # Adds all possible nodes adjacent to position
    def addAdjacent(self, node, world, h, heap):
        position = node.getPosition()
        for i in range(position[1] - 1, position[1] + 2):
            if i >= 0 and i < len(world):
                for j in range(position[0] - 1, position[0] + 2):
                    if j >= 0 and j < len(world[0]):
                        curr = world[i][j]
                        if curr != '2':
                            total = 20 if curr == '1' else 10
                            total += node.getDistance()
                            if i != position[1] and j != position[0]:
                                total += 4
                            total += h((j, i), world)
                            heap.addOrUpdate(Node((j, i), total, node))

    def readSolution(self, lastNode, world):
        solutionWorld = [[j for j in i] for i in world]
        print "---------------Log-----------------"
        def printAndPopulate(currNode, world):
            if currNode.getParent() is not None:
                printAndPopulate(currNode.getParent(), world)
            print currNode
            currPosn = currNode.getPosition()
            world[currPosn[1]][currPosn[0]] = 'x'
        printAndPopulate(lastNode, solutionWorld)
        print "---------------Maze-----------------"
        for row in reversed(solutionWorld):
            print " ".join(row)

def manhattanHeuristic(position, world):
    return (len(world[0]) - position[0] - 1) + (len(world) - position[1] - 1)

def readChoices():
    print "\n--------------------------------------------"
    print "1:   Solve world 1 with Manhattan heuristic."
    print "2:   Solve world 1 with custom heuristic."
    print "3:   Solve world 2 with Manhattan heuristic."
    print "4:   Solve world 2 with custom heuristic."
    print "q:   Quit"
    print "--------------------------------------------"

if __name__ == '__main__':
    wb = WorldBuilder()
    ms = MazeSolver()
    world1 = wb.readWorld(1)
    world2 = wb.readWorld(2)
    running = True
    while (running):
        readChoices()
        userInput = str(raw_input('> '))
        if userInput == 'q':
            running = False
        elif userInput == '1':
            ms.solveMaze((0, 0), (9, 7), world1, manhattanHeuristic)
        elif userInput == '2':
            print "2 shall be done"
        elif userInput == '3':
            print "3 shall be done"
        elif userInput == '4':
            print "4 shall be done"
        elif userInput == 't':
            print world1[2][2]
        else:
            print "Invalid input, please make another choice."
