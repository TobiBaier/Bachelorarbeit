from control import get_inst
import re
from pprint import pprint

c = get_inst("Z:\Studenten\Baier\Messungen")
# c = get_inst("C:/Users/baier/OneDrive/Uni/Bachelorarbeit")

c.c_file.sort_to_dirs()
# c.plot_dir("data/spec/uv-led")
# c.plot_dir("data/uv-vis")
# c.plot_dir("data/sev/ej200", identifiers=["good"])

"""name = c.search_in_dir("data/spec/ppo5",
                       identifiers=["sr90", "good"])[0]
print(name)
c.auto_plot_data(name, auto_title=False,
                 ax_config={
                     "save": False,
                     "draw": True,
                     # "path": "Z:/Studenten/Baier/Latex/images/pu_sev",
                     "draw": True,
                     "xbounds": [300, 550]
                 }
)"""

# names = ["spec_pu_brg2s076_sr90_good", "spec_pu_brg2s076_5step_filter_good"]
# labels = c.extract_labels_from_path(names)
# c.multi_plot(names, labels, path=None, show_final_plot=True)


cmap = {
    "pu": "gray",
    "ppo1": "xkcd:light violet",
    "ppo5": "xkcd:neon purple",
    "3hf1": "lime green",
    "combi14": "aquamarine",
    "combi92": "light teal",
    "bis105": "sea blue",
    "popop105": "cornflower blue",
}

"""def color_mapping(names):
    colors = []
    for name in names:
        inst, sample = c.c_file.get_inst_and_sample(name)
        colors.append(cmap[sample])
    return colors

names = c.search_in_dir("data/spec", identifiers=["good"], or_identifiers=["pu", "ppo1", "ppo5", "3hf1"], not_identifiers=["_e"])
print(names)
print(color_mapping(names))"""






"""
color mapping (alt):
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

names = c.search_in_dir("data/sev/dsf",
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
        "yscale": "log",
        "draw": False,
        "save": False
    }
}
# style = {"c": ["xkcd:light teal", 'xkcd:neon green', "xkcd:light violet", "xkcd:charcoal"]}
# labels = c.extract_labels_from_path(names)
labels = ["am", "cm", "na"]
c.multi_plot(names, labels,
             "zz_sev_combis/testitest.png",
             title="10cm source distance, 100s, room temp, americium214 irradiation",
             style=style, show_final_plot=True, )
