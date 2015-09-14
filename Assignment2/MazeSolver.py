from WorldBuilder import WorldBuilder

def readChoices():
    print "\n--------------------------------------------"
    print "1:   Solve world 1 with Manhattan heuristic."
    print "2:   Solve world 1 with other heuristic."
    print "3:   Solve world 2 with Manhattan heuristic."
    print "4:   Solve world 2 with other heuristic."
    print "q: Quit"
    print "--------------------------------------------"

if __name__ == '__main__':
    wb = WorldBuilder()
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
        else:
            print "Invalid input, please make another choice."
