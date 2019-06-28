import simpy
import random
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mcav.zipf import Zipf
import numpy as np
from lru_simulator import Simulator
from lru_simulator_uniform import SimulatorUniform
from lru_simulator_exponential import SimulatorExponential

from model import Reactive, ProactiveRemove, ProactiveRenew
from model_uniform import ReactiveUniform, ProactiveRemoveUniform
from model_exponential import ReactiveExponential, ProactiveRemoveExponential

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
    expected_value = 20
    simulation_time = 50000
    # random.seed(42)
    zipf = Zipf(amount, z)

    # pattern = "reactive"
    # pattern = "proactive_remove"
    pattern = "proactive_renew"
    # pattern = "proactive_update_origin"

    popularity_dict = zipf.popularity()
    content = [i for i in range(1, amount + 1)]
    popularity = [popularity_dict[i] for i in range(1, amount)]

    index = []
    hit_ratio_model_reactive = []
    hit_ratio_model_proactive_remove = []
    hit_ratio_model_proactive_renew = []
    for cachesize in np.arange(155, 251, 5):
        index.append(cachesize)
        reactive = ReactiveUniform(amount, cachesize, total_rate, expected_value,
                            popularity_dict)
        hit_ratio_model_reactive.append(reactive.totalHitRatio())
        print("reactive ready!")

        proactive_remove = ProactiveRemoveUniform(amount, cachesize, total_rate, expected_value,
                            popularity_dict)
        hit_ratio_model_proactive_remove.append(proactive_remove.totalHitRatio())
        print("proactive_remove ready!")

        proactive_renew = ProactiveRenew(amount, cachesize, total_rate, expected_value,
                                   popularity_dict)
        hit_ratio_model_proactive_renew.append(proactive_renew.totalHitRatio())
        print("proactive_renew ready!")

        print(cachesize)

    print(hit_ratio_model_reactive)
    print(hit_ratio_model_proactive_remove)
    print(hit_ratio_model_proactive_renew)

    # plt.plot(index, hit_ratio_sim, "+", color="orangered", ms="6", label="simulation")
    plt.plot(index, hit_ratio_model_reactive, color="steelblue", linewidth="1.5", label="model: reactive")
    plt.plot(index, hit_ratio_model_proactive_remove, color="darkorange", linewidth="1.5", label="model: proactive remove")
    plt.plot(index, hit_ratio_model_proactive_renew, color="darkgreen", linewidth="1.5", label="model: proactive renew")

    # plt.plot(index, hit_ratio_model_uniform, label="model-uniform")
    # plt.plot(index, hit_ratio_model_exponential, label="model-exponential")

    plt.xlabel("staleness time", font1)
    plt.ylabel("hit probability", font1)
    plt.grid(True)
    # plt.axis([0, 41, 0, 0.2], font1)
    plt.legend(prop=font1)
    # plt.savefig("kan6.eps")
    plt.show()

