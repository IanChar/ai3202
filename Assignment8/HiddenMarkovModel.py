from DataParser import DataParser
import numpy as np
import math

A_ASCII = ord('a')
NUM_STATES = 27

class HiddenMarkovModel(object):
    def __init__(self, trainFile, targetFile):
        dp = DataParser(trainFile)
        self.ePtm, self.sPtm, self.initVect = dp.computeProbabilities()
        self.trueStates, self.emissions = self.parseTarget(targetFile)

    def correctText(self):
        probs = self.findSequenceProbs()
        sequence = self.findMostLikelySequence(probs)
        for s in sequence:
            print s
        print "\nError went from", self.computeAccuracy(self.emissions), "%",
        print "to", self.computeAccuracy(sequence), "%"

    def findMostLikelySequence(self, seqProbs):
        seqProbs = seqProbs[::-1]
        currState = (seqProbs[0][chr(A_ASCII)], chr(A_ASCII))
        for key, value in seqProbs[0].iteritems():
            if currState < (value, key):
                currState = (value, key)
        seq = [currState[1]]
        currIndex = 1
        while currState[0][1] is not None:
            currState = (seqProbs[currIndex][currState[0][1]], currState[0][1])
            seq.insert(0, currState[1])
            currIndex += 1
        return seq

    def computeAccuracy(self, sequence):
        countCorrect = 0
        for sIndex, s in enumerate(sequence):
            countCorrect += s == self.trueStates[sIndex]
        return (1 - float(countCorrect)/len(self.trueStates)) * 100

    def findSequenceProbs(self):
        stateProbs = []
        firstState = True
        for e in self.emissions:
            currProbs = {}
            if firstState:
                for pIndex, p in enumerate(self.initVect.tolist()[0]):
                    if pIndex == 26:
                        state = '_'
                    else:
                        state = chr(A_ASCII + pIndex)
                    currProbs[state] = (math.log(p)
                            + math.log(self.getEProb(state, e)), None)
                firstState = False
            else:
                for s1 in range(NUM_STATES):
                    if s1 == 26:
                        currState = '_'
                    else:
                        currState = chr(A_ASCII + s1)
                    currCombos = []
                    for s2 in range(NUM_STATES):
                        if s2 == 26:
                            prevState = '_'
                        else:
                            prevState = chr(A_ASCII + s2)
                        currCombos.append((
                                math.log(self.getSProb(prevState, currState))
                                + math.log(self.getEProb(currState, e))
                                + stateProbs[-1][prevState][0],
                                prevState))
                    currProbs[currState] = max(currCombos)
            stateProbs.append(currProbs)
        return stateProbs

    def parseTarget(self, targetFile):
        f = open(targetFile, 'r')
        trueStates = []
        emissions = []
        for line in f:
            splitted = line.split(' ')
            if len(splitted) == 2:
                trueStates.append(splitted[0])
                emissions.append(splitted[1][:-1])
        return trueStates, emissions

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

    def getInitProb(self, subject):
        if subject == '_':
            return self.initVect[0, 26]
        else:
            return self.initVect[0, ord(subject) - A_ASCII]

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
                print "P(", jChar, "|", iChar, ") = ", self.getEProb(
                        iChar, jChar)

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
                print "P(", jChar, "|", iChar, ") = ", self.getSProb(
                        iChar, jChar)
    def printInitTable(self):
        for i in range(26):
            print "P(", chr(i + A_ASCII), ") =", self.getInitProb(chr(
                    i + A_ASCII))
        print "P( _ ) =", self.getInitProb('_')

if __name__ == '__main__':
    hmm = HiddenMarkovModel('typos20.data', 'typos20Test.data')
    hmm.correctText()
