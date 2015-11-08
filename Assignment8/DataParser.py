class DataParser(object):
    def __init__(self, filename):
        self.filename = filename
        # P(E_t | X_t)
        self.evidenceProbs = {}
        # P(E_(t+1) | E_t)
        self.transitionProbs = {}

    def parseInData(self):
        f = open(self.filename, 'r')
        curr = f.readline().split(' ')
        nxt = f.readline().split(' ')
        if len(curr) == 1 or len(nxt) == 1:
            raise Exception("Invalid file given.")
        else:
            curr[1] = curr[1][:-1]
        # While there are still valid lines in the file
        while len(nxt) == 2:
            nxt[1] = nxt[1][:-1]
            print curr, nxt
            curr = nxt
            nxt = f.readline().split(' ')
        f.close()

if __name__ == '__main__':
    dp = DataParser('test.data')
    dp.parseInData()
