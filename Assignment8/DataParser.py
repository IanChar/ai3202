import numpy as np
A_ASCII = ord('a')
Z_ASCII = ord('z')
NUM_STATES = 27
# Consts for the counter list
SPACE_INDEX = 26
COUNT_INDEX = 27

class DataParser(object):
    def __init__(self, filename):
        self.filename = filename

    def computeProbabilities(self):
        ev, states, c = self.parseInData()
        # P(E_t | X_t), stored matrix where row is x and column is e
        evidenceProbs = np.matrix([[0 for _ in range(NUM_STATES)]
                for __ in range(NUM_STATES)])
        evidenceProbs = evidenceProbs.astype(float)
        # P(E_(t+1) | E_t), stored as matrix where row is x_t anc col is x_t+1
        transitionProbs = np.matrix([[0 for _ in range(NUM_STATES)]
                for __ in range(NUM_STATES)])
        transitionProbs = transitionProbs.astype(float)
        # Vector for initial states
        initStateProbs = np.matrix([float(c[i])/c[COUNT_INDEX]
                for i in range(COUNT_INDEX)])
        # Fill out evidence
        for prior, observed in ev.iteritems():
            for s in range(A_ASCII, Z_ASCII + 1):
                if chr(s) in observed.keys():
                    seen = observed[chr(s)]
                else:
                    seen = 0
                if prior == "_":
                    evidenceProbs[SPACE_INDEX, s - A_ASCII] = (float(seen + 1)
                            / (observed['count'] + NUM_STATES))
                else:
                    evidenceProbs[ord(prior) - A_ASCII, s - A_ASCII] = (float(
                            seen + 1) / (observed['count'] + NUM_STATES))
            s = '_'
            if s in observed.keys():
                seen = observed[s]
            else:
                seen = 0
            if prior == "_":
                evidenceProbs[SPACE_INDEX, SPACE_INDEX] = (float(seen + 1)
                        / (observed['count'] + NUM_STATES))
            else:
                evidenceProbs[ord(prior) - A_ASCII, SPACE_INDEX] = (float(
                        seen + 1) / (observed['count'] + NUM_STATES))
        # Fill out state transitions
        for prior, observed in states.iteritems():
            for s in range(A_ASCII, Z_ASCII + 1):
                if chr(s) in observed.keys():
                    seen = observed[chr(s)]
                else:
                    seen = 0
                if prior == "_":
                    transitionProbs[SPACE_INDEX, s - A_ASCII] = (float(seen + 1)
                            / (observed['count'] + NUM_STATES))
                else:
                    transitionProbs[ord(prior) - A_ASCII, s - A_ASCII] = (float(
                            seen + 1) / (observed['count'] + NUM_STATES))
            s = '_'
            if s in observed.keys():
                seen = observed[s]
            else:
                seen = 0
            if prior == "_":
                transitionProbs[SPACE_INDEX, SPACE_INDEX] = (float(seen + 1)
                        / (observed['count'] + NUM_STATES))
            else:
                transitionProbs[ord(prior) - A_ASCII, SPACE_INDEX] = (float(
                        seen + 1) / (observed['count'] + NUM_STATES))
        return evidenceProbs, transitionProbs, initStateProbs

    def parseInData(self):
        f = open(self.filename, 'r')

        # Count the evidences and state transitions these will be nested dicts.
        # Also count how many times each state appears index 26 is _ and 27
        # is total count
        tmpEvidence = {}
        tmpState = {}
        tmpCounter = [0 for _ in range(NUM_STATES + 1)]
        for i in range(A_ASCII, 123):
            tmpEvidence[chr(i)] = {'count' : 0}
            tmpState[chr(i)] = {'count' : 0}
        tmpEvidence['_'] = {'count' : 0}
        tmpState['_'] = {'count': 0}

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
            # Update evidence
            e = tmpEvidence[curr[0]]
            if curr[1] in e.keys():
                e[curr[1]] += 1
            else:
                e[curr[1]] = 1
            e['count'] += 1
            # Update state
            s = tmpState[curr[0]]
            if nxt[0] in s.keys():
                s[nxt[0]] += 1
            else:
                s[nxt[0]] = 1
            s['count'] += 1
            # update count
            if ord(curr[0]) >= A_ASCII and ord(curr[0]) <= Z_ASCII:
                tmpCounter[ord(curr[0]) - A_ASCII] += 1
            else:
                tmpCounter[SPACE_INDEX] += 1
            tmpCounter[COUNT_INDEX] += 1
            curr = nxt
            nxt = f.readline().split(' ')
        f.close()
        return tmpEvidence, tmpState, tmpCounter

if __name__ == '__main__':
    dp = DataParser('typos20.data')
    e, s, i = dp.computeProbabilities()
    print s
