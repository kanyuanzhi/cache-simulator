from scipy.integrate import quad
from mcav.zipf import Zipf
from math import exp


class ValidationConstant(object):
    def __init__(self, amount, total_rate, expected_value, popularity):
        self._amount = amount
        self._popularity = popularity
        self._total_rate = total_rate
        self._ev = expected_value
        self._rate = self._requestRate()
        self._validation_ratio = self._validationRatio()

    def _requestRate(self):
        rr = {}
        for i in range(1, self._amount + 1):
            rr[i] = self._total_rate * self._popularity[i]
        return rr

    def _validationRatio(self):
        ev = self._ev
        validation_ratio = {}
        for i in range(1, self._amount + 1):
            rate = self._rate[i]
            validation_ratio[i] = quad(self._F(rate, ev).F1, 0, ev)[0]/ev
        return validation_ratio

    def validationSize(self):
        return sum(list(self._validation_ratio.values()))

    def validationRatio(self):
        return self._validation_ratio

    def totalValidationRatio(self):
        thr = 0
        for i in range(1, self._amount + 1):
            thr = thr + self._popularity[i] * self._validation_ratio[i]
        return thr

    class _F(object):
        def __init__(self, rate, ev):
            self._rate = rate
            self._ev = ev

        def F1(self, Tv):
            return 1 - exp(-self._rate*Tv)

class ValidationUniform(object):
    def __init__(self, amount, total_rate, expected_value, popularity):
        self._amount = amount
        self._popularity = popularity
        self._total_rate = total_rate
        self._ev = expected_value
        self._rate = self._requestRate()
        self._validation_ratio = self._validationRatio()
    
    def _requestRate(self):
        rr = {}
        for i in range(1, self._amount+1):
            rr[i] = self._total_rate * self._popularity[i]
        return rr
    
    def _validationRatio(self):
        ev = self._ev
        validation_ratio = {}
        for i in range(1, self._amount+1):
            rate = self._rate[i]
            validation_ratio[i] = quad(self._F(rate, ev).F1, 0, 2 * ev)[0]
        return validation_ratio

    def validationSize(self):
        return sum(list(self._validation_ratio.values()))

    def validationRatio(self):
        return self._validation_ratio

    def totalValidationRatio(self):
        thr = 0
        for i in range(1, self._amount+1):
            thr = thr + self._popularity[i]*self._validation_ratio[i]
        return thr

    class _F(object):
        def __init__(self, rate, ev):
            self._rate = rate
            self._ev = ev

        def F1(self, Tv):
            return (Tv + exp(-self._rate * Tv)/self._rate - 1/self._rate) / (2 * self._ev * self._ev)


class ValidationExponential(object):
    def __init__(self, amount, total_rate, expected_value, popularity):
        self._amount = amount
        self._popularity = popularity
        self._total_rate = total_rate
        self._ev = expected_value
        self._rate = self._requestRate()
        self._validation_ratio = self._validationRatio()

    def _requestRate(self):
        rr = {}
        for i in range(1, self._amount + 1):
            rr[i] = self._total_rate * self._popularity[i]
        return rr

    def _validationRatio(self):
        ev = self._ev
        validation_ratio = {}
        for i in range(1, self._amount + 1):
            rate = self._rate[i]
            validation_ratio[i] = quad(self._F(rate, ev).F1, 0, float("inf"))[0]
        return validation_ratio

    def validationSize(self):
        return sum(list(self._validation_ratio.values()))

    def validationRatio(self):
        return self._validation_ratio

    def totalValidationRatio(self):
        thr = 0
        for i in range(1, self._amount + 1):
            thr = thr + self._popularity[i] * self._validation_ratio[i]
        return thr

    class _F(object):
        def __init__(self, rate, ev):
            self._rate = rate
            self._ev = ev

        def F1(self, Ts):
            return (Ts + exp(-self._rate * Ts) / self._rate - 1 / self._rate) * exp(-Ts/self._ev) / (self._ev * self._ev)


if __name__ == "__main__":
    amount = 10000
    z = 0.8
    cachesize = 50
    total_rate = 20
    expected_value = 2

    zipf = Zipf(amount, z)
    popularity = zipf.popularity()
    validation_uniform = ValidationUniform(amount,total_rate,expected_value,popularity)
    validation_exponential = ValidationExponential(amount, total_rate, expected_value, popularity)

    print(validation_uniform.totalValidationRatio())
    print(validation_uniform.validationSize())

    print(validation_exponential.totalValidationRatio())
    print(validation_exponential.validationSize())
    # for expected_value in range(4, 41):
    #     index.append(expected_value)
    #
    #     validation = ValidationUniform(amount,total_rate,expected_value,popularity)
    #     result.append(validation.totalValidationRatio())
    #
    #     print(expected_value)
    #
    #
    # plt.plot(index, result, "+-", label="simulation")
    # plt.xlabel("content ID")
    # plt.ylabel("validation ratio")
    # plt.grid(True)
    # # plt.axis([0, 51, 0, 1])
    # plt.legend()
    # plt.show()
    
    
   