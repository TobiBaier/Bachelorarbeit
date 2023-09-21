from control import get_inst
curr_cont = get_inst()
# curr_cont.auto_plot_data("sev_ppo1_na22_hist_1_3.txt")
# curr_cont.plot_dir("sev/ppo1")
# print(curr_cont.curr_file.ids)

s = "sev_ppo1_na22_hist_1_3.txt"

# curr_cont.auto_plot_data(s)

# curr_cont.plot_dir("condensed_data/ppo1", extra_identifier="sev")

# curr_cont.plot_dir("uv-vis")

name_list = ["uv-vis_ppo1_trans_fast", "spec_ppo1_sr_1"]
label_list = ["uv-vis", "spec"]

curr_cont.multi_plot(name_list, label_list, path="uv-vis_combis/uv-vis_spec_ppo1.png",
             title="Transmission and Emission of ppo1")

'''
the design for the spec plots looks shit -> no more measurement points?

somehow add twin-plot capability to allow for two instruments in one graph
 -> https://matplotlib.org/stable/gallery/subplots_axes_and_figures/two_scales.html
 
add function to allow different presets in plots -> probably needs rework of control class and
overhaul of filemanager (maybe combine a few functions?)
'''





