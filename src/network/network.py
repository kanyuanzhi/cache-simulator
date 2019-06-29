class Network(object):
    def __init__(self, staleness):
        self.staleness = staleness
        self.hit = 0
        self.miss = 0

    def hitCount(self):
        self.hit = self.hit + 1
    
    def missCount(self):
        self.miss = self.miss + 1