import simpy
import random
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mcav.zipf import Zipf
from simulator import Simulator

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
    cachesize = 100
    total_rate = 20
    N = 20
    # expected_value = 20
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
    for expected_value in range(2, 51, 2):
        index.append(expected_value)
        env = simpy.Environment()
        simulator = Simulator(env, cachesize, amount, expected_value, total_rate, content, popularity, N, pattern,
                              distribution).getSimulator()
        simulator.setDuration(0.01)
        simulator.setDelta(1000)
        env.process(simulator.updateSim())
        env.process(simulator.insertSim())
        env.run(until=simulation_time)
        hit_ratio.append(simulator.cache.totalHitRatio())
        load.append(simulator.cache.totalLoad())
        print("simulation: ", simulator.cache.totalHitRatio())

        print(expected_value)

    print(hit_ratio)
    print(load)
    # print(hit_ratio_model_proactive_remove)
    # print(hit_ratio_model_proactive_renew)

    # plt.plot(index, hit_ratio_sim, "+", color="orangered", ms="6", label="simulation")
    plt.plot(index, hit_ratio, color="steelblue", linewidth="1.5", label="model: reactive")
    # plt.plot(index, hit_ratio_model_proactive_remove, color="darkorange", linewidth="1.5", label="model: proactive remove")
    # plt.plot(index, hit_ratio_model_proactive_renew, color="darkgreen", linewidth="1.5", label="model: proactive renew")

    # plt.plot(index, hit_ratio_model_uniform, label="model-uniform")
    # plt.plot(index, hit_ratio_model_exponential, label="model-exponential")

    plt.xlabel("staleness time", font1)
    plt.ylabel("hit probability", font1)
    plt.grid(True)
    # plt.axis([0, 41, 0, 0.2], font1)
    plt.legend(prop=font1)
    # plt.savefig("kan6.eps")
    plt.show()

