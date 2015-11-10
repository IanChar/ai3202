from DataParser import DataParser
import numpy as np

A_ASCII = ord('a')

class HiddenMarkovModel(object):
    def __init__(self, filename):
        dp = DataParser(filename)
        self.ePtm, self.sPtm = dp.computeProbabilities()

    def getEProb(self, prior, subject):
        if prior == '_':
            prior = 26
        else:
            prior = ord(prior) - A_ASCII
        if subject == '_':
            subject = 26
        else:
            subject = ord(subject) - A_ASCII
        return self.ePtm[prior, subject]

    def getSProb(self, prior, subject):
        if prior == '_':
            prior = 26
        else:
            prior = ord(prior) - A_ASCII
        if subject == '_':
            subject = 26
        else:
            subject = ord(subject) - A_ASCII
        return self.sPtm[prior, subject]

    def printEPtmTable(self):
        for i in range(27):
            if i == 26:
                iChar = "_"
            else:
                iChar = chr(i + A_ASCII)
            for j in range(27):
                if j == 26:
                    jChar = "_"
                else:
                    jChar = chr(j + A_ASCII)
                print "P(", jChar, "|", iChar, ") = ", self.getEProb(iChar, jChar)

    def printSPtmTable(self):
        for i in range(27):
            if i == 26:
                iChar = "_"
            else:
                iChar = chr(i + A_ASCII)
            for j in range(27):
                if j == 26:
                    jChar = "_"
                else:
                    jChar = chr(j + A_ASCII)
                print "P(", jChar, "|", iChar, ") = ", self.getSProb(iChar, jChar)

if __name__ == '__main__':
    hmm = HiddenMarkovModel('typos20.data')
    print "--------------Evidence Probabilties--------------"
    hmm.printEPtmTable()
    print "--------------Transition Probabilties--------------"
    hmm.printSPtmTable()
