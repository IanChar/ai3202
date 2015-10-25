import traceback
from Node import Node
from Node import PriorNode
from Reasoning import Reasoning

class CombinedReasoning(Reasoning):
    def __init__(self, net, levels, typeFuncs):
        super(CombinedReasoning, self).__init__(net, levels, typeFuncs)

    def compute(self, subject, condtions):
        raise self.NOT_IMPLEMENTED
