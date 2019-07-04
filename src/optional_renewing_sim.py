import simpy
import random
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from mcav.zipf import Zipf
from simulator import Simulator
from model import Model
# from math import round
from new_simulator import NewSimulator


if __name__ == "__main__":

    amount = 5000
    z = 0.8
    cachesize = 100
    total_rate = 20
    expected_value = 10
    N = 20
    simulation_time = 5000
    # random.seed(42)
    zipf = Zipf(amount, z)

    # pattern = "reactive"
    # pattern = "proactive_remove"
    # pattern = "proactive_renew"
    pattern = "proactive_optional_renew"

    # distribution = "constant"
    # distribution = "uniform"
    distribution = "exponential"


    popularity_dict = zipf.popularity()
    content = [i for i in range(1, amount + 1)]
    popularity = [popularity_dict[i] for i in range(1, amount)]
    index = []
    hit_ratio = []
    load = []

    new_simulator = NewSimulator(cachesize, amount, expected_value, total_rate, z, 30, pattern, simulation_time)
    print(new_simulator.cache.totalHitRatio())
    print(new_simulator.cache.totalLoad()/float(simulation_time))

    for N in range(10, 151, 10):
        new_simulator = NewSimulator(cachesize, amount, expected_value, total_rate, z, N, pattern, simulation_time)
        hit_ratio.append(new_simulator.cache.totalHitRatio())
        load.append(new_simulator.cache.totalLoad()/float(simulation_time))
        index.append(N)
        print("N: ", N)

    print(hit_ratio)
    print(load)


    font1 = {
        'family': 'Arial',
        'size': 13,
    }

    font2 = {
        'family': 'Arial',
        'size': 15,
    }
    font1 = {
        'family': 'Arial',
        'size': 16,
    }

    font2 = {
        'family': 'Arial',
        'size': 20,
    }

    plt.figure("1")
    plt.plot(index, hit_ratio)
    plt.figure("2")
    plt.plot(index, load)

    plt.xlabel("content ID", font2)
    plt.ylabel("hit probability", font2)
    plt.grid(True)
    # plt.axis([0, 51, 0, 1], font2)
    plt.legend(prop=font2)
    # plt.savefig("kan6.eps")
    plt.show()