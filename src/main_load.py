import simpy
import random
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mcav.zipf import Zipf
from lru_simulator import Simulator
from scipy import integrate
from model import Reactive, ProactiveRemove, ProactivePublish

if __name__ == "__main__":

    amount = 1000
    z = 0.8
    cachesize = 100
    total_rate = 20
    Ts = 5
    simulation_time = 10000
    # random.seed(42)
    zipf = Zipf(amount, z)

    # pattern = "reactive"
    # pattern = "proactive_delete"
    # pattern = "proactive_update_top"
    pattern = "proactive_update_origin"

    popularity_dict = zipf.popularity()
    content = [i for i in range(1, amount + 1)]
    popularity = [popularity_dict[i] for i in range(1, amount)]

    total_load = []
    index = []

    for Ts in range(5,50,1):
        index.append(Ts)
        proactive_publish = ProactivePublish(amount,cachesize,total_rate,Ts,popularity_dict)
        total_load.append(proactive_publish.totalLoad())


    # plt.plot(index, total_load, "+", label="simulation")
    # plt.plot(index, hit_ratio_sim_original, "*", label="simulation-original")
    # plt.plot(index, hit_ratio_model_reactive, label="model-reactive")
    # plt.plot(index, hit_ratio_model_original, label="model-original")
    # plt.plot(index, hit_ratio_model_pd, label="model-proactive-delete")
    plt.plot(index, total_load, label="model-proactive-publish")

    plt.xlabel("rate")
    plt.ylabel("total load")
    plt.grid(True)
    # plt.axis([0, 51, 0, 1])
    plt.legend()
    plt.show()