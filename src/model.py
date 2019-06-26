from scipy.integrate import quad
from scipy.optimize import fsolve
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mcav.zipf import Zipf
from che import Che
from math import exp


class Reactive(object):
    def __init__(self, amount, cachesize, total_rate, Ts, popularity):
        self._amount = amount
        self._popularity = popularity
        self._total_rate = total_rate
        self._che = Che(amount, cachesize, self._popularity, total_rate)
        self._Ts = Ts
        self._rate = self._requestRate()
        self._hit_ratio = self._hitRatio()
    
    def _requestRate(self):
        rr = {}
        for i in range(1, self._amount+1):
            rr[i] = self._total_rate * self._popularity[i]
        return rr
    
    def _hitRatio(self):
        Tc = self._che.T
        Ts = self._Ts
        hit_ratio = {}
        if Tc > Ts:
            for i in range(1, self._amount+1):
                rate = self._rate[i]
                hit_ratio[i] = quad(self._F(rate, Ts, Tc).F1, 0, Ts)[0]
        else:
            for i in range(1, self._amount+1):
                rate = self._rate[i]
                hit_ratio[i] = 1/Ts*quad(self._F(rate, Ts, Tc).F2, 0, Tc)[0] + (1-Tc/Ts)*(1-exp(-rate*Tc))
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
        def __init__(self, rate, Ts, Tc):
            self._rate = rate
            self._Ts = Ts
            self._Tc = Tc

        def F1(self, t):
            return (1-exp(-self._rate*t))/self._Ts

        def F2(self, t):
            return (1-exp(-self._rate*t))

class ProactiveRemove(object):
    def __init__(self, amount, cachesize, total_rate, Ts, popularity):
        self._amount = amount
        self._popularity = popularity
        self._total_rate = total_rate
        self._cachesize = cachesize
        self._che = Che(amount, cachesize, self._popularity, total_rate)
        self._Ts = Ts
        self._Tc0 = 0
        self._rate = self._requestRate()
        self._hit_ratio = self._hitRatio()

    def _requestRate(self):
        rr = {}
        for i in range(1, self._amount+1):
            rr[i] = self._total_rate * self._popularity[i]
        return rr

    def _hitRatio(self):
        Tc = self._che.T
        Ts = self._Ts
        hit_ratio = {}

        def f(x):
            formula = 0
            for i in range(1, self._amount+1):
                rate = self._rate[i]
                formula = formula + quad(self._F(rate, Ts, x).F2, 0, x)[0]/Ts + (1-x/Ts)*(1-exp(-rate*x))
            return formula-self._cachesize

        if Tc > Ts:
            for i in range(1, self._amount+1):
                rate = self._rate[i]
                hit_ratio[i] = quad(self._F(rate, Ts, Tc).F1, 0, Ts)[0]
        else:
            Tc0 = fsolve(f, [1])[0]
            self._Tc0 = Tc0
            for i in range(1, self._amount+1):
                rate = self._rate[i]
                hit_ratio[i] = quad(self._F(rate, Ts, Tc0).F2, 0, Tc0)[0]/Ts + (1-Tc0/Ts)*(1-exp(-rate*Tc0))
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
        def __init__(self, rate, Ts, Tc):
            self._rate = rate
            self._Ts = Ts
            self._Tc = Tc

        def F1(self, t):
            return (1-exp(-self._rate*t))/self._Ts

        def F2(self, t):
            return 1-exp(-self._rate*t)

class ProactiveRenew(object):
    def __init__(self, amount, cachesize, total_rate, Ts, popularity):
        self._amount = amount
        self._popularity = popularity
        self._total_rate = total_rate
        self._che = Che(amount, cachesize, self._popularity, total_rate)
        self._Ts = Ts
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
            self._pub_load_c[i] = 1.0/self._Ts*self._che.hitRatio()[i]
            load = load + 1.0/self._Ts*self._che.hitRatio()[i]
        return load

    def pubLoadC(self):
        return self._pub_load_c
    
    def pubLoad(self):
        return self._pub_load
    
    def totalLoad(self):
        return self._total_rate*(1-self.totalHitRatio()) + self._pub_load


    class _F(object):
        def __init__(self, rate, Ts, Tc):
            self._rate = rate
            self._Ts = Ts
            self._Tc = Tc

        def F1(self, t):
            return (1-exp(-self._rate*t))/self._Ts

        def F2(self, t):
            return (1-exp(-self._rate*t))/self._Tc
    

if __name__ == "__main__":
    amount = 1000
    z = 0.8
    cachesize = 100
    total_rate = 10
    Ts = 20

    zipf = Zipf(amount, z)
    popularity = zipf.popularity()

    # che = Che(amount, cachesize, popularity, total_rate)
    # print(total_rate*popularity[1], total_rate*popularity[2])

    
    # Tc = che.T
    # print("Tc: ", Tc)

    reactive = Reactive(amount,cachesize,total_rate,Ts,popularity)
    hit_ratio = reactive.hitRatio()
    total_hit_ratio = reactive.totalHitRatio()
    print("Tc: ", reactive.Che().T)
    print("total hit ratio: ", total_hit_ratio)
    
    index = []
    result = []
    for i in range(1, 51):
        index.append(i)
        result.append(hit_ratio[i])
    for i in range(11):
        print(result[i])

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