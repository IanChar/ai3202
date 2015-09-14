class WorldBuilder(object):

    # Returns a matrix representing world 1
    def readWorld(self, worldNumber):
        world = []
        f = open('World' + str(worldNumber) + '.txt', 'r')
        for line in f:
            world.append(line.split(" "))
        # Take out new line characters
        for row in world:
            row[-1] = row[-1][:1]
        return world[:(len(world) - 1)]

if __name__ == '__main__':
    wb = WorldBuilder()
    print "-------Read in Wold 1-------"
    print wb.readWorld(1)
    print "\n-------Read in Wold 2-------"
    print wb.readWorld(2)
