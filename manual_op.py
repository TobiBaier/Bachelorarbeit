from control_old import get_inst
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

# names = curr_cont.get_names("data/uv-vis", ["combi92", "fast"])
# names.extend(curr_cont.get_names("data/uv-vis", ["combi14", "fast", "_1"]))
# labels = curr_cont.extract_label_from_path(names)
# print(names, labels)
# title = "Vergleich verschiedene Combi92 Proben und Combi14"
# path = "zz_uv-vis_combis/combi_comp.png"
# curr_cont.multi_plot(names, labels, path, title=title)"

names = curr_cont.get_names("data/spec", identifiers=["sr", "ppo1"])
names.extend(curr_cont.get_names("data/uv-vis", identifiers=["_1", "fast", "ppo1"]))
print(names)
labels = curr_cont.extract_label_from_path(names)
print(labels)
title = "read the description"
path = "zz_spec_uv/lotsofspectracomp.png"
curr_cont.twin_xscale_plot(names, labels, path, draw_label=False)










