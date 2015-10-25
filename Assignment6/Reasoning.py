import traceback
from Node import Node
from Node import PriorNode
'''
Reasoning is an abstract class for the other reasonings that include helper
functions. This class is not meant to be initialized.
'''

NOT_IMPLEMENTED = NotImplementedError("Unable to compute the following request")

class Reasoning(object):
    def __init__(self, net, levels, typeFuncs):
        self.net = net
        self.levels = levels
        # Sets a dictionary of string -> compute functions where the possibilities
        # for keys are "marginal", "joint", and "conditional"
        self.typeFuncs = typeFuncs

    def getFromNet(self, key):
        result = None
        try:
            result = self.net[key]
        except KeyError as err:
            traceback.print_stack()
            print "  Node", err, "not found in net.\n"
        return result

    # Find the chain of nodes linking a child to a parent with BFS
    def findDepChain(self, start, finish):
        curr = start
        visited = [start.getName()]
        if start.getDependencies() is None:
            return None
        Q = [(n, "") for n in start.getDependencies()]
        while len(Q) > 0:
            curr, prev = Q.pop()
            if curr == finish.getName():
                return prev + curr
            if curr not in visited:
                toAdd = self.getFromNet(curr).getDependencies()
                if toAdd is not None:
                    Q += [(n, prev + curr)
                            for n in self.getFromNet(curr).getDependencies()]
                visited.append(curr)
        return None

    # Find the chain of nodes linking a child to a parent with BFS
    def findChildChain(self, start, finish):
        curr = start
        visited = [start.getName()]
        if start.getChildren() is None:
            return None
        Q = [(n, "") for n in start.getChildren()]
        while len(Q) > 0:
            curr, prev = Q.pop()
            if curr == finish.getName():
                return prev + curr
            if curr not in visited:
                toAdd = self.getFromNet(curr).getChildren()
                if toAdd is not None:
                    Q += [(n, prev + curr)
                            for n in self.getFromNet(curr).getChildren()]
                visited.append(curr)
        return None

    # Strips negates and capitalizes. Makes copy so don't have to worry about
    # a change in the data.
    def getNodes(self, l):
        l = list(l)
        for i, n in enumerate(l):
            if n[:1] == "~":
                l[i] = n[1:]
            l[i] = l[i].upper()
        return l

    # Alerts that a command cannot be exectued. Command should be a list of args
    def notImplemented(self, command):
        msg = "P(" + "".join(command) + ")"
        raise NotImplementedError("The logic to compute " + msg
                + " is not available.")
