import getopt
import sys
from Node import Node
from Node import PriorNode

FLAGS = ':g:j:m:p:'

class BayesNetCalculator(object):
    def __init__(self, net):
        # net is a dictionary of all the nodes
        self.net = net

    # Executes a given command. Commands are expected to be in tuple form.
    # Returns list of tuples where first element is the result and the
    # second element is the command that produced that result.
    def execCommand(self, command):
        if (command[0][1:] == 'g'):
            toReturn = self.execConditional(command[1])
        elif (command[0][1:] == 'j'):
            toReturn = self.execJoint(command[1])
        elif (command[0][1:] == 'm'):
            toReturn = self.execMarginal(command[1])
        elif (command[0][1:] == 'p'):
            toReturn = self.changePrior(command[1])
        else:
            raise Exception("Unknown flag passed in.")
        if not isinstance(toReturn, list):
            toReturn = [toReturn]
        return toReturn

    def execConditional(self, command):
        pass

    def execJoint(self, command):
        pass

    def execMarginal(self, command):
        if command.upper() == command:
            # Case that all options are wanted (capital letter entered)
            toReturn = []
            toReturn.append(self.execMarginal(command.lower()))
            toReturn.append(self.execMarginal('^' + command.lower()))
            return toReturn
        else:
            result = 0
            resultString = "P(" + command + ")"
            negated = command[:1] == "^"
            if negated:
                command = command[1:]
            try:
                node = self.net[command.upper()]
            except KeyError:
                raise Exception("Invalid command given " + command)
            if isinstance(node, PriorNode):
                result = node.getProbability()
            else:
                deps = node.getDependencies()
                # Iterate on possibilites of dependencies
                for i in range(1 << len(deps)):
                    resultComponent = 1
                    # Bit logic magic to generate all combos of queries
                    query = tuple([1 == ((i >> j) & 1)
                            for j in range(len(deps))])
                    resultComponent *= node.getProbability(query)
                    for k in range(len(deps)):
                        nestedCommand = "^" if not query[k] else ""
                        nestedCommand += deps[k].lower()
                        resultComponent *= self.execMarginal(nestedCommand)[0]
                    result += resultComponent
            if negated:
                result = 1 - result
            return (result, resultString)

    def changePrior(self, command):
        toChange = command[:1]
        newVal = float(command[2:])
        try:
            self.net[toChange].setProbability(newVal)
        except KeyError:
            raise Exception("Invalid command given " + command)
        return (newVal, "P(" + toChange + ")")

# returns dict of nodes in the graph
def buildCancerNetwork():
    nodes = {}
    nodes['P'] = PriorNode('P', 0.9)
    nodes['S'] = PriorNode('S', 0.3)
    # Note that here high pollution is represented by False
    cancerProbabilities = {(False, True): 0.05,
            (False, False): 0.02,
            (True, True): 0.03,
            (True, False): 0.001}
    nodes['C'] = Node('C', ['P', 'S'], cancerProbabilities)
    xProbabilities = {tuple([True]): 0.9, tuple([False]): 0.2}
    nodes['X'] = Node('X', ['C'], xProbabilities)
    dProbabilities = {tuple([True]): 0.65, tuple([False]): 0.3}
    nodes['D'] = Node('D', ['C'], dProbabilities)
    return nodes

if __name__ == '__main__':
    parsed = True
    try:
        optlist, args = getopt.getopt(sys.argv[1:], FLAGS)
    except getopt.GetoptError as err:
        print err
        parsed = False

    if parsed:
        bn = BayesNetCalculator(buildCancerNetwork())
        for command in optlist:
            try:
                for ans, question in bn.execCommand(command):
                    print question + " = " + str(ans)
            except KeyError as err:
                print err
