from control import get_inst
curr_cont = get_inst()
# curr_cont.auto_plot_data("sev_ppo1_na22_hist_1_3.txt")
# curr_cont.plot_dir("sev/ppo1")
# print(curr_cont.curr_file.ids)
# curr_cont.auto_plot_data(s)
# curr_cont.plot_dir("data/uv-vis/pu", extra_identifier=["040"])
# print(curr_cont.curr_file.save_in_dir())


# names = curr_cont.get_names("data/uv-vis", ["pu", "_1", "fast"])
# labels = curr_cont.extract_label_from_path(names)
# title = "Vergleich Auswirkung Probendicke (bei PU)"
# path = "uv-vis_combis/size_comp_pu.png"
# curr_cont.multi_plot(names, labels, path, title=title)

names = [
    "spec_ppo1_sr_1",
    "uv-vis_ppo1_bcg2s082_trans_survey_1"
]
labels = curr_cont.extract_label_from_path(names)
path = "zz_spec_uv/ppo1_trans_emi.png"
curr_cont.twin_xscale_plot(names, labels, path)









# curr_cont.plot_dir("uv-vis")



'''
the design for the spec plots looks shit -> no more measurement points?

somehow add twin-plot capability to allow for two instruments in one graph
 -> https://matplotlib.org/stable/gallery/subplots_axes_and_figures/two_scales.html
 
add function to allow different presets in plots -> probably needs rework of control class and
overhaul of filemanager (maybe combine a few functions?)
'''

'''
curr_cont.multi_plot(name_list, label_list, path, title=title)

title = "Vergleich Transmission PU mit versch. Substanzen"
name_list = ["uv-vis_3hf1_bng2s069_trans_survey_1",
             "uv-vis_combi14_bng2s086_trans_survey_1",
             "uv-vis_ppo1_bcg2s082_trans_survey_1",
             "uv-vis_ppo5_bcg2s067_trans_survey_1",
             "uv-vis_pu_brg2s076_trans_survey_1"]
label_list = ["3hf1_bng2s069",
              "combi14_bng2s086",
              "ppo1_bcg2s082",
              "ppo5_bcg2s067",
              "pu_brg2s076"]
path = "uv-vis_combis/all_samples_21-09-23.png"


curr_cont.multi_plot(name_list, label_list, path, title=title)
'''


