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
        self.updatetime = {}
        self.updatetime_in_cache = {}
        for i in range(1, amount + 1):
            self.chit[i] = 0
            self.cmiss[i] = 0
            #self.updatetime[i] = random.uniform(-staleness, 0)
            self.updatetime[i] = random.randint(-staleness+1, 0)
            # self.updatetime[i] = 0


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
        if item in self.stack:
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

    def update(self, now):
        for i in range(1, self.amount + 1):
            if now - self.updatetime[i] >= self.staleness:
                self.updatetime[i] = self.updatetime[i] + self.staleness
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

