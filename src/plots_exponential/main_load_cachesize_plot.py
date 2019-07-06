import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":
    font1 = {
        'family': 'Arial',
        'size': 13,
    }

    font2 = {
        'family': 'Arial',
        'size': 10,
    }

    hit_ratio_model_reactive = [17.562917751439862, 17.030643451475605, 16.67187198047576, 16.41586960257692, 16.227012492948106, 16.084851303535608, 15.976440801566723, 15.893040499023229, 15.828492002872254, 15.778325792915435, 15.73922768448687, 15.708700771640329, 15.684841356815086, 15.666184996473373, 15.651597593527544, 15.640196511174798, 15.63129232725801, 15.624345158542827, 15.61893150059447]

    hit_ratio_model_proactive_remove = [17.36307104946143, 16.712297266446527, 16.24284214912956, 15.89215956749791, 15.64118427520718, 15.600470446793684, 15.600470446793814, 15.600470446793683, 15.600470446802333, 15.600470446802333, 15.600470446802333, 15.600470446802333, 15.600470446802333, 15.600470446802333, 15.600470446802333, 15.600470446802333, 15.600470446802333, 15.600470446802333, 15.600470446802333]

    hit_ratio_model_proactive_renew = [22.28215722995861, 24.033753920903496, 25.946550310647133, 27.956225556228137, 30.03089548674283, 32.152738045058385, 34.31067812001709, 36.4972817800206, 38.707282832345456, 40.93680022806325, 43.18288394752425, 45.44323442021019, 47.71602101528011, 49.99976025756005, 52.29323155928258, 54.595417333269495, 56.90545943059181, 59.222626800731646, 61.5462910494364]

    hit_ratio_model_proactive_optional_renew = [17.957417792602534, 17.434922528797514, 17.04285259748406, 16.732155496204378, 16.489862646352908, 16.396513217741898, 16.396513217741898, 16.396513217741898, 16.396513217741898, 16.396513217741898, 16.396513217741898, 16.396513217741898, 16.396513217741898, 16.396513217741898, 16.396513217741898, 16.396513217741898, 16.396513217741898, 16.396513217741898, 16.396513217741898]

    hit_ratio_model_proactive_optional_renew_fixed = [17.717527389066362, 17.27666183346245, 17.04285259748406, 16.96002192388173, 17.021586425687218, 17.327557887223684, 17.666897293501727, 18.01683867238713, 18.375867088576015, 18.742787055376905, 19.11663614255073, 19.49662646252814, 19.88210375634235, 20.272518008514123, 20.66740185321826, 21.06635438821391, 21.46902883004781, 21.875122953691573, 22.28437158703909]


    hit_ratio_sim_reactive = [17.468, 17.293, 16.841, 16.526, 16.271, 16.195, 16.234, 15.768, 15.801, 16.087, 15.676, 15.918, 15.573, 15.415, 15.639, 15.755, 15.835, 15.738, 15.466]

    hit_ratio_sim_proactive_remove = [17.4034, 16.6999, 16.2535, 15.9678, 15.7587, 15.6363, 15.5661, 15.5675, 15.6153, 15.5508, 15.5987, 15.6747, 15.5797, 15.6818, 15.6067, 15.5567, 15.5862, 15.536, 15.6734]

    hit_ratio_sim_proactive_renew = [22.2758, 23.9918, 25.9068, 27.9733, 30.0014, 32.088, 34.3324, 36.5355, 38.696, 40.8834, 43.1195, 45.5253, 47.6401, 49.88, 52.1843, 54.5599, 56.7829, 59.0782, 61.5441]

    hit_ratio_sim_proactive_optional_renew = [17.9565, 17.4184, 17.0524, 16.7855, 16.4688, 16.4068, 16.4577, 16.3055, 16.4064, 16.3319, 16.3779, 16.3888, 16.4114, 16.3852, 16.4239, 16.4407, 16.3818, 16.3408, 16.3589]



    index_model = [i*25+50 for i in range(len(hit_ratio_model_reactive))]
    index_sim = [i*25+50 for i in range(len(hit_ratio_sim_proactive_remove))]
    plt.plot(index_sim, hit_ratio_sim_proactive_optional_renew, "x", color="black", label="sim: proactive optional renewing")
    plt.plot(index_sim, hit_ratio_sim_proactive_renew, ".", color="black", label="sim: proactive renewing")
    plt.plot(index_sim, hit_ratio_sim_proactive_remove, "2", color="black", label="sim: proactive removing")
    plt.plot(index_sim, hit_ratio_sim_reactive, "+", color="black", label="sim: reactive")

    plt.plot(index_model, hit_ratio_model_proactive_optional_renew_fixed,dashes=[10, 5, 20, 5], color="black", linewidth="1", label="model: proactive optional renewing")

    plt.plot(index_model, hit_ratio_model_proactive_optional_renew,"--", color="black", linewidth="1", label="model: proactive optional renewing")
    plt.plot(index_model, hit_ratio_model_proactive_renew,"-", color="black", linewidth="1", label="model: proactive renewing")
    plt.plot(index_model, hit_ratio_model_proactive_remove,":", color="black", linewidth="1", label="model: proactive removing")
    plt.plot(index_model, hit_ratio_model_reactive, "-.", color="black", linewidth="1", label="model: reactive")


    # plt.plot(index, hit_ratio_model_uniform, label="model-uniform")
    # plt.plot(index, hit_ratio_model_exponential, label="model-exponential")

    plt.xlabel("cache capacity", font1)
    plt.ylabel("server load (req/s)", font1)
    plt.grid(True)
    # plt.axis([50, 255, 0.1, 0.35], font1)
    my_x_ticks = np.arange(0, 501, 100)
    my_y_ticks = np.arange(15, 80, 10)
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)
    plt.legend(prop=font2)
    # plt.savefig("kan6.eps")
    plt.show()

