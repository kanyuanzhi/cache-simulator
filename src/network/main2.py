import simpy
import random
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mcav.zipf import Zipf

from node import Node
from network import Network
from simulator import LeafSim, NetworkSim


def sim(amount, cachesize, total_rate, expected_value, N, simulation_time, z, pattern, hit_ratio, load):
    network = Network(amount, expected_value, simulation_time ,N ,pattern)

    node1 = Node(cachesize, network, "root", pattern, 1)
    node2 = Node(cachesize, network, "router", pattern, 2)
    node3 = Node(cachesize, network, "router", pattern, 3)
    node4 = Node(cachesize, network, "router", pattern, 4)
    node5 = Node(cachesize, network, "router", pattern, 5)
    node6 = Node(cachesize, network, "router", pattern, 6)
    node7 = Node(cachesize, network, "router", pattern, 7)
    node8 = Node(cachesize, network, "leaf", pattern, 7)
    node9 = Node(cachesize, network, "leaf", pattern, 7)
    node10 = Node(cachesize, network, "leaf", pattern, 7)
    node11 = Node(cachesize, network, "leaf", pattern, 7)
    node12 = Node(cachesize, network, "leaf", pattern, 7)
    node13 = Node(cachesize, network, "leaf", pattern, 7)
    node14 = Node(cachesize, network, "leaf", pattern, 7)
    node15 = Node(cachesize, network, "leaf", pattern, 7)

    nodes = [node1, node2, node3, node4, node5, node6, node7 ,node8, node9, node10, node11, node12, node13, node14, node15]
    network.registerNodes(nodes)

    node2.nextNode(node1)
    node3.nextNode(node1)
    node4.nextNode(node2)
    node5.nextNode(node2)
    node6.nextNode(node3)
    node7.nextNode(node3)

    node8.nextNode(node4)
    node9.nextNode(node4)
    node10.nextNode(node5)
    node11.nextNode(node5)
    node12.nextNode(node6)
    node13.nextNode(node6)
    node14.nextNode(node7)
    node15.nextNode(node7)

    env = simpy.Environment()
    leaf_sim1 = LeafSim(env, node8, amount, z, total_rate)
    print("sim1 ready")
    leaf_sim2 = LeafSim(env, node9, amount, z, total_rate)
    print("sim2 ready")
    leaf_sim3 = LeafSim(env, node10, amount, z, total_rate)
    print("sim3 ready")
    leaf_sim4 = LeafSim(env, node11, amount, z, total_rate)
    print("sim4 ready")
    leaf_sim5 = LeafSim(env, node12, amount, z, total_rate)
    print("sim5 ready")
    leaf_sim6 = LeafSim(env, node13, amount, z, total_rate)
    print("sim6 ready")
    leaf_sim7 = LeafSim(env, node14, amount, z, total_rate)
    print("sim7 ready")
    leaf_sim8 = LeafSim(env, node15, amount, z, total_rate)
    print("sim8 ready")
    network_sim = NetworkSim(env, network, expected_value)
    print("network sim ready")

    env.process(leaf_sim1.request())
    env.process(leaf_sim2.request())
    env.process(leaf_sim3.request())
    env.process(leaf_sim4.request())
    env.process(leaf_sim5.request())
    env.process(leaf_sim6.request())
    env.process(leaf_sim7.request())
    env.process(leaf_sim8.request())

    env.process(network_sim.update())

    env.run(until=simulation_time)

    print(network.totalHitRatio())
    hit_ratio.append(network.totalHitRatio())
    print(network.totalLoad())
    load.append(network.totalLoad()/float(simulation_time))


if __name__ == "__main__":
    amount = 5000
    z = 0.8
    cachesize = 100
    total_rate = 20
    expected_value = 10
    simulation_time = 500
    N = 20

    # random.seed(42)

    # pattern = "reactive"
    # pattern = "proactive_remove"
    # pattern = "proactive_renew"
    pattern = "proactive_optional_renew"

    hit_ratio = []
    load = []

    for cachesize in range(50, 251, 50):
        sim(amount, cachesize, total_rate, expected_value, N, simulation_time, z, pattern, hit_ratio, load)
        print("period: ", cachesize)

    print(hit_ratio)
    print(load)


