from scipy import integrate
import math
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mcav.zipf import Zipf


def F(t):
    # return (math.exp(-rate * staleness) - math.exp(-rate * t)) * t
    return -(1-math.exp(-rate*staleness))*rate*t*math.exp(-rate*t)

if __name__ == "__main__":
    amount = 1000
    z = 0.8
    total_rate = 10
    staleness = 5

    zipf = Zipf(amount, z)
    popularity = zipf.popularity()

    index = []
    result = []
    for i in range(1, 51):
        index.append(i)
        rate = total_rate * popularity[i]
        # result.append(
        #     integrate.quad(F, 0, staleness)[0] *
        #     (1 - math.exp(-rate * staleness)))
        result.append(integrate.quad(F, 0, staleness)[0])
    for i in range(11):
        print(result[i])

    plt.plot(index, result, "+-", label="simulation")
    plt.xlabel("content ID")
    plt.ylabel("hit ratio")
    plt.grid(True)
    # plt.axis([0, 51, 0, 1])
    plt.legend()
    plt.show()