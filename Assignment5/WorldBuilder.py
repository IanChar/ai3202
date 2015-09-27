import Node

class WorldBuilder(object):
    # Returns a matrix representing world 1
    def readWorld(self):
        world = []
        f = open('World1MDP.txt', 'r').readlines()
        # Reverse to match normal coordinates
        for line in reversed(f):
            world.append(line.split(" "))
        world = world[1:]
        nodes = []
        for i in range(len(world)):
            nodes.append([])
            for j in range(len(world[0])):
                nodes[i].append(Node.Node((j, i), int(world[i][j])))
        # Take out new line characters
        return nodes

if __name__ == '__main__':
    wb = WorldBuilder()
    print "-------Read in World-------"
    print wb.readWorld()[7][9]
    for row in wb.readWorld():
        print ""
        for n in row:
            print n.getUtility(),
