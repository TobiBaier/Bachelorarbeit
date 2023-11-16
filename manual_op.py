from control import get_inst
import re
from pprint import pprint

c = get_inst("Z:\Studenten\Baier\Messungen")
# c = get_inst("C:/Users/baier/OneDrive/Uni/Bachelorarbeit")

c.c_file.sort_to_dirs()
# c.plot_dir("data/spec/uv-led")
# c.plot_dir("data/uv-vis")
# c.plot_dir("data/sev/ej200", identifiers=["good"])

name = c.search_in_dir("data/sev/pvcebis110",
                       identifiers=["cm244", "100s", "hist", "hight"])[0]
print(name)
c.draw_by_name(name, draw_kwargs={
    "ax_config":{
        "save": False,
        "draw": True,
        "yscale": "linear",
        "xlabel": "Kanäle"
    }
})


"""
color mapping:
    3hf1: 'xkcd:bright green'
    bis105: 'xkcd:electric blue'
    combi14: 'xkcd:neon green'
    combi92: 'xkcd:light teal',
    popop105: 'xkcd:dark blue' 
    ppo1: 'xkcd:light violet', 
    ppo5: 'xkcd:neon purple', 
    pu: 'gray'
    ebis110: "xkcd:electric_blue"
    sebis110: "xkcd:dusky blue"
    pvcebis110: "xkcd:lightblue"
    ebis510: "xkcd:cobalt"
    ebis105: "xkcd:dark indigo"
    ebis0201: "robin's egg blue"
    e3hf110: xkcd:neon green
    e3hf101: xkcd:light teal
    ej200: "xkcd:charcoal"
"""

"""names = c.search_in_dir("data/sev/dsf",
                        identifiers=["hist", "hight"])
# names.append("sev_ej260_bng2s100_na22_530_15min_hist.txt")
pprint(names)
style = {
    "plot_kwargs": {
        "color": ["xkcd:electric blue", "xkcd:dusky blue", "xkcd:lightblue"],
    },
    "ax_config":{
        "xbounds": [0, None],
        "ybounds": [None, None],
        "yscale": "log"
    }
}
# style = {"c": ["xkcd:light teal", 'xkcd:neon green', "xkcd:light violet", "xkcd:charcoal"]}
# labels = c.extract_labels_from_path(names)
labels = ["am", "cm", "na"]
c.multi_plot(names, labels,
             "zz_sev_combis/testitest.png",
             title="10cm source distance, 100s, room temp, americium214 irradiation",
             style=style, show_final_plot=True, )"""
"""

"Transmission spectrum: 1%PPO+0.1%Bis, 0.2%PPO+0.01%Bis, 5%PPO+0.1%Bis"
names = c.search_in_dir("data/spec", identifiers=["good"])
labels = c.extract_labels_from_path(names)
uv_names = []
for label in labels:
    print(label)
    uv_names.extend(c.search_in_dir("data/uv-vis", identifiers=[label, "good", "survey"]))

for name, uv_name, label in zip(names, uv_names, labels):
    print(name, uv_name)
    sample = c.c_file.get_inst_and_sample(name)[1]
    c.twin_x_scale_plot([name, uv_name], ["spec", "uv-vis"], "zz_spec_uv/with_popop_bis/"+sample+".png", title=sample)"""

#c.plot_dir("data/sev", identifiers=["good"])
#c.plot_dir("data/spec", identifiers=["good"])
#c.plot_dir("data/uv-vis", identifiers=["good"])

"""names = c.search_in_dir("data/uv-vis", identifiers=["good", "fast"], or_identifiers=["ppo1", "ppo5"])
pprint(names)
labels = c.extract_labels_from_path(names)
c.multi_plot(names, labels, "zz_uv-vis_combis/ppo_1and5.png", title="Spectrum of: PPO (1%/5%)")"""



"""pprint(c.search_in_dir("processed_data/spec", identifiers=["good"], no_filecheck=True))
c.c_file.copy_to_new_dictionary(c.search_in_dir("processed_data/spec", identifiers=["good"], no_filecheck=True), "zz_good_data/spec")
c.c_file.copy_to_new_dictionary(c.search_in_dir("processed_data/sev", identifiers=["good"], no_filecheck=True), "zz_good_data/sev")
c.c_file.copy_to_new_dictionary(c.search_in_dir("processed_data/uv-vis", identifiers=["good"], no_filecheck=True), "zz_good_data/uv-vis")"""



