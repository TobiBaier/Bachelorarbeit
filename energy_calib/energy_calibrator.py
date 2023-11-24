import numpy as np
from control import get_inst
import matplotlib as mpl
import matplotlib.pyplot as plt
import json
import re
import numpy as np

c = get_inst("Z:\Studenten\Baier\Messungen")
# c = get_inst("C:/Users/baier/OneDrive/Uni/Bachelorarbeit")

with open("calibration.json", "r") as of:
    data_dict = json.load(of)

def E_calib(data, temp, save=False, plot=False):
    mass = data["mass"]
    data = data[temp+"emp"]
    lin_poly = np.polynomial.Polynomial(data["linear"])
    quad_poly = np.polynomial.Polynomial(data["quadratic"])
    pivot = data["switch"]
    cutoff = data["spec_cutoff"]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    for name in data["filenames"]:
        vals, bins = c.c_data.auto_read("sev", c.c_file.get_datafile_path(name), bin_ret=True)
        e_bins = []
        e_vals = []
        dose = 0

        iso_name = re.search(r"_([a-z]{2}[0-9]{2,3})_", name).group(1)
        irr_time = re.search(r"_([0-9]{3})s_", name).group(1)
        try:
            sample_name = re.search(r"_([a-z]{4,7}110)_", name).group(1)
        except AttributeError:
            sample_name = "dsf"

        for i in range(len(bins)-1):
            bin_nr = bins[i]
            val = vals[i]
            if bin_nr > cutoff:
                if bin_nr >= pivot:
                    e_bin = quad_poly(bin_nr)
                    dose = dose + e_bin * val
                else:
                    e_bin = lin_poly(bin_nr)
                    dose = dose + e_bin * val
                e_bins.append(e_bin)
                e_vals.append(val)
            else:
                e_bin = lin_poly(bin_nr)
                e_bins.append(e_bin)
                e_vals.append(0)

        '''save values'''
        if save == True:
            save_array = np.zeros(shape=(len(e_bins) + 4, 2))
            for i in range(len(e_bins)):
                save_array[i+4][0] = e_bins[i]
                save_array[i+4][1] = e_vals[i]

            inst, sample = c.c_file.get_inst_and_sample(name)
            id = re.search(r"_(b[\w]+g[\d]{1}s[\d]{3})_", name).group(1)

            if temp == "roomt":
                st = "hight"
            else:
                st = "lowt"

            save_name = inst + "_" + sample + "_" + id + "_" + iso_name + "_" + "10cm" + "_" + irr_time + "s_" + st + "_ecalib_hist.txt"

            # save_array = np.append(np.array([[1, 1], [1, 1], [1, 1], [1, 1]]), save_array)
            np.savetxt("Z:/Studenten/Baier/Messungen/sortme/" + save_name, save_array, delimiter=";")

        """calculate dose"""
        e_bins.append(quad_poly(bins[-1]))

        dose = dose * 1000 * 1.602176487E-19 / mass

        print(f"Sample {sample_name} got irradiated by {iso_name} for {irr_time}s at {temp}emp: dose = {dose*10**6} muSV, dose rate: {8600*(dose*10**6)/int(irr_time)} muSv/h")
        if plot:
            ax.stairs(e_vals, e_bins, label=f"{iso_name} for {irr_time}")



    if plot:
        ax.set_xlabel(r"Energie / keV")
        ax.set_ylabel(r"gezählte Ereignisse")
        # ax.set_title("Irgendeine Messung von sonstwas")

        ax.tick_params(direction="in", top=True, right=True)
        ax.ticklabel_format(style="sci", useMathText=False, useLocale=True)
        ax.grid(visible=True)
        ax.set_xbound([0, 50])
        ax.set_ybound([0, 30000])


        ax.legend()
        plt.show()


E_calib(data_dict["pvcebis110"], "roomt", save=False, plot=False)
print("")
# E_calib(data_dict["pvcebis110"], "lowt", plot=True)
print("")
E_calib(data_dict["ebis110"], "roomt")
print("")
# E_calib(data_dict["ebis110"], "lowt")
# E_calib(data_dict["dsf"], "roomt", plot=True)



"""name = c.search_in_dir("data/sev/ebis110",
                       identifiers=["na22", "900s", "hist", "lowt", "ecalib"])[0]
print(name)
c.draw_by_name(name, draw_kwargs={
    "ax_config":{
        "save": False,
        "draw": True,
        "yscale": "linear",
        "xlabel": "Kanäle"
    }
})"""



"""
Messnotizen 
ebis110
 - kalte Messung als allererstes, Na als letztes in der Reihe -> Detektor bis dahin vllt schon sehr kalt?
 - stärktes nichtlineares Verhalten?
 - vllt funktioniert Detektor bei geringen Temperaturen tatsächlich besser und die Kante ist echt?
"""








