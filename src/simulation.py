import simpy
import math
import random
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mcav.sca import SCA


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

    def insert(self, item, now):
        if item in self.stack:
            if now - self.updatetime_in_cache[item] < self.staleness:
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

            # if item not in self.updatetime:
            #     # self.updatetime[item] = now

            self.updatetime_in_cache[item] = self.updatetime[item]

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

    def update(self, now):
        # for i in range(1, self.amount +1 ):
        #     if i in self.updatetime:
        #         if now - self.updatetime[i] >= self.staleness:
        #             self.updatetime[i] = now
        for i in range(1, self.amount + 1):
            if now - self.updatetime[i] >= self.staleness:
                self.updatetime[i] = self.updatetime[i] + self.staleness
                # if i in self.stack:
                #     self.stack.remove(i)

        # if 1 in self.updatetime:
        #     print(self.updatetime[1])


def simulation(env, rate, content, popularity, cache, staleness):
    flag = True
    print_flag = True
    while True:
        item = random_pick(content, popularity)
        cache.update(env.now)
        cache.insert0(item, env.now)
        duration = random.expovariate(rate)
        
        # if int(env.now *10 ) % 10 == 0 and flag:
        #     cache.update(env.now)
        #     print(env.now)
        #     # print(len(cache.stack))
        #     flag = False
        # if int(env.now *10 ) % 10 != 0:
        #     flag = True
            # if int(env.now) > 20:
            #     print("simulation: ",cache.totalHitRatio())
        if int(env.now) % 2000 == 0 and print_flag:
            print(env.now)
            print_flag = False
        if int(env.now)% 2000 != 0 and not print_flag:
            print_flag = True
        yield env.timeout(duration)


class SCAV(object):
    # realize the SCA algorithm
    def __init__(self, amount, size, popularity, rate, time):
        self._amount = amount
        self._size = size
        self._alpha = popularity
        self._P = {}
        # self._P[1] = self._alpha
        self._B = {}
        self._request_rate = rate
        self._staleness_time = time
        self._validation_rate = self._validationRate()
        self._validation_probability = self._validationProbability()
        self._P[1] = self._computeP1()
        self._original_hit_ratio = {}
        self._hitRatio()

    def originalHitRatio(self):
        return self._original_hit_ratio

    def hitRatio(self):
        return self._B[self._size]

    def totalHitRatio(self):
        total_hit_ratio = 0.0
        for i in range(1, self._amount + 1):
            total_hit_ratio = total_hit_ratio + \
                self._alpha[i]*self._B[self._size][i]
        return total_hit_ratio

    def _hitRatio(self):
        for i in range(1, self._size + 1):
            self._computeB(i)
            i = i + 1
            if i <= self._size:
                self._computeP(i)
        for i in range(1, self._amount + 1):
            self._original_hit_ratio[i] = self._B[self._size][i]
            self._B[self._size][i] = self._B[
                self._size][i] * self._validation_probability[i]

    def _computeP(self, position):
        # position starts from 2
        p = {}
        molecule = []
        denominator = 0.0
        for i in range(1, self._amount + 1):
            denominator = denominator + \
                self._nonNegative(
                    self._alpha[i] * (1 - self._B[position-1][i]))
        for i in range(1, self._amount + 1):
            molecule = self._nonNegative(self._alpha[i] *
                                         (1 - self._B[position - 1][i]))
            p[i] = molecule / denominator
            # p[i] = molecule / denominator

        self._P[position] = p
        # print p
        # print sum(p.values())
        # print "-----=------"

    def _computeB(self, position):
        # position starts from 1
        b = {}
        for i in range(1, self._amount + 1):
            b[i] = 0.0
            for j in range(1, position + 1):
                b[i] = b[i] + self._P[j][i]
        self._B[position] = b

    def _nonNegative(self, number):
        if number > 0:
            return number
        else:
            return 0.0

    # def _validationProbability(self):
    #     VP = {}
    #     for i in range(1, self._amount + 1):
    #         vp = {}
    #         for j in range(1, self._size + 1):
    #             vp[j] = 1 - pow(
    #                 e, -self._validation_rate[i] * self._staleness_time *
    #                 (1 - pow(e, -(j - 1))))
    #             # vp[j] = 1-pow(e,-self._validation_rate[i]*self._staleness_time*j/self._size)
    #         VP[i] = vp
    #     return VP

    def _validationProbability(self):
        vp = {}
        for i in range(1, self._amount + 1):
            vp[i] = self._staleness_time * self._validation_rate[i] / (
                self._staleness_time * self._validation_rate[i] + 1)
            # vp[i] = self._staleness_time / 13.39
            # vp[i] = self._staleness_time/(self._staleness_time + 1/self._validation_rate[i]*(1-math.pow(math.e, -self._staleness_time*self._validation_rate[i])))
            # vp = {}
            # for j in range(1, self._size + 1):
            #     vp[j] = 1 - pow(
            #         e, -self._validation_rate[i] * self._staleness_time *
            #         (1 - pow(e, -(j - 1))))
            #     # vp[j] = 1-pow(e,-self._validation_rate[i]*self._staleness_time*j/self._size)
        return vp

    def _validationRate(self):
        validation_rate = {}
        for i in range(1, self._amount + 1):
            validation_rate[i] = self._alpha[i] * self._request_rate
        return validation_rate

    def _computeP1(self):
        P1 = {}
        for i in range(1, self._amount + 1):
            P1[i] = self._alpha[i]
            # P1[i] = self._alpha[i]
        return P1


if __name__ == "__main__":

    amount = 1000
    z = 0.8
    cachesize = 100
    rate = 10
    staleness = 20
    simulation_time = 10000
    # random.seed(42)
    zipf = Zipf(amount, z)
    popularity_dict = zipf.popularity()
    content = [i for i in range(1, amount + 1)]
    popularity = [popularity_dict[i] for i in range(1, amount)]

    cache = lruCache(cachesize, amount, staleness)

    env = simpy.Environment()
    env.process(simulation(env, rate, content, popularity, cache, staleness))
    env.run(until=simulation_time)

    print("simulation: ", cache.totalHitRatio())

    scav = SCAV(amount, cachesize, popularity_dict, rate, staleness)
    # ratio_validation = scav.hitRatio()
    print("model: ", scav.totalHitRatio())

    hit_ratio_model = []
    hit_ratio_model_original = []
    hit_ratio_sim = []
    index = []
    for i in range(1, 101):
        index.append(i)
        hit_ratio_sim.append(cache.hitRatio()[i])
        hit_ratio_model.append(scav.hitRatio()[i])
        hit_ratio_model_original.append(scav.originalHitRatio()[i])
    plt.plot(index, hit_ratio_sim, "+", label="simulation")
    plt.plot(index, hit_ratio_model, label="model")
    plt.plot(index, hit_ratio_model_original, label="model-original")


    plt.xlabel("content ID")
    plt.ylabel("hit ratio")
    plt.grid(True)
    # plt.axis([0, 51, 0, 1])
    plt.legend()
    plt.show()