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

    load_sim_reactive = [66.806, 62.296, 59.192, 57.258, 55.806, 55.198, 55.51, 53.468, 53.172, 53.088]

    load_sim_proactive_remove = [66.184, 59.292, 56.198, 54.64, 53.198, 52.274, 51.546, 50.592, 50.542, 50.224]

    load_sim_proactive_renew = [82.7, 91.748, 102.008, 113.01, 123.496, 134.444, 143.904, 154.096, 163.826, 172.954]

    load_sim_proactive_optional_renew = [66.874, 60.422, 56.378, 53.122, 52.544, 52.28, 51.198, 51.134, 50.47, 49.752]



    index_sim = [i*50+50 for i in range(len(load_sim_reactive))]
    plt.plot(index_sim, load_sim_proactive_optional_renew, 'x--', color="black", label="sim: proactive optional renewing")
    plt.plot(index_sim, load_sim_proactive_renew, ".-", color="black", label="sim: proactive renewing")
    plt.plot(index_sim, load_sim_proactive_remove, "2:", color="black", label="sim: proactive removing")
    plt.plot(index_sim, load_sim_reactive, "+-.", color="black", label="sim: reactive")


    # plt.plot(index, hit_ratio_model_uniform, label="model-uniform")
    # plt.plot(index, hit_ratio_model_exponential, label="model-exponential")

    plt.xlabel("cache capacity", font1)
    plt.ylabel("server load (req/s)", font1)
    plt.grid(True)
    # plt.axis([50, 255, 0.1, 0.35], font1)
    my_x_ticks = np.arange(0, 501, 100)
    my_y_ticks = np.arange(45, 180, 20)
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)
    plt.legend(prop=font2)
    # plt.savefig("kan6.eps")
    plt.show()

