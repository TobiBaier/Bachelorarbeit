from control import get_inst
import re
from pprint import pprint

# c = get_inst("Z:\Studenten\Baier\Messungen")
c = get_inst("C:/Users/baier/OneDrive/Uni/Bachelorarbeit")

cmap = {
    "ebis110": ["xkcd:primary blue", "EP mit 1% PPO und 0,1% Bis-MSB (EBIS110)"],
    "sebis110": ["xkcd:baby blue", "EBIS110 mit 2% NaCl"],
    "pvcebis110": ["xkcd:sea blue", "EBIS110 mit 5.7% PVC"],
    "dsf": ["xkcd:hot pink", "DF-01"],
    "ej200": ["xkcd:navy blue", "EJ200"],
    "ej260": ["xkcd:neon green", "EJ260"],
    "e3hf101": ["xkcd:light teal", "EP mit 1% PPO und 0,01% 3HF"],
}

short_cmap = {
    "ebis110": ["xkcd:primary blue", "1% PPO, 0,1% Bis-MSB (EBIS110)"],
    "sebis110": ["xkcd:baby blue", "EBIS110 mit 2% NaCl"],
    "pvcebis110": ["xkcd:sea blue", "EBIS110 mit 5.7% PVC"],
    "dsf": ["xkcd:hot pink", "DF-01"],
    "ej200": ["xkcd:royal blue", "EJ200"],
    "ej260": ["xkcd:neon green", "EJ260"],
    "e3hf101": ["xkcd:light teal", "EP, 1% PPO, 0,01% 3HF"],
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


def emission_comp(path="Z:/Studenten/Baier/Latex/images/"):
    names = c.search_in_dir("data/spec",
                            identifiers=["sr90", "run24", "movingavg"],
                            or_identifiers=["ebis110", "pvcebis110", "sebis110"],)
    colors = color_mapping(names)
    labels = label_mapping(names, short=True)
    c.multi_plot(names, labels, path + "spec_all_doped_samples.pdf",
                 show_final_plot=True,
                 plot_kwargs={
                     "color": colors,
                 },
                 ax_config={
                     "xbounds": [360, 640],
                 },
                 legend_kwargs={
                     "fontsize": "small"
                 }
                 )


def psev_comp(path="Z:/Studenten/Baier/Latex/images/"):
    names = c.search_in_dir("data/sev",
                            identifiers=["na22", "15min", "hist", "good"],
                            or_identifiers=["ebis110", "pvcebis110", "sebis110", ])
    pprint(names)

    colors = color_mapping(names)
    labels = label_mapping(names)
    c.multi_plot(names, labels, path + "sev_all_doped_samples.pdf",
                 show_final_plot=True,
                 plot_kwargs={
                     "color": colors,
                 },
                 ax_config={
                     "xbounds": [15.233, 1250],
                 },
                 legend_kwargs={
                     "fontsize": "small"
                 }
                 )

# psev_comp(path="C:/Users/baier/OneDrive/Uni/Bachelorarbeit_2/latex/images/")
# emission_comp(path="C:/Users/baier/OneDrive/Uni/Bachelorarbeit_2/latex/images/")



def calibrated_psev(path="Z:/Studenten/Baier/Latex/images/"):
    names = c.search_in_dir("data/sev",
                            identifiers=["cm244", "100s",  "hight", "ecalib", "rebin", "binning"],
                            or_identifiers=["pvcebis110", "ebis110", "dsf"],)
    pprint(names)
    colors = color_mapping(names)
    labels = label_mapping(names)
    c.multi_plot(names, labels, path + "sev_cm244_comp.pdf",
                 show_final_plot=False,
                 plot_kwargs={
                     "color": colors,
                 },
                 ax_config={
                     "xbounds": [15.233, 80],
                     "yscale": "linear",
                     "xlabel": "Pulsenergie / keV"
                 })


    names = c.search_in_dir("data/sev",
                            identifiers=["am241","100", "hight", "ecalib", "rebin", "binning"],
                            or_identifiers=["pvcebis110", "ebis110", "dsf"], )
    colors = color_mapping(names)
    labels = label_mapping(names)
    c.multi_plot(names, labels, path + "sev_am241_comp.pdf",
                 show_final_plot=True,
                 plot_kwargs={
                     "color": colors,
                 },
                 ax_config={
                     "xbounds": [15.233, 250],
                     "yscale": "log",
                     "xlabel": "Pulsenergie / keV"
                 })


    names = c.search_in_dir("data/sev",
                            identifiers=["na22", "hight", "ecalib", "rebin", "rebin", "binning"],
                            or_identifiers=["pvcebis110", "ebis110", "dsf"], )
    colors = color_mapping(names)
    labels = label_mapping(names)
    c.multi_plot(names, labels, path + "sev_na22_comp.pdf",
                 show_final_plot=True,
                 plot_kwargs={
                     "color": colors,
                 },
                 ax_config={
                     "xbounds": [14.42, 2250],
                     "yscale": "log",
                     "xlabel": "Pulsenergie / keV"
                 })


def ej_comparison(path="Z:/Studenten/Baier/Latex/images/"):
    names = c.search_in_dir("data/sev",
                            identifiers=["na22", "15min", "comp"],
                            or_identifiers=["e3hf101", "ebis110", "ej200", "ej260"])
    colors=color_mapping(names)
    labels = label_mapping(names)
    c.multi_plot(names, labels, path + "sev_ej_comp.svg",
                 show_final_plot=False,
                 plot_kwargs={
                     "color": colors,
                 },
                 ax_config={
                     "xbounds": [0, 1000],
                     "yscale": "linear",
                 })

    names = c.search_in_dir("data/uv-vis",
                            identifiers=["fast"],
                            or_identifiers=["e3hf101", "ebis110", "ej200", "ej260"],
                            not_identifiers=["exclude", "sebis"])
    pprint(names)
    colors = color_mapping(names)
    labels = label_mapping(names, short=True)
    c.multi_plot(names, labels, path + "uv-vis_ej_comp.svg",
                 show_final_plot=True,
                 plot_kwargs={
                     "color": colors,
                 },
                 ax_config={
                     "xbounds": [340, 800],
                     "yscale": "linear",
                 })

    names = c.search_in_dir("data/spec",
                            identifiers=["sr90", "movingavg", "run24"],
                            or_identifiers=["e3hf101", "ebis110", "ej200", "ej260"],
                            not_identifiers=["sebis", "pvcebis"])
    names.append('spec_e3hf101_bng2s111_sr90_movingavg2.csv')
    names[1], names[3] = names[3], names[1]
    pprint(names)
    colors = color_mapping(names)
    labels = label_mapping(names, short=True)
    c.multi_plot(names, labels, path + "spec_ej_comp.svg",
                 show_final_plot=False,
                 plot_kwargs={
                     "color": colors,
                 },
                 ax_config={
                     "xbounds": [360, 640],
                     "yscale": "linear",
                 },
                 legend_kwargs={
                     "fontsize": "x-small"
                 })


def hot_cold_comp(path="Z:/Studenten/Baier/Latex/images/"):
    names = c.search_in_dir("data/sev/pvcebis110",
                            identifiers=["am241", "100s", "ecalib", "rebin", "binning"],)
    pprint(names)
    colors = ["red", "blue"]
    labels = ["23°C", "-20°C"]
    c.multi_plot(names, labels, path + "hot_cold_comp_am241.pdf",
                 show_final_plot=True,
                 plot_kwargs={
                     "color": colors,
                 },
                 ax_config={
                     "xbounds": [18.5, 200],
                     "yscale": "log",
                     "xlabel": "Pulsenergie / keV"
                 },
                 legend_kwargs={
                     "fontsize": "medium"
                 })

    names = c.search_in_dir("data/sev/pvcebis110",
                            identifiers=["cm244", "100s", "ecalib", "rebin", "binning"], )
    pprint(names)
    colors = ["red", "blue"]
    labels = ["23°C", "-20°C"]
    c.multi_plot(names, labels, path + "hot_cold_comp_cm244.pdf",
                 show_final_plot=True,
                 plot_kwargs={
                     "color": colors,
                 },
                 ax_config={
                     "xbounds": [18.5, 75],
                     "yscale": "linear",
                     "xlabel": "Pulsenergie / keV"
                 },
                 legend_kwargs={
                     "fontsize": "medium"
                 })

    names = c.search_in_dir("data/sev/pvcebis110",
                            identifiers=["na22", "ecalib", "rebin", "binning"],)
    pprint(names)
    colors = ["red", "blue"]
    labels = ["23°C", "-20°C"]
    c.multi_plot(names, labels, path + "hot_cold_comp_na22.pdf",
                 show_final_plot=True,
                 plot_kwargs={
                     "color": colors,
                 },
                 ax_config={
                     "xbounds": [18.5, 2000],
                     "yscale": "log",
                     "xlabel": "Pulsenergie / keV"
                 },
                 legend_kwargs={
                     "fontsize": "medium"
                 })



# hot_cold_comp(path="C:/Users/baier/OneDrive/Uni/Bachelorarbeit_2/latex/images/")

# c.c_file.sort_to_dirs()
# calibrated_psev(path="C:/Users/baier/OneDrive/Uni/Bachelorarbeit_2/latex/images/")

# emission_comp()
ej_comparison(path="C:/Users/baier/OneDrive/Uni/Bachelorarbeit_2/Präsentation/images/")

