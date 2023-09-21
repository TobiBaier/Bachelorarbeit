from control import get_inst
curr_cont = get_inst()
# curr_cont.auto_plot_data("sev_ppo1_na22_hist_1_3.txt")
# curr_cont.plot_dir("sev/ppo1")
# print(curr_cont.curr_file.ids)
# curr_cont.auto_plot_data(s)
# curr_cont.plot_dir("data/uv-vis")
# print(curr_cont.curr_file.save_in_dir())

# names = curr_cont.get_names("data", ["uv-vis", "_1"])
# labels = curr_cont.extract_label_from_path(names)















'''
title = "Vergleich Auswirkung Probendicke (bei PU)"
name_list = ["uv-vis_pu_brg2s076_trans_survey_1",
             "uv-vis_pu_bcg2s025_trans_survey_1"]
label_list = ["pu_brg2s076", "pu_bcg2s025"]
path = "uv-vis_combis/size_comp_pu.png"

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


