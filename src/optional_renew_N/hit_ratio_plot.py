import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    hit_ratio_model = [[0.21173059490456606, 0.21796342106219485, 0.22047104271784848, 0.22166722681649817, 0.22226885536418614, 0.22256021489505157, 0.22267472100623092, 0.22268233003425572, 0.22262272100959726, 0.22251975050472675, 0.22238841636266612, 0.2222384813982745, 0.22207647773887856, 0.22190687177910734, 0.22173276961511523], 
    [0.2801743391128086, 0.3166551353248151, 0.3441681928723656, 0.3554051147524066, 0.3517015581344847, 0.34890169615799144, 0.34646434510164437, 0.34427142023162866, 0.3422750954557372, 0.3404453695617542, 0.3387594493421298, 0.33719882440175064, 0.33574810136907096, 0.33439434179537586, 0.3331265959568424], 
    [0.2999606297507934, 0.3441681928723656, 0.376548558497511, 0.40256993275574904, 0.42453290820938633, 0.44364906271260884, 0.4461907094335505, 0.440715746857731, 0.43560431733841715, 0.43099876348724364, 0.4268706566597469, 0.4231596503309734, 0.4198054659488298, 0.4167555793210707, 0.4139661172152113], 
    [0.3166551353248151, 0.3666299073389893, 0.40256993275574904, 0.4311785209401317, 0.45518141881974256, 0.4759865751106372, 0.4944254269487152, 0.5010611866840842, 0.4957461948546288, 0.49051669102418877, 0.48563559678051577, 0.4811374342214366, 0.4770025359926269, 0.473197118245128, 0.4696857026651701], 
    [0.3312066455711007, 0.38578142064794807, 0.42453290820938633, 0.45518141881974256, 0.4807934468252069, 0.5029324383645511, 0.5225137680393401, 0.540123615974901, 0.5390863815947206, 0.5337085268383648, 0.528495120443284, 0.5236065500417041, 0.5190654059541134, 0.5148555168892904, 0.5109494146906955]]

    hit_ratio_sim_100 = [0.21014132165605096, 0.21650956584255301, 0.2211517341906112, 0.21739697051717743, 0.21998722860791825, 0.22203354276752804, 0.22316336213354643, 0.2210510555472376, 0.22171096627374262, 0.21909678712846473, 0.2228625366386805, 0.2209255533199195, 0.21953673723536737, 0.22072108242662705, 0.22080326671137043]
    
    hit_ratio_sim_200 = [0.2800805756549277, 0.31561371841155234, 0.3439751689832922, 0.3513374951111646, 0.3481129059717785, 0.34452, 0.34199693518824553, 0.34215566950657433, 0.34195105826730643, 0.33536871770784404, 0.33517237236034486, 0.3343750936086509, 0.33303679417850324, 0.3341112134930492, 0.3301585080653221]

    hit_ratio_sim_300 = [0.29737600576438095, 0.341512615162281, 0.37439727331963313, 0.40052478774031985, 0.4245915081698366, 0.4437254274892316, 0.4447503509123722, 0.44171352944114266, 0.42844860336312557, 0.4299753805958901, 0.4227622018677803, 0.41946291993657947, 0.41776483655029567, 0.40960609809634035, 0.40978449269118633]

    hit_ratio_sim_400 = [0.3166550174737893, 0.3668180550575674, 0.40249899638699316, 0.4295763373291441, 0.4532646220043028, 0.47364471393408175, 0.4898786635054093, 0.5014001450092645, 0.4905140083829693, 0.4838252727601519, 0.4839369715449193, 0.47306081033564734, 0.4757635526866296, 0.4725346324251719, 0.4663783051117733]

    hit_ratio_sim_500 = [0.33135013725979534, 0.38541541058724227, 0.42324862809618874, 0.45181499355534904, 0.47696226208598236, 0.5017614999347593, 0.5195696086078279, 0.5357448927857803, 0.528871575068098, 0.5274957403772381, 0.5233693581697512, 0.5204550666547018, 0.5153480806113125, 0.5105869445968184, 0.5080196235482579]

    mp0_index = [0.21714285714285714, 0.355, 0.4577777777777778, 0.528, 0.5854545454545454, 0.63, 0.6707692307692308, 0.7, 0.7306666666666667, 0.7525, 0.7694117647058824, 0.7866666666666666, 0.8021052631578948, 0.818, 0.8304761904761905, 0.84]
    mp0_data = [0.31279594350310247, 0.3570096160023439, 0.3880444770031509, 0.411759122052386, 0.43182709954193566, 0.4489450156516402, 0.4648651865252173, 0.4784077097862468, 0.49142381429646714, 0.5031758291379648, 0.5137811570299275, 0.5239888750409808, 0.5336356197461385, 0.5429650202199953, 0.5515649659357376, 0.559797305843365]

    index = [i*0.1+0.1 for i in range(len(hit_ratio_sim_100))]

    font1 = {
        'family': 'Arial',
        'size': 13,
    }

    font2 = {
        'family': 'Arial',
        'size': 10,
    }

    plt.plot(index, hit_ratio_sim_100, ".", color="black", label="sim: $C=100$")
    plt.plot(index, hit_ratio_sim_200, "1", color="black", label="sim: $C=200$")
    plt.plot(index, hit_ratio_sim_300, "2", color="black", label="sim: $C=300$")
    plt.plot(index, hit_ratio_sim_400, "+", color="black", label="sim: $C=400$")
    plt.plot(index, hit_ratio_sim_500, "x", color="black", label="sim: $C=500$")
    plt.plot(index, hit_ratio_model[0], dashes=[10, 2, 2, 2], color="black", linewidth="1", label="model: $C=100$")
    plt.plot(index, hit_ratio_model[1], "-.", color="black", linewidth="1", label="model: $C=200$")
    plt.plot(index, hit_ratio_model[2], ":", color="black", linewidth="1", label="model: $C=300$")
    plt.plot(index, hit_ratio_model[3], "--", color="black", linewidth="1", label="model: $C=400$")
    plt.plot(index, hit_ratio_model[4], dashes=[10, 5, 20, 5], color="black", linewidth="1", label="model: $C=500$")
    plt.plot(mp0_index, mp0_data, "-", color="black", linewidth="1", label="model: turning points")


    plt.xlabel("$M_p/C$", font1)
    plt.ylabel("hit probability", font1)
    plt.grid(True)
    # plt.axis([50, 255, 0.1, 0.35], font1)
    my_x_ticks = np.arange(0.1, 1.6, 0.2)
    my_y_ticks = np.arange(0.15, 0.8, 0.1)
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)
    plt.legend(prop=font2,ncol=3,loc='upper left',columnspacing=1)
    # plt.savefig("kan6.eps")
    plt.show()