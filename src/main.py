import simpy
import random
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mcav.zipf import Zipf
from lru_simulator import Simulator
from scipy import integrate
from model import Reactive

if __name__ == "__main__":

    amount = 10000
    z = 0.8
    cachesize = 100
    total_rate = 20
    Ts = 20
    simulation_time = 10000
    # random.seed(42)
    zipf = Zipf(amount, z)

    # pattern = "reactive"
    pattern = "proactive_delete"
    # pattern = "proactive_update_top"
    # pattern = "proactive_update_origin"

    popularity_dict = zipf.popularity()
    content = [i for i in range(1, amount + 1)]
    popularity = [popularity_dict[i] for i in range(1, amount)]

   
    env = simpy.Environment()
    simulator = Simulator(env, cachesize, amount, Ts, total_rate, content,
                          popularity, pattern)
    env.process(simulator.updateSim())
    env.process(simulator.insertSim())
    env.run(until=simulation_time)
    print("simulation: ", simulator.cache.totalHitRatio())

    reactive = Reactive(amount,cachesize,total_rate,Ts,popularity_dict)
    print("model: ", reactive.totalHitRatio())


    validation_rate_under_hit = []
    validation_rate = []

    hit_ratio_model = []
    hit_ratio_model_original = []
    hit_ratio_sim = []
    hit_ratio_sim_original = []
    index = []
    for i in range(1, 101):
        index.append(i)
        hit_ratio_sim.append(simulator.cache.hitRatio()[i])
        hit_ratio_sim_original.append(simulator.cache.originalHitRatio()[i])
        hit_ratio_model.append(reactive.hitRatio()[i])
        hit_ratio_model_original.append(reactive.Che().hitRatio()[i])
        # validation_rate_under_hit.append(simulator.cache.validationRateUnderHit()[i])
        # validation_rate.append(simulator.cache.validationRate()[i])
    
    # print('%s : %s : %s : %s'%('有效|命中', '有效','有效且命中', '命中'))
    # for i in range(0, 11):
    #     print('%.3f : %.6f : %.6f : %.3f' %(validation_rate_under_hit[i],validation_rate[i], hit_ratio_sim[i],hit_ratio_sim_original[i]) )
        # print(validation_rate_under_hit[i], " : ", validation_rate[i])


    plt.plot(index, hit_ratio_sim, "+", label="simulation")
    # plt.plot(index, hit_ratio_sim_original, "*", label="simulation-original")
    plt.plot(index, hit_ratio_model, label="model")
    # plt.plot(index, hit_ratio_model_original, label="model-original")
    plt.xlabel("content ID")
    plt.ylabel("hit ratio")
    plt.grid(True)
    # plt.axis([0, 51, 0, 1])
    plt.legend()
    plt.show()