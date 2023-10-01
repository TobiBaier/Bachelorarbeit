from utility_deprecated.getdata import GetData
from utility_deprecated.drawdiagrams import DrawDiagrams
from utility_deprecated.filemanager import FileManager
import os
import re
import matplotlib.pyplot as plt
import numpy as np

data_presets = {
    "sev": {
        "data_type": "txt",
        "skip_lines": 5,
        "cols": [0, 1]
    },
    "spec": {
        "data_type": "csv",
        "skip_lines": 0,
    },
    "uv-vis": {
        "data_type": "csv",
        "skip_lines": 2,
        "delimiter": ",",
        "skipfooter": 2,
        "cols": [0, 1],
    },
    "osc": {
        "data_type": "txt",
        "skip_lines": 5,
        "delimiter": ";",
        "cols": [0, 1],
    }
}

draw_presets = {
    "spec": {
        "plot_type": "plot",
        "plot_kwargs": {  # NEEDS to contain ALL graphical plot infos
            "ls": "-",
            "marker": None,  # "+"
            "c": "black",  # "blue"
            # "mec" = "blue",
            # "ms": 6,
            "lw": 1,
            "label": None
        },
        "xlabel": r"Wellenlänge/nm",
        "ylabel": r"Zählrate/$\frac{1}{s}$",
        "grid": True,
        "ybounds": [0, None],
        "draw_label": True,
    },
    "uv-vis": {
        "plot_type": "plot",
        "plot_kwargs": {
            "ls": "-",
            "marker": None,
            "c": "black",
            "label": None,
            "lw": 1,
        },
        "xlabel": r"Wellenlänge/nm",
        "ylabel": "transmission / %",
        "grid": True,
        "ybounds": [0, None],
        "draw_label": True,
    },
    "sev": {
        "plot_type": "plot",
        "plot_kwargs": {
            "ls": "-",
            "marker": None,
            "c": "black",
            "label": None,
            "linewidth": 1,
        },
        "xlabel": r"energy/channels",
        "ylabel": "counts",
        "grid": True,
        "ybounds": [0, None],
        "xbounds": [0, 1500],
        "draw_label": True,
    },
    "osc": {
        "plot_type": "plot",
        "plot_kwargs": {
            "ls": "-",
            "marker": None,
            "c": "black",
            "label": None,
            "linewidth": 0.5,
        },
        "xlabel": r"time",
        "ylabel": "pulse height",
        "grid": True,
        "ybounds": [None, None],
        "draw_label": True,
    }

}


class Control:
    # instances
    curr_draw: DrawDiagrams
    curr_file: FileManager
    curr_data: GetData

    # constructor
    def __init__(self, draw: DrawDiagrams, file: FileManager, data: GetData):
        self.curr_draw = draw
        self.curr_file = file
        self.curr_data = data

        self.curr_data.load_presets(data_presets)
        self.curr_draw.load_presets(draw_presets)

    def name_constructor(self, file_name):

        inst, sample = self.curr_file.filecheck(file_name)

        st_str = ""
        t_str = None
        # if inst == "sev":
        #     st_str = st_str + "SEV-Spektrum einer "
        # elif inst == "spec":
        #     st_str = st_str + "Gitterspektrometer Messung einer "
        # elif inst == "uv-vis":
        #     st_str = st_str + "Cary-50 Messung einer "
        # elif inst == "osc":
        #     st_str = st_str + "Oszilloskop Messung einer "
        # else:
        #     st_str = st_str + "Messung einer "

        st_str = "Grafik zu Daten aus: " + file_name

        y = re.search(r"_b+[\w]+g[\w]+s+([0-9]{3})", file_name)
        if y is not None:
            sample_description = y.group(0)
            t_str = "Proben-Details: "

            bubbles = sample_description[1:3]
            grind = sample_description[3:5]
            size = sample_description[6:8]
            size2 = sample_description[8]

            if bubbles == "bn":
                t_str = t_str + "keine Blasen, "
            elif bubbles == "bc":
                t_str = t_str + "Blasen mittig, "
            elif bubbles == "br":
                t_str = t_str + "Blasen am Rand, "

            if grind == "g0":
                t_str = t_str + "ungeschliffen, "
            elif grind == "g1":
                t_str = t_str + "eine Seite geschliffen, "
            elif grind == "g2":
                t_str = t_str + "beide Seiten geschliffen, "

            t_str = t_str + size + "." + size2 + "mm dick (-> [" + sample_description + "])"

        return st_str, t_str

    def auto_plot_data(self, file_name, **d_kwargs):
        d_kwargs["title"] = None
        d_kwargs["suptitle"] = None
        # add ending to file path if needed
        temp = file_name
        file_name = self.curr_file.check_ending(file_name)

        # print(file_name, file_path)

        if file_name is False:
            print(f"Skipped file '{temp}', because not plottable!")
            # raise FileNotFoundError(f"There is no data file called '{file_name}'!")
        else:
            # check if file actually exists
            file_path = self.curr_file.check_if_file(file_name)

            # get instrument id
            inst = file_name.split("_")[0]

            # get measurement data
            rec_data = self.curr_data.auto_read(inst, file_path)

            # get path to save image to (mirror of data path, just in processed folder)
            save_path = self.curr_file.get_save_path(file_name)
            d_kwargs["path"] = save_path
            print(f"...Saving plot to '{save_path}'.")

            # get a title
            if d_kwargs["title"] is None and d_kwargs["suptitle"] is None:
                d_kwargs["suptitle"], d_kwargs["title"] = self.name_constructor(file_name)

            # draw and save the plot
            self.curr_draw.make_plot(inst, rec_data, **d_kwargs)

    def plot_all_inst_data(self, inst_list=None):
        if inst_list is not None:
            names = self.curr_file.get_file_names(inst_list)
            for name in names:
                self.auto_plot_data(name)

    def plot_dir(self, direc, extra_identifier=None):
        for file_path in os.listdir(self.curr_file.path + "/" + direc):
            if os.path.isdir(self.curr_file.path + "/" + direc + "/" + file_path):
                print(direc + "/" + file_path)
                self.plot_dir(direc + "/" + file_path, extra_identifier=extra_identifier)
            else:
                if extra_identifier is None:
                    self.auto_plot_data(file_path)
                else:
                    do_it = True
                    for i in extra_identifier:
                        if i not in file_path:
                            do_it = False
                            break

                    if do_it:
                        self.auto_plot_data(file_path)

    def multi_plot(self, name_list, label_list, path, title=None, clist=None):
        if clist is None:
            clist = ["c", "m", "y", "r", "g", "b"]
        path = self.curr_file.prodata_path + "/" + path

        fig = plt.figure()
        ax = fig.add_subplot(111)

        clist = clist[:len(name_list)]

        for name, c, label in zip(name_list, clist, label_list):
            file_name = self.curr_file.check_ending(name)
            file_path = self.curr_file.check_if_file(file_name)
            # print(file_name, file_path)
            if file_path is None:
                raise FileNotFoundError(f"There is no data file called '{file_name}'!")

            inst = file_name.split("_")[0]
            rec_data = self.curr_data.auto_read(inst, file_path)
            self.curr_draw.make_plot(inst, rec_data, ax=ax, draw=False, save=False, title=None, c=c, label=label)

        ax.set_title(title)
        ax.grid(True)

        plt.savefig(path, dpi=400)

        plt.show()

    def get_names(self, direc, identifiers=None, or_identifiers=None):
        # supposed to return all names from a directory, fulfilling identifiers
        # or_identifiers works the same way, with the difference, that only one has to be True
        names = []
        # print(direc)
        for file_path in os.listdir(self.curr_file.path + "/" + direc):
            if os.path.isdir(self.curr_file.path + "/" + direc + "/" + file_path):
                names.extend(
                    self.get_names(direc + "/" + file_path, identifiers=identifiers, or_identifiers=or_identifiers))
            else:
                do_it = True
                if or_identifiers is not None:
                    for i in or_identifiers:
                        if i in file_path:
                            do_it = True
                            break
                        else:
                            do_it = False

                if identifiers is not None:
                    for i in identifiers:
                        if i not in file_path:
                            do_it = False
                            break
                if do_it:
                    names.append(file_path)

        return names

    def extract_label_from_path(self, names):
        labels = []
        for name in names:
            inst, sample = self.curr_file.filecheck(name)
            y = re.search(r"_b+[\w]+g[\w]+s+([0-9]{3})", name)
            try:
                labels.append(sample + y.group(0))
            except AttributeError:
                labels.append(sample + "_" + name.split("_")[2])

        return labels

    def twin_xscale_plot(self, names, labels, path, **d_kwargs):
        standards = {
            "ax": None, "draw": False, "save": False, "title": None, "label": None
        }

        d_kwargs = standards | d_kwargs

        if "c" in d_kwargs:
            c = d_kwargs["c"]
        else:
            c = ["k", "r"]

        path = self.curr_file.prodata_path + "/" + path

        inst_list = []
        for name in names:
            inst_list.append(name.split("_")[0])

        inst1 = inst_list[0]
        inst2 = None
        for inst in inst_list:
            if inst != inst1:
                inst2 = inst
                break

        if inst2 is None:
            raise NameError("You need to provide data from two different instruments! (Consider using multi_plot)")

        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twinx()

        dias = []

        for name, label, inst in zip(names, labels, inst_list):
            file_name = self.curr_file.check_ending(name)
            file_path = self.curr_file.check_if_file(file_name)

            rec_data = self.curr_data.auto_read(inst, file_path)

            if inst == inst1:
                ax = ax1
                ci = c[0 % len(c)]
            else:
                ax = ax2
                ci = c[1 % len(c)]

            d_kwargs["label"] = label
            d_kwargs["c"] = ci
            d_kwargs["ax"] = ax

            dias.append(self.curr_draw.make_plot(inst, rec_data, **d_kwargs))

        ax2.set_yticks(np.linspace(ax2.get_yticks()[0], ax2.get_yticks()[-1], len(ax1.get_yticks())))

        ax1.set_ylabel(draw_presets[inst1]["ylabel"], color=c[0])
        ax1.set_ybound([0, ax1.get_yticks()[-1]])
        ax1.tick_params(axis="y", labelcolor=c[0])
        ax2.set_ylabel(draw_presets[inst2]["ylabel"], color=c[1])
        ax2.set_ybound([0, ax2.get_yticks()[-1]])
        ax2.tick_params(axis="y", labelcolor=c[1])

        fig.tight_layout()

        lns = dias[1] + dias[0]
        labs = [l.get_label() for l in lns]
        ax1.legend(lns, labs)

        plt.savefig(path, dpi=400)


def get_inst():
    dr = DrawDiagrams()
    fi = FileManager()
    da = GetData()

    return Control(dr, fi, da)


# a.auto_plot_data("spec_ppo1_sr_1")
# a.plot_all_inst_data(["uv-vis"])

'''
name_list = ["uv-vis_pu_trans_fast", "uv-vis_ppo1_trans_fast", "uv-vis_combi14_trans_fast", "uv-vis_3hf1_trans_fast"]
label_list = ["pu", "pu+ppo", "combi14", "3hf1"]
a.multi_plot(name_list, label_list, path="uv-vis_combis/pu_ppo1_combi14_3hf1.png",
             title="Transmission spectrum of differently doped PU")
'''


'''
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
'''
