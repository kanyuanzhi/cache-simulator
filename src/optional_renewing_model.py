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
from Mp0 import Mp0

if __name__ == "__main__":

    amount = 5000
    z = 0.8
    cachesize = 200
    total_rate = 20
    expected_value = 10
    N = 71
    simulation_time = 10000
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
    #
    # model = Model(amount, cachesize, total_rate, expected_value, popularity_dict, N, pattern, distribution).getModel()
    # print(model.totalHitRatio())
    # print(model.totalLoad())


    # N = np.arange(10,100,10)
    # cachesize = np.arange(100, 200, 10)
    # N, cachesize = np.meshgrid(N, cachesize)
    # model = Model(amount, cachesize, total_rate, expected_value, popularity_dict, N, pattern, distribution).getModel()
    # hit_ratio = model.totalHitRatio()
    # load = model.totalLoad()
    # Z = hit_ratio/load
    # fig = plt.figure()
    # ax = Axes3D(fig)
    # ax.plot_surface(N, cachesize, Z, rstride=1, cstride=1, cmap='rainbow')
    # plt.show()
    hit_ratio_list = []
    load_list = []
    # for cachesize in range(100, 501, 100):
    #     hit_ratio = []
    #     load = []
    #     index = []
    #     for r in np.arange(1.5, 1.6, 0.1):
    #         index.append(r)
    #         model = Model(amount, cachesize, total_rate, expected_value, popularity_dict, int(r*cachesize), pattern, distribution).getModel()
    #         hit_ratio.append(model.totalHitRatio())
    #         load.append(model.totalLoad())
    #         print("cachesize - r: ", cachesize, r)
    #     hit_ratio_list.append(hit_ratio)
    #     load_list.append(load)

            

    for cachesize in range(175, 551, 25):
        mp0 = Mp0(cachesize, amount, total_rate, expected_value, popularity_dict).getMp0()
        index.append(mp0/cachesize)
        print(mp0)
        model = Model(amount, cachesize, total_rate, expected_value, popularity_dict, mp0, pattern, distribution).getModel()
        hit_ratio.append(model.totalHitRatio())
        load.append(model.totalLoad())
        print("cachesize - mp0: ", cachesize, mp0)
    print(index)

    print(hit_ratio)
    print(load)

    # print(hit_ratio_list)
    # print(load_list)

    font1 = {
        'family': 'Arial',
        'size': 13,
    }

    font2 = {
        'family': 'Arial',
        'size': 10,
    }

    # plt.figure("1")
    # for i in range(len(hit_ratio_list)):
    #     plt.plot(index, hit_ratio_list[i])
    # plt.figure("2")
    # for i in range(len(load_list)):
    #     plt.plot(index, load_list[i])
    #
    # plt.show()


    plt.figure("1")
    plt.plot(index, hit_ratio)
    plt.figure("2")
    plt.plot(index, load)

    plt.xlabel("content ID", font1)
    plt.ylabel("hit probability", font1)
    plt.grid(True)
    # plt.axis([0, 51, 0, 1], font2)
    plt.legend(prop=font2)
    # plt.savefig("kan6.eps")
    plt.show()