import random

class LRUCache(object):
    def __init__(self, size, amount, staleness):
        self.size = size
        self.amount = amount
        self.staleness = staleness
        self.stack = []
        self.hit = 0
        self.miss = 0
        self.chit = {}
        self.cmiss = {}
        self.original_hit=0
        self.original_chit={}
        self.original_miss=0
        self.original_cmiss={}
        self.updatetime = {}
        self.updatetime_in_cache = {}

        self.vtime_in_cache = {}
        self.vtime = {}
        self.val = {}
        self.inval = {}

        for i in range(1, amount + 1):
            self.chit[i] = 0
            self.cmiss[i] = 0
            self.original_chit[i] = 0
            self.original_cmiss[i]=0
            self.val[i] = 0
            self.inval[i] = 0
            #self.updatetime[i] = random.uniform(-staleness, 0)
            self.updatetime[i] = random.randint(-staleness+1, 0)
            # self.updatetime[i] = 0
        self.vtime = self.updatetime


    def insert0(self, item, now):
        if item in self.stack:
            self.hit = self.hit + 1
            self.chit[item] = self.chit[item] + 1

            self.stack.remove(item)
            self.stack.append(item)
        else:
            self.miss = self.miss + 1
            self.cmiss[item] = self.cmiss[item] + 1

            if len(self.stack) == self.size:
                self.stack.pop(0)
                self.stack.append(item)
            else:
                self.stack.append(item)

    def insert(self, item):
        if item in self.vtime_in_cache:
            if self.vtime_in_cache[item] == self.vtime[item]:
                self.val[item] = self.val[item] + 1
            else:
                self.inval[item] = self.inval[item] + 1
                self.vtime_in_cache[item] = self.vtime[item]
        else:
            self.vtime_in_cache[item] = self.vtime[item]
            self.inval[item] = self.inval[item] + 1
        
        if item in self.stack:
            if len(self.stack) == self.size:
                self.original_hit = self.original_hit + 1
                self.original_chit[item] = self.original_chit[item] + 1
            if self.updatetime_in_cache[item] == self.updatetime[item]:
                if len(self.stack) == self.size:
                    self.hit = self.hit + 1
                    self.chit[item] = self.chit[item] + 1
            else:
                self.updatetime_in_cache[item] = self.updatetime[item]
                if len(self.stack) == self.size:
                    self.miss = self.miss + 1
                    self.cmiss[item] = self.cmiss[item] + 1
            self.stack.remove(item)
            self.stack.append(item)
        else:
            if len(self.stack) == self.size:
                self.miss = self.miss + 1
                self.cmiss[item] = self.cmiss[item] + 1
                self.original_miss = self.original_miss + 1
                self.original_cmiss[item] = self.original_cmiss[item] + 1

            self.updatetime_in_cache[item] = self.updatetime[item]

            if len(self.stack) == self.size:
                self.stack.pop(0)
            
            self.stack.append(item)

    def totalHitRatio(self):
        return float(self.hit) / (self.miss + self.hit)

    def hitRatio(self):
        hit_ratio = {}
        for i in range(1, self.amount):
            if self.chit[i] == 0 and self.cmiss[i] == 0:
                hit_ratio[i] = 0
            else:
                hit_ratio[i] = float(
                    self.chit[i]) / (self.chit[i] + self.cmiss[i])
        return hit_ratio

    def originalHitRatio(self):
        original_hit_ratio = {}
        for i in range(1, self.amount):
            if self.original_chit[i] == 0 and self.original_cmiss[i] == 0:
                original_hit_ratio[i] = 0
            else:
                original_hit_ratio[i] = float(
                    self.original_chit[i]) / (self.original_chit[i] + self.original_cmiss[i])
        return original_hit_ratio
    
    def validationRateUnderHit(self):
        vuh = {}
        for i in range(1, self.amount):
            if self.original_chit[i] == 0:
                vuh[i] = 0
            else:
                vuh[i] = float(self.chit[i]) / self.original_chit[i]
        return vuh
    
    def validationRate(self):
        vr = {}
        for i in range(1, self.amount):
            if self.val[i] == 0 and self.inval[i] == 0:
                vr[i] = 0
            else:
                vr[i] = float(self.val[i] / (self.val[i]+self.inval[i]))
        return vr

    def update(self, now):
        for i in range(1, self.amount + 1):
            if now - self.updatetime[i] >= self.staleness:
                self.updatetime[i] = self.updatetime[i] + self.staleness
                self.vtime[i] = self.vtime[i] + self.staleness
                # if i in self.stack:
                #     self.stack.remove(i)

class Simulator(object):
    def __init__(self, env, size, amount, staleness, rate, content, popularity):
        self.env = env
        self.cache = LRUCache(size, amount, staleness)
        self.rate = rate
        self.content = content
        self.popularity = popularity

    def updateSim(self):
        while True:
            self.cache.update(self.env.now)
            duration = 1
            yield self.env.timeout(duration)


    def insertSim(self):
        print_flag = True
        while True:
            item = self._random_pick(self.content, self.popularity)
            self.cache.insert(item)
            duration = random.expovariate(self.rate)
            if int(self.env.now) % 2000 == 0 and print_flag:
                print(self.env.now)
                print_flag = False
            if int(self.env.now) % 2000 != 0 and not print_flag:
                print_flag = True
            yield self.env.timeout(duration)
    
    def _random_pick(self, some_list, probabilities):
        x = random.uniform(0, 1)
        cumulative_probability = 0.0
        for item, item_probability in zip(some_list, probabilities):
            cumulative_probability += item_probability
            if x < cumulative_probability: break
        return item

