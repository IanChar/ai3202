import sys
import getopt
from BayesNetCalculator import BayesNetCalculator
from Node import Node
from Node import PriorNode

FLAGS = ':g:j:m:p:'

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
