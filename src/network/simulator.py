from mcav.zipf import Zipf
import random

class LeafSim(object):
    def __init__(self, env, leaf, amount, z, rate):
        self.env = env
        self.leaf = leaf
        self.rate = rate
        self.content = [i for i in range(1, amount + 1)]
        self.popularity = [Zipf(amount, z).popularity()[i] for i in range(1, amount)]

    def request(self):
        print_flag = True
        while True:
            item = self._random_pick(self.content, self.popularity)
            self.leaf.insert(item, self.env.now)
            duration = random.expovariate(self.rate)
            # if int(self.env.now) % 2000 == 0 and print_flag:
            #     print(self.env.now)
            #     print(self.cache.cacheSize())
            #     print(self.cache.totalHitRatio())
            #     print_flag = False
            # if int(self.env.now) % 2000 != 0 and not print_flag:
            #     print_flag = True
            yield self.env.timeout(duration)
    
    def _random_pick(self, some_list, probabilities):
        x = random.uniform(0, 1)
        cumulative_probability = 0.0
        for item, item_probability in zip(some_list, probabilities):
            cumulative_probability += item_probability
            if x < cumulative_probability: break
        return item

class NetworkSim(object):
    def __init__(self, env, network, staleness):
        self.env = env
        self.network = network
        self.staleness = staleness
    
    def update(self):
        print_flag = True
        while True:
            self.network.update(self.env.now)
            duration = 1
            if int(self.env.now) % 2000 == 0 and print_flag:
                print(self.env.now)
                if self.env.now > 1:
                    print(self.network.miss/self.env.now)
                print_flag = False
            if int(self.env.now) % 2000 != 0 and not print_flag:
                print_flag = True
            yield self.env.timeout(duration)

