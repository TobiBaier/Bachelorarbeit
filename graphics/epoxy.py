from control import get_inst
import re
from pprint import pprint

c = get_inst("Z:\Studenten\Baier\Messungen")
# c = get_inst("C:/Users/baier/OneDrive/Uni/Bachelorarbeit")

c.c_file.sort_to_dirs()

cmap = {
    "ep": ["black", "Epoxidharz (EP)"],
    "eppo1": ["xkcd:soft purple", "EP mit 1% PPO"],
    "eppo5": ["xkcd:electric purple", "EP mit 5% PPO"],
    "e3hf101": ["xkcd:light teal", "EP mit 1% 3HF und 0,01% 3HF"],
    "e3hf110": ["xkcd:lime green", "EP mit 1% PPO und 0,1% 3HF"],
    "ebis110": ["xkcd:primary blue", "EP mit 1% PPO und 0,1% Bis-MSB"],
    "ebis105": ["xkcd:lightish blue", "EP mit 1% PPO und 0,05% Bis-MSB"],
    "ebis0201": ["xkcd:neon blue", "EP mit 0,2% PPO und 0,01% Bis-MSB"],
    "ebis510": ["xkcd:blueberry", "EP mit 5% PPO und 0,1% Bis-MSB"]
}

"""cmap = {
    "ep": ["black", "Epoxidharz (EP)"],
    "eppo1": ["xkcd:soft purple", "1% PPO"],
    "eppo5": ["xkcd:electric purple", "5% PPO"],
    "e3hf101": ["xkcd:light teal", "1% 3HF, 0,01% 3HF"],
    "e3hf110": ["xkcd:lime green", "1% PPO, 0,1% 3HF"],
    "ebis110": ["xkcd:primary blue", "1% PPO, 0,1% Bis-MSB"],
    "ebis105": ["xkcd:lightish blue", "1% PPO, 0,05% Bis-MSB"],
    "ebis0201": ["xkcd:neon blue", "0,2% PPO, 0,01% Bis-MSB"],
    "ebis510": ["xkcd:blueberry", "5% PPO, 0,1% Bis-MSB"]
}"""


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




def with_avg():
    """names = c.search_in_dir("data/spec",
                            identifiers=["movingavg", "sr90"],
                            or_identifiers=["ep", "eppo1", "eppo5", "e3hf110", "e3hf101", "ebis510", "ebis110", "ebis0201", "ebis105"], )
    labels = label_mapping(names)
    colors = color_mapping(names)
    c.multi_plot(names, labels, "Z:/Studenten/Baier/Latex/images/spec_all_ep_samples.pdf",
                 show_final_plot=False,
                 plot_kwargs={
                     "color": colors
                 },
                 ax_config={
                     "xbounds": [310, 640],
                     "ybounds": [65, None],
                 },
                 legend_kwargs={
                     "fontsize": "small",
                     "labelcolor": "black"
    })

    names = c.search_in_dir("data/spec",
                            identifiers=["movingavg", "sr90"],
                            or_identifiers=["ep", "eppo1", "eppo5"], )
    labels = label_mapping(names)
    colors = color_mapping(names)
    c.multi_plot(names, labels, "Z:/Studenten/Baier/Latex/images/spec_ep_ppo_samples.pdf",
                 show_final_plot=True,
                 plot_kwargs={
                     "color": colors
                 },
                 ax_config={
                     "xbounds": [310, 540],
                     "ybounds": [65, None],
                 })"""

with_avg()