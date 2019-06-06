from scipy import integrate
from scipy.optimize import fsolve

import math
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mcav.zipf import Zipf

from che import Che


def F(t):
    # return (math.exp(-rate * t)-math.exp(-rate * staleness)) * t
        # return t*rate*math.exp(-rate*t)
    return (1-math.exp(-rate*t))/Ts

def F2(t):
    # return (math.exp(-rate * t)-math.exp(-rate * staleness)) * t
        # return t*rate*math.exp(-rate*t)
    return (1-math.exp(-rate*t))/Tc


if __name__ == "__main__":
    amount = 1000
    z = 0.8
    cachesize = 100
    total_rate = 10
    Ts = 20

    zipf = Zipf(amount, z)
    popularity = zipf.popularity()

    che = Che(amount, cachesize, popularity, total_rate)
    print(total_rate*popularity[1], total_rate*popularity[2])

    
    Tc = che.T
    print("Tc: ", Tc)
    
    index = []
    result = []
    for i in range(1, 51):
        index.append(i)
        rate = total_rate * popularity[i]
        # result.append(
        #     integrate.quad(F, 0, Ts)[0] *
        #     (1 - math.exp(-rate * Ts)))
        Pv = integrate.quad(F, 0, Ts)[0]
        # result.append(integrate.quad(F, 0, Ts)[0])
        result.append(Tc/Ts*integrate.quad(F2, 0, Tc)[0] + (1-Tc/Ts)*(1-math.exp(-rate*Tc)))
    for i in range(11):
        print(result[i])

    plt.plot(index, result, "+-", label="simulation")
    plt.xlabel("content ID")
    plt.ylabel("hit ratio")
    plt.grid(True)
    # plt.axis([0, 51, 0, 1])
    plt.legend()
    plt.show()