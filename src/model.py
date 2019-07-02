import sys
sys.path.append('./src/model')
import model_constant as mc
import model_uniform as mu
import model_exponential as me

from mcav.zipf import Zipf


class Model(object):
    def __init__(self, amount, cachesize, total_rate, expected_value, popularity, N, pattern, distribution):
        # pattern options: reactive, proactive_remove, proactive_renew, proactive_optional_renew 
        # distribution options: constant, uniform, exponential
        if distribution == "constant":
            self.distribution = mc
        elif distribution == "uniform":
            self.distribution = mu
        else:
            self.distribution = me

        if pattern == "reactive":
            self.model = self.distribution.Reactive(amount, cachesize, total_rate, expected_value, popularity)
        elif pattern == "proactive_remove":
            self.model = self.distribution.ProactiveRemove(amount, cachesize, total_rate, expected_value, popularity)
        elif pattern == "proactive_renew":
            self.model = self.distribution.ProactiveRenew(amount, cachesize, total_rate, expected_value, popularity)
        else:
            self.model = self.distribution.ProactiveOptionalRenew(amount, cachesize, total_rate, expected_value, popularity, N)
    
    def getModel(self):
        return self.model

if __name__ == "__main__":

    amount = 5000
    z = 0.8
    cachesize = 50
    total_rate = 20
    expected_value = 5
    N = 20
    simulation_time = 10000
    # random.seed(42)
    zipf = Zipf(amount, z)

    pattern = "reactive"
    # pattern = "proactive_remove"
    # pattern = "proactive_renew"
    # pattern = "proactive_optional_renew"

    distribution = "constant"
    # distribution = "uniform"
    # distribution = "exponential"


    popularity_dict = zipf.popularity()
    content = [i for i in range(1, amount + 1)]
    popularity = [popularity_dict[i] for i in range(1, amount)]

    model = Model(amount, cachesize, total_rate, expected_value, popularity_dict, N, pattern, distribution).getModel()
    print("model: ", model.totalHitRatio())