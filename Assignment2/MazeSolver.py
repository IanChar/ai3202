from WorldBuilder import WorldBuilder

class MazeSolver(object):

    def solveMaze(self, start, world, heuristic):
        if not instanceof(start, tuple):
            raise TypeError("Start position must be of type tuple.")
        xLimit = len(world[0])
        yLimit = len(world)
        print xLimit, yLimit

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
            print "1 shall be done"
        elif userInput == '2':
            print "2 shall be done"
        elif userInput == '3':
            print "3 shall be done"
        elif userInput == '4':
            print "4 shall be done"
        elif userInput == 't':
            ms.solveMaze((0,0), world1, manhattanHeuristic)
        else:
            print "Invalid input, please make another choice."
