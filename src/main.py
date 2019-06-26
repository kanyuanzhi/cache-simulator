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

from model_uniform import ReactiveUniform, ProactiveRemoveUniform

if __name__ == "__main__":

    amount = 5000
    z = 0.8
    cachesize = 50
    total_rate = 20
    Ts = 10
    simulation_time = 10000
    # random.seed(42)
    zipf = Zipf(amount, z)

    # pattern = "reactive"
    pattern = "proactive_remove"
    # pattern = "proactive_update_top"
    # pattern = "proactive_update_origin"

    popularity_dict = zipf.popularity()
    content = [i for i in range(1, amount + 1)]
    popularity = [popularity_dict[i] for i in range(1, amount)]

    
    # env = simpy.Environment()
    # simulator = Simulator(env, cachesize, amount, Ts, total_rate, content,
    #                       popularity, pattern)
    # env.process(simulator.updateSim())
    # env.process(simulator.insertSim())
    # env.run(until=simulation_time)
    # print("simulation: ", simulator.cache.totalHitRatio())
    # print("pub load: ", simulator.cache.pubLoad()/10000.0)
    # print("total load: ", simulator.cache.totalLoad()/10000.0)

    env = simpy.Environment()
    simulator_uniform = SimulatorUniform(env, cachesize, amount, Ts, total_rate, content,
                          popularity, pattern)
    env.process(simulator_uniform.updateSim())
    env.process(simulator_uniform.insertSim())
    env.run(until=simulation_time)
    print("simulation-uniform: ", simulator_uniform.cache.totalHitRatio())
    # print("pub load: ", simulator.cache.pubLoad()/10000.0)
    # print("total load: ", simulator.cache.totalLoad()/10000.0)

    # reactive = Reactive(amount,cachesize,total_rate,Ts,popularity_dict)
    # print("model-reactive: ", reactive.totalHitRatio())
    # # print("Tc: ", reactive.Che().T)

    # reactive_uniform = ReactiveUniform(amount,cachesize,total_rate,Ts,popularity_dict)
    # print("model-reactive-uniform: ", reactive_uniform.totalHitRatio())

    proactive_remove = ProactiveRemove(amount,cachesize,total_rate,Ts,popularity_dict)
    print("model-proactive-remove: ", proactive_remove.totalHitRatio())
    print("Tc: ", proactive_remove.Che().T)
    print("Tc0: ", proactive_remove.Tc0())
    print("model-che: ", proactive_remove.Che().totalHitRatio())

    proactive_remove_uniform = ProactiveRemoveUniform(amount,cachesize,total_rate,Ts,popularity_dict)
    print("model-proactive-remove-uniform: ", proactive_remove_uniform.totalHitRatio())
    print("Tc: ", proactive_remove_uniform.Che().T)
    print("Tc0: ", proactive_remove_uniform.Tc0())
    print("model-che: ", proactive_remove_uniform.Che().totalHitRatio())

    

    # proactive_publish = ProactivePublish(amount,cachesize,total_rate,Ts,popularity_dict)
    # print("model-proactive-publish: ", proactive_publish.totalHitRatio())
    # # print("Tc: ", proactive_delete.Che().T)
    # print("pub load: ", proactive_publish.pubLoad())
    # print("total load: ", proactive_publish.totalLoad())



    

    validation_rate_under_hit = []
    validation_rate = []

    pub_load_model = []
    pub_load_sim = []

    hit_ratio_model_reactive = []
    hit_ratio_model_reactive_uniform = []
    hit_ratio_model_original = []
    hit_ratio_model_proactive_remove = []
    hit_ratio_model_proactive_remove_uniform = []
    hit_ratio_model_pp = []
    hit_ratio_sim = []
    hit_ratio_sim_uniform = []
    hit_ratio_sim_original = []
    index = []
    for i in range(1, 51):
        index.append(i)
        # hit_ratio_sim.append(simulator.cache.hitRatio()[i])
        hit_ratio_sim_uniform.append(simulator_uniform.cache.hitRatio()[i])

        # hit_ratio_sim_original.append(simulator.cache.originalHitRatio()[i])
        # hit_ratio_model_reactive.append(reactive.hitRatio()[i])
        # hit_ratio_model_reactive_uniform.append(reactive_uniform.hitRatio()[i])
        # hit_ratio_model_original.append(reactive.Che().hitRatio()[i])
        hit_ratio_model_proactive_remove.append(proactive_remove.hitRatio()[i])
        hit_ratio_model_proactive_remove_uniform.append(proactive_remove_uniform.hitRatio()[i])
        # hit_ratio_model_pp.append(proactive_publish.hitRatio()[i])
        # validation_rate_under_hit.append(simulator.cache.validationRateUnderHit()[i])
        # validation_rate.append(simulator.cache.validationRate()[i])
        # pub_load_model.append(proactive_publish.pubLoadC()[i])
        # pub_load_sim.append(simulator.cache.pubLoadC()[i]/10000.0)
    
    # print('%s : %s : %s : %s'%('有效|命中', '有效','有效且命中', '命中'))
    # for i in range(0, 11):
    #     print('%.3f : %.6f : %.6f : %.3f' %(validation_rate_under_hit[i],validation_rate[i], hit_ratio_sim[i],hit_ratio_sim_original[i]) )
        # print(validation_rate_under_hit[i], " : ", validation_rate[i])


    # plt.plot(index, hit_ratio_sim, "*",color="black", label="simulation")
    plt.plot(index, hit_ratio_sim_uniform, "+",color="black", label="simulation-uniform")

    # plt.plot(index, hit_ratio_sim_original, "*", label="simulation-original")
    # plt.plot(index, hit_ratio_model_reactive, label="model-reactive")
    # plt.plot(index, hit_ratio_model_reactive_uniform, label="model-reactive-uniform")

    # plt.plot(index, hit_ratio_model_original, label="model-original")
    plt.plot(index, hit_ratio_model_proactive_remove, label="model-proactive-delete")
    plt.plot(index, hit_ratio_model_proactive_remove_uniform, label="model-proactive-remove-uniform")
    # plt.plot(index, hit_ratio_model_pp, label="model-proactive-publish")
    # plt.plot(index, pub_load_sim,"+", label="simulation")
    # plt.plot(index, pub_load_model, label="model")

    plt.xlabel("content ID")
    plt.ylabel("hit probability")
    # plt.ylabel("publish load")
    plt.grid(True)
    plt.axis([0, 52, 0, 1])
    plt.legend()
    plt.show()