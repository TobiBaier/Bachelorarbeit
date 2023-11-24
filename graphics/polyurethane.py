from control import get_inst
import re
from pprint import pprint

c = get_inst("Z:\Studenten\Baier\Messungen")
# c = get_inst("C:/Users/baier/OneDrive/Uni/Bachelorarbeit")

c.c_file.sort_to_dirs()

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

def no_avg():
    names = c.search_in_dir("data/spec", identifiers=["good", "sr90"], or_identifiers=["pu", "ppo1", "ppo5", "combi92", "bis105", "popop105", "combi14"], not_identifiers=["_e"])
    names[1], names[3] = names[3], names[1]
    labels = label_mapping(names)
    colors = color_mapping(names)
    c.multi_plot(names, labels, "Z:/Studenten/Baier/Latex/images/spec_all_pu_samples.pdf",
                 show_final_plot=False,
                 plot_kwargs={
                     "color": colors
                 },
                 ax_config={
                     "xbounds": [300, 650],
                     "ybounds": [80, None],
                 })

    names = c.search_in_dir("data/spec", identifiers=["good", "sr90"], or_identifiers=["pu", "ppo1", "ppo5"], not_identifiers=["_e"])
    labels = label_mapping(names)
    colors = color_mapping(names)
    c.multi_plot(names, labels, "Z:/Studenten/Baier/Latex/images/spec_pu_ppo.pdf",
                 show_final_plot=False,
                 plot_kwargs={
                     "color": colors
                 },
                 ax_config={
                     "xbounds": [300, 550],
                     "ybounds": [80, None]
                 })




    names = c.search_in_dir("data/uv-vis", identifiers=["good", "fast"], or_identifiers=["pu", "ppo1", "ppo5"], not_identifiers=["_e"])
    labels = label_mapping(names)
    colors = color_mapping(names)
    c.multi_plot(names, labels, "Z:/Studenten/Baier/Latex/images/uv-vis_pu_ppo.pdf",
                 show_final_plot=False,
                 plot_kwargs={
                     "color": colors
                 },
                 ax_config={
                     "xbounds": [300, 800],
                     "ybounds": [0, None]
                 })
    names = c.search_in_dir("data/uv-vis", identifiers=["good", "fast"], or_identifiers=["pu", "ppo1", "ppo5", "combi92", "bis105", "popop105", "combi14"], not_identifiers=["_e"])
    names[1], names[3] = names[3], names[1]
    labels = label_mapping(names)
    colors = color_mapping(names)
    c.multi_plot(names, labels, "Z:/Studenten/Baier/Latex/images/uv-vis_all_pu_samples.pdf",
                 show_final_plot=False,
                 plot_kwargs={
                     "color": colors
                 },
                 ax_config={
                     "xbounds": [300, 800],
                     "ybounds": [0, None]
                 })


    names = c.search_in_dir("data/sev", identifiers=["good", "na22", "hist"], or_identifiers=["pu", "ppo1", "ppo5"], not_identifiers=["_e"])
    labels = label_mapping(names)
    colors = color_mapping(names)
    c.multi_plot(names, labels, "Z:/Studenten/Baier/Latex/images/sev_pu_ppo.pdf",
                 show_final_plot=False,
                 plot_kwargs={
                     "color": colors
                 },
                 ax_config={
                     "xbounds": [60, 1000],
                     "ybounds": [0, None],
                     "xlabel": "Pulsintegral / Kanal"
                 })

    names = c.search_in_dir("data/sev", identifiers=["good", "hist", "na22"], or_identifiers=["pu", "ppo1", "ppo5", "combi92", "bis105", "popop105", "combi14"], not_identifiers=["_e"])
    names[1], names[3] = names[3], names[1]
    labels = label_mapping(names)
    colors = color_mapping(names)
    c.multi_plot(names, labels, "Z:/Studenten/Baier/Latex/images/sev_all_pu_samples.pdf",
                 show_final_plot=False,
                 plot_kwargs={
                     "color": colors
                 },
                 ax_config={
                     "xbounds": [60, 1000],
                     "ybounds": [0, None],
                     "xlabel": "Pulsintegral / Kanal"
                 })


def with_avg():
    names = c.search_in_dir("data/spec", identifiers=["movingavg2", "sr90"],
                            or_identifiers=["pu", "ppo1", "ppo5", "combi92", "bis105", "popop105", "combi14"],
                            not_identifiers=["_e"])
    names[1], names[3] = names[3], names[1]
    labels = label_mapping(names)
    colors = color_mapping(names)
    c.multi_plot(names, labels, "Z:/Studenten/Baier/Latex/images/spec_all_pu_samples.pdf",
                 show_final_plot=False,
                 plot_kwargs={
                     "color": colors
                 },
                 ax_config={
                     "xbounds": [310, 640],
                     "ybounds": [75, None],
                 })

    names = c.search_in_dir("data/spec", identifiers=["movingavg2", "sr90"], or_identifiers=["pu", "ppo1", "ppo5"],
                            not_identifiers=["_e"])
    labels = label_mapping(names)
    colors = color_mapping(names)
    c.multi_plot(names, labels, "Z:/Studenten/Baier/Latex/images/spec_pu_ppo.pdf",
                 show_final_plot=True,
                 plot_kwargs={
                     "color": colors
                 },
                 ax_config={
                     "xbounds": [310, 540],
                     "ybounds": [75, None]
                 })

    """names = c.search_in_dir("data/uv-vis", identifiers=["good", "fast"], or_identifiers=["pu", "ppo1", "ppo5"],
                            not_identifiers=["_e"])
    labels = label_mapping(names)
    colors = color_mapping(names)
    c.multi_plot(names, labels, "Z:/Studenten/Baier/Latex/images/uv-vis_pu_ppo.pdf",
                 show_final_plot=True,
                 plot_kwargs={
                     "color": colors
                 },
                 ax_config={
                     "xbounds": [300, 800],
                     "ybounds": [0, None]
                 })"""
    """

    names = c.search_in_dir("data/uv-vis", identifiers=["good", "fast"],
                            or_identifiers=["pu", "ppo1", "ppo5", "combi92", "bis105", "popop105", "combi14"],
                            not_identifiers=["_e", "025", "040"])
    names[1], names[3] = names[3], names[1]
    pprint(names)
    labels = label_mapping(names)
    colors = color_mapping(names)
    c.multi_plot(names, labels, "C:/Users/baier\OneDrive/Uni\Bachelorarbeit_2\latex\images/uv-vis_all_pu_samples.pdf",
                 show_final_plot=False,
                 plot_kwargs={
                     "color": colors
                 },
                 ax_config={
                     "xbounds": [300, 800],
                     "ybounds": [0, None]
                 })
    names = c.search_in_dir("data/sev", identifiers=["good", "na22", "hist"], or_identifiers=["pu", "ppo1", "ppo5"],
                            not_identifiers=["_e"])
    labels = label_mapping(names)
    colors = color_mapping(names)
    c.multi_plot(names, labels, "Z:/Studenten/Baier/Latex/images/sev_pu_ppo.pdf",
                 show_final_plot=False,
                 plot_kwargs={
                     "color": colors
                 },
                 ax_config={
                     "xbounds": [60, 1000],
                     "ybounds": [0, None],
                     "xlabel": "Pulsintegral / Kanal"
                 })
    
    names = c.search_in_dir("data/sev", identifiers=["good", "hist", "na22"],
                            or_identifiers=["pu", "ppo1", "ppo5", "combi92", "bis105", "popop105", "combi14"],
                            not_identifiers=["_e"])
    names[1], names[3] = names[3], names[1]
    labels = label_mapping(names)
    colors = color_mapping(names)
    c.multi_plot(names, labels, "C:/Users/baier\OneDrive/Uni\Bachelorarbeit_2\latex\images/sev_all_pu_samples.pdf", #"Z:/Studenten/Baier/Latex/images/sev_all_pu_samples.pdf",
                 show_final_plot=True,
                 plot_kwargs={
                     "color": colors
                 },
                 ax_config={
                     "xbounds": [60, 1000],
                     "ybounds": [0, None],
                     "xlabel": "Pulsintegral / Kanal"
                 })"""


def pure_pu():
    pu_spec = c.search_in_dir("data/spec/pu", identifiers=["movingavg2", "sr90"])[0]
    pu_uvvis = c.search_in_dir("data/uv-vis/pu", identifiers=["good", "fast"])[0]

    c.auto_plot_data(pu_spec, auto_title=False,
                     plot_kwargs={
                         "color": "black"
                     },
                     ax_config={
                         "xbounds": [310, 440],
                         "ybounds": [75, None],
                         "path": "Z:/Studenten/Baier/Latex/images/spec_pu.pdf"
                     })
    c.auto_plot_data(pu_uvvis, auto_title=False,
                     plot_kwargs={
                         "color": "black"
                     },
                     ax_config={
                         "xbounds": [300, 800],
                         "ybounds": [0, None],
                         "path": "Z:/Studenten/Baier/Latex/images/uv-vis_pu.pdf"
                     })

pure_pu()
with_avg()