import traceback
from Node import Node
from Node import PriorNode
from Reasoning import Reasoning

class DiagnosticReasoning(Reasoning):
    def __init__(self, net, levels, typeFuncs):
        super(DiagnosticReasoning, self).__init__(net, levels, typeFuncs)
