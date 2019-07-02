from scipy.integrate import quad, dblquad, nquad
from scipy.optimize import fsolve
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mcav.zipf import Zipf
from che import Che
from math import exp
from model_validation import ValidationExponential


class Reactive(object):
    def __init__(self, amount, cachesize, total_rate, expected_value,
                 popularity):
        self._amount = amount
        self._popularity = popularity
        self._total_rate = total_rate
        self._che = Che(amount, cachesize, self._popularity, total_rate)
        self._ev = expected_value
        self._rate = self._requestRate()
        self._hit_ratio = self._hitRatio()

    def _requestRate(self):
        rr = {}
        for i in range(1, self._amount + 1):
            rr[i] = self._total_rate * self._popularity[i]
        return rr

    def _hitRatio(self):
        Tc = self._che.T
        ev = self._ev
        hit_ratio = {}
        for i in range(1, self._amount + 1):
            rate = self._rate[i]
            F = self._F(rate, ev, Tc)
            a = quad(F.F1, 0, Tc)
            b = quad(F.F2, Tc, float("inf"))
            c = quad(F.F3, Tc, float("inf"))
            hit_ratio[i] = a[0] + b[0] + c[0]
        return hit_ratio

    def hitRatio(self):
        return self._hit_ratio

    def totalHitRatio(self):
        thr = 0
        for i in range(1, self._amount + 1):
            thr = thr + self._popularity[i] * self._hit_ratio[i]
        return thr

    def Che(self):
        return self._che

    def totalLoad(self):
        return self._total_rate * (1 - self.totalHitRatio())
    
    def h(self, x):
        return x

    def g(self, x):
        return 0

    class _F(object):
        def __init__(self, rate, ev, Tc):
            self._rate = rate
            self._ev = ev
            self._Tc = Tc

        def F1(self, Ts):
            return (Ts + exp(-self._rate * Ts)/self._rate - 1/self._rate) * exp(-Ts/self._ev) / (self._ev * self._ev)

        def F2(self, Ts):
            return (self._Tc + exp(-self._rate * self._Tc)/self._rate - 1/self._rate) * exp(-Ts/self._ev) / (self._ev * self._ev)
        
        def F3(self, Ts):
            return (Ts - self._Tc) * (1 - exp(-self._rate * self._Tc)) * exp(-Ts/self._ev) / (self._ev * self._ev)

class ProactiveRemove(object):
    def __init__(self, amount, cachesize, total_rate, expected_value, popularity):
        self._amount = amount
        self._popularity = popularity
        self._total_rate = total_rate
        self._cachesize = cachesize
        self._che = Che(amount, cachesize, self._popularity, total_rate)
        self._ev = expected_value
        self._Tc0 = 0
        self._rate = self._requestRate()
        self._hit_ratio = self._hitRatio()

    def _requestRate(self):
        rr = {}
        for i in range(1, self._amount + 1):
            rr[i] = self._total_rate * self._popularity[i]
        return rr

    def _hitRatio(self):
        ev = self._ev
        hit_ratio = {}

        def f(x):
            formula = 0
            for i in range(1, self._amount + 1):
                rate = self._rate[i]
                F = self._F(rate, ev, x)
                formula = formula + quad(F.F1, 0, x)[0] + quad(F.F2, x, float("inf"))[0] + quad(F.F3, x, float("inf"))[0]
            return formula - self._cachesize

        Tc0 = fsolve(f, [1])[0]
        self._Tc0 = Tc0
        for i in range(1, self._amount + 1):
            rate = self._rate[i]
            F = self._F(rate, ev, Tc0)
            a = quad(F.F1, 0, Tc0)
            b = quad(F.F2, Tc0, float("inf"))
            c = quad(F.F3, Tc0, float("inf"))
            hit_ratio[i] = a[0] + b[0] + c[0]
        return hit_ratio

    def hitRatio(self):
        return self._hit_ratio

    def totalHitRatio(self):
        thr = 0
        for i in range(1, self._amount + 1):
            thr = thr + self._popularity[i] * self._hit_ratio[i]
        return thr

    def Che(self):
        return self._che

    def Tc0(self):
        return self._Tc0

    def totalLoad(self):
        return self._total_rate * (1 - self.totalHitRatio())

    class _F(object):
        def __init__(self, rate, expected_value, Tc):
            self._rate = rate
            self._ev = expected_value
            self._Tc = Tc

        def F1(self, Ts):
            return (Ts + exp(-self._rate * Ts)/self._rate - 1/self._rate) * exp(-Ts/self._ev) / (self._ev * self._ev)

        def F2(self, Ts):
            return (self._Tc + exp(-self._rate * self._Tc)/self._rate - 1/self._rate) * exp(-Ts/self._ev) / (self._ev * self._ev)
        
        def F3(self, Ts):
            return (Ts - self._Tc) * (1 - exp(-self._rate * self._Tc)) * exp(-Ts/self._ev) / (self._ev * self._ev)


class ProactiveRenew(object):
    def __init__(self, amount, cachesize, total_rate, expected_value, popularity):
        self._amount = amount
        self._popularity = popularity
        self._total_rate = total_rate
        self._che = Che(amount, cachesize, self._popularity, total_rate)
        self._ev = expected_value
        self._rate = self._requestRate()
        self._hit_ratio = self._hitRatio()
        self._pub_load_c = {}
        self._pub_load = self._pubLoad()

    def _requestRate(self):
        rr = {}
        for i in range(1, self._amount + 1):
            rr[i] = self._total_rate * self._popularity[i]
        return rr

    def _hitRatio(self):
        return self._che.hitRatio()

    def hitRatio(self):
        return self._hit_ratio

    def totalHitRatio(self):
        return self._che.totalHitRatio()

    def Che(self):
        return self._che

    def _pubLoad(self):
        load = 0
        for i in range(1, self._amount + 1):
            self._pub_load_c[i] = self._che.hitRatio()[i] / self._ev
            load = load + self._che.hitRatio()[i] / self._ev
        return load

    def pubLoadC(self):
        return self._pub_load_c

    def pubLoad(self):
        return self._pub_load

    def totalLoad(self):
        return self._total_rate * (1 - self.totalHitRatio()) + self._pub_load


class ProactiveOptionalRenew(object):
    def __init__(self, amount, cachesize, total_rate, expected_value, popularity, N):
        self._amount = amount
        self._popularity = popularity
        self._total_rate = total_rate
        self._cachesize = cachesize
        self._che = Che(amount, cachesize, self._popularity, total_rate)
        self._ev = expected_value
        self._N = N
        self._Tc0 = 0
        self._rate = self._requestRate()
        self._occupancy_size = self._occupancySize()
        self._hit_ratio = self._hitRatio()

        self._pub_load = self._pubLoad()

    def _occupancySize(self):
        validation_ratio = ValidationExponential(self._amount, self._total_rate, self._ev, self._popularity).validationRatio()
        existence_ratio = self._che.hitRatio()
        validation_size = 0
        for i in range(1, self._amount + 1):
            if i < self._N + 1:
                validation_size = validation_size + existence_ratio[i]
            else:
                validation_size = validation_size + validation_ratio[i]
        return min(validation_size, self._cachesize)

    def _requestRate(self):
        rr = {}
        for i in range(1, self._amount + 1):
            rr[i] = self._total_rate * self._popularity[i]
        return rr

    def _hitRatio(self):
        ev = self._ev
        hit_ratio = {}

        def f(x):
            formula = 0
            for i in range(1, self._amount + 1):
                rate = self._rate[i]
                if i < self._N + 1:
                    formula = formula + 1 - exp(-rate*x)
                else:
                    F = self._F(rate, ev, x)
                    formula = formula + quad(F.F1, 0, x)[0] + quad(F.F2, x, float("inf"))[0] + quad(F.F3, x, float("inf"))[0]
            return formula - self._occupancy_size
        
        Tc0 = fsolve(f, [1])[0]
        for i in range(1, self._amount + 1):
            rate = self._rate[i]
            if i < self._N + 1:
                hit_ratio[i] = 1 - exp(-rate*Tc0)
            else:
                F = self._F(rate, ev, Tc0)
                a = quad(F.F1, 0, Tc0)
                b = quad(F.F2, Tc0, float("inf"))
                c = quad(F.F3, Tc0, float("inf"))
                hit_ratio[i] = a[0] + b[0] + c[0]
        self._Tc0 = Tc0
        return hit_ratio

    def hitRatio(self):
        return self._hit_ratio

    def totalHitRatio(self):
        thr = 0
        for i in range(1, self._amount + 1):
            thr = thr + self._popularity[i] * self._hit_ratio[i]
        return thr

    def Che(self):
        return self._che

    def Tc0(self):
        return self._Tc0

    def _pubLoad(self):
        load = 0
        for i in range(1, self._N + 1):
            load = load + self.hitRatio()[i]/ self._ev
        return load

    def pubLoad(self):
        return self._pub_load

    def totalLoad(self):
        return self._total_rate * (1 - self.totalHitRatio()) + self._pub_load


    class _F(object):
        def __init__(self, rate, expected_value, Tc):
            self._rate = rate
            self._ev = expected_value
            self._Tc = Tc

        def F1(self, Ts):
            return (Ts + exp(-self._rate * Ts)/self._rate - 1/self._rate) * exp(-Ts/self._ev) / (self._ev * self._ev)

        def F2(self, Ts):
            return (self._Tc + exp(-self._rate * self._Tc)/self._rate - 1/self._rate) * exp(-Ts/self._ev) / (self._ev * self._ev)
        
        def F3(self, Ts):
            return (Ts - self._Tc) * (1 - exp(-self._rate * self._Tc)) * exp(-Ts/self._ev) / (self._ev * self._ev)





# if __name__ == "__main__":
#     amount = 100
#     z = 0.8
#     cachesize = 20
#     total_rate = 20
#     expected_value = 5
#     simulation_time = 10000

#     zipf = Zipf(amount, z)
#     popularity_dict = zipf.popularity()
#     content = [i for i in range(1, amount + 1)]
#     popularity = [popularity_dict[i] for i in range(1, amount)]

#     reactive = ReactiveExponential(amount, cachesize, total_rate, expected_value,
#                                popularity_dict)
#     hit_ratio = reactive.hitRatio()
#     total_hit_ratio = reactive.totalHitRatio()
#     print("Tc: ", reactive.Che().T)
#     print("total hit ratio: ", total_hit_ratio)

#     env = simpy.Environment()
#     simulator_exponential = SimulatorExponential(env, cachesize, amount, expeted_value, total_rate, content,
#                           popularity, "reactive")
#     env.process(simulator_exponential.updateSim())
#     env.process(simulator_exponential.insertSim())
#     env.run(until=simulation_time)
#     print("simulation-exponential: ", simulator_exponential.cache.totalHitRatio())

    

#     index = []
#     hit_ratio_sim = []
#     hit_ratio_model = []
#     for i in range(1, 51):
#         index.append(i)
#         hit_ratio_sim.append(simulator_exponential.cache.hitRatio()[i])
#         hit_ratio_model.append(reactive.hitRatio()[i])

#     plt.plot(index, hit_ratio_sim, "+", label="simulation")
#     plt.plot(index, hit_ratio_model, label="model")
#     plt.xlabel("content ID")
#     plt.ylabel("hit ratio")
#     plt.grid(True)
#     # plt.axis([0, 51, 0, 1])
#     plt.legend()
#     plt.show()
