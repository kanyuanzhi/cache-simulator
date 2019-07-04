from scipy.integrate import quad
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import math
import random
from mcav.zipf import Zipf

from che import Che

if __name__ == "__main__":
    amount = 50
    z = 0.8
    cachesize = 60
    total_rate = 20
    Ts = 4
    simulation_time = 10000
    # random.seed(42)
    zipf = Zipf(amount, z)
    popularity_dict = zipf.popularity()
    content = [i for i in range(1, amount + 1)]
    popularity = [popularity_dict[i] for i in range(1, amount)]

    che = Che(amount, cachesize, zipf.popularity(), total_rate)

    result = []
    index = []

    for i in range(1, 50+1):
        result.append(che.hitRatio()[i])
        index.append(i)

    plt.plot(index,result)
    plt.show()