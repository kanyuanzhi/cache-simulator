import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

if __name__ == "__main__":
    hit_ratio_model = [0.21173059490456683, 0.21796342106218286, 0.22047104271785775, 0.22166722681652343, 0.2222688553641679, 0.22256021489502334, 0.22267472100624344, 0.22268233003427526, 0.22262272100959543, 0.22251975050472725, 0.22238841636267428, 0.22223848139826352, 0.22207647773887682, 0.22190687177908458, 0.22173276961511343]

    hit_ratio_sim = [0.21111431462317548, 0.21716716716716716, 0.21984905735980606, 0.2204803235526724, 0.22361939850226262, 0.22154586375912774, 0.22173969731312745, 0.2227346850516449, 0.22145422172430004, 0.2227394103693663, 0.2230414194089792, 0.22112407716122887, 0.22289855072463768, 0.22138808852958452, 0.22083454158208926]


    load_model = [16.616082751665477, 17.04285259748406, 17.393131536034748, 17.68465697507344, 17.933612002866642, 18.150826554455527, 18.343579249546313, 18.516931730929493, 18.67452824174178, 18.819074056234772, 18.952630679166706, 19.076804507337595, 19.19287147906159, 19.301861930474164, 19.404619913486048]

    load_sim = [16.6286, 17.0438, 17.3994, 17.6888, 17.8926, 18.173, 18.283, 18.4952, 18.625, 18.8604, 18.9358, 19.1496, 19.1378, 19.3474, 19.375]



    index = [i*10+10 for i in range(len(hit_ratio_model))]

    font1 = {
        'family': 'Arial',
        'size': 13,
    }

    font2 = {
        'family': 'Arial',
        'size': 10,
    }

    fig = plt.figure()


    ax1 = fig.add_subplot(111)

    ax1.plot(index, hit_ratio_sim, "+", color="black", label="sim: hit probability")
    ax1.plot(index, hit_ratio_model, "--", color="black", linewidth="1", label="model: hit probability")
    ax1.set_ylabel("hit probability", font1)
    ax1.axis([0, 161, 0.2, 0.25])
    ax1.set_xlabel("$M_p$", font1)

    ax2 = ax1.twinx()
    ax2.plot(index, load_sim, ".", color="black", label="sim: server load")
    ax2.plot(index, load_model, "-", color="black", linewidth="1", label="sim: server load")
    ax2.set_ylabel("server load (req/s)", font1)

    ax1.grid(True)
    # plt.axis([10, 151, 0, 1])
    fig.legend(prop=font2,loc=1, bbox_to_anchor=(0.4,1), bbox_transform=ax2.transAxes)
    # ax2.legend(prop=font2)
    # plt.savefig("kan6.eps")
    plt.show()