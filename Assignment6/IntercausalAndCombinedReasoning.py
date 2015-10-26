import traceback
from Node import Node
from Node import PriorNode
from Reasoning import Reasoning

class IntercausalAndCombinedReasoning(Reasoning):
    def __init__(self, net, levels, typeFuncs):
        super(IntercausalAndCombinedReasoning, self).__init__(
                net, levels, typeFuncs)

    def compute(self, subject, conditions):
        # Use definition of conditional probability to compute
        numerator = self.typeFuncs['joint'](subject + conditions)
        denomenator = self.typeFuncs['joint'](conditions)
        return numerator / denomenator
