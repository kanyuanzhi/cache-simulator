import simpy
import math
import random
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mcav.sca import SCA
from mcav.zipf import Zipf
from lru_simulator import Simulator
from scipy import integrate


class SCAV(object):
    # realize the SCA algorithm
    def __init__(self, amount, size, popularity, rate, time):
        self._amount = amount
        self._size = size
        self._alpha = popularity
        self._P = {}
        # self._P[1] = self._alpha
        self._B = {}
        self._total_rate = rate
        self._request_rate = self._requestRate()
        self._staleness_time = time
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
            # delta_t = self._staleness_time * math.exp(-self._request_rate[i]*self._staleness_time)
            # if self._staleness_time - delta_t < 1/self._request_rate[i]:
            #     vp[i] = (1-math.exp(-self._request_rate[i]*self._staleness_time))/(math.exp(-self._request_rate[i]*self._staleness_time)+1/self._request_rate[i]/self._staleness_time)
            # else:
            #     vp[i] = 1-math.exp(-self._request_rate[i]*self._staleness_time)

            vp[i] = self._staleness_time * self._request_rate[i] / (
                self._staleness_time * self._request_rate[i] + 1)

            # vp[i] = 1 - (1 - (self._request_rate[i] * self._staleness_time + 1) *
            #          math.exp(-self._request_rate[i] * self._staleness_time)
            #          ) / (self._request_rate[i]**
            #               2) / self._staleness_time * (1 - math.exp(
            #                   -self._request_rate[i] * self._staleness_time))
            # rate = self._request_rate[i]
            # vp[i] = integrate.quad(F, 0, self._staleness_time)[0] * (1 - math.exp(-rate * self._staleness_time)) / self._staleness_time
        return vp

    def _requestRate(self):
        request_rate = {}
        for i in range(1, self._amount + 1):
            request_rate[i] = self._alpha[i] * self._total_rate
        return request_rate

    def _computeP1(self):
        P1 = {}
        for i in range(1, self._amount + 1):
            P1[i] = self._alpha[i]
            # P1[i] = self._alpha[i]
        return P1

def F(t):
    return t * math.exp(-rate * t)


if __name__ == "__main__":

    amount = 1000
    z = 0.8
    cachesize = 100
    rate = 10
    staleness = 10
    simulation_time = 10000
    # random.seed(42)
    zipf = Zipf(amount, z)

    popularity_dict = zipf.popularity()
    content = [i for i in range(1, amount + 1)]
    popularity = [popularity_dict[i] for i in range(1, amount)]

    env = simpy.Environment()
    simulator = Simulator(env, cachesize, amount, staleness, rate, content,
                          popularity)
    env.process(simulator.updateSim())
    env.process(simulator.insertSim())
    env.run(until=simulation_time)
    print("simulation: ", simulator.cache.totalHitRatio())

    scav = SCAV(amount, cachesize, popularity_dict, rate, staleness)
    print("model: ", scav.totalHitRatio())

    validation_rate_under_hit = []
    validation_rate = []

    hit_ratio_model = []
    hit_ratio_model_original = []
    hit_ratio_sim = []
    hit_ratio_sim_original = []
    index = []
    for i in range(1, 101):
        index.append(i)
        hit_ratio_sim.append(simulator.cache.hitRatio()[i])
        hit_ratio_sim_original.append(simulator.cache.originalHitRatio()[i])
        hit_ratio_model.append(scav.hitRatio()[i])
        hit_ratio_model_original.append(scav.originalHitRatio()[i])
        validation_rate_under_hit.append(simulator.cache.validationRateUnderHit()[i])
        validation_rate.append(simulator.cache.validationRate()[i])
    
    print('%s : %s : %s : %s'%('有效|命中', '有效','有效且命中', '命中'))
    for i in range(0, 11):
        print('%.3f : %.6f : %.6f : %.3f' %(validation_rate_under_hit[i],validation_rate[i], hit_ratio_sim[i],hit_ratio_sim_original[i]) )
        # print(validation_rate_under_hit[i], " : ", validation_rate[i])


    plt.plot(index, hit_ratio_sim, "+", label="simulation")
    plt.plot(index, hit_ratio_sim_original, "*", label="simulation-original")

    plt.plot(index, hit_ratio_model, label="model")
    plt.plot(index, hit_ratio_model_original, label="model-original")
    plt.xlabel("content ID")
    plt.ylabel("hit ratio")
    plt.grid(True)
    # plt.axis([0, 51, 0, 1])
    plt.legend()
    plt.show()