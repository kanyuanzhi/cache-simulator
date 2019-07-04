import random
import simpy
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

from mcav.zipf import Zipf


class LRUCache(object):
    def __init__(self, size, amount, staleness, N, pattern="normal"):
        # pattern options: normal, reactive, proactive_remove, proactive_renew, proactive_update_top 
        self.size = size
        self.amount = amount
        self.staleness = staleness
        self.N = N
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
        self.validation_time = {}
        self.updatetime_in_cache = {}
        self.validation_time_in_cache = {}


        self.pattern = pattern

        self.pub_load = 0
        self.pub_load_c = {}

        # self.vtime_in_cache = {}
        # self.vtime = {}
        # self.val = {}
        # self.inval = {}

        for i in range(1, amount + 1):
            self.chit[i] = 0
            self.cmiss[i] = 0
            self.original_chit[i] = 0
            self.original_cmiss[i]=0
            # self.val[i] = 0
            # self.inval[i] = 0
            # self.updatetime[i] = random.uniform(-staleness, 0)
            # self.updatetime[i] = random.randint(-staleness+1, 0)
            # self.validation_time[i]
            # self.updatetime[i] = 0
            # self.vtime[i] = random.randint(-staleness+1, 0)
            self.pub_load_c[i] = 0

    def insert(self, item, now):
        if self.pattern == "reactive":
            self.insertReactive(item, now)
        else:
            self.insertNormal(item)

    def insertNormal(self, item):
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

    def insertReactive(self, item, now):
        if item in self.stack:
            self.original_hit = self.original_hit + 1
            self.original_chit[item] = self.original_chit[item] + 1
            if now - self.updatetime_in_cache[item] < self.validation_time[item]:
                self.hit = self.hit + 1
                self.chit[item] = self.chit[item] + 1
            else:
                self.updatetime_in_cache[item] = self.updatetime[item]
                self.miss = self.miss + 1
                self.cmiss[item] = self.cmiss[item] + 1
            self.stack.remove(item)
            self.stack.append(item)
        else:
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
        for i in range(1, self.amount + 1):
            if self.chit[i] == 0 and self.cmiss[i] == 0:
                hit_ratio[i] = 0
            else:
                hit_ratio[i] = float(
                    self.chit[i]) / (self.chit[i] + self.cmiss[i])
        return hit_ratio

    def originalHitRatio(self):
        original_hit_ratio = {}
        for i in range(1, self.amount + 1):
            if self.original_chit[i] == 0 and self.original_cmiss[i] == 0:
                original_hit_ratio[i] = 0
            else:
                original_hit_ratio[i] = float(
                    self.original_chit[i]) / (self.original_chit[i] + self.original_cmiss[i])
        return original_hit_ratio
    
    def validationRateUnderHit(self):
        vuh = {}
        for i in range(1, self.amount + 1):
            if self.original_chit[i] == 0:
                vuh[i] = 0
            else:
                vuh[i] = float(self.chit[i]) / self.original_chit[i]
        return vuh

    def cacheSize(self):
        return len(self.stack)

    def pubLoadC(self):
        return self.pub_load_c

    def pubLoad(self):
        return self.pub_load
    
    def totalLoad(self):
        return self.miss + self.pub_load

    def update(self, id, now, validation_time):
        if self.pattern == "reactive":
            self.updatetime[id] = now
            self.validation_time[id] = validation_time
        elif self.pattern == "proactive_remove":
            self.updatetime[id] = now
            self.validation_time[id] = validation_time
            if id in self.stack:
                self.stack.remove(id)
        elif self.pattern == "proactive_renew":
            self.updatetime[id] = now
            self.validation_time[id] = validation_time
            if id in self.stack:
                # self.stack.remove(i)
                # self.stack.append(i)
                self.pub_load = self.pub_load + 1
                self.pub_load_c[id] = self.pub_load_c[id] +1
        elif self.pattern == "proactive_optional_renew":
            self.updatetime[id] = now
            self.validation_time[id] = validation_time
            if id in self.stack:
                # self.stack.remove(i)
                # self.stack.append(i)
                if id < self.N+1:
                    self.pub_load = self.pub_load + 1
                else:
                    self.stack.remove(id)
        else:
            pass


class Simulator(object):
    def __init__(self, env, size, amount, staleness, rate, content, popularity, pattern="normal"):
        self.env = env
        self.cache = LRUCache(size, amount, staleness, pattern)
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
            self.cache.insert(item,self.env.now)
            # print(self.cache.cacheSize())
            duration = random.expovariate(self.rate)
            if int(self.env.now) % 50 == 0 and print_flag:
                print(self.env.now)
                print(self.cache.cacheSize())
                print(self.cache.totalHitRatio())
                print_flag = False
            if int(self.env.now) % 50 != 0 and not print_flag:
                print_flag = True
            yield self.env.timeout(duration)
    
    def _random_pick(self, some_list, probabilities):
        x = random.uniform(0, 1)
        cumulative_probability = 0.0
        for item, item_probability in zip(some_list, probabilities):
            cumulative_probability += item_probability
            if x < cumulative_probability: break
        return item


class Item(object):
    def __init__(self, env, id, cache, staleness):
        self.env = env
        self.id = id
        self.cache = cache
        self.staleness = staleness

    def update(self):
        while True:
            # duration = random.uniform(0, 2*self.staleness)
            duration = random.expovariate(1.0 / self.staleness)
            self.cache.update(self.id, self.env.now, duration)
            yield self.env.timeout(duration)

class User(object):
    def __init__(self, env, cache, amount, z, rate):
        self.env = env
        self.cache = cache
        self.rate = rate
        self.content = [i for i in range(1, amount + 1)]
        self.popularity = [Zipf(amount, z).popularity()[i] for i in range(1, amount)]

    def request(self):
        print_flag = True
        while True:
            item = self._random_pick(self.content, self.popularity)
            self.cache.insert(item, self.env.now)
            # print(self.cache.cacheSize())
            duration = random.expovariate(self.rate)
            if int(self.env.now) % 2000 == 0 and print_flag:
                print(self.env.now)
                print(self.cache.cacheSize())
                print(self.cache.totalHitRatio())
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


class NewSimulator(object):
    def __init__(self, cachesize, amount, staleness, total_rate, z, N, pattern, simulation_time=10000):
        env = simpy.Environment()
        self.cache = LRUCache(cachesize, amount, staleness, N, pattern)
        for id in range(1, amount + 1):
            env.process(Item(env, id, self.cache, staleness).update())

        env.process(User(env, self.cache, amount, z, total_rate).request())
        env.run(until=simulation_time)
        print("sim: ", self.cache.totalHitRatio())

if __name__ == "__main__":

    simulation_time = 10000

    amount = 5000
    z = 0.8
    cachesize = 100
    staleness = 6
    total_rate = 20
    # pattern = "reactive"
    # pattern = "proactive_remove"
    # pattern = "proactive_renew"
    pattern = "proactive_optional_renew"

    # reactive = ReactiveUniform(amount, cachesize, total_rate, staleness, Zipf(amount, z).popularity())
    #
    # print("model: ", reactive.totalHitRatio())

    env = simpy.Environment()
    cache = LRUCache(cachesize, amount, staleness, pattern)

    for id in range(1, amount+1):
        env.process(Item(env, id, cache, staleness).update())

    env.process(User(env, cache, amount, z, total_rate).request())
    env.run(until=simulation_time)

    print("sim: ", cache.totalHitRatio())

    index = []
    sim = []
    model = []
    for i in range(1, amount + 1):
        index.append(i)
        sim.append(cache.hitRatio()[i])
        # model.append(reactive.hitRatio()[i])

    plt.plot(index, sim, "+", color="black", label="simulation")
    # plt.plot(index, model, color="black", linewidth="1", label="model")


    plt.xlabel("content ID",)
    plt.ylabel("hit probability")
    plt.grid(True)
    plt.axis([0, 51, 0, 1],)
    plt.legend()

    plt.show()


