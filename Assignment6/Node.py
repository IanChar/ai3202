class Node(object):
    def __init__(self, name, dependencies, probabilities):
        self.name = name
        # dependencies is a list with the names of the dependencies
        self.dependencies = dependencies
        # probabilities is a dict of probabilities where key is tuple with
        # boolean values of dependencies (ordered the same as dependencies)
        self.probabilities = probabilities

    def getName(self):
        return self.name

    def getDependencies(self):
        return self.dependencies

    def getProbability(self, condition = None):
        if condition is None:
            raise Exception("A condition to retrieve a probability.")
        # Here condition is expected to be a tuple
        return self.probabilities[condition]

class PriorNode(Node):
    def __init__(self, name, probability):
        super(PriorNode, self).__init__(name, None, probability)

    def getProbability(self, condition = None):
        return self.probabilities

    def setProbability(self, probability):
        self.probabilities = probability

if __name__ == '__main__':
    test = PriorNode("test", 0.5)
    print test.getProbability()
