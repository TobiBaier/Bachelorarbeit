from control import get_inst
import re
from pprint import pprint

# c = get_inst("Z:\Studenten\Baier\Messungen")
c = get_inst("C:/Users/baier/OneDrive/Uni/Bachelorarbeit")

c.c_file.sort_to_dirs()

pprint(c.search_in_dir("data/sev/dsf"))

c.draw_by_name('sev_dsf_bng2s100_na22_10cm_300s_hight_hist.txt',
               draw_kwargs=
               {
                   "ax_config":{
                       "save": False,
                       "draw": True
                   }
               })

"""name = c.search_in_dir("data/spec/pu",
                       identifiers=["sr90", "good"])[0]
print(name)
c.auto_plot_data(name, auto_title=False,
                 ax_config={
                     "save": False,
                     "draw": True,
                     "path": "Z:/Studenten/Baier/Latex/images/uv-vis_pu.pdf",
                     "xbounds": [300, 450],
                     "ybounds": [75, None],
                 },
                 plot_kwargs={
                     "color": "black"
                 }
)"""

# names = ["spec_pu_brg2s076_sr90_good", "spec_pu_brg2s076_5step_filter_good"]
# labels = c.extract_labels_from_path(names)
# c.multi_plot(names, labels, path=None, show_final_plot=True)

cmap = {
    "pu": ["black", "Polyurethan (PU)"],
    "ppo1": ["xkcd:soft purple", "PU mit 1% PPO"],
    "ppo5": ["xkcd:electric purple", "PU mit 5% PPO"],
    "3hf1": ["xkcd:lime green", "PU mit 1% 3HF"],
    "combi14": ["xkcd:aquamarine", "PU mit 1% PPO und 0,1% 3HF"],
    "combi92": ["xkcd:light teal", "PU mit 1% PPO und 0,05% 3HF"],
    "bis105": ["xkcd:lightish blue", "PU mit 1% PPO und 0,05% Bis-MSB"],
    "popop105": ["xkcd:blueberry", "PU mit 1% PPO und 0,05% POPOP"]
}


def color_mapping(names):
    colors = []
    for name in names:
        inst, sample = c.c_file.get_inst_and_sample(name)
        colors.append(cmap[sample][0])
    return colors


def label_mapping(names):
    labels = []
    for name in names:
        inst, sample = c.c_file.get_inst_and_sample(name)
        labels.append(cmap[sample][1])
    return labels





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

