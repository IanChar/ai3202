from DataParser import DataParser
import numpy as np

A_ASCII = ord('a')

class HiddenMarkovModel(object):
    def __init__(self, filename):
        dp = DataParser(filename)
        self.ePtm, self.sPtm = dp.computeProbabilities()

    def getEProb(self, prior, subject):
        return self.ePtm[ord(prior) - A_ASCII, ord(subject) - A_ASCII]

    def getSProb(self, prior, subject):
        return self.sPtm[ord(prior) - A_ASCII, ord(subject) - A_ASCII]

if __name__ == '__main__':
    hmm = HiddenMarkovModel('typos20.data')
    print hmm.getEProb('a', 'a'), hmm.getEProb('a', 's'), hmm.getEProb('a', 'p')
    print hmm.getSProb('q', 'u'), hmm.getSProb('q', 'z')
