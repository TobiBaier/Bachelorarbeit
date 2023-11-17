from control import get_inst
import numpy as np
import re
import json
import matplotlib.pyplot as plt

c = get_inst("Z:\Studenten\Baier\Messungen")


def extract_file_info(filename):
    inst, sample = c.c_file.get_inst_and_sample(filename)
    s_id = re.search(r"_(b[\w]+g[\d]{1}s[\d]{3})_", filename).group(1)
    iso_name = re.search(r"_([a-z]{2}[0-9]{2,3})_", filename).group(1)
    irr_time = re.search(r"_([0-9]{3})s_", filename).group(1)
    t = re.search(r"_([a-z]{3,4})t_", filename).group(1)

    r_dic = {
        "inst": inst,
        "sample": sample,
        "s_id": s_id,
        "iso_name": iso_name,
        "irr_time": irr_time,
        "t": t
    }

    return r_dic


def e_calc(name):
    file_info = extract_file_info(name)

    t = file_info["t"]
    if t == "low":
        temp = "lowtemp"
    else:
        temp = "roomtemp"

    sample_name = file_info["sample"]

    data = json.load(open("../calibration.json", "r"))

    data = data[sample_name][temp]
    lin_poly = np.polynomial.Polynomial(data["linear"])
    quad_poly = np.polynomial.Polynomial(data["quadratic"])
    pivot = data["switch"]
    cutoff = data["spec_cutoff"]

    vals, bins = c.c_data.auto_read("sev", c.c_file.get_datafile_path(name), bin_ret=True)
    e_bins = []
    e_vals = []
    dose = 0

    for i in range(len(bins) - 1):
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

    return e_bins, e_vals


def do_rebin(filename, bin_size, save=False, relpath="Z:/Studenten/Baier/Messungen/sortme/"):
    bins, vals = c.c_data.auto_read("sev", c.c_file.get_datafile_path(filename), bin_ret=False)

    cut_away = 0
    while True:
        if (len(bins)-cut_away)%bin_size != 0:
            pass
        else:
            break
        cut_away += 1

    old_vals = vals[:-cut_away]
    bins = bins[:-cut_away]

    bins = bins[::bin_size]
    vals = np.zeros(np.shape(bins))

    for i in range(len(bins)):
        for j in range(bin_size):
            vals[i] = vals[i] + old_vals[i*bin_size + j]

    bins = np.append(bins, bins[-1] + (bins[-1] - bins[-2]))
    plt.stairs(vals, bins)
    plt.show()


    if save:
        save_array = np.column_stack((np.append([0, 0, 0, 0], bins), np.append([0, 0, 0, 0], vals)))
        np.savetxt(relpath + filename + "_rebin" + str(bin_size) + ".txt", save_array, delimiter=";")


do_rebin("sev_dsf_bng2s100_am241_10cm_100s_hight_ecalib_hist", 25)


def save_with_e_calibration(filename, relpath="Z:/Studenten/Baier/Messungen/sortme/"):
    save_array = get_formatted_e_calibration(filename)

    file_info = extract_file_info(filename)
    inst = file_info["inst"]
    sample = file_info["sample"]
    s_id = file_info["s_id"]
    iso_name = file_info["iso_name"]
    irr_time = file_info["irr_time"]
    t = file_info["t"]

    new_name = inst + "_" + sample + "_" + s_id + "_" + iso_name + "_" + "10cm" + "_" + irr_time + "s_" + t + "t" + "_ecalib_hist.txt"

    np.savetxt(relpath + new_name, save_array, delimiter=";")

    print(f"Converted and saved {filename} to {relpath}!")


def get_formatted_e_calibration(filename):
    e_bins, e_vals = e_calc(filename)

    return np.column_stack((np.append([0, 0, 0, 0], e_bins), np.append([0, 0, 0, 0], e_vals)))


def calibrate_and_save_all_data(sample_id, temp):
    data = json.load(open("../calibration.json", "r"))

    data = data[sample_id][temp]

    for name in data["filenames"]:
        save_with_e_calibration(name)


def draw_calibrated_data(filename, xbounds=None, ax=None, save=False, draw=True,
                         path=None, yscale="log", color="black", label=None, auto_title=False):
    filepath = c.c_file.get_datafile_path(filename)

    hist_data = c.c_data.auto_read("sev", filepath)

    file_info = extract_file_info(filename)
    iso_name = file_info["iso_name"]

    if xbounds is None:
        lowx = hist_data[1][0]
        if iso_name == "cm244":
            highx = 80
        if iso_name == "am241":
            highx = 220
        if iso_name == "na22":
            highx = 2500
        if iso_name == "ba133":
            highx = 1000

        xbounds = [lowx, highx]

    if label is None:
        if iso_name == "cm244":
            label = r"$^{244}$Cm"
        if iso_name == "am241":
            label = r"$^{241}$Am"
        if iso_name == "na22":
            label = r"$^{22}$Na"
        if iso_name == "ba133":
            label = r"$^{133}$Ba"

    if path is None:
        c.auto_plot_data(filename, auto_title=auto_title,
                         ax_config={
                             "save": save,
                             "draw": draw,
                             "xbounds": xbounds,
                             "yscale": yscale,
                             "ax": ax},
                         plot_kwargs={
                             "color": color,
                             "label": label
                         })
    else:
        c.auto_plot_data(filename, auto_title=auto_title,
                         ax_config={
                             "save": save,
                             "draw": draw,
                             "path": None,
                             "xbounds": xbounds,
                             "yscale": yscale,
                             "ax": ax},
                         plot_kwargs={
                             "color": color,
                             "label": label
                         })


# calibrate_and_save_all_data("pvcebis110", "roomtemp")
# calibrate_and_save_all_data("pvcebis110", "lowtemp")
# calibrate_and_save_all_data("ebis110", "lowtemp")
# calibrate_and_save_all_data("ebis110", "roomtemp")
# calibrate_and_save_all_data("dsf", "roomtemp")
# c.c_file.sort_to_dirs()



# Duo-Plot Code
"""fig = plt.figure()
ax = fig.add_subplot(111)

draw_calibrated_data("sev_pvcebis110_bng2s103_cm244_10cm_100s_hight_ecalib_hist",
                     ax=ax, draw=False, color="xkcd:electric blue")
draw_calibrated_data("sev_pvcebis110_bng2s103_am241_10cm_100s_hight_ecalib_hist",
                     ax=ax, color="xkcd:neon purple")
"""
"""c.c_draw.make_diagram("sev", c.c_data.auto_read("sev", c.c_file.get_datafile_path("sev_pvcebis110_bng2s103_cm244_10cm_100s_hight_ecalib_hist")),
                        ax_config={"draw": True, "save": False})"""

# c.c_file.sort_to_dirs()
