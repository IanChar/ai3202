import traceback
from Node import Node
from Node import PriorNode
from PredictiveReasoning import PredictiveReasoning
from DiagnosticReasoning import DiagnosticReasoning
from CombinedReasoning import CombinedReasoning
from IntercausalReasoning import IntercausalReasoning

class BayesNetCalculator(object):
    def __init__(self, net):
        # net is a dictionary of all the nodes
        self.net = net
        self.levels = self.findNumDeps()
        typeFuncs = {'marginal': self.execMarginal,
                'joint': self.execJoint,
                'conditional': self.execConditional}
        self.predictive = PredictiveReasoning(self.net, self.levels, typeFuncs)
        self.diagnostic = DiagnosticReasoning(self.net, self.levels, typeFuncs)
        self.combined = CombinedReasoning(self.net, self.levels, typeFuncs)
        self.intercausal = IntercausalReasoning(self.net, self.levels, typeFuncs)

    # Executes a given command. Commands are expected to be in tuple form.
    # Returns list of tuples where first element is the result and the
    # second element is the command that produced that result.
    def execCommand(self, command):
        if (command[0][1:] == 'g'):
            toReturn = self.loopThroughCapitals(
                    command[1], self.execConditional)
        elif (command[0][1:] == 'j'):
            toReturn = self.loopThroughCapitals(
                    command[1], self.execJoint)
        elif (command[0][1:] == 'm'):
            toReturn = self.execMarginal(command[1])
        elif (command[0][1:] == 'p'):
            toReturn = self.changePrior(command[1])
        else:
            raise Exception("Unknown flag passed in.")
        if not isinstance(toReturn, list):
            toReturn = [toReturn]
        return toReturn

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


    def execConditional(self, args):
        # Seperate the subject from the conditions
        index = 0
        while args[index] != "|" and index < len(args):
            index += 1
        if index == len(args):
            raise Exception("Invalid input, no conditions")
        subject = args[:index]
        conditions = args[index + 1:]

        # Check to see if the subject is the same as the condition
        if subject == conditions:
            return 1

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
                if self.levels[c] <= self.levels[s]:
                    diagnostic = False
                if self.levels[c] >= self.levels[s]:
                    predictive = False
                if self.levels[c] < self.levels[s]:
                    intercausal = False
        if diagnostic:
            return self.diagnostic.compute(subject, conditions)
        elif predictive:
            return self.predictive.compute(subject, conditions)
        elif intercausal:
            return self.intercausal.compute(subject, conditions)
        else:
            return self.combined.compute(subject, conditions)

    def execJoint(self, args):
        # Check if we should use marginal instead
        if len(args) == 1:
            return self.execMarginal(args[0])[0][0]
        argNames = self.getNodes(args)
        # cluster the args based on the level which the occur
        clusteredArgs = []
        seenLevels = []
        for i, aN1 in enumerate(argNames):
            currLevel = self.levels[aN1]
            if currLevel not in seenLevels:
                nodesInLevel = [args[i]]
                for j, aN2 in enumerate(argNames):
                    if i != j  and self.levels[aN2] == currLevel:
                        nodesInLevel.append(args[j])
                seenLevels.append(currLevel)
                clusteredArgs.append((currLevel, nodesInLevel))
        # Check if there is only one level present, then we assume independence
        if len(clusteredArgs) == 1:
            result = 1
            for a in clusteredArgs[0][1]:
                result *= self.execMarginal(a)[0][0]
            return result
        else:
            # Sort clusteredArgs in descending level order
            clusteredArgs.sort()
            clusteredArgs = clusteredArgs[::-1]
            # Make the joint probability into a series of conditionals
            result = 1
            for i in range(len(clusteredArgs)):
                if i == len(clusteredArgs) - 1:
                    result *= self.execJoint(clusteredArgs[i][1])
                else:
                    former = clusteredArgs[i][1]
                    latter = []
                    for j in range(i + 1, len(clusteredArgs)):
                        latter += clusteredArgs[j][1]
                    result *= self.execConditional(former + ["|"] + latter)
            return result

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

    # HELPER FUNCTIONS
    def getFromNet(self, key):
        result = None
        try:
            result = self.net[key]
        except KeyError as err:
            traceback.print_stack()
            print "  Node", err, "not found in net.\n"
        return result


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

    # Strips negates and capitalizes. Makes copy so don't have to worry about
    # a change in the data.
    def getNodes(self, l):
        l = list(l)
        for i, n in enumerate(l):
            if n[:1] == "~":
                l[i] = n[1:]
            l[i] = l[i].upper()
        return l
