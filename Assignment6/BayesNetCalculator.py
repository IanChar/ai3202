import getopt
import sys
from Node import Node
from Node import PriorNode

FLAGS = ':g:j:m:p:'

class BayesNetCalculator(object):
    def __init__(self, net):
        # net is a dictionary of all the nodes
        self.net = net
        self.levels = self.findNumDeps()

    # Executes a given command. Commands are expected to be in tuple form.
    # Returns list of tuples where first element is the result and the
    # second element is the command that produced that result.
    def execCommand(self, command):
        if (command[0][1:] == 'g'):
            toReturn = self.loopThroughCapitals(
                    command[1], self.execConditional)
        elif (command[0][1:] == 'j'):
            toReturn = self.loopThroughCapitals(
                    command[1], self.execMarginal)
        elif (command[0][1:] == 'm'):
            toReturn = self.execMarginal(command[1])
        elif (command[0][1:] == 'p'):
            toReturn = self.changePrior(command[1])
        else:
            raise Exception("Unknown flag passed in.")
        if not isinstance(toReturn, list):
            toReturn = [toReturn]
        return toReturn

    def execConditional(self, args):
        # Seperate the subject from the conditions
        index = 0
        while args[index] != "|" and index < len(args):
            index += 1
        if index == len(args):
            raise Exception("Invalid input, no conditions")
        subject = args[:index]
        conditions = args[index + 1:]

        # Check to see what kind of reasoning
        # diagnostic if condition levels > subject level
        diagnostic = True
        # predictive if condition levels < subject level
        predictive = True
        # intercausal if condition levels >= subject level
        intercausal = True
        processedS = self.getNodes(subject)
        processedC = self.getNodes(conditions)
        for s in processedS:
            for c in processedC:
                diagnostic = self.levels[c] > self.levels[s]
                predictive = self.levels[c] < self.levels[s]
                intercausal = self.levels[c] >= self.levels[s]
        if diagnostic:
            return self.diagnosticReasoning(subject, conditions)
        elif predictive:
            return self.predictiveReasoning(subject, conditions)
        elif intercausal:
            return self.intercausalReasoning(subject, conditions)
        else:
            return self.combinedReasoning(subject, conditions)

    def execJoint(self, args):
        pass

    def execMarginal(self, command):
        if command.upper() == command:
            # Case that all options are wanted (capital letter entered)
            toReturn = []
            toReturn += self.execMarginal(command.lower())
            toReturn += self.execMarginal('~' + command.lower())
            return toReturn
        else:
            result = 0
            resultString = "P(" + command + ")"
            negated = command[:1] == "~"
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
                        nestedCommand = "~" if not query[k] else ""
                        nestedCommand += deps[k].lower()
                        resultComponent *= self.execMarginal(nestedCommand)[0][0]
                    result += resultComponent
            if negated:
                result = 1 - result
            return [(result, resultString)]

    def changePrior(self, command):
        toChange = command[:1]
        newVal = float(command[2:])
        try:
            self.net[toChange].setProbability(newVal)
        except KeyError:
            raise Exception("Invalid command given " + command)
        return (newVal, "P(" + toChange + ")")

    def diagnosticReasoning(self, subject, conditions):
        pass

    def predictiveReasoning(self, subject, conditions):
        sNodes = self.getNodes(subject)
        cNodes = self.getNodes(conditions)
        # Can only handle one variable right now
        s = self.net[sNodes[0]]
        deps = s.getDependencies()
        # Categorize the dependencies. These will hold tuples of indices of the
        # dependencies of the subject and the index of the original condition.
        directDependence = []
        indirectDependence = []
        for i in range(len(deps)):
            for cIndex, c in enumerate(cNodes):
                if c == deps[i]:
                    directDependence.append((i, cIndex))

        # For now we only deal with direct dependencies
        result = 0
        unknowns = len(deps) - len(directDependence)
        for i in range(1 << unknowns):
            query = []
            tmp = [1 == ((i >> j) & 1) for j in range(unknowns)]
            # Form a query
            for k in range(len(deps)):
                found = False
                for index, cIndex in directDependence:
                    if k == index:
                        query.append(conditions[cIndex][:1] != "~")
                        found = True
                if not found:
                    query.append(tmp.pop())
            acc = s.getProbability(tuple(query))
            print acc
            # Multiply by marginals
            for index, val in enumerate(deps):
                needsAccounting = True
                for ddIndex, cIndex in directDependence:
                    if index == ddIndex:
                        needsAccounting = False
                if needsAccounting:
                    command = "~" if not query[index] else ""
                    command += deps[index].lower()
                    acc *= self.execMarginal(command)[0][0]
            result += acc
        return result

    def intercausalReasoning(self, subject, conditions):
        pass
    def combinedReasoning(self, subject, conditions):
        pass

    # HELPER FUNCTIONS

    # Performs depth first search to map how far down in the net each node is.
    # Note that if there are multiple paths the highest will be selected.
    def findNumDeps(self):
        deps = {}
        # Nested helper function
        def depHelper(curr, level):
            if curr.getName() in deps.keys():
                if level < deps[curr.getName()]:
                    deps[curr.getName()] = level
            else:
                deps[curr.getName()] = level
            for child in curr.getChildren():
                depHelper(self.net[child], level + 1)

        # Main function logic
        for value in self.net.values():
            if isinstance(value, PriorNode):
                depHelper(value, 0)
        return deps

    def parseArgs(self, command):
        args = []
        i = 0
        for char in command:
            if i == len(args):
                args.append(char)
            else:
                args[i] = args[i] + char
            if char != "~":
                i += 1
        return args

    def loopThroughCapitals(self, command, func, prevArgs = (None, None)):
        toReturn = []
        # Set args and see if there any capital letters
        startPoint = 0
        capitalFound = False
        if prevArgs[0] is not None:
            args = prevArgs[0]
            startPoint = prevArgs[1]
        else:
            args = self.parseArgs(command)
        if startPoint < len(args):
            if args[startPoint] == "|":
                startPoint += 1
            if args[startPoint].upper() == args[startPoint]:
                capitalFound = True
                argCopy = list(args)
                argCopy[startPoint] = argCopy[startPoint].lower()
                toReturn += self.loopThroughCapitals("".join(argCopy), func,
                        (argCopy, startPoint + 1))
                argCopy[startPoint] = "~" + argCopy[startPoint]
                toReturn += self.loopThroughCapitals("".join(argCopy), func,
                        (argCopy, startPoint + 1))

        # Calculate the actual probability
        if not capitalFound:
            toReturn.append((func(args), "P(" + command + ")"))
        return toReturn

    # Strips negates and capitalizes. Makes copy so don't have to worry about
    # a change in the data.
    def getNodes(self, l):
        l = list(l)
        for i, n in enumerate(l):
            if n[:1] == "~":
                l[i] = n[1:]
            l[i] = n.upper()
        return l

# returns dict of nodes in the graph
def buildCancerNetwork():
    nodes = {}
    nodes['P'] = PriorNode('P', 0.9, ['C'])
    nodes['S'] = PriorNode('S', 0.3, ['C'])
    # Note that here high pollution is represented by False
    cancerProbabilities = {(False, True): 0.05,
            (False, False): 0.02,
            (True, True): 0.03,
            (True, False): 0.001}
    nodes['C'] = Node('C', ['P', 'S'], cancerProbabilities, ['X', 'D'])
    xProbabilities = {tuple([True]): 0.9, tuple([False]): 0.2}
    nodes['X'] = Node('X', ['C'], xProbabilities, [])
    dProbabilities = {tuple([True]): 0.65, tuple([False]): 0.3}
    nodes['D'] = Node('D', ['C'], dProbabilities, [])
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
