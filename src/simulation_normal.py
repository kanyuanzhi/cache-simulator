import simpy
import math
import random
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mcav.sca import SCA
from scipy.optimize import fsolve
import numpy as np



class Zipf(object):
    # calucate the popularity of the contents
    def __init__(self, amount, z):
        self._amount = amount
        self._z = z
        self._factor = self._normalization()

    def _normalization(self):
        factor = 0.0
        for i in range(1, self._amount + 1):
            factor = factor + math.pow(1.0 / i, self._z)
        return 1 / factor

    def popularity(self):
        popularity_dict = {}
        for i in range(1, self._amount + 1):
            # popularity_dict[self._amount + 1 - i] = self._factor/math.pow(i, self._z)
            popularity_dict[i] = self._factor / math.pow(i, self._z)
        return popularity_dict


def random_pick(some_list, probabilities):
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(some_list, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability: break
    return item


class lruCache(object):
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
            self.updatetime[i] = random.uniform(-staleness, 0)

    def insert(self, item):
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


def simulation(env, rate, content, popularity, cache):
    flag = True
    while True:
        item = random_pick(content, popularity)
        cache.insert(item)
        duration = random.expovariate(rate)
        if int(env.now) % 2000 == 0 and flag:
            print(env.now)
            flag = False
        if int(env.now) % 2000 != 0 and not flag:
            flag = True
        yield env.timeout(duration)


class Che(object):
    def __init__(self, amount, cachesize, popularity, rate):
        self.amount = amount
        self.cachesize = cachesize
        self.popularity = popularity
        self.rate = rate
        self.T = self._characteristicTime()
        self.hit_ratio = self._hitRatio()

    def _f1(self, t):
        temp = 0
        for i in range(1, self.amount + 1):
            temp = temp + 1 - np.exp(-self.rate * self.popularity[i] * t)
            # temp = temp + pow(math.e, i*t)
        f = temp - self.cachesize
        return f
    
    def _characteristicTime(self):
        T = fsolve(self._f1,[1])[0]
        return T
    
    def _hitRatio(self):
        hit_ratio = {}
        for i in range(1, self.amount+1):
            hit_ratio[i] = 1 - np.exp(-self.rate*self.popularity[i]*self.T)
        return hit_ratio
    
    def hitRatio(self):
        return self.hit_ratio
    
    def totalHitRatio(self):
        total = 0
        for i in range(1, self.amount+1):
            total = total + self.hit_ratio[i]*self.popularity[i]
        return total

if __name__ == "__main__":
    amount = 1000
    z = 0.8
    cachesize = 100
    rate = 10
    staleness = 5
    simulation_time = 10000
    # random.seed(42)
    zipf = Zipf(amount, z)
    popularity_dict = zipf.popularity()
    content = [i for i in range(1, amount + 1)]
    popularity = [popularity_dict[i] for i in range(1, amount)]

    sca = SCA(amount, cachesize, popularity_dict)
    print("model-SCA: ", sca.totalHitRatio())

    che = Che(amount, cachesize, popularity_dict, rate)
    print("model-CHE: ", che.totalHitRatio())
    print("characteristic time: ", che.T)

    cache = lruCache(cachesize, amount, staleness)
    env = simpy.Environment()
    env.process(simulation(env, rate, content, popularity, cache))
    env.run(until=simulation_time)
    print("simulation: ", cache.totalHitRatio())


    hit_ratio_model_sca = []
    hit_ratio_model_che = []
    hit_ratio_sim = []
    index = []
    for i in range(1, 101):
        index.append(i)
        hit_ratio_sim.append(cache.hitRatio()[i])
        hit_ratio_model_sca.append(sca.hitRatio()[i])
        hit_ratio_model_che.append(che.hitRatio()[i])
    plt.plot(index, hit_ratio_sim, "+", label="simulation")
    plt.plot(index, hit_ratio_model_sca, label="model-SCA")
    plt.plot(index, hit_ratio_model_che, label="model-CHE")

    plt.xlabel("content ID")
    plt.ylabel("hit ratio")
    plt.grid(True)
    # plt.axis([0, 51, 0, 1])
    plt.legend()
    plt.show()