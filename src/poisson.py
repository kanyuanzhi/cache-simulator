from scipy import integrate
from scipy.optimize import fsolve

import math
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mcav.zipf import Zipf


def F(t):
    # return (math.exp(-rate * t)-math.exp(-rate * staleness)) * t
        # return t*rate*math.exp(-rate*t)
    return (1-math.exp(-rate*t))/Ts

def Fm(T, T0):
    return 1/(Ts-T0)/(Tz-Ts)*(1-math.exp(-rate*(T-T0)))

def Fr(T, T0):
    return 1/(Tz-T0)/Tz*(1-math.exp(-rate*(T-T0)))

def h(T0):
    return T0

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
            temp = temp + 1 - math.exp(-self.rate * self.popularity[i] * t)
            # temp = temp + pow(math.e, i*t)
        f = temp - self.cachesize
        return f
    
    def _characteristicTime(self):
        T = fsolve(self._f1,[1])[0]
        return T
    
    def _hitRatio(self):
        hit_ratio = {}
        for i in range(1, self.amount+1):
            hit_ratio[i] = 1 - math.exp(-self.rate*self.popularity[i]*self.T)
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
    total_rate = 10
    Ts = 5

    zipf = Zipf(amount, z)
    popularity = zipf.popularity()

    che = Che(amount, cachesize, popularity, total_rate)

    
    Tz = che.T
    print("Tz: ", Tz)
    # index = []
    # result = []
    # for i in range(1, 51):
    #     index.append(i)
    #     rate = total_rate * popularity[i]
    #     # result.append(
    #     #     integrate.quad(F, 0, Ts)[0] *
    #     #     (1 - math.exp(-rate * Ts)))
    #     result.append(integrate.quad(F, 0, Ts)[0])
    # for i in range(11):
    #     print(result[i])

    # plt.plot(index, result, "+-", label="simulation")
    # plt.xlabel("content ID")
    # plt.ylabel("hit ratio")
    # plt.grid(True)
    # # plt.axis([0, 51, 0, 1])
    # plt.legend()
    # plt.show()
    Wm = int(Tz / Ts) * float(Ts) / Tz
    Wl = (1 - Wm)/2
    Wr = (1 - Wm)/2
    print(Wm)
    index = []
    result = []
    
    for i in range(1, 51):
        index.append(i)
        rate = total_rate * popularity[i]
        # result.append(
        #     integrate.quad(F, 0, Ts)[0] *
        #     (1 - math.exp(-rate * Ts)))
        Pm = integrate.dblquad(lambda T,T0: 1/(Ts-T0)/(Tz-Ts)*(1-math.exp(-rate*(T-T0))),
                                0, 
                                Tz-Ts, 
                                lambda T0: T0, 
                                lambda T0: Ts)[0]
        Pr = integrate.dblquad(lambda T,T0: 1/(Tz-T0)/Tz*(1-math.exp(-rate*(T-T0))),
                                0, 
                                Tz, 
                                lambda T0: T0, 
                                lambda T0: Tz)[0]
        P = Wl * 1 + Wm * Pm + Wr*Pr
        result.append(P)
    for i in range(11):
        print(result[i])

    plt.plot(index, result, "+-", label="simulation")
    plt.xlabel("content ID")
    plt.ylabel("hit ratio")
    plt.grid(True)
    # plt.axis([0, 51, 0, 1])
    plt.legend()
    plt.show()