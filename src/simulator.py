import sys
sys.path.append('./src/simulator')
import lru_simulator_constant as sc
import lru_simulator_uniform as su
import lru_simulator_exponential as se

class Simulator(object):
    def __init__(self, env, size, amount, staleness, rate, content, popularity, N, pattern, distribution):
        # pattern options: reactive, proactive_remove, proactive_renew, proactive_optional_renew 
        # distribution options: constant, uniform, exponential
        if distribution == "constant":
            self.distribution = sc
        elif distribution == "uniform":
            self.distribution = su
        else:
            self.distribution = se
        
        self.simulator = self.distribution.Simulator(env, size, amount, staleness, rate, content, popularity, N, pattern)

    def getSimulator(self):
        return self.simulator