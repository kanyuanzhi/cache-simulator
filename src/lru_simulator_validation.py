import simpy
import numpy as np
import random
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mcav.zipf import Zipf
from scipy.integrate import quad 
from math import exp
from che import Che

class LRUCache(object):
    def __init__(self, size, amount, staleness, pattern="normal"):
        # pattern options: normal, reactive, proactive_delete, proactive_update_origin, proactive_update_top 
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
        self.validation_time = {}
        self.validation_time_in_cache = {}


        self.pattern = pattern

        self.val = {}
        self.inval = {}
        self.vt = []

        for i in range(1, amount + 1):
            self.val[i] = 0
            self.inval[i] = 0
            #self.updatetime[i] = random.uniform(-staleness, 0)
            self.validation_time[i] = np.random.uniform(0, 2*staleness)
            # self.validation_time[i] = staleness
            self.validation_time_in_cache[i] = self.validation_time[i]
            # self.updatetime[i] = np.random.uniform(-self.validation_time[i], 0)
            self.updatetime[i] = 0
            
            self.updatetime_in_cache[i] = self.updatetime[i]

    def insert(self, item, now):
        if now - self.updatetime_in_cache[item] < self.validation_time_in_cache[item]:
            self.val[item] = self.val[item] + 1
        else:
            self.inval[item] = self.inval[item] + 1
            self.updatetime_in_cache[item] = self.updatetime[item]
            self.validation_time_in_cache[item] = self.validation_time[item]

    def update(self, now):
        for i in range(1, self.amount + 1):
            if now - self.updatetime[i] >= self.validation_time[i]:
                self.updatetime[i] = self.updatetime[i] + self.validation_time[i]
                self.validation_time[i] = np.random.uniform(0, 2*self.staleness)
                # self.validation_time[i] = self.staleness

    def validationRatio(self):
        validation_ratio = {}
        for i in range(1, self.amount):
            if self.val[i] == 0 and self.inval[i] == 0:
                validation_ratio[i] = 0
            else:
                validation_ratio[i] = float(self.val[i]) / (self.val[i] + self.inval[i])
        return validation_ratio
    
    def totalRatio(self):
        total_val = 0
        total_inval = 0
        for i in range(1, self.amount):
            total_val = total_val + self.val[i]
            total_inval = total_inval + self.inval[i]
        return float(total_val/(total_val+total_inval))



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
            duration = 0.1
            yield self.env.timeout(duration)


    def insertSim(self):
        print_flag = True
        while True:
            item = self._random_pick(self.content, self.popularity)
            self.cache.insert(item,self.env.now)
            # print(self.cache.cacheSize())
            duration = random.expovariate(self.rate)
            if int(self.env.now) % 2000 == 0 and print_flag:
                print(self.env.now)
                print_flag = False
            if int(self.env.now) % 2000 != 0 and not print_flag:
                print_flag = True
            yield self.env.timeout(duration)
    
    def _random_pick(self, some_list, probabilities):
        x = np.random.uniform(0, 1)
        cumulative_probability = 0.0
        for item, item_probability in zip(some_list, probabilities):
            cumulative_probability += item_probability
            if x < cumulative_probability: break
        return item

class Reactive(object):
    def __init__(self, amount, cachesize, total_rate, Ts, popularity):
        self._amount = amount
        self._popularity = popularity
        self._total_rate = total_rate
        self._che = Che(amount, cachesize, self._popularity, total_rate)
        self._Ts = Ts
        self._rate = self._requestRate()
        self._hit_ratio = self._hitRatio()
    
    def _requestRate(self):
        rr = {}
        for i in range(1, self._amount+1):
            rr[i] = self._total_rate * self._popularity[i]
        return rr
    
    def _hitRatio(self):
        Tc = self._che.T
        Ts = self._Ts
        hit_ratio = {}
        for i in range(1, self._amount+1):
            rate = self._rate[i]
            hit_ratio[i] = quad(self._F(rate, Ts, Tc).F1, 0, Ts)[0]
        return hit_ratio

    def hitRatio(self):
        return self._hit_ratio

    def totalHitRatio(self):
        thr = 0
        for i in range(1, self._amount+1):
            thr = thr + self._popularity[i]*self._hit_ratio[i]
        return thr

    def Che(self):
        return self._che
    
    def totalLoad(self):
        return self._total_rate*(1-self.totalHitRatio())

    class _F(object):
        def __init__(self, rate, Ts, Tc):
            self._rate = rate
            self._Ts = Ts
            self._Tc = Tc

        def F1(self, t):
            return (1-exp(-self._rate*t))/self._Ts

        def F2(self, t):
            return (1-exp(-self._rate*t))

class ReactiveUniform(object):
    def __init__(self, amount, cachesize, total_rate, expected_value,
                 popularity):
        self._amount = amount
        self._popularity = popularity
        self._total_rate = total_rate
        self._che = Che(amount, cachesize, self._popularity, total_rate)
        self._ev = expected_value
        self._rate = self._requestRate()
        self._hit_ratio = self._hitRatio()

    def _requestRate(self):
        rr = {}
        for i in range(1, self._amount + 1):
            rr[i] = self._total_rate * self._popularity[i]
        return rr

    def _hitRatio(self):
        Tc = self._che.T
        ev = self._ev
        hit_ratio = {}
        for i in range(1, self._amount + 1):
            rate = self._rate[i]
            F = self._F(rate, ev, Tc)
            a = quad(F.F1, 0, 2 * ev)
            hit_ratio[i] = a[0]
            # hit_ratio[i] = 1/(2*rate*rate*ev*ev)*(1-exp(-2*rate*ev))-1/(rate*ev)+1
        return hit_ratio

    def hitRatio(self):
        return self._hit_ratio

    def totalHitRatio(self):
        thr = 0
        for i in range(1, self._amount + 1):
            thr = thr + self._popularity[i] * self._hit_ratio[i]
        return thr

    def Che(self):
        return self._che

    def totalLoad(self):
        return self._total_rate * (1 - self.totalHitRatio())
    
    def h(self, x):
        return x

    def g(self, x):
        return 0

    class _F(object):
        def __init__(self, rate, ev, Tc):
            self._rate = rate
            self._ev = ev
            self._Tc = Tc

        def F1(self, Tv):
            return (Tv + exp(-self._rate * Tv)/self._rate - 1/self._rate) / (2*self._ev*self._ev)

        def F2(self, Tv):
            return (self._Tc + exp(-self._rate * self._Tc)/self._rate - 1/self._rate) / (2 * self._ev * Tv)
        
        def F3(self, Tv):
            return (Tv - self._Tc) * (1 - exp(-self._rate * self._Tc)) / (2 * self._ev * Tv)

if __name__ == "__main__":

    amount = 100
    z = 0.8
    cachesize = 50
    total_rate = 10
    Ts = 10
    simulation_time = 10000
    # np.random.seed(42)
    zipf = Zipf(amount, z)

    pattern = "reactive"
    # pattern = "proactive_delete"
    # pattern = "proactive_update_top"
    # pattern = "proactive_update_origin"

    popularity_dict = zipf.popularity()
    content = [i for i in range(1, amount + 1)]
    popularity = [popularity_dict[i] for i in range(1, amount)]

    env = simpy.Environment()
    simulator = Simulator(env, cachesize, amount, Ts, total_rate, content,
                          popularity, pattern)
    env.process(simulator.updateSim())
    env.process(simulator.insertSim())
    env.run(until=simulation_time)

    

    reactive = Reactive(amount,cachesize,total_rate,Ts,popularity_dict)
    reactive_uniform = ReactiveUniform(amount,cachesize,total_rate,Ts,popularity_dict)

    print("sim: ", simulator.cache.totalRatio())
    print("model: ", reactive.totalHitRatio())
    print("model-uniform: ", reactive_uniform.totalHitRatio())


    index = []
    value_sim = []
    vt_sim = simulator.cache.vt
    value_model = []
    value_model_uniforrm = []

    
    
    for i in range(1, 51):
        index.append(i)
        value_sim.append(simulator.cache.validationRatio()[i])
        value_model.append(reactive.hitRatio()[i])
        value_model_uniforrm.append(reactive_uniform.hitRatio()[i])

    plt.plot(index, value_sim, "+",color="black", label="simulation")
    plt.plot(index, value_model, label="model")
    plt.plot(index, value_model_uniforrm, label="model-uniform")




    plt.xlabel("content ID")
    plt.ylabel("validation ratio")
    plt.grid(True)
    # plt.axis([0, 51, 0, 1])
    plt.legend()
    plt.show()

