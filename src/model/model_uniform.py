from scipy.integrate import quad, dblquad, nquad
from scipy.optimize import fsolve
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mcav.zipf import Zipf
from che import Che
from math import exp
from model_validation import ValidationUniform


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
        if Tc < 2*ev:
            for i in range(1, self._amount + 1):
                rate = self._rate[i]
                F = self._F(rate, ev, Tc)
                a = quad(F.F1, 0, Tc)
                b = quad(F.F2, Tc, 2 * ev)
                c = quad(F.F3, Tc, 2 * ev)
                hit_ratio[i] = a[0] + b[0] + c[0]
        else:
            for i in range(1, self._amount + 1):
                rate = self._rate[i]
                F = self._F(rate, ev, Tc)
                a = quad(F.F1, 0, 2 * ev)
                hit_ratio[i] = a[0]
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

        def F1(self, Tv):
            return (Tv + exp(-self._rate * Tv)/self._rate - 1/self._rate) / (2 * self._ev * self._ev)

        def F2(self, Tv):
            return (self._Tc + exp(-self._rate * self._Tc)/self._rate - 1/self._rate) / (2 * self._ev * self._ev)
        
        def F3(self, Tv):
            return (Tv - self._Tc) * (1 - exp(-self._rate * self._Tc)) / (2 * self._ev * self._ev)

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
        self._validation_size = ValidationUniform(amount,total_rate,expected_value,popularity).validationSize()
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
                formula = formula + quad(F.F1, 0, x)[0] + quad(F.F2, x, 2 * ev)[0] + quad(F.F3, x, 2 * ev)[0]
            return formula - self._cachesize

        if self._validation_size < self._cachesize:
            # Tc0 = fsolve(f1, [1])[0]
            self._Tc0 = None
            for i in range(1, self._amount + 1):
                rate = self._rate[i]
                F = self._F(rate, ev, None)
                a = quad(F.F1, 0, 2 * ev)
                hit_ratio[i] = a[0]
        else:
            Tc0 = fsolve(f, [1])[0]
            self._Tc0 = Tc0
            for i in range(1, self._amount + 1):
                rate = self._rate[i]
                F = self._F(rate, ev, Tc0)
                a = quad(F.F1, 0, Tc0)
                b = quad(F.F2, Tc0, 2 * ev)
                c = quad(F.F3, Tc0, 2 * ev)
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
        def __init__(self, rate, expeted_value, Tc):
            self._rate = rate
            self._ev = expeted_value
            self._Tc = Tc

        def F1(self, Ts):
            return (Ts + exp(-self._rate * Ts)/self._rate - 1/self._rate) / (2 * self._ev * self._ev)

        def F2(self, Ts):
            return (self._Tc + exp(-self._rate * self._Tc)/self._rate - 1/self._rate) / (2 * self._ev * self._ev)
        
        def F3(self, Ts):
            return (Ts - self._Tc) * (1 - exp(-self._rate * self._Tc)) / (2 * self._ev * self._ev)


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
        validation_ratio = ValidationUniform(self._amount, self._total_rate, self._ev, self._popularity).validationRatio()
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
                    F = self._F(rate, ev, None)
                    formula = formula + quad(F.F1, 0, 2*ev)[0]
            return formula - self._cachesize

        def f2(x):
            formula = 0
            for i in range(1, self._amount + 1):
                rate = self._rate[i]
                if i < self._N + 1:
                    formula = formula + 1 - exp(-rate*x)
                else:
                    F = self._F(rate, ev, x)
                    formula = formula + quad(F.F1, 0, x)[0] + quad(F.F2, x, 2 * ev)[0] + quad(F.F3, x, 2 * ev)[0]
            return formula - self._cachesize

        Tc0 = fsolve(f2, [1])[0]
        for i in range(1, self._amount + 1):
            rate = self._rate[i]
            if i < self._N + 1:
                hit_ratio[i] = 1 - exp(-rate * Tc0)
            else:
                F = self._F(rate, ev, Tc0)
                a = quad(F.F1, 0, Tc0)
                b = quad(F.F2, Tc0, 2 * ev)
                c = quad(F.F3, Tc0, 2 * ev)
                hit_ratio[i] = a[0] + b[0] + c[0]
        # if self._occupancy_size < self._cachesize:
        #     Tc0 = fsolve(f1, [1])[0]
        #     for i in range(1, self._amount + 1):
        #         rate = self._rate[i]
        #         if i < self._N + 1:
        #             hit_ratio[i] = 1 - exp(-rate * Tc0)
        #         else:
        #             F = self._F(rate, ev, None)
        #             a = quad(F.F1, 0, 2 * ev)
        #             hit_ratio[i] = a[0]
        # else:
        #     Tc0 = fsolve(f2, [1])[0]
        #     for i in range(1, self._amount + 1):
        #         rate = self._rate[i]
        #         if i < self._N + 1:
        #             hit_ratio[i] = 1 - exp(-rate*Tc0)
        #         else:
        #             F = self._F(rate, ev, Tc0)
        #             a = quad(F.F1, 0, Tc0)
        #             b = quad(F.F2, Tc0, 2 * ev)
        #             c = quad(F.F3, Tc0, 2 * ev)
        #             hit_ratio[i] = a[0] + b[0] + c[0]
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

        def F1(self, Tv):
            return (Tv + exp(-self._rate * Tv) / self._rate - 1 / self._rate) / (2 * self._ev * self._ev)

        def F2(self, Tv):
            return (self._Tc + exp(-self._rate * self._Tc) / self._rate - 1 / self._rate) / (2 * self._ev * self._ev)

        def F3(self, Tv):
            return (Tv - self._Tc) * (1 - exp(-self._rate * self._Tc)) / (2 * self._ev * self._ev)


if __name__ == "__main__":
    amount = 5000
    z = 0.8
    cachesize = 50
    total_rate = 20
    expected_value = 4
    N=20

    zipf = Zipf(amount, z)
    popularity = zipf.popularity()

    # che = Che(amount, cachesize, popularity, total_rate)
    # print(total_rate*popularity[1], total_rate*popularity[2])

    # Tc = che.T
    # print("Tc: ", Tc)

    poru = ProactiveOptionalRenew(amount, cachesize, total_rate, expected_value,
                               popularity,N)
    hit_ratio = poru.hitRatio()
    total_hit_ratio = poru.totalHitRatio()
    print("Tc: ", poru.Che().T)
    print("Tc0: ", poru.Tc0())
    print("total hit ratio: ", total_hit_ratio)
    print(poru._occupancy_size)
    print()

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