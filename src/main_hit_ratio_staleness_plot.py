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

    hit_ratio_model_reactive = [0.10177498105202491, 0.10517784976113859, 0.10796997150978983, 0.11030060122570066, 0.11227453210169952,
     0.1139673181892544, 0.11543472042003723, 0.11671874625633243, 0.1178516206641657, 0.11885846418471274,
     0.11975914100537595, 0.12056956093935196, 0.12130261397368534, 0.12196885250985554, 0.12257699710996364,
     0.12313431667788896, 0.12364691791838253, 0.12411996831420247, 0.12455786974670068, 0.12496439503177877,
     0.1253427962813375, 0.12569589163849426, 0.12602613525376, 0.12633567415795738, 0.12662639480489707,
     0.126899961406461, 0.1271578476990158, 0.12740136341672856, 0.12763167647216667, 0.12784983163430758,
     0.12805676633227814, 0.128253324087611, 0.1284402659798163, 0.12861828047302845, 0.1287879918705326,
     0.12894996761551233, 0.12910472461753658, 0.1292527347530974, 0.12939442966327913, 0.1295302049510987,
     0.1296604238643498, 0.12978542053600556, 0.1299055028429772, 0.13002095493461688, 0.13013203947464508,
     0.13023899963365757, 0.13034206086401026, 0.13044143248428525, 0.13053730909677427, 0.1306298718581122,
     0.13071928962055002, 0.13080571995893794, 0.1308893100965544, 0.13097019774123447, 0.13104851184174726,
     0.13112437327317192, 0.13119789545892824, 0.13126918493617193, 0.13133834187049698, 0.1314054605251603,
     0.1314706296894489, 0.13153393307027592, 0.1315954496506455, 0.13165525401819897, 0.13171341666672862,
     0.13177000427320498, 0.13182507995261145, 0.13187870349263972, 0.13193093157006577, 0.13198181795046457,
     0.13203141367273322, 0.13207976721976078, 0.13212692467642786, 0.13217292987604937]
    hit_ratio_model_proactive_remove = [0.12094326148350029, 0.12419908056350894, 0.1259306829402453, 0.1271707367179963, 0.12811979828421458,
     0.1288748782685497, 0.12949212839995988, 0.13000718008227197, 0.1304440290700223, 0.13081954488413905,
     0.1311459866185748, 0.13143250335185333, 0.1316860752633063, 0.1319121279797876, 0.1321149469283479,
     0.13229796456146264, 0.1324639641741986, 0.13261522750089452, 0.1327536435213948, 0.1328807899491895,
     0.1329979951293369, 0.13310638565792887, 0.13320692344193014, 0.13330043484626275, 0.13338763383884567,
     0.13346914053331524, 0.13354549616644718, 0.1336171752875787, 0.13368459574922054, 0.13374812694923752,
     0.13380809667240912, 0.13386479680195507, 0.13391848811374701, 0.13396940432040214, 0.13401775549962414,
     0.1340637310131379, 0.13410750200280994, 0.1341492235338446, 0.13418903644181832, 0.13422706893062705,
     0.13426343795929882, 0.13429825045002328, 0.13433160434338628, 0.13436358952314897, 0.13439428862883251,
     0.1344237777719349, 0.13445212716860622, 0.1344794017002293, 0.134505661410954, 0.1345309619507475,
     0.1345553549704068, 0.13457888847476376, 0.13460160713906616, 0.13462355259296177, 0.134644763675814,
     0.13466527666683845, 0.1346851254927445, 0.1347043419154818, 0.13472295570233647, 0.13474099478015109,
     0.13475848537552051, 0.13477545214226086, 0.1347919182776772, 0.13480790562857978, 0.13482343478825629,
     0.13483852518506917, 0.13485319516381772, 0.13486746206017397, 0.13488134226923634, 0.13489485130847553,
     0.13490800387568755, 0.13492081390244015, 0.13493329460339412, 0.13494545852186765]
    hit_ratio_model_proactive_renew = [0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016,
     0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016,
     0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016,
     0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016,
     0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016,
     0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016,
     0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016,
     0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016,
     0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016,
     0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016,
     0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016,
     0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016,
     0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016,
     0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016,
     0.13589213850207016, 0.13589213850207016, 0.13589213850207016, 0.13589213850207016]



    hit_ratio_sim_reactive = [0.10029932342515516, 0.11093629190118058, 0.1166581309091782, 0.12077714354263093, 0.12291794941506673,
     0.12473600051297054, 0.12658284935433275, 0.1274015489866013, 0.12776380802895743, 0.1289795282167697,
     0.12944637737411893, 0.12954839407202148, 0.1304400910705797, 0.13082052107783965, 0.13143161477209253,
     0.13137009648679376, 0.13235806757942567, 0.13146348464345758, 0.1312168307430913]
    hit_ratio_sim_proactive_remove = [0.11611377727256353, 0.12622962942236896, 0.12925733360934685, 0.13079061040752177, 0.13199126398252797,
     0.13191619507573107, 0.13247465223415483, 0.1333449888107417, 0.13334939402542254, 0.1343117020255352,
     0.1340138419365924, 0.13452875762190547, 0.1340671371443897, 0.1338482586045452, 0.1342466027278134,
     0.13492281437203482, 0.13461649973906106, 0.13455903046911333, 0.1349547143578741]
    hit_ratio_sim_proactive_renew = [0.13668498036675383, 0.13572073940071439, 0.1360563081370904, 0.13643921969673514, 0.13624561859015968,
     0.13609040610711462, 0.13574786979157283, 0.13648819277060253, 0.13590157894947602, 0.1360422969176481,
     0.13536792737033743, 0.1360255654258051, 0.1362093335225921, 0.13525109087193624, 0.13593695596435168,
     0.13657221079534718, 0.13517553395574883, 0.13652610646034416, 0.13561861384951907]

    # hit_ratio_sim_reactive = [0.04477271826576309, 0.073778933160026, 0.09159672262190248, 0.10143451828336977, 0.10655248552843588,
    #  0.11100194494014798, 0.11582819150526809, 0.11836759082217974, 0.11894564086142022, 0.12162756305208042]
    # hit_ratio_sim_proactive_remove = [0.046596995165787414, 0.07518842146353182, 0.10133245435295057, 0.11605477913901309, 0.12312183223200808,
    #  0.12748703726034005, 0.12603681371623837, 0.13012992988387329, 0.13003626309779015, 0.13044779096439613]

    index_model = [i*0.5+4 for i in range(len(hit_ratio_model_reactive))]
    index_sim = [2*(i+1)+2 for i in range(len(hit_ratio_sim_proactive_remove))]
    plt.plot(index_sim, hit_ratio_sim_proactive_renew, "2", color="black", label="sim: proactive invalidation with renewing")
    plt.plot(index_sim, hit_ratio_sim_proactive_remove, "x", color="black", label="sim: proactive invalidation with removing")
    plt.plot(index_sim, hit_ratio_sim_reactive, "+", color="black", label="sim: reactive invalidation")
    plt.plot(index_model, hit_ratio_model_proactive_renew,"-", color="black", linewidth="1", label="model: proactive invalidation with renewing")
    plt.plot(index_model, hit_ratio_model_proactive_remove,":", color="black", linewidth="1", label="model: proactive invalidation with removing")
    plt.plot(index_model, hit_ratio_model_reactive, "-.", color="black", linewidth="1", label="model: reactive invalidation")


    # plt.plot(index, hit_ratio_model_uniform, label="model-uniform")
    # plt.plot(index, hit_ratio_model_exponential, label="model-exponential")

    plt.xlabel("mean staleness time", font1)
    plt.ylabel("hit probability", font1)
    plt.grid(True)
    # plt.axis([2, 42, 0.09, 0.15], font1)
    my_x_ticks = np.arange(4, 42, 4)
    my_y_ticks = np.arange(0.09, 0.155, 0.01)
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)
    plt.legend(prop=font2)
    # plt.savefig("kan6.eps")
    plt.show()
