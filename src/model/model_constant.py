from scipy.integrate import quad
from scipy.optimize import fsolve,root
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mcav.zipf import Zipf
from che import Che
from math import exp
from model_validation import ValidationConstant

class Reactive(object):
    def __init__(self, amount, cachesize, total_rate, expected_value, popularity):
        self._amount = amount
        self._popularity = popularity
        self._total_rate = total_rate
        self._che = Che(amount, cachesize, self._popularity, total_rate)
        self._ev = expected_value
        self._rate = self._requestRate()
        self._hit_ratio = self._hitRatio()
    
    def _requestRate(self):
        rr = {}
        for i in range(1, self._amount+1):
            rr[i] = self._total_rate * self._popularity[i]
        return rr
    
    def _hitRatio(self):
        Tc = self._che.T
        ev = self._ev
        hit_ratio = {}
        if Tc > ev:
            for i in range(1, self._amount+1):
                rate = self._rate[i]
                # hit_ratio[i] = quad(self._F(rate).F1, 0, ev)[0]/ev
                hit_ratio[i] = self.df1(rate, ev)/ev
        else:
            for i in range(1, self._amount+1):
                rate = self._rate[i]
                # hit_ratio[i] = quad(self._F(rate).F1, 0, Tc)[0]/ev + (ev-Tc)*(1-exp(-rate*Tc))/ev
                hit_ratio[i] = self.df1(rate, Tc)/ev + (ev - Tc) * (1 - exp(-rate * Tc)) / ev
        return hit_ratio

    def hitRatio(self):
        return self._hit_ratio

    def totalHitRatio(self):
        thr = 0
        for i in range(1, self._amount+1):
            thr = thr + self._popularity[i]*self._hit_ratio[i]
        return thr

    def Che(self):
        return self._che
    
    def totalLoad(self):
        return self._total_rate*(1-self.totalHitRatio())

    class _F(object):
        def __init__(self, rate):
            self._rate = rate

        def F1(self, t):
            return (1-exp(-self._rate*t))

    def df1(self, rate, x):
        return (x + exp(-rate*x)/rate-1/rate)



class ProactiveRemove(object):
    def __init__(self, amount, cachesize, total_rate, expected_value, popularity):
        self._amount = amount
        self._popularity = popularity
        self._total_rate = total_rate
        self._cachesize = cachesize
        self._che = Che(amount, cachesize, self._popularity, total_rate)
        self._ev = float(expected_value)
        self._validation_size = ValidationConstant(self._amount, self._total_rate, self._ev,
                                                   self._popularity).validationSize()
        self._occupancy_size = self._occupancySize()
        self._Tc0 = 0
        self._rate = self._requestRate()
        self._hit_ratio = self._hitRatio()

    def _occupancySize(self):
        return min(self._validation_size, self._cachesize)

    def _requestRate(self):
        rr = {}
        for i in range(1, self._amount+1):
            rr[i] = self._total_rate * self._popularity[i]
        return rr

    def _hitRatio(self):
        Tc = self._che.T
        ev = self._ev
        hit_ratio = {}

        def f(x):
            formula = 0
            for i in range(1, self._amount+1):
                rate = self._rate[i]
                formula = formula + self.df1(rate,x)/ev + (ev-x)*(1-exp(-rate*x))/ev
            return formula-self._cachesize

        # if ev < Tc:
        #     for i in range(1, self._amount+1):
        #         rate = self._rate[i]
        #         hit_ratio[i] = quad(self._F(rate).F1, 0, ev)[0]/ev
        # else:
        #     Tc0 = fsolve(f, [1])[0]
        #     self._Tc0 = Tc0
        #     for i in range(1, self._amount + 1):
        #         rate = self._rate[i]
        #         hit_ratio[i] = quad(self._F(rate).F1, 0, Tc0)[0] / ev + (ev - Tc0) * (1 - exp(-rate * Tc0)) / ev
        if self._validation_size < self._cachesize:
            for i in range(1, self._amount+1):
                rate = self._rate[i]
                hit_ratio[i] = self.df1(rate,ev)/ev
        else:
            Tc0 = fsolve(f, [1])[0]
            self._Tc0 = Tc0
            for i in range(1, self._amount+1):
                rate = self._rate[i]
                hit_ratio[i] = self.df1(rate,Tc0)/ev + (ev-Tc0)*(1-exp(-rate*Tc0))/ev
        return hit_ratio
    
    def hitRatio(self):
        return self._hit_ratio

    def totalHitRatio(self):
        thr = 0
        for i in range(1, self._amount+1):
            thr = thr + self._popularity[i]*self._hit_ratio[i]
        return thr

    def Che(self):
        return self._che
    
    def Tc0(self):
        return self._Tc0
    
    def totalLoad(self):
        return self._total_rate*(1-self.totalHitRatio())

    class _F(object):
        def __init__(self, rate):
            self._rate = rate

        def F1(self, t):
            return (1-exp(-self._rate*t))

    def df1(self, rate, x):
        return (x + exp(-rate*x)/rate-1/rate)


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
        for i in range(1, self._amount+1):
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
            self._pub_load_c[i] = self._che.hitRatio()[i]/self._ev
            load = load + self._che.hitRatio()[i]/self._ev
        return load

    def pubLoadC(self):
        return self._pub_load_c
    
    def pubLoad(self):
        return self._pub_load
    
    def totalLoad(self):
        return self._total_rate*(1-self.totalHitRatio()) + self._pub_load

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
        self._validation_size = 0
        self._occupancy_size = self._occupancySize()
        self._hit_ratio = self._hitRatio()

        self._pub_load = self._pubLoad()

    def _occupancySize(self):
        validation_ratio = ValidationConstant(self._amount, self._total_rate, self._ev, self._popularity).validationRatio()
        existence_ratio = self._che.hitRatio()
        validation_size = 0
        for i in range(self._N + 1, self._amount + 1):
            # if i < self._N + 1:
            #     validation_size = validation_size + existence_ratio[i]
            # else:
            validation_size = validation_size + validation_ratio[i]
        validation_size = validation_size + self._N
        self._validation_size = validation_size
        return min(validation_size, self._cachesize)

    def _requestRate(self):
        rr = {}
        for i in range(1, self._amount + 1):
            rr[i] = self._total_rate * self._popularity[i]
        return rr

    def _hitRatio(self):
        Tc = self._che.T
        ev = self._ev
        hit_ratio = {}

        def f1(x):
            formula = 0
            for i in range(1, self._amount + 1):
                rate = self._rate[i]
                if i < self._N + 1:
                    formula = formula + 1 - exp(-rate*x)
                else:
                    formula = formula + self.df1(rate,ev)/ev
            return formula - self._occupancy_size

        def f2(x):
            formula = 0
            for i in range(1, self._amount + 1):
                rate = self._rate[i]
                if i < self._N + 1:
                    formula = formula + 1 - exp(-rate*x)
                else:
                    formula = formula + self.df1(rate,x)/ev + (ev-x)*(1-exp(-rate*x))/ev
            return formula - self._occupancy_size

        if self._occupancy_size < self._cachesize:
            Tc0 = fsolve(f2, [0])[0]
            for i in range(1, self._amount + 1):
                rate = self._rate[i]
                if i < self._N + 1:
                    hit_ratio[i] = 1 - exp(-rate*Tc0)
                else:
                    # hit_ratio[i] = self.df1(rate,ev)/ev
                    hit_ratio[i] = self.df1(rate,Tc0)/ev + (ev-Tc0)*(1-exp(-rate*Tc0))/ev
        else:
            Tc0 = fsolve(f2, [0])[0]
            for i in range(1, self._amount+1):
                rate = self._rate[i]
                if i < self._N+1:
                    hit_ratio[i] = 1 - exp(-rate*Tc0)
                else:
                    hit_ratio[i] = self.df1(rate,Tc0)/ev + (ev-Tc0)*(1-exp(-rate*Tc0))/ev
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
            load = load + self._che.hitRatio()[i]/ self._ev
        return load

    def pubLoad(self):
        return self._pub_load

    def totalLoad(self):
        return self._total_rate * (1 - self.totalHitRatio()) + self._pub_load


    class _F(object):
        def __init__(self, rate):
            self._rate = rate

        def F1(self, t):
            return 1-exp(-self._rate*t)

    def df1(self, rate, x):
        return (x + exp(-rate * x) / rate - 1 / rate)


if __name__ == "__main__":
    amount = 100
    z = 0.8
    cachesize = 50
    total_rate = 20
    Ts = 10
    N=20

    zipf = Zipf(amount, z)
    popularity = zipf.popularity()

    # che = Che(amount, cachesize, popularity, total_rate)
    # print(total_rate*popularity[1], total_rate*popularity[2])

    
    # Tc = che.T
    # print("Tc: ", Tc)

    reactive = ProactiveOptionalRenew(amount,cachesize,total_rate,Ts,popularity,N)
    hit_ratio = reactive.hitRatio()
    total_hit_ratio = reactive.totalHitRatio()
    print("Tc: ", reactive.Che().T)
    print("total hit ratio: ", total_hit_ratio)
    
    index = []
    result = []
    for i in range(1, 51):
        index.append(i)
        result.append(hit_ratio[i])

    plt.plot(index, result, "+-", label="simulation")
    plt.xlabel("content ID")
    plt.ylabel("hit ratio")
    plt.grid(True)
    # plt.axis([0, 51, 0, 1])
    plt.legend()
    plt.show()
    
    
    # index = []
    # result = []
    # Pms = []
    # Prs=[]
    
    # for i in range(1, 51):
    #     index.append(i)
    #     rate = total_rate * popularity[i]
    #     Tz = math.exp(rate*Tc)/rate-1/rate+Tc
    #     Wm = 1-Ts/Tz
    #     Wl = (1 - Wm)/2
    #     Wr = (1 - Wm)/2
    #     # result.append(
    #     #     integrate.quad(F, 0, Ts)[0] *
    #     #     (1 - math.exp(-rate * Ts)))
    #     Pm = integrate.dblquad(lambda T,T0: 1/Ts/(Tz-Ts)*(1-math.exp(-rate*(T-T0))),
    #                             0, 
    #                             Tz-Ts, 
    #                             lambda T0: T0, 
    #                             lambda T0: T0+Ts)[0]
    #     Pr = integrate.dblquad(lambda T,T0: 1/(Tz-T0)/Tz*(1-math.exp(-rate*(T-T0))),
    #                             Tz-Ts, 
    #                             Tz, 
    #                             lambda T0: T0, 
    #                             lambda T0: Tz)[0]
    #     Pms.append(Pm)
    #     Prs.append(Pr)
    #     P = Wl * 1 + Wm * Pm + Wr*Pr
    #     result.append(integrate.quad(F, 0, Ts)[0])
    #     # result.append(P)
    # for i in range(11):
    #     print(result[i])

    # plt.plot(index, result, "+-", label="simulation")
    # plt.plot(index, Pms, "+-", label="Pm")
    # plt.plot(index, Prs, "+-", label="Pr")
    # plt.xlabel("content ID")
    # plt.ylabel("hit ratio")
    # plt.grid(True)
    # # plt.axis([0, 51, 0, 1])
    # plt.legend()
    # plt.show()