import numpy as np
from control import get_inst
import matplotlib as mpl
import matplotlib.pyplot as plt
import json
import re
import numpy as np

c = get_inst("Z:\Studenten\Baier\Messungen")


with open("calibration.json", "r") as of:
    data_dict = json.load(of)

def E_calib(data, temp):
    mass = data["mass"]
    data = data[temp]
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

        e_bins.append(quad_poly(bins[-1]))

        iso_name = re.search(r"_([a-z]{2}[0-9]{2,3})_", name).group(1)
        irr_time = re.search(r"_([0-9]{3})s_", name).group(1)
        sample_name = re.search(r"_([a-z]{4,7}110)_", name).group(1)

        dose = dose * 1000 * 1.602176487E-19 / mass

        print(f"Sample {sample_name} got irradiated by {iso_name} for {irr_time}s: dose = {dose*10**6} muSV, dose rate: {8600*(dose*10**6)/int(irr_time)} muSv/h")


        ax.stairs(e_vals, e_bins, label=f"{iso_name} for {irr_time}")

    ax.legend()
    plt.show()


E_calib(data_dict["pvcebis110"], "roomtemp")
E_calib(data_dict["pvcebis110"], "lowtemp")
E_calib(data_dict["ebis110"], "roomtemp")








"""def Energy_Calib(ch):
    E = np.zeros((len(ch)))
    for i, channel in enumerate(ch):
        if channel < 300:
            E[i] = 7.61706783 + 0.0809628 * channel
        else:
            E[i] = 67.17851564179762 - 0.0679408186449754*channel**1 + 9.306476220015559e-05*channel**2


    return E


file_name = c.search_in_dir("data/sev/ebis110", identifiers=["cm244", "100s", "hist", "hight", "1000K"])[0]
data = c.c_data.auto_read("sev", c.c_file.get_datafile_path(file_name), bin_ret=True)
calib_data = [data[0], Energy_Calib(data[1])]

fig = plt.figure()
ax = fig.add_subplot(111)

ax.stairs(*calib_data, zorder=1000)

ax.set_xbound([0, 400])
ax.set_xlabel("Energie / keV")
ax.set_ylabel("gezählte Ereignisse in 15 min")
ax.set_title(r"$^{241}$Am gemessen mit Epoxidharzszintillator (ohne PVC)")

ax.grid(visible=True, color="#87878790", zorder=-1, lw=1)
ax.tick_params(direction="in", top=True, right=True)
ax.ticklabel_format(style="sci", useMathText=False, useLocale=True)
ax.set_yscale("log")

plt.show()"""






