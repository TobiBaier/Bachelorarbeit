from control import get_inst
import re
from pprint import pprint

c = get_inst("Z:\Studenten\Baier\Messungen")
# c = get_inst("C:/Users/baier/OneDrive/Uni/Bachelorarbeit")

c.c_file.sort_to_dirs()
# c.plot_dir("data/spec/uv-led")
# c.plot_dir("data/uv-vis")
# c.plot_dir("data/sev/ej200", identifiers=["good"])

name = c.search_in_dir("data/sev/pu",
                       identifiers=["na22", "hist"])[0]
print(name)
c.auto_plot_data(name, auto_title=False,
                 ax_config={
                     "save": True,
                     "path": "Z:/Studenten/Baier/Latex/images/pu_sev",
                     "draw": True,
                     "yscale": "log",
                     "xlabel": "Kanäle",
                     "xbounds": [0, 750]
                 }
)

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
