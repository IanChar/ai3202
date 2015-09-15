import heapq
from Node import Node

class NodeHeap(object):
    def __init__(self):
        # Heap of nodes
        self.heapList = []
        # Dict with (x, y) key and node value
        self.openLookup = {}
        # Dict with (x, y) key and node value
        self.closedLookup = {}

    # Will add a new node or update a previous node if the new node has a
    # smaller distance. Returns True if a change was made to the heap.
    def addOrUpdate(self, node):
        nodePosn = node.getPosition()
        if nodePosn in self.closedLookup:
            return False
        nodeDist = node.getDistance()
        if nodePosn in self.openLookup:
            existing = self.openLookup[nodePosn]
            if existing > node:
                existing.setDistance(nodeDist)
                heapq.heapify(self.heapList)
                return True
            return False
        else:
            heapq.heappush(self.heapList, node)
            self.openLookup[nodePosn] = node
            return True

    def pop(self):
        popped = heapq.heappop(self.heapList)
        del self.openLookup[popped.getPosition()]
        self.closedLookup[popped.getPosition()] = popped
        return popped

    def isOpenEmpty(self):
        return len(self.openLookup) == 0

    def __str__(self):
        heapHeader = "-------heap--------"
        openLookup = "-------open--------"
        closedLookup = "-------closed-------"
        final = [heapHeader]
        for n in self.heapList:
            final.append(str(n))
        final.append(openLookup)
        for o in self.openLookup:
            final.append(str(self.openLookup[o]))
        final.append(closedLookup)
        for c in self.closedLookup:
            final.append(str(c))
        return "\n".join(final)

import random
if __name__ == '__main__':
    nh = NodeHeap()
    print "Add a node..."
    nh.addOrUpdate(Node((1,1), 6))
    print nh, "\n"
    print "Update node..."
    nh.addOrUpdate(Node((1,1), 5))
    print nh, "\n"
    print "Pop then try to readd..."
    nh.pop()
    nh.addOrUpdate(Node((1,1), 5))
    print nh, "\n"
    print "Try adding a whole bunch of nodes and see if pops in order..."
    for _ in range(50):
        x = random.randrange(2, 7)
        y = random.randrange(100)
        nh.addOrUpdate(Node((x, x), y))
    while not nh.isOpenEmpty():
        print nh.pop()
