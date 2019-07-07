import sys
sys.path.append('./src/model')
from scipy.optimize import fsolve
from model_validation import ValidationExponential
from mcav.zipf import Zipf
import math


class Mp0(object):
    def __init__(self,cachesize, amount, total_rate, expected_value, popularity):
        self.cachesize = cachesize
        self.amount = amount
        self.total_rate = total_rate
        self.ev = expected_value
        self.popularity = popularity
        self.validation_ratio = ValidationExponential(self.amount, self.total_rate, self.ev, self.popularity).validationRatio()
    
    def getMp0(self):
        print(ValidationExponential(self.amount, self.total_rate, self.ev, self.popularity).validationSize())
        def f(x):
            s = x
            for i in range(x+1, self.amount+1):
                s = s + self.validation_ratio[i]
            return (s - self.cachesize)

        Mp_max = self.amount
        Mp_min = 0
        Mp = Mp_max / 2
        temp = 0
        while True:
            result = f(int(Mp))
            print(result)
            if result == temp:
                break
            else:
                temp = result
                if result > 0:
                    Mp_max = Mp
                    Mp_min = Mp_min
                else:
                    Mp_max = Mp_max
                    Mp_min = Mp
                Mp = (Mp_max - Mp_min) / 2 + Mp_min
        return int(Mp)

if __name__ == "__main__":
    amount = 5000
    z = 0.8
    cachesize = 200
    total_rate = 20
    expected_value = 10
    N = 20
    simulation_time = 10000
    # random.seed(42)
    zipf = Zipf(amount, z)

    popularity_dict = zipf.popularity()
    content = [i for i in range(1, amount + 1)]
    popularity = [popularity_dict[i] for i in range(1, amount)]

    mp0 = Mp0(cachesize, amount, total_rate, expected_value, popularity_dict).getMp0()
    print(mp0)