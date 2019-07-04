import simpy
import random
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mcav.zipf import Zipf
from lru_simulator import Simulator
from lru_simulator_uniform import SimulatorUniform
from scipy import integrate
from model import Reactive, ProactiveRemove, ProactivePublish

from model_uniform import ReactiveUniform

if __name__ == "__main__":

    amount = 100
    z = 0.8
    cachesize = 50
    total_rate = 10
    Ts = 20
    simulation_time = 5000
    # random.seed(42)
    zipf = Zipf(amount, z)

    pattern = "reactive"
    # pattern = "proactive_delete"
    # pattern = "proactive_update_top"
    # pattern = "proactive_update_origin"

    popularity_dict = zipf.popularity()
    content = [i for i in range(1, amount + 1)]
    popularity = [popularity_dict[i] for i in range(1, amount)]


    # print("Tc: ", reactive.Che().T)

    hit_ratio = []
    hit_ratio_uniform = []
    index = []
    for Ts in range(1, 41):
        index.append(Ts)
        simulator = Reactive(amount,cachesize,total_rate,Ts,popularity_dict)
        simulator_uniform = ReactiveUniform(amount,cachesize,total_rate,Ts,popularity_dict)
        hit_ratio.append(simulator.totalHitRatio())
        hit_ratio_uniform.append(simulator_uniform.totalHitRatio())
    print(simulator.Che().T)



    plt.plot(index, hit_ratio, label="model-reactive")
    plt.plot(index, hit_ratio_uniform, label="model-reactive-uniform")


    plt.xlabel("validation time")
    plt.ylabel("hit ratio")
    plt.grid(True)
    # plt.axis([0, 51, 0, 1])
    plt.legend()
    plt.show()