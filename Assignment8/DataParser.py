import numpy as np
NUM_LETTERS = 26

class DataParser(object):
    def __init__(self, filename):
        self.filename = filename

    def computeProbabilities(self):
        # P(E_t | X_t), stored matrix where row is x and column is e
        evidenceProbs = np.matrix([[0 for _ in range(26)] for __ in range(26)])
        evidenceProbs = evidenceProbs.astype(float)
        # P(E_(t+1) | E_t), stored as matrix where row is x_t anc col is x_t+1
        transitionProbs = np.matrix([[0 for _ in range(26)] for __ in range(26)])
        transitionProbs = transitionProbs.astype(float)
        ev, states = self.parseInData()
        # Fill out evidence
        for prior, observed in ev.iteritems():
            for s in range(97, 123):
                if chr(s) in observed.keys():
                    seen = observed[chr(s)]
                else:
                    seen = 0
                evidenceProbs[ord(prior) - 97, s - 97] = (float(seen + 1)
                        / (observed['count'] + NUM_LETTERS))
        # Fill out state transitions
        for prior, observed in states.iteritems():
            for s in range(97, 123):
                if chr(s) in observed.keys():
                    seen = observed[chr(s)]
                else:
                    seen = 0
                transitionProbs[ord(prior) - 97, s - 97] = (float(seen + 1)
                        / (observed['count'] + NUM_LETTERS))
        return evidenceProbs, transitionProbs

    def parseInData(self):
        f = open(self.filename, 'r')

        # Count the evidences and state transitions these will be nested dicts.
        tmpEvidence = {}
        tmpState = {}
        for i in range(97, 123):
            tmpEvidence[chr(i)] = {'count' : 0}
            tmpState[chr(i)] = {'count' : 0}

        # Iterate over the lines of the file
        curr = f.readline().split(' ')
        nxt = f.readline().split(' ')
        if len(curr) == 1 or len(nxt) == 1:
            raise Exception("Invalid file given.")
        else:
            curr[1] = curr[1][:-1]

        # While there are still valid lines in the file
        while len(nxt) == 2:
            nxt[1] = nxt[1][:-1]
            if curr[0] != '_':
                # Update evidence
                e = tmpEvidence[curr[0]]
                if curr[1] in e.keys():
                    e[curr[1]] += 1
                else:
                    e[curr[1]] = 1
                e['count'] += 1
                # Update state
                if nxt[0] != "_":
                    s = tmpState[curr[0]]
                    if nxt[0] in s.keys():
                        s[nxt[0]] += 1
                    else:
                        s[nxt[0]] = 1
                    s['count'] += 1
            curr = nxt
            nxt = f.readline().split(' ')
        f.close()
        return tmpEvidence, tmpState

if __name__ == '__main__':
    dp = DataParser('typos20.data')
    e, s = dp.computeProbabilities()
    print s[ord('q') - 97, ord('u') - 97]
