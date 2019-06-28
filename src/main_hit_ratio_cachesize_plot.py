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

    hit_ratio_model_reactive = [0.03809550620113882, 0.05400132722542427, 0.06818740808264195, 0.08089172715324872, 0.09232022077742179, 0.10264965578737854, 0.1120307908841709, 0.12059158242293845, 0.1284402659798163, 0.13566820834807228, 0.14235247361663694, 0.14855808249430869, 0.15433996808292894, 0.1597446463010286, 0.16481162745023242, 0.1695745990001676, 0.17406241013322205, 0.17829988713143613, 0.1823085061573544, 0.186106946961721, 0.18971154792197198, 0.1931366798076919, 0.19639505291096987, 0.19949796973054545, 0.20245553327502613, 0.20527681924115435, 0.20797001880341415, 0.2105425574882915, 0.2130011945667776, 0.21535210654847461, 0.21760095766966153, 0.21975295970879533, 0.22181292301236494, 0.22378530025196697, 0.22567422414311356, 0.22748354012363953, 0.2292168348032588, 0.23087746084674998, 0.23246855883355097, 0.2339930765405933, 0.235453786017932, 0.2368532987643313, 0.23819407925952674, 0.23947845706873294, 0.24070863770154435, 0.24188671237974274, 0.24301466684591536, 0.2440943893258992, 0.24512767774243419]

    hit_ratio_model_proactive_remove = [0.038531332545108446, 0.0548883529452718, 0.06961863038675842, 0.08292930711740244, 0.09500517867824446, 0.10600919347862642, 0.11608358690958825, 0.12535144076777824, 0.13391848811374701, 0.1418750188488178, 0.1492977767573649, 0.15625177104046897, 0.1627919526785388, 0.1689647277340176, 0.17480929615951712, 0.1803588164484115, 0.18564140436980708, 0.19068097889150837, 0.19549797096650076, 0.20010991177602788, 0.20453191679849395, 0.20877708110543564, 0.2128567998683301, 0.21678102640430794, 0.22055847833796727, 0.22419680069651743, 0.22770269302717608, 0.2310820059236376, 0.2343398106186868, 0.2374804434181882, 0.24050752447567816, 0.24342394726300318, 0.24623183011598032, 0.24893241230098104, 0.2515258590538714, 0.25401089921904024, 0.25638411230871466, 0.2586383413938354, 0.2607582110383584, 0.26269591750646, 0.26417501905417984, 0.2655464457241902, 0.2668782669371014, 0.268182711913185, 0.2694659396907308, 0.27073173728872424, 0.2719826925245524, 0.2732206956732137, 0.2744471928792541]

    hit_ratio_model_proactive_renew = [0.03856456784328156, 0.054990783635593454, 0.06983994691072123, 0.08332285913459683, 0.0956239910561822, 0.10690334730751537, 0.11729872038657445, 0.12692810928238216, 0.13589213850207016, 0.14427636639445912, 0.15215341475853428, 0.15958488447426258, 0.16662304532919958, 0.17331230395482766, 0.17969046355853668, 0.1857897945198518, 0.191637937229892, 0.19725865882481308, 0.20267248446764338, 0.20789722212067105, 0.21294839770107013, 0.2178396153746904, 0.22258285567141245, 0.22718872218859096, 0.2316666459306885, 0.23602505482763814, 0.24027151467843788, 0.2444128466657669, 0.24845522566285613, 0.2524042627840335, 0.25626507499397416, 0.26004234406789306, 0.2637403667672058, 0.2673630977470805, 0.2709141864293858, 0.27439700884563234, 0.27781469526929736, 0.28117015430721093, 0.2844660939991428, 0.28770504037695876, 0.2908893538561175, 0.29402124376829536, 0.29710278129239925, 0.3001359109989728, 0.3031224611889265, 0.3060641531792701, 0.3089626096655701, 0.3118193622718457, 0.3146358583827293]


    hit_ratio_sim_reactive = [0.03805009545092419, 0.06828588193403111, 0.0929157031742695, 0.11086271567891973, 0.12629477475308362, 0.14274337745856686, 0.1535767081756909, 0.16380228517138784, 0.17325500897954269, 0.18203308511169974, 0.1880791785921582, 0.19571510425749233, 0.202044612461206, 0.20719228781195267, 0.2117181036427909, 0.21612695303716953, 0.2200667490605595, 0.22452218139586108, 0.22971190454777107, 0.2319766481246902, 0.23531708684595207, 0.23898561997646542, 0.24050860762911444, 0.24212774684734706, 0.24352124432093644]

    hit_ratio_sim_proactive_remove = [0.0390360893108228, 0.0694556476865653, 0.09383052675735602, 0.11425328572361251, 0.13385992206220015, 0.15134228690353202, 0.1620718462823726, 0.17424715263665097, 0.1837982097966405, 0.19611790150898348, 0.20332227570897662, 0.21204303655707543, 0.21720055291784363, 0.2283559291575984, 0.23332251865531958, 0.23894075538758042, 0.24456969824161656, 0.24882622035421784, 0.2540738742519158, 0.2589860468353109, 0.2610963576440464, 0.26217359913360877, 0.2616859388296541, 0.2641305814110347, 0.26418340120769557]

    hit_ratio_sim_proactive_renew = [0.038391270490984966, 0.07116914302866577, 0.0961774723573419, 0.11861595624931515, 0.13574362202835988, 0.152481473164159, 0.16623952931790986, 0.18060926623587237, 0.1910931174089069, 0.2030767996067475, 0.2112720576798607, 0.22336280872498404, 0.23222388425576196, 0.24113432626879253, 0.2477010203827059, 0.2550832622649131, 0.26421371269868227, 0.26881069781862915, 0.2794452525455184, 0.283571410702224, 0.29221178813181975, 0.2956532619303821, 0.3022732613075627, 0.3083071553228621, 0.31449646183984326]



    index_model = [i*5+10 for i in range(len(hit_ratio_model_reactive))]
    index_sim = [(i+1)*10 for i in range(len(hit_ratio_sim_proactive_remove))]
    plt.plot(index_sim, hit_ratio_sim_proactive_renew, "2", color="black", label="sim: proactive invalidation with renewing")
    plt.plot(index_sim, hit_ratio_sim_proactive_remove, "x", color="black", label="sim: proactive invalidation with removing")
    plt.plot(index_sim, hit_ratio_sim_reactive, "+", color="black", label="sim: reactive invalidation")
    plt.plot(index_model, hit_ratio_model_proactive_renew,"-", color="black", linewidth="1", label="model: proactive invalidation with renewing")
    plt.plot(index_model, hit_ratio_model_proactive_remove,":", color="black", linewidth="1", label="model: proactive invalidation with removing")
    plt.plot(index_model, hit_ratio_model_reactive, "-.", color="black", linewidth="1", label="model: reactive invalidation")


    # plt.plot(index, hit_ratio_model_uniform, label="model-uniform")
    # plt.plot(index, hit_ratio_model_exponential, label="model-exponential")

    plt.xlabel("cache size", font1)
    plt.ylabel("hit probability", font1)
    plt.grid(True)
    # plt.axis([50, 255, 0.1, 0.35], font1)
    my_x_ticks = np.arange(10, 260, 40)
    my_y_ticks = np.arange(0, 0.36, 0.05)
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)
    plt.legend(prop=font2)
    # plt.savefig("kan6.eps")
    plt.show()

