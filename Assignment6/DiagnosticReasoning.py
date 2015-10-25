import traceback
from Node import Node
from Node import PriorNode
from Reasoning import Reasoning

class DiagnosticReasoning(Reasoning):
    def __init__(self, net, levels, typeFuncs):
        super(DiagnosticReasoning, self).__init__(net, levels, typeFuncs)

    def compute(self, subject, conditions):
        sNodes = self.getNodes(subject)
        cNodes = self.getNodes(conditions)
        # Can only handle one variable right now
        if len(sNodes) == 1:
            s = self.getFromNet(sNodes[0])
            # Find the dependencies where they are a string of the path to the
            # given node.
            childChains = [self.findChildChain(s, self.getFromNet(c))
                    for c in cNodes]

            # Check if one path is a substring of the other so the problem
            # can be simplified.
            indicesToRemove = []
            for i, cC1 in enumerate(childChains):
                for j, cC2 in enumerate(childChains):
                    if i != j and (cC1 == cC2 or cC1 == cC2[:-1]):
                        indicesToRemove.append(j)
            # Remove redundent dependencies and start over
            if len(indicesToRemove) > 0:
                # Make sure to sort list and but in reverse order so that
                # removal of elements isn't a problem. This also works because
                # we assume conditions and childChains match up
                indicesToRemove.sort()
                for i in indicesToRemove[::-1]:
                    childChains.pop(i)
                    conditions.pop(i)
                return self.compute(
                        [s.getName().lower()], conditions)

            # Performs Bayes Theorem
            result = self.bayes(s, conditions, childChains)
            if subject[0][:1] == "~":
                result = 1 - result
            return result
        else:
            # Case where there are multiple subjects
            self.notImplemented(subject + ["|"] + conditions)

    def bayes(self, subject, conditions, childChains):
        # Check if the problem can be computed given current implementation
        # we can compute with Bayes if only one condition or if the path
        # the the dependent is the same up to the last node.
        canCompute = len(conditions) == 1
        if not canCompute:
            canCompute = True
            for i, cC1 in enumerate(childChains):
                for j, cC2 in enumerate(childChains):
                    if i != j and cC1[:-1] != cC2[:-1]:
                        canCompute = False
                        break
        if canCompute:
            result = 0
            # Get the reverse of the chain minus the last character
            mainChain = childChains[0][-2::-1]
            # Loop over possibilities that path to condition can take
            for iterNum in range(1 << len(mainChain)):
                resultComponent = 1
                # Generate list of true or falses to represent chain config
                currConfig = [1 == ((iterNum >> j) & 1)
                        for j in range(len(mainChain))]

                # Loop through the chain and multiply conditionals together
                former = conditions
                for i, latter in enumerate(mainChain):
                    l = ("~" if not currConfig[i] else "") + latter.lower()
                    if i == 0:
                        # Utilizing that the conditions are conditionally
                        # indpendent...
                        for c in conditions:
                            command = [c] + ["|"] + [l]
                            resultComponent *= self.typeFuncs[
                                    'conditional'](command)
                    else:
                        f = (("~" if not currConfig[i - 1] else "")
                                + former.lower())
                        command = [f] + ["|"] + [l]
                        resultComponent *= self.typeFuncs['conditional'](
                                command)
                    former = latter
                # Final components of the chain
                if len(currConfig) > 0:
                    f = ("~" if not currConfig[-1] else "") + former.lower()
                    command = [f] + ["|"] + [subject.getName().lower()]
                    resultComponent *= self.typeFuncs['conditional'](command)
                else:
                    for c in conditions:
                        command = [c] + ["|"] + [subject.getName().lower()]
                        resultComponent *= self.typeFuncs[
                                'conditional'](command)
                resultComponent *= self.typeFuncs['marginal'](
                            subject.getName().lower())[0][0]
                result += resultComponent
            toDivide = 0
            if len(conditions) == 1:
                toDivide = self.typeFuncs['marginal'](conditions[0])[0][0]
            else:
                toDivide = self.typeFuncs['joint'](conditions)[0][0]
            return result / toDivide
        else:
            self.notImplemented(subject + ["|"] + conditions)
