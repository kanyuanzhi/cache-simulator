import simpy
import random
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mcav.zipf import Zipf
import numpy as np
from model import Model

if __name__ == "__main__":
    font1 = {
        'family': 'Arial',
        'size': 13,
    }

    font2 = {
        'family': 'Arial',
        'size': 15,
    }

    amount = 5000
    z = 0.8
    cachesize = 50
    total_rate = 20
    expected_value = 10

    N = 20
    simulation_time = 50000
    # random.seed(42)
    zipf = Zipf(amount, z)

    # pattern = "reactive"
    pattern = "proactive_remove"
    # pattern = "proactive_renew"
    pattern = "proactive_optional_renew"

    # distribution = "constant"
    # distribution = "uniform"
    distribution = "exponential"
    popularity_dict = zipf.popularity()
    content = [i for i in range(1, amount + 1)]
    popularity = [popularity_dict[i] for i in range(1, amount)]

    index = []
    hit_ratio_model_reactive = []
    hit_ratio_model_proactive_remove = []
    hit_ratio_model_proactive_renew = []
    hit_ratio_model_proactive_optional_renew = []
    load_model_reactive = []
    load_model_proactive_remove = []
    load_model_proactive_renew = []
    load_model_proactive_optional_renew = []
    i = 0
    for cachesize in range(50, 501, 25):
        # index.append(cachesize)
        # model1 = Model(amount, cachesize, total_rate, expected_value, popularity_dict, N, "reactive",
        #                distribution).getModel()
        # hit_ratio_model_reactive.append(model1.totalHitRatio())
        # load_model_reactive.append(model1.totalLoad())
        # print("reactive ready!")
        #
        # model2 = Model(amount, cachesize, total_rate, expected_value, popularity_dict, N, "proactive_remove",
        #                distribution).getModel()
        # hit_ratio_model_proactive_remove.append(model2.totalHitRatio())
        # load_model_proactive_remove.append(model2.totalLoad())
        # print("proactive_remove ready!")
        #
        # model3 = Model(amount, cachesize, total_rate, expected_value, popularity_dict, N, "proactive_renew",
        #                distribution).getModel()
        # hit_ratio_model_proactive_renew.append(model3.totalHitRatio())
        # load_model_proactive_renew.append(model3.totalLoad())
        #
        # print("proactive_renew ready!")
        #
        # model4 = Model(amount, cachesize, total_rate, expected_value, popularity_dict, N, "proactive_optional_renew",
        #                distribution).getModel()
        # hit_ratio_model_proactive_optional_renew.append(model4.totalHitRatio())
        # load_model_proactive_optional_renew.append(model4.totalLoad())
        # print("proactive_optional_renew ready!", hit_ratio_model_proactive_optional_renew[i])

        model4 = Model(amount, cachesize, total_rate, expected_value, popularity_dict, int(cachesize*0.2), "proactive_optional_renew",
                       distribution).getModel()
        hit_ratio_model_proactive_optional_renew.append(model4.totalHitRatio())
        load_model_proactive_optional_renew.append(model4.totalLoad())
        print("proactive_optional_renew ready!", hit_ratio_model_proactive_optional_renew[i])
        i = i + 1

        print(cachesize)

    print(hit_ratio_model_reactive)
    print(hit_ratio_model_proactive_remove)
    print(hit_ratio_model_proactive_renew)
    print(hit_ratio_model_proactive_optional_renew)

    print(load_model_reactive)
    print(load_model_proactive_remove)
    print(load_model_proactive_renew)
    print(load_model_proactive_optional_renew)

    # plt.plot(index, hit_ratio_sim, "+", color="orangered", ms="6", label="simulation")
    plt.plot(index, hit_ratio_model_reactive, color="steelblue", linewidth="1.5", label="model: reactive")
    plt.plot(index, hit_ratio_model_proactive_remove, color="darkorange", linewidth="1.5", label="model: proactive remove")
    plt.plot(index, hit_ratio_model_proactive_renew, color="darkgreen", linewidth="1.5", label="model: proactive renew")
    plt.plot(index, hit_ratio_model_proactive_optional_renew, color="red", linewidth="1.5", label="model: proactive optional renew")


    # plt.plot(index, hit_ratio_model_uniform, label="model-uniform")
    # plt.plot(index, hit_ratio_model_exponential, label="model-exponential")

    plt.xlabel("cache size", font1)
    plt.ylabel("hit probability", font1)
    plt.grid(True)
    # plt.axis([0, 41, 0, 0.2], font1)
    plt.legend(prop=font1)
    # plt.savefig("kan6.eps")
    plt.show()

