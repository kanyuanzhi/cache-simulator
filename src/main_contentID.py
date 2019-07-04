import simpy
import random
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mcav.zipf import Zipf
from simulator import Simulator
from model import Model
# from math import round

if __name__ == "__main__":

    amount = 5000
    z = 0.8
    cachesize = 125
    total_rate = 20
    expected_value = 10
    N = 20
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

    model = Model(amount, cachesize, total_rate, expected_value, popularity_dict, N, pattern, distribution).getModel()
    if pattern == "proactive_remove" or pattern == "proactive_optional_renew":
        # print("Tc:", model.Che().T)
        print("Tc0: ", model.Tc0())
        print("occupancy size: ", model._occupancy_size)
        print("validation size: ", model._validation_size)

    print("model: ", model.totalHitRatio())

    env = simpy.Environment()
    simulator = Simulator(env, cachesize, amount, expected_value, total_rate, content, popularity, N, pattern, distribution).getSimulator()
    simulator.setDuration(0.01)
    simulator.setDelta(50)
    env.process(simulator.updateSim())
    env.process(simulator.insertSim())
    env.run(until=simulation_time)
    print("simulation: ", simulator.cache.totalHitRatio())

    print("Error: ", (model.totalHitRatio()-simulator.cache.totalHitRatio())/simulator.cache.totalHitRatio())

    index = []
    hit_ratio_sim = []
    hit_ratio_model = []

    for i in range(1, 51):
        index.append(i)
        hit_ratio_sim.append(simulator.cache.hitRatio()[i])
        hit_ratio_model.append(model.hitRatio()[i])
    
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

    # f = open('./hit_ratio_id/'+pattern+'_'+distribution+'_'+str(expected_value)+'.txt','w')
    # f.write(str(hit_ratio_sim))
    # f.write('\n')
    # f.write(str(hit_ratio_model))
    # f.write('\n')
    # f.write(str(hit_ratio_sim[0:51]))
    # f.write('\n')
    # f.write(str(hit_ratio_model[0:51]))
    # f.write('\n')
    # f.write(str((model.totalHitRatio()-simulator.cache.totalHitRatio())/simulator.cache.totalHitRatio()))
    # f.close()

    plt.plot(index, hit_ratio_sim, "+", color="black", label="simulation")
    plt.plot(index, hit_ratio_model, color="black", linewidth="1", label="model")

    plt.xlabel("content ID", font2)
    plt.ylabel("hit probability", font2)
    plt.grid(True)
    plt.axis([0, 51, 0, 1], font2)
    plt.legend(prop=font2)
    # plt.savefig("kan6.eps")
    plt.show()