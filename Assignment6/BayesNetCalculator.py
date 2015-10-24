import getopt
import sys
import traceback
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

        # Check to see if there is no dependence between subject and condition
        isIndependent = True
        for s in self.getNodes(subject):
            if not isinstance(self.getFromNet(s.upper()), PriorNode):
                isIndependent = False
        for c in self.getNodes(conditions):
            if not isinstance(self.getFromNet(c.upper()), PriorNode):
                isIndependent = False
        if isIndependent:
            if len(subject) == 1:
                return self.execMarginal(subject[0])[0][0]
            else:
                return self.execJoint(subject)

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
                node = self.getFromNet(command.upper())
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
            self.getFromNet(toChange).setProbability(newVal)
        except KeyError:
            raise Exception("Invalid command given " + command)
        return (newVal, "P(" + toChange + ")")

    def diagnosticReasoning(self, subject, conditions):
        raise NotImplementedError("Logic required to compute this has"
                + " not yet been implemented.")

    def predictiveReasoning(self, subject, conditions):
        sNodes = self.getNodes(subject)
        cNodes = self.getNodes(conditions)
        # Can only handle one variable right now
        if len(sNodes) == 1:
            s = self.getFromNet(sNodes[0])
            subjDeps = s.getDependencies()
            # Find the dependencies where they are a string of the path to the
            # given node.
            depChains = [self.findDepChain(s, self.getFromNet(c))
                    for c in cNodes]

            # Check if directly dpenedent
            directlyDependent = True
            for dC in depChains:
                if len(dC) > 1:
                    directlyDependent = False
            if directlyDependent:
                result = self.directPredictive(s, conditions, subjDeps,
                        depChains)
                if subject[0][:1] == "~":
                    result = 1 - result
                return result
            else:
                # Case where not directly dependent
                raise NotImplementedError("Logic required to compute this has"
                        + " not yet been implemented.")
        else:
            # Case where there are multiple subjects
            raise NotImplementedError("Logic required to compute this has not"
                    + " yet been implemented.")

    # Case where all conditions have some direct dependence to the subject.
    # subject is a node of the single subject, conditions is a list of the
    # names of the conditions, subjDeps is the names of s's direct dependents,
    # and depChains is the chain to get from the subject to each condition.
    def directPredictive(self, subject, conditions, subjDeps, depChains):
        result = 0
        unknowns = len(subjDeps) - len(depChains)
        for i in range(1 << unknowns):
            # Construct the query
            query = []
            # tmp array that holds possibilities of unlisted dependents
            tmp = [1 == ((i >> j) & 1) for j in range(unknowns)]
            # Figure out which to elements of tmp to insert in query
            for sD in subjDeps:
                found = False
                for dCIndex, dC in enumerate(depChains):
                    if dC == sD:
                        # This all assumes that depChains keeps the
                        # same order as condtions
                        query.append(conditions[dCIndex][:1] != "~")
                        found = True
                if not found:
                    query.append(tmp.pop())
            acc = subject.getProbability(tuple(query))
            # Multiply by marginals
            for index, val in enumerate(subjDeps):
                needsAccounting = True
                for dC in depChains:
                    if val == dC:
                        needsAccounting = False
                if needsAccounting:
                    command = "~" if not query[index] else ""
                    command += subjDeps[index].lower()
                    acc *= self.execMarginal(command)[0][0]
            result += acc
        return result

    def intercausalReasoning(self, subject, conditions):
        raise NotImplementedError("Logic required to compute this has"
                + " not yet been implemented.")
    def combinedReasoning(self, subject, conditions):
        raise NotImplementedError("Logic required to compute this has"
                + " not yet been implemented.")

    # HELPER FUNCTIONS

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
                depHelper(self.getFromNet(child), level + 1)

        # Main function logic
        for value in self.net.values():
            if isinstance(value, PriorNode):
                depHelper(value, 0)
        return deps

    # Return an array of events for a given string
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
        while startPoint < len(args) and not capitalFound:
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
            startPoint += 1

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
            l[i] = l[i].upper()
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
        cancerNet = buildCancerNetwork()
        bn = BayesNetCalculator(cancerNet)
        for command in optlist:
            try:
                for ans, question in bn.execCommand(command):
                    print question + " = " + str(ans)
            except KeyError as err:
                print err
