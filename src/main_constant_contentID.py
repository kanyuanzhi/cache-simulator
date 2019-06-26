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
from model_uniform_exponential import ReactiveExponential, ProactiveRemoveExponential

if __name__ == "__main__":

    amount = 5000
    z = 0.8
    cachesize = 100
    total_rate = 20
    expected_value = 10
    simulation_time = 10000
    # random.seed(42)
    zipf = Zipf(amount, z)

    pattern = "reactive"
    # pattern = "proactive_remove"
    # pattern = "proactive_renew"
    # pattern = "proactive_update_origin"

    popularity_dict = zipf.popularity()
    content = [i for i in range(1, amount + 1)]
    popularity = [popularity_dict[i] for i in range(1, amount)]

    env = simpy.Environment()
    simulator = Simulator(env, cachesize, amount, expected_value, total_rate,
                          content, popularity, pattern)
    # simulator = SimulatorUniform(env, cachesize, amount, expected_value, total_rate,
    #                       content, popularity, pattern)
    env.process(simulator.updateSim())
    env.process(simulator.insertSim())
    env.run(until=simulation_time)
    print("simulation: ", simulator.cache.totalHitRatio())

    reactive = Reactive(amount, cachesize, total_rate, expected_value,
                        popularity_dict)
    # reactive = ReactiveUniform(amount, cachesize, total_rate, expected_value,
    #                     popularity_dict)
    
    print("model: ", reactive.totalHitRatio())
    print("Tc: ", reactive.Che().T)
    print("model ready!")
    # reactive_uniform = ReactiveUniform(amount,cachesize,total_rate,expected_value,popularity_dict)
    # print("reactive uniform ready!")
    # reactive_exponential = ReactiveExponential(amount, cachesize, total_rate, expected_value, popularity_dict)
    # print("reactive exponential ready!")

    index = []
    hit_ratio_sim = []
    hit_ratio_model = []
    hit_ratio_model_uniform = []
    hit_ratio_model_exponential = []
    for i in range(1, 51):
        index.append(i)
        hit_ratio_sim.append(simulator.cache.hitRatio()[i])
        hit_ratio_model.append(reactive.hitRatio()[i])
        # hit_ratio_model_uniform.append(reactive_uniform.hitRatio()[i])
        # hit_ratio_model_exponential.append(reactive_exponential.hitRatio()[i])

    font1 = {
        'family': 'Times New Roman',
        'weight': 'normal',
        'size': 13,
    }

    font2 = {
        'family': 'Times New Roman',
        'weight': 'normal',
        'size': 15,
    }

    plt.plot(index, hit_ratio_sim, "+", color="black", label="simulation")
    plt.plot(index, hit_ratio_model, color="black",linewidth="1", label="model")
    # plt.plot(index, hit_ratio_model_uniform, label="model-uniform")
    # plt.plot(index, hit_ratio_model_exponential, label="model-exponential")

    plt.xlabel("content ID", font2)
    plt.ylabel("hit probability", font2)
    plt.grid(True)
    plt.axis([0, 51, 0, 1], font2)
    plt.legend(prop=font2)
    # plt.savefig("kan6.eps")
    plt.show()