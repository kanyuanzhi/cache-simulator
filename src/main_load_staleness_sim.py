import simpy
import random
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mcav.zipf import Zipf
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
    # expected_value = 20
    simulation_time = 10000
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
    load_sim_proactive_renew = []
    for expected_value in range(4, 41, 2):
        index.append(expected_value)
        env = simpy.Environment()
        simulator = Simulator(env, cachesize, amount, expected_value, total_rate,
                              content, popularity, "proactive_renew")
        # simulator = SimulatorUniform(env, cachesize, amount, expected_value, total_rate,
        #                       content, popularity, "proactive_remove")
        # simulator = SimulatorExponential(env, cachesize, amount, expected_value, total_rate,
        #                              content, popularity, pattern)
        env.process(simulator.updateSim())
        env.process(simulator.insertSim())
        env.run(until=simulation_time)
        load_sim_proactive_renew.append(simulator.cache.totalLoad()/10000)

        print(expected_value)

    print(load_sim_proactive_renew)
    # print(hit_ratio_model_proactive_remove)
    # print(hit_ratio_model_proactive_renew)

    # plt.plot(index, hit_ratio_sim, "+", color="orangered", ms="6", label="simulation")
    plt.plot(index, load_sim_proactive_renew, color="steelblue", linewidth="1.5", label="model: reactive")
    # plt.plot(index, hit_ratio_model_proactive_remove, color="darkorange", linewidth="1.5", label="model: proactive remove")
    # plt.plot(index, hit_ratio_model_proactive_renew, color="darkgreen", linewidth="1.5", label="model: proactive renew")

    # plt.plot(index, hit_ratio_model_uniform, label="model-uniform")
    # plt.plot(index, hit_ratio_model_exponential, label="model-exponential")

    plt.xlabel("staleness time", font1)
    plt.ylabel("load", font1)
    plt.grid(True)
    # plt.axis([0, 41, 0, 0.2], font1)
    plt.legend(prop=font1)
    # plt.savefig("kan6.eps")
    plt.show()

    # reactive = ReactiveUniform(amount, cachesize, total_rate, expected_value,
    #                     popularity_dict)
    # # reactive = ReactiveExponential(amount, cachesize, total_rate, expected_value,
    # #                            popularity_dict)
    # print("model: ", reactive.totalHitRatio())
    # print("Tc: ", reactive.Che().T)
    # print("model ready!")

    # proactive = ProactiveRemove(amount, cachesize, total_rate, expected_value,
    #                     popularity_dict)
    # # proactive = ProactiveRemoveUniform(amount, cachesize, total_rate, expected_value,
    # #                     popularity_dict)
    # # proactive = ProactiveRemoveExponential(amount, cachesize, total_rate, expected_value,
    # #                            popularity_dict)
    # print("model: ", proactive.totalHitRatio())
    # print("Tc: ", proactive.Che().T)
    # print("Tc0: ", proactive.Tc0())
    # print("model ready!")

    # proactive = ProactiveRenew(amount, cachesize, total_rate, expected_value,
    #                     popularity_dict)
    # print("model: ", proactive.totalHitRatio())
    # print("Tc: ", proactive.Che().T)
    # print("model ready!")
    #
    # env = simpy.Environment()
    # simulator = Simulator(env, cachesize, amount, expected_value, total_rate,
    #                       content, popularity, pattern)
    # # simulator = SimulatorUniform(env, cachesize, amount, expected_value, total_rate,
    # #                       content, popularity, pattern)
    # # simulator = SimulatorExponential(env, cachesize, amount, expected_value, total_rate,
    # #                              content, popularity, pattern)
    # env.process(simulator.updateSim())
    # env.process(simulator.insertSim())
    # env.run(until=simulation_time)
    # print("simulation: ", simulator.cache.totalHitRatio())
    #
    # print("error: ", (simulator.cache.totalHitRatio()-proactive.totalHitRatio())/simulator.cache.totalHitRatio())
    #
    #
    # # reactive_uniform = ReactiveUniform(amount,cachesize,total_rate,expected_value,popularity_dict)
    # # print("reactive uniform ready!")
    # # reactive_exponential = ReactiveExponential(amount, cachesize, total_rate, expected_value, popularity_dict)
    # # print("reactive exponential ready!")
    #
    # index = []
    # hit_ratio_sim = []
    # hit_ratio_model = []
    # hit_ratio_model_uniform = []
    # hit_ratio_model_exponential = []
    # for i in range(1, 51):
    #     index.append(i)
    #     hit_ratio_sim.append(simulator.cache.hitRatio()[i])
    #     # hit_ratio_model.append(reactive.hitRatio()[i])
    #     hit_ratio_model.append(proactive.hitRatio()[i])
    #
    #     # hit_ratio_model_uniform.append(reactive_uniform.hitRatio()[i])
    #     # hit_ratio_model_exponential.append(reactive_exponential.hitRatio()[i])
    #
    #
    #
    # plt.plot(index, hit_ratio_sim, "+", color="orangered",ms="6", label="simulation")
    # plt.plot(index, hit_ratio_model, color="steelblue", linewidth="1.5", label="model")
    # # plt.plot(index, hit_ratio_model_uniform, label="model-uniform")
    # # plt.plot(index, hit_ratio_model_exponential, label="model-exponential")
    #
    # plt.xlabel("content ID", font2)
    # plt.ylabel("hit probability", font2)
    # plt.grid(True)
    # plt.axis([0, 51, 0, 1], font2)
    # plt.legend(prop=font2)
    # # plt.savefig("kan6.eps")
    # plt.show()