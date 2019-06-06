from scipy.optimize import fsolve
from math import exp

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
            temp = temp + 1 - exp(-self.rate * self.popularity[i] * t)
            # temp = temp + pow(math.e, i*t)
        f = temp - self.cachesize
        return f
    
    def _characteristicTime(self):
        T = fsolve(self._f1,[1])[0]
        return T
    
    def _hitRatio(self):
        hit_ratio = {}
        for i in range(1, self.amount+1):
            hit_ratio[i] = 1 - exp(-self.rate*self.popularity[i]*self.T)
        return hit_ratio
    
    def hitRatio(self):
        return self.hit_ratio
    
    def totalHitRatio(self):
        total = 0
        for i in range(1, self.amount+1):
            total = total + self.hit_ratio[i]*self.popularity[i]
        return total