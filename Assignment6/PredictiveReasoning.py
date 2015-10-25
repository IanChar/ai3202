import traceback
from Node import Node
from Node import PriorNode
from Reasoning import Reasoning

class PredictiveReasoning(Reasoning):
    def __init__(self, net, levels, typeFuncs):
        super(PredictiveReasoning, self).__init__(net, levels, typeFuncs)

    def compute(self, subject, conditions):
        sNodes = self.getNodes(subject)
        cNodes = self.getNodes(conditions)
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
                result = self.directPredictive(s, conditions, depChains)
            else:
                # Case where not directly dependent
                result = self.indirectPredictive(s, conditions, depChains)
            if subject[0][:1] == "~":
                result = 1 - result
            return result
        else:
            # Case where there are multiple subjects
            return self.multipleSubjects(subject, conditions)

    # Case where all conditions have some direct dependence to the subject.
    # subject is a node of the single subject, conditions is a list of the
    # names of the conditions, and depChains is the chain to get from the
    # subject to each condition.
    def directPredictive(self, subject, conditions, depChains):
        subjDeps = subject.getDependencies()
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
                    try:
                        acc *= self.typeFuncs['marginal'](command)[0][0]
                    except KeyError as err:
                        traceback.print_stack()
                        print "Function", err, "was not found in dict."
            result += acc
        return result

    # Opposite of directPredictive
    def indirectPredictive(self, subject, conditions, depChains):
        subjDeps = subject.getDependencies()
        # CASE 1
        # Check if one path is a substring of the other (> 1 condition).
        indicesToRemove = []
        for i, dC1 in enumerate(depChains):
            for j, dC2 in enumerate(depChains):
                if i != j and (dC1 == dC2 or dC1 == dC2[:-1]):
                    indicesToRemove.append(j)
        # Remove redundent dependencies and start over
        if len(indicesToRemove) > 0:
            # Make sure to sort list and but in reverse order so that
            # removal of elements isn't a problem. This also works because
            # we assume conditions and depChains match up
            indicesToRemove.sort()
            for i in indicesToRemove[::-1]:
                depChains.pop(i)
                conditions.pop(i)
            return self.compute(
                    [subject.getName().lower()], conditions)

        # CASE 2
        # Either there is only one condition or the conditions have the same
        # path leading up to the condition.
        canCompute = len(conditions) == 1
        if not canCompute:
            canCompute = True
            for i, dC1 in enumerate(depChains):
                for j, dC2 in enumerate(depChains):
                    if i != j and dC1[:-1] != dC2[:-1]:
                        canCompute = False
                        break
        if canCompute:
            result = 0
            mainChain = depChains[0][:-1]
            # Loop over possibilities that path to condition can take
            for iterNum in range(1 << len(mainChain)):
                resultComponent = 1
                # Generate list of true or falses to represent chain config
                currConfig = [1 == ((iterNum >> j) & 1)
                        for j in range(len(mainChain))]

                # Loop through the chain and multiply conditionals together
                former = subject.getName()
                for i, latter in enumerate(mainChain):
                    if i > 0:
                        f = (("~" if not currConfig[i - 1] else "")
                                + former.lower())
                    else:
                        f = former.lower()
                    l = ("~" if not currConfig[i] else "") + latter.lower()
                    resultComponent *= self.compute([f], [l])
                    former = latter
                # Final component of the chain
                f = ("~" if not currConfig[-1] else "") + former.lower()
                resultComponent *= self.compute([f], conditions)
                result += resultComponent
            return result
        else:
            self.notImplemented(subject + ["|"] + conditions)

    def multipleSubjects(self, subjects, conditions):
        sNodes = self.getNodes(subjects)
        cNodes = self.getNodes(conditions)

        # See if the subjects have any common dependencies
        possibleCommon = self.getFromNet(sNodes[0]).getDependencies()
        for pC in possibleCommon[::-1]:
            foundTally = len(sNodes) - 1
            for i in range(1, len(sNodes)):
                foundCommon = False
                for otherDep in self.getFromNet(sNodes[i]).getDependencies():
                    if pC == otherDep:
                        foundCommon = True
                if foundCommon:
                    foundTally -= 1
            if foundTally != 0:
                possibleCommon.remove(pC)
        # If there are no common dependencies then we do cannot compute
        if len(possibleCommon) == 0:
            self.notImplemented(subjects + ["|"] + conditions)
        # Check to see if the common dependencies are in the conditions
        commonDep = None
        for pC in possibleCommon:
            for i,c in enumerate(cNodes):
                if pC == c:
                    commonDep = conditions[i]
        # If commonDep is already in the conditions we can remove the other
        # conditions and the subjects become independent
        if commonDep is not None:
            result = 1
            for s in subjects:
                result *= self.compute([s], [commonDep])
            return result
        else:
            commonDep = possibleCommon[0]
            result = self.multipleSubjects(subjects, [commonDep.lower()])
            result *= self.compute([commonDep.lower()], conditions)
            addToResult = self.multipleSubjects(subjects, ["~"
                    + commonDep.lower()])
            addToResult *= self.compute(["~" + commonDep.lower()], conditions)
            return result + addToResult
