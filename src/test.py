from sympy import *
from scipy.integrate import quad
import math
import random

if __name__ == "__main__":
    # def f(x):
    #     return math.exp(-0.1*x)/0.1/x

    # rate = 1.2293414655658288
    # def F1(Tv):
    #     return (Tv + math.exp(-rate * Tv)/rate - 1/rate) / (2 * 10.0 * Tv)

    
    # result = quad(F1, 0, 10.425828976866992)

    # print(result)

    size = 10000
    value = []
    ave = 10
    count = 0.0
    for i in range(size):
        item = random.uniform(0,2*ave)
        if item>ave:
            count = count + 1
        value.append(item)
    
    
    print(count/size)