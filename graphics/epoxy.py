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
    "e3hf101": ["xkcd:light teal", "EP mit 1% PPO und 0,01% 3HF"],
    "e3hf110": ["xkcd:lime green", "EP mit 1% PPO und 0,1% 3HF"],
    "ebis110": ["xkcd:primary blue", "EP mit 1% PPO und 0,1% Bis-MSB"],
    "ebis105": ["xkcd:lightish blue", "EP mit 1% PPO und 0,05% Bis-MSB"],
    "ebis0201": ["xkcd:neon blue", "EP mit 0,2% PPO und 0,01% Bis-MSB"],
    "ebis510": ["xkcd:blueberry", "EP mit 5% PPO und 0,1% Bis-MSB"]
}

short_cmap = {
    "ep": ["black", "Epoxidharz (EP)"],
    "eppo1": ["xkcd:soft purple", "1% PPO"],
    "eppo5": ["xkcd:electric purple", "5% PPO"],
    "e3hf101": ["xkcd:light teal", "1% PPO, 0,01% 3HF"],
    "e3hf110": ["xkcd:lime green", "1% PPO, 0,1% 3HF"],
    "ebis110": ["xkcd:primary blue", "1% PPO, 0,1% Bis-MSB"],
    "ebis105": ["xkcd:lightish blue", "1% PPO, 0,05% Bis-MSB"],
    "ebis0201": ["xkcd:neon blue", "0,2% PPO, 0,01% Bis-MSB"],
    "ebis510": ["xkcd:blueberry", "5% PPO, 0,1% Bis-MSB"]
}


def color_mapping(names):
    colors = []
    for name in names:
        inst, sample = c.c_file.get_inst_and_sample(name)
        colors.append(cmap[sample][0])
    return colors


def label_mapping(names, short=False):
    labels = []
    for name in names:
        inst, sample = c.c_file.get_inst_and_sample(name)
        if not short:
            labels.append(cmap[sample][1])
        else:
            labels.append(short_cmap[sample][1])
    return labels




def with_avg(path="Z:/Studenten/Baier/Latex/images/"):
    names = c.search_in_dir("data/spec",
                            identifiers=["movingavg", "sr90"],
                            or_identifiers=["ep", "eppo1", "eppo5", "e3hf110", "e3hf101", "ebis510", "ebis110", "ebis0201", "ebis105"],
                            not_identifiers=["pvcebis", "sebis"])
    labels = label_mapping(names, short=True)
    colors = color_mapping(names)
    c.multi_plot(names, labels, path + "spec_all_ep_samples.pdf",
                 show_final_plot=False,
                 plot_kwargs={
                     "color": colors,
                     "lw": 2,
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
                            or_identifiers=["ep", "eppo1", "eppo5"],
                            not_identifiers=["pvcebis", "sebis"])
    labels = label_mapping(names, short=False)
    colors = color_mapping(names)
    c.multi_plot(names, labels, path + "spec_ep_ppo_samples.pdf",
                 show_final_plot=False,
                 plot_kwargs={
                     "color": colors,
                     "lw": 2,
                 },
                 ax_config={
                     "xbounds": [310, 540],
                     "ybounds": [65, None],
                 })

    names = c.search_in_dir("data/uv-vis", identifiers=["fast"],
                            or_identifiers=["ep", "eppo1", "eppo5"],
                            not_identifiers=["pvcebis", "sebis"])
    labels = label_mapping(names)
    colors = color_mapping(names)
    c.multi_plot(names, labels, path + "uv-vis_ep_ppo.pdf",
                 show_final_plot=False,
                 plot_kwargs={
                     "color": colors,
                     "lw": 2,
                 },
                 ax_config={
                     "xbounds": [250, 800],
                     "ybounds": [0, None]
                 })

    names = c.search_in_dir("data/uv-vis", identifiers=["fast"],
                            or_identifiers=["ep", "eppo1", "eppo5", "e3hf110", "e3hf101", "ebis510", "ebis110", "ebis0201", "ebis105"],
                            not_identifiers=["pvcebis", "sebis", "exclude"])
    labels = label_mapping(names, short=True)
    colors = color_mapping(names)
    c.multi_plot(names, labels, path + "uv-vis_all_ep_samples.pdf",
                 show_final_plot=False,
                 plot_kwargs={
                     "color": colors,
                     "lw": 2
                 },
                 ax_config={
                     "xbounds": [250, 800],
                     "ybounds": [0, None]
                 })

    names = c.search_in_dir("data/sev", identifiers=["good", "na22", "hist"], or_identifiers=["ep", "eppo1", "eppo5"],
                            not_identifiers=["pvcebis", "sebis"])
    labels = label_mapping(names)
    colors = color_mapping(names)
    c.multi_plot(names, labels, path + "sev_ep_ppo.pdf",
                 show_final_plot=False,
                 plot_kwargs={
                     "color": colors,
                 },
                 ax_config={
                     "xbounds": [60, 1000],
                     "ybounds": [0, None],
                     "xlabel": "Pulsintegral / Kanal"
                 })

    names = c.search_in_dir("data/sev", identifiers=["good", "hist", "na22"],
                            or_identifiers=["ep", "eppo1", "eppo5", "e3hf110", "e3hf101", "ebis510", "ebis110", "ebis0201", "ebis105"],
                            not_identifiers=["pvcebis", "sebis"])
    labels = label_mapping(names)
    colors = color_mapping(names)
    c.multi_plot(names, labels, path + "sev_all_ep_samples.pdf",
                 show_final_plot=False,
                 plot_kwargs={
                     "color": colors
                 },
                 ax_config={
                     "xbounds": [60, 1300],
                     "ybounds": [0, None],
                     "xlabel": "Pulsintegral / Kanal"
                 })


def pure_ep(path="Z:/Studenten/Baier/Latex/images/"):
    pu_spec = c.search_in_dir("data/spec/ep", identifiers=["movingavg2", "sr90"])[0]
    pu_uvvis = c.search_in_dir("data/uv-vis/ep", identifiers=["fast"])[0]
    pu_sev = c.search_in_dir("data/sev/ep", identifiers=["good", "hist"])[0]

    c.auto_plot_data(pu_spec, auto_title=False,
                     plot_kwargs={
                         "color": "black",
                         "lw": 2,
                     },
                     ax_config={
                         "draw": False,
                         "xbounds": [310, 440],
                         "ybounds": [65, None],
                         "path": path + "spec_ep.pdf"
                     })
    c.auto_plot_data(pu_uvvis, auto_title=False,
                     plot_kwargs={
                         "color": "black",
                         "lw": 2,
                     },
                     ax_config={
                         "draw": False,
                         "xbounds": [300, 800],
                         "ybounds": [0, None],
                         "path": path + "uv-vis_ep.pdf"
                     })
    c.auto_plot_data(pu_sev, auto_title=False,
                     plot_kwargs={
                         "color": "black",
                         "lw": 2,
                     },
                     ax_config={
                         "draw": False,
                         "xbounds": [0, 400],
                         "ybounds": [0, None],
                         "path": path + "sev_ep.pdf"
                     })


def ep_pu_comp(path="Z:/Studenten/Baier/Latex/images/"):
    ep_uvvis = c.search_in_dir("data/uv-vis/ep", identifiers=["fast"])[0]
    pu_uvvis = c.search_in_dir("data/uv-vis/pu", identifiers=["good", "fast"])[0]

    names = [pu_uvvis, ep_uvvis]
    labels = [ "Polyurethan", "Epoxidharz"]
    colors = ["gray", "black"]
    c.multi_plot(names, labels, path + "uv-vis_pu_ep_comp.pdf",
                 show_final_plot=True,
                 plot_kwargs={
                     "color": colors,
                     "lw": 2
                 },
                 ax_config={
                     "xbounds": [250, 800],
                     "ybounds": [0, None]
                 })

# pure_ep()
# with_avg()

ep_pu_comp()



# with_avg("C:/Users/baier/OneDrive/Uni/Bachelorarbeit_2/latex/images/")
# pure_ep("C:/Users/baier/OneDrive/Uni/Bachelorarbeit_2/latex/images/")



