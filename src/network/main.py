import simpy
import random
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mcav.zipf import Zipf

from node import Node
from network import Network
from simulator import LeafSim, NetworkSim


if __name__ == "__main__":
    amount = 5000
    z = 0.8
    cachesize = 50
    total_rate = 20
    expected_value = 20
    simulation_time = 10000


    # random.seed(42)

    # pattern = "reactive"
    # pattern = "proactive_remove"
    pattern = "proactive_renew"

    network = Network(expected_value)

    node1 = Node(cachesize, network, "root", 1)
    node2 = Node(cachesize, network, "router", 2)
    node3 = Node(cachesize, network, "router", 3)
    node4 = Node(cachesize, network, "leaf", 4)
    node5 = Node(cachesize, network, "leaf", 5)
    node6 = Node(cachesize, network, "leaf", 6)
    node7 = Node(cachesize, network, "leaf", 7)

    node2.nextNode(node1)
    node3.nextNode(node1)
    node4.nextNode(node2)
    node5.nextNode(node2)
    node6.nextNode(node3)
    node7.nextNode(node3)
   
    env = simpy.Environment()
    leaf_sim1 = LeafSim(env, node4, amount, z, total_rate)
    print("sim1 ready")
    leaf_sim2 = LeafSim(env, node5, amount, z, total_rate)
    print("sim2 ready")
    leaf_sim3 = LeafSim(env, node6, amount, z, total_rate)
    print("sim3 ready")
    leaf_sim4 = LeafSim(env, node7, amount, z, total_rate)
    print("sim4 ready")
    network_sim = NetworkSim(env, network, expected_value)
    print("network sim ready")

    env.process(leaf_sim1.request())
    env.process(leaf_sim2.request())
    env.process(leaf_sim3.request())
    env.process(leaf_sim4.request())

    env.process(network_sim.update())

    env.run(until=simulation_time)
    


    

    print(network.hit)