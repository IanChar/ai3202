import random
UNIFORMS = [0.82,	0.56,	0.08,	0.81,	0.34,	0.22,	0.37,	0.99,	0.55,	0.61,	0.31,	0.66,	0.28,	1.0,	0.95,
0.71,	0.14,	0.1,	1.0,	0.71,	0.1,	0.6,	0.64,	0.73,	0.39,	0.03,	0.99,	1.0,	0.97,	0.54,	0.8,	0.97,
0.07,	0.69,	0.43,	0.29,	0.61,	0.03,	0.13,	0.14,	0.13,	0.4,	0.94,	0.19, 0.6,	0.68,	0.36,	0.67,
0.12,	0.38,	0.42,	0.81,	0.0,	0.2,	0.85,	0.01,	0.55,	0.3,	0.3,	0.11,	0.83,	0.96,	0.41,	0.65,
0.29,	0.4,	0.54,	0.23,	0.74,	0.65,	0.38,	0.41,	0.82,	0.08,	0.39,	0.97,	0.95,	0.01,	0.62,	0.32,
0.56,	0.68,	0.32,	0.27,	0.77,	0.74,	0.79,	0.11,	0.29,	0.69,	0.99,	0.79,	0.21,	0.2,	0.43,	0.81,
0.9,	0.0,	0.91,	0.01]

class BayesNetSamlper(object):
    def __init__(self):
        # List of lists where each inner list has booleans that represents
        # the states in the order Cloudy, Sprinkler, Rain, Wet Grass
        self.samples = []

    def computePriorSamples(self):
        # 25 samples will be generated since 100 uniforms given
        i = 0
        self.samples = []
        while i < len(UNIFORMS) - 3:
            sample, i = self.generateASample(i)
            self.samples.append(sample)

    def computeRejectionSamples(self, requirements):
        i = 0
        self.samples = []
        while i < len(UNIFORMS) - 3:
            sample, i = self.generateASample(i, requirements)
            if sample is not None:
                self.samples.append(sample)

    def computeRejectionSamplesForA(self):
        samplesToReturn = []
        for u in UNIFORMS:
            samplesToReturn.append([u < 0.5, None, None, None])
        return samplesToReturn

    def computeRejectionSamplesForB(self):
        samplesToReturn = []
        i = 0
        while i < len(UNIFORMS) - 1:
            c = UNIFORMS[i] < 0.5
            i += 1
            if c:
                r = UNIFORMS[i] < 0.8
            else:
                r = UNIFORMS[i] < 0.2
            i += 1
            if r:
                samplesToReturn.append([c, None, r, None])
        return samplesToReturn

    # Returns a given sampled (or None) and the current index
    def generateASample(self, startingIndex, requirements = None):
        i = startingIndex
        returnSample = []
        if not startingIndex < len(UNIFORMS) - 3:
            return None, i
        # Cloudy probability
        returnSample.append(UNIFORMS[i] < 0.5)
        i += 1
        if (requirements is not None and requirements[0] is not None
                and requirements[0] != returnSample[0]):
            return None, i
        if returnSample[0]:
            # Sprinkler probability
            returnSample.append(UNIFORMS[i] < 0.1)
            i += 1
            if (requirements is not None and requirements[1] is not None
                    and requirements[1] != returnSample[1]):
                return None, i
            # Rain probability
            returnSample.append(UNIFORMS[i] < 0.8)
            i += 1
            if (requirements is not None and requirements[2] is not None
                    and requirements[2] != returnSample[2]):
                return None, i
        else:
            # Sprinkler probability
            returnSample.append(UNIFORMS[i] < 0.5)
            i += 1
            if (requirements is not None and requirements[1] is not None
                    and requirements[1] != returnSample[1]):
                return None, i
            # Rain probability
            returnSample.append(UNIFORMS[i] < 0.2)
            i += 1
            if (requirements is not None and requirements[2] is not None
                    and requirements[2] != returnSample[2]):
                return None, i
        # wet grass probabilities
        if returnSample[1] == True and returnSample[2] == True:
            returnSample.append(UNIFORMS[i] < 0.99)
        elif returnSample[1] == False and returnSample[2] == False:
            returnSample.append(False)
        else:
            returnSample.append(UNIFORMS[i] < 0.9)
        i += 1
        if (requirements is not None and requirements[3] is not None
                and requirements[3] != returnSample[3]):
            return None, i
        return returnSample, i

    # Answers P(c = true), no distinction between prior and rejection for this
    def answerA(self, rejection = False):
        if rejection:
            relevantData = self.computeRejectionSamplesForA()
        else:
            if len(self.samples) != len(UNIFORMS)/4:
                self.computePriorSamples()
            relevantData = self.samples
        count = 0
        for s in relevantData:
            if s[0]:
                count += 1
        return float(count)/len(relevantData)

    # Answers P(c = True | r = True)
    def answerB(self, rejection = False):
        relevantData = None
        if rejection:
            relevantData = self.computeRejectionSamplesForB()
        else:
            if len(self.samples) != len(UNIFORMS)/4:
                self.computePriorSamples()
            filterFunc = lambda currS: currS[2]
            relevantData = filter(filterFunc, self.samples)
        count = 0
        for rD in relevantData:
            if rD[0]:
                count += 1
        return float(count)/len(relevantData)

    # Answers P(s = True | w = True)
    def answerC(self, rejection = False):
        relevantData = None
        if rejection:
            self.computeRejectionSamples([None, None, None, True])
            relevantData = self.samples
        else:
            if len(self.samples) != len(UNIFORMS)/4:
                self.computePriorSamples()
            filterFunc = lambda currS: currS[3]
            relevantData = filter(filterFunc, self.samples)
        count = 0
        for rD in relevantData:
            if rD[1]:
                count += 1
        return float(count)/len(relevantData)

    # Answers P(s = True | w = True)
    def answerD(self, rejection = False):
        relevantData = None
        if rejection:
            self.computeRejectionSamples([True, None, None, True])
            relevantData = self.samples
        else:
            if len(self.samples) != len(UNIFORMS)/4:
                self.computePriorSamples()
            filterFunc = lambda currS: currS[3] and currS[0]
            relevantData = filter(filterFunc, self.samples)
        count = 0
        for rD in relevantData:
            if rD[1]:
                count += 1
        return float(count)/len(relevantData)

    def getSamples(self):
        return self.samples

if __name__ == '__main__':
    bns = BayesNetSamlper()
    print bns.answerA()
    print bns.answerB()
    print bns.answerC()
    print bns.answerD()

    print ""

    print bns.answerA(True)
    print bns.answerB(True)
    print bns.answerC(True)
    print bns.answerD(True)
