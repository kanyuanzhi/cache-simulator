import simpy
import random
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import math

def transfer(a_list):
    length = len(a_list)
    new_list = []
    for i in range(length):
        if i%2 == 0:
            new_list.append(a_list[i])
    return new_list

def loadPerSecond(a_list):
    length = len(a_list)
    new_list = []
    for i in range(length):
        new_list.append(a_list[i]/5000.0)
    return new_list

if __name__ == "__main__":
    font1 = {
        'family': 'Arial',
        'size': 13,
    }

    font2 = {
        'family': 'Arial',
        'size': 10,
    }


    load_model_reactive = [18.14505371091212, 17.71171898009583, 17.415960485100065, 17.203155475659393, 17.04334791533843, 16.919188907751607, 16.82006135525634, 16.739144562787008, 16.67187198047576, 16.615077491932983, 16.56649973276966, 16.524481898524403, 16.487783118474123, 16.45545604976805, 16.426765164615226, 16.401130823306246, 16.37809013832063, 16.357269041396936, 16.338361989781987, 16.321116984723556, 16.305324350180296, 16.290808216401153, 16.27741997802933, 16.265033213114577, 16.253539696466394, 16.24284624215542, 16.23287218088919, 16.223547328282365, 16.214810336157385, 16.20660734525485, 16.198890877008967, 16.191618916349807, 16.184754148210516, 16.178263318521672, 16.17211669664958, 16.166287620983923, 16.16075211305264, 16.155488548408886, 16.150477374781996, 16.145700869762095, 16.14114293169884, 16.136788898623376, 16.132625390909066, 16.128640174119017, 16.124822039082677, 16.12116069672941, 16.11764668560333, 16.11427129031079, 16.111026469422963]

    load_model_proactive_remove = [18.11340746471132, 17.596490447526968, 17.182488648968995, 16.83428189751661, 16.532145251194407, 16.405706813016447, 16.333302507333787, 16.28180540793535, 16.24284214912956, 16.212188216797667, 16.18738325979479, 16.166871898844136, 16.149614206519036, 16.13488519525382, 16.12216252561183, 16.11105962757607, 16.101283922098194, 16.092609698107722, 16.084859932136784, 16.07789376739403, 16.071597686771955, 16.06587916179413, 16.060662000021175, 16.055882881637608, 16.051488743930136, 16.047434780269924, 16.043682891063046, 16.04020047160867, 16.03695945418144, 16.03393554411358, 16.03110760545225, 16.02845716304846, 16.02596799608265, 16.023625803990598, 16.021417930159856, 16.019333132052967, 16.017361388895395, 16.015493739946997, 16.013722147825156, 16.012039382462042, 16.01043892214667, 16.008914868785844, 16.007461875055135, 16.006075081533897, 16.00475006226613, 16.003482777454398, 16.002269532220556, 16.00110694054488, 15.999991893637372]

    load_model_proactive_renew = [65.94655031064678, 49.279883643980334, 40.946550310646955, 35.94655031064713, 32.61321697731373, 30.232264596361357, 28.446550310647044, 27.057661421758223, 25.946550310647133, 25.037459401556188, 24.279883643980433, 23.63885800295479, 23.089407453504244, 22.613216977313773, 22.196550310647087, 21.828903251823547, 21.502105866202676, 21.209708205383954, 20.946550310647133, 20.708455072551857, 20.49200485610166, 20.29437639760365, 20.113216977313783, 19.94655031064711, 19.792704156800962, 19.650254014350818, 19.51797888207569, 19.39482617271608, 19.27988364398045, 19.172356762260037, 19.07155031064711, 18.97685334095014, 18.88772678123534, 18.80369316778997, 18.724328088424905, 18.649253013349814, 18.578129258015544, 18.510652874749685, 18.446550310647133, 18.385574700891027, 18.327502691599495, 18.272131705995953, 18.219277583374396, 18.168772532869337, 18.12046335412539, 18.074209885115216, 18.029883643980455, 17.98736663717773, 17.94655031064712]

    load_model_proactive_optional_renew = [25.538187205792433, 22.035886107204007, 20.209420765303854, 19.057786774527987, 18.138483767740023, 17.681389374516982, 17.395056785165483, 17.193604558460088, 17.04285259748406, 16.925335510775568, 16.830955153335417, 16.753394986593925, 16.68847567324068, 16.63331107040231, 16.585839135525962, 16.544545011876465, 16.508289574386595, 16.476199053430218, 16.447591624101122, 16.421927206549014, 16.398772304946945, 16.377774857762457, 16.358645912452594, 16.341146050637466, 16.325075182353142, 16.31026477004188, 16.2965718315398, 16.28387426362694, 16.27206715820572, 16.261059873235972, 16.250773683664637, 16.241139882427422, 16.232098233883633, 16.223595705557663, 16.215585421386336, 16.208025792557255, 16.200879791716655, 16.194114343660335, 16.187699811248926, 16.181609559604812, 16.175819585019283, 16.170308197618535, 16.165055748910472, 16.16004439697312, 16.15525790334657, 16.150681456744337, 16.14630151953555, 16.14210569363974, 16.1380826030253]

    load_model_reactive = transfer(load_model_reactive)
    load_model_proactive_remove = transfer(load_model_proactive_remove)
    load_model_proactive_renew = transfer(load_model_proactive_renew)
    load_model_proactive_optional_renew = transfer(load_model_proactive_optional_renew)


    load_sim_reactive = [90842, 87340, 85411, 84064, 83809, 82464, 82371, 82056, 81634, 82010, 81672, 80883, 81296, 81349, 80763, 81229, 80505, 80906, 80513, 80937, 80930, 80635, 80367, 80536, 80377]

    load_sim_proactive_remove = [90723, 85976, 82952, 81435, 81249, 81107, 80589, 80505, 80546, 80686, 80825, 80549, 80503, 79835, 80389, 80431, 79641, 79640, 80373, 80121, 79953, 80266, 79484, 80614, 79807]

    load_sim_proactive_renew = [328807, 204860, 163423, 142142, 129346, 121762, 115256, 111041, 107270, 104511, 101984, 100209, 98708, 97712, 96383, 95036, 94450, 93693, 93015, 91642, 91757, 90587, 90517, 90261, 89964]

    load_sim_proactive_optional_renew = [127365, 100904, 90671, 87114, 85025, 84130, 83652, 83586, 82855, 82418, 82116, 81803, 81576, 81237, 81011, 81919, 81366, 80728, 81116, 80752, 81216, 80927, 80679, 80477, 80685]

    load_sim_reactive = loadPerSecond(load_sim_reactive)
    load_sim_proactive_remove = loadPerSecond(load_sim_proactive_remove)
    load_sim_proactive_renew = loadPerSecond(load_sim_proactive_renew)
    load_sim_proactive_optional_renew = loadPerSecond(load_sim_proactive_optional_renew)

    index_model = [i*2+2 for i in range(len(load_model_reactive))]
    index_sim = [i*2+2 for i in range(len(load_sim_reactive))]
    plt.plot(index_sim, load_sim_proactive_optional_renew, "x", color="black",
             label="sim: proactive optional renewing")
    plt.plot(index_sim, load_sim_proactive_renew, ".", color="black", label="sim: proactive renewing")
    plt.plot(index_sim, load_sim_proactive_remove, "2", color="black", label="sim: proactive removing")
    plt.plot(index_sim, load_sim_reactive, "+", color="black", label="sim: reactive")

    plt.plot(index_model, load_model_proactive_optional_renew, "--", color="black", linewidth="1",
             label="model: proactive optional renewing")
    plt.plot(index_model, load_model_proactive_renew, "-", color="black", linewidth="1",
             label="model: proactive renewing")
    plt.plot(index_model, load_model_proactive_remove, ":", color="black", linewidth="1",
             label="model: proactive removing")
    plt.plot(index_model, load_model_reactive, "-.", color="black", linewidth="1", label="model: reactive")


    # plt.plot(index, hit_ratio_model_uniform, label="model-uniform")
    # plt.plot(index, hit_ratio_model_exponential, label="model-exponential")

    plt.xlabel("mean staleness time (s)", font1)
    plt.ylabel("server load (req/s)", font1)
    plt.grid(True)
    # plt.axis([30, 60, 15, 20], font1)
    my_x_ticks = np.arange(0, 51, 10 )
    my_y_ticks = np.arange(15,70, 10)
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)
    plt.legend(prop=font2)
    # plt.savefig("kan6.eps")
    plt.show()
