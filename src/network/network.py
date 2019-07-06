import random
class Network(object):
    def __init__(self, amount, staleness, simulation_time, N, pattern):
        self.amount = amount
        self.staleness = staleness
        self.simulation_time = simulation_time
        self.pattern = pattern
        self.N = N

        self.nodes = None
        self.hit = 0
        self.miss = 0
        self.pub_load = 0

        self.updatetime = {}
        self.validation_time = {}

        for i in range(1, self.amount+1):
            self.updatetime[i] = 0
            self.validation_time[i] = random.uniform(0, 2*self.staleness)
    
    def registerNodes(self, nodes):
        self.nodes = nodes

    def hitCount(self):
        self.hit = self.hit + 1
    
    def missCount(self):
        self.miss = self.miss + 1
    
    def totalHitRatio(self):
        return float(self.hit)/(self.hit+self.miss)

    def totalLoad(self):
        # return (self.miss + self.pub_load)/float(self.simulation_time)
        return self.miss + self.pub_load

    def update(self, now):
        if self.pattern == "reactive":
            for i in range(1, self.amount + 1):
                if now - self.updatetime[i] >= self.validation_time[i]:
                    self.updatetime[i] = now
                    self.validation_time[i] = random.expovariate(1.0/self.staleness)
        elif self.pattern == "proactive_remove":
            for i in range(1, self.amount + 1):
                if now - self.updatetime[i] >= self.validation_time[i]:
                    self.updatetime[i] = now
                    self.validation_time[i] = random.expovariate(1.0/self.staleness)
                    for node in self.nodes:
                        if i in node.stack:
                            node.stack.remove(i)
        elif self.pattern == "proactive_renew":
            for i in range(1, self.amount + 1):
                if now - self.updatetime[i] >= self.validation_time[i]:
                    self.updatetime[i] = now
                    self.validation_time[i] = random.expovariate(1.0/self.staleness)
                    flag = False
                    for node in self.nodes:
                        if i in node.stack:
                            flag = True
                            break
                            # node.stack.remove(i)
                            # node.stack.append(i)
                    if flag:
                        self.pub_load = self.pub_load + 1
        elif self.pattern == "proactive_optional_renew":
            for i in range(1, self.amount + 1):
                if now - self.updatetime[i] >= self.validation_time[i]:
                    self.updatetime[i] = now
                    self.validation_time[i] = random.expovariate(1.0/self.staleness)
                    flag = False
                    for node in self.nodes:
                        if i in node.stack:
                            if i < self.N + 1:
                                flag = True
                                break
                            else:
                                node.stack.remove(i)
                    if flag:
                        self.pub_load = self.pub_load + 1
                    # if i in self.stack:
                    #     # self.stack.remove(i)
                    #     # self.stack.append(i)
        else:
            pass