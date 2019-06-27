import simpy
import random
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from mcav.zipf import Zipf
from lru_simulator import Simulator
from lru_simulator_uniform import SimulatorUniform
from lru_simulator_exponential import SimulatorExponential

from model import Reactive, ProactiveRemove, ProactiveRenew
from model_uniform import ReactiveUniform, ProactiveRemoveUniform
from model_exponential import ReactiveExponential, ProactiveRemoveExponential

if __name__ == "__main__":
    font1 = {
        'family': 'Arial',
        'size': 13,
    }

    font2 = {
        'family': 'Arial',
        'size': 10,
    }
    hit_ratio_model_reactive = [0.10177498105202491, 0.10796997150978983, 0.11227453210169952,
     0.11543472042003723, 0.1178516206641657, 0.11975914100537595, 0.12130261397368534, 0.12257699710996364,
     0.12364691791838253, 0.12455786974670068, 0.1253427962813375, 0.12602613525376, 0.12662639480489707,
     0.1271578476990158, 0.12763167647216667, 0.12805676633227814, 0.1284402659798163]
    hit_ratio_model_proactive_remove = [0.12094326148350029, 0.1259306829402453, 0.12811979828421458,
     0.12949212839995988, 0.1304440290700223, 0.1311459866185748, 0.1316860752633063, 0.1321149469283479,
     0.1324639641741986, 0.1327536435213948, 0.1329979951293369, 0.13320692344193014, 0.13338763383884567,
     0.13354549616644718, 0.13368459574922054, 0.13380809667240912, 0.13391848811374701]
    hit_ratio_model_proactive_renew = [0.13589213850207016, 0.13589213850207016, 0.13589213850207016,
     0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016,
     0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016,
     0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016]
    hit_ratio_sim_proactive_remove = [0.11650008767315448, 0.12504366398195554, 0.128933357262503, 0.1306330888427166,
     0.13183802242966355, 0.13187198333700506, 0.13334870455673234, 0.13225682044706671, 0.13274704558103156]
    hit_ratio_sim_reactive = [0.10074712129792456, 0.11124658335123899, 0.11705399178603626, 0.12100479474679933,
     0.12376123990778536, 0.12606684832879178, 0.12607237599479454, 0.127959813448114, 0.1271556783051237]
    hit_ratio_sim_proactive_renew = [0.13706710737877514, 0.13706540661526984, 0.1360748729440954, 0.13793465595102947,
     0.13561517113783533, 0.13532955669454186, 0.13719408819833656, 0.13611873335069202, 0.13641590177375168]

    # hit_ratio_sim_reactive = [0.04477271826576309, 0.073778933160026, 0.09159672262190248, 0.10143451828336977, 0.10655248552843588,
    #  0.11100194494014798, 0.11582819150526809, 0.11836759082217974, 0.11894564086142022, 0.12162756305208042]
    # hit_ratio_sim_proactive_remove = [0.046596995165787414, 0.07518842146353182, 0.10133245435295057, 0.11605477913901309, 0.12312183223200808,
    #  0.12748703726034005, 0.12603681371623837, 0.13012992988387329, 0.13003626309779015, 0.13044779096439613]

    index_model = [i+4 for i in range(len(hit_ratio_model_reactive))]
    index_sim = [2*(i+1)+2 for i in range(len(hit_ratio_sim_proactive_remove))]
    plt.plot(index_sim, hit_ratio_sim_proactive_renew, "2", color="black", label="sim: proactive renew")
    plt.plot(index_sim, hit_ratio_sim_proactive_remove, "x", color="black", label="sim: proactive remove")
    plt.plot(index_sim, hit_ratio_sim_reactive, "+", color="black", label="sim: reactive")
    plt.plot(index_model, hit_ratio_model_proactive_renew,"-", color="black", linewidth="1", label="model: proactive renew")
    plt.plot(index_model, hit_ratio_model_proactive_remove,":", color="black", linewidth="1", label="model: proactive remove")
    plt.plot(index_model, hit_ratio_model_reactive, "-.", color="black", linewidth="1", label="model: reactive")


    # plt.plot(index, hit_ratio_model_uniform, label="model-uniform")
    # plt.plot(index, hit_ratio_model_exponential, label="model-exponential")

    plt.xlabel("staleness time", font1)
    plt.ylabel("hit probability", font1)
    plt.grid(True)
    plt.axis([3, 21, 0.09, 0.15], font1)
    # my_x_ticks = np.arange(2, 22, 2)
    # my_y_ticks = np.arange(0.06, 0.15, 0.01)
    # plt.xticks(my_x_ticks)
    # plt.yticks(my_y_ticks)
    plt.legend(prop=font2)
    # plt.savefig("kan6.eps")
    plt.show()

