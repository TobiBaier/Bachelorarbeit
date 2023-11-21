import numpy as np
from control import get_inst
import re
from pprint import pprint

import matplotlib.pyplot as plt

c = get_inst("Z:\Studenten\Baier\Messungen")


def extract_file_info(filename):
    inst, sample = c.c_file.get_inst_and_sample(filename)
    s_id = re.search(r"_(b[\w]+g[\d]{1}s[\d]{3})_", filename).group(1)
    # iso_name = re.search(r"_([a-z]{2}[0-9]{2,3})_", filename).group(1)
    # irr_time = re.search(r"_([0-9]{3})s_", filename).group(1)
    # t = re.search(r"_([a-z]{3,4})t_", filename).group(1)

    r_dic = {
        "inst": inst,
        "sample": sample,
        "s_id": s_id,
        # "iso_name": iso_name,
        # "irr_time": irr_time,
        # "t": t
    }

    return r_dic


def do_moving_avg(name, filter_size=2, plot=False):
    wl, vals = c.c_data.auto_read("spec", c.c_file.get_datafile_path(name))

    new_wl, new_vals = [], []

    for i in range (filter_size, len(wl)-filter_size):
        in_region = vals[i-filter_size:i+filter_size]

        new_wl.append(wl[i])
        new_vals.append(np.sum(in_region)/(2*filter_size + 1))

    if plot:
        plt.plot(wl, vals)
        plt.plot(new_wl, new_vals)
        plt.show()

    return new_wl, new_vals


def save_filtered_data(name, relpath="Z:/Studenten/Baier/Messungen/sortme/", filter_size=2):
    wl, vals = do_moving_avg(name, filter_size=filter_size)

    file_info = extract_file_info(name)
    inst = file_info["inst"]
    sample = file_info["sample"]
    s_id = file_info["s_id"]

    new_name = inst + "_" + sample + "_" + s_id + "_sr90_movingavg" + str(filter_size) + ".csv"

    np.savetxt(relpath + new_name, np.column_stack((wl, vals)), delimiter=";")



names = c.search_in_dir("data/spec",
                        identifiers=["good", "sr90"],
                        or_identifiers=["ep", "eppo1", "eppo5", "e3hf110", "e3hf101", "ebis510", "ebis110", "ebis0201", "ebis105"])
# for name in names:
#     print(name)
save_filtered_data("spec_ebis510_bcg2s090_sr90_good")




def comp_image():
    names = ["spec_combi92_brg2s072_sr90_good", "spec_combi92_brg2s072_sr90_movingavg2"]
    labels = ["ohne Filter", "mit Filter"]


    c.multi_plot(names, labels, path="Z:/Studenten/Baier/Latex/images/moving_average_comparison.pdf",
                 show_final_plot=True,
                 plot_kwargs={
                     "color": ["black", "red"]
                 },
                 ax_config={
                     "xbounds": [325, 650],
                     "ybounds": [80, None]
                 })








