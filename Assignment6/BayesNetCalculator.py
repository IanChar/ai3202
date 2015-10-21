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
    def execCommand(self, command):
        if (command[0][1:] == 'g'):
            return self.execConditional(command[1])
        elif (command[0][1:] == 'j'):
            return self.execJoint(command[1])
        elif (command[0][1:] == 'm'):
            return self.execMarginal(command[1])
        elif (command[0][1:] == 'p'):
            return self.changePrior(command[1])
        else:
            raise Exception("Unknown flag passed in.")

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
    xProbabilities = {(True): 0.9, (False): 0.2}
    nodes['X'] = Node('X', ['C'], xProbabilities)
    dProbabilities = {(True): 0.65, (False): 0.3}
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
        # for command in optlist:
        #     bn.execCommand(command)
