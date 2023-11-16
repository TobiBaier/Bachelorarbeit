"""
Wrapper-Program, that allows for fast data and plotting applications
-> specially modified for scintillation testing, might be able to reuse parts of the code though
"""

from utility.diagrammaker import DiagramMaker
from utility.filemanager import FileManager
from utility.dataloader import DataLoader

import os
import re
import matplotlib.pyplot as plt
import numpy as np
import json
from pprint import pprint





class Control:
    c_draw: DiagramMaker
    c_file: FileManager
    c_data: DataLoader

    def __init__(self, c_draw: DiagramMaker, c_file: FileManager, c_data: DataLoader):
        self.c_data = c_data
        self.c_file = c_file
        self.c_draw = c_draw

        # standard settings
        self.mp_settings = None
        self.tx_settings = None
        self.ap_settings = None

        # load settings
        self.config()

    def config(self):
        try:
            with open(os.path.abspath(os.path.dirname(__file__)) + "/utility/config/control_settings.json", "r") as of:
                settings = json.load(of)
        except FileNotFoundError:
            raise FileNotFoundError("Could not load config/control_settings.json because file does not exists!")

        self.mp_settings = settings["multi_plot"]
        self.tx_settings = settings["twin_xscale"]
        self.ap_settings = settings["auto_plot"]

    """
    --------------------------------------------------------------------------
    UTILITY FUNCTIONS
    """

    def title_constructor(self, filename):
        t_str = None
        st_str = ""

        inst, sample = self.c_file.get_inst_and_sample(filename)
        if inst == "spec":
            st_str = "emission spectrum of: "
        if inst == "uv-vis":
            st_str = "transmission spectrum of: "
        if inst == "sev":
            st_str = "SEV histogram of: "
        if inst == "osc":
            st_str = "waveform of: "

        st_str = st_str + self.c_file.sample_desciptions[sample]


        y = re.search(r"[_b\w]{3}[g\d]{2}s([0-9]{3})", filename)
        if y is not None:
            sample_description = y.group(0)
            t_str = "Sample-Details: "

            bubbles = sample_description[1:3]
            grind = sample_description[3:5]
            size = sample_description[6:8]
            size2 = sample_description[8]

            if bubbles == "bn":
                t_str = t_str + "no bubbles, "
            elif bubbles == "bc":
                t_str = t_str + "central bubbles, "
            elif bubbles == "br":
                t_str = t_str + "bubbles on egdes, "

            if grind == "g0":
                t_str = t_str + "unground, "
            elif grind == "g1":
                t_str = t_str + "one side sanded, "
            elif grind == "g2":
                t_str = t_str + "both sides sanded, "

            t_str = t_str + size + "." + size2 + "mm thick (-> [" + sample_description + "])"

        return st_str, t_str

    def extract_labels_from_path(self, names, re_str=None):
        """
        takes list of filenames and returns their labels (either sample description or info text)

        :param re_str: search using a regex string
        :param names: list of filenames (can include filepath)
        :return: labels
        """

        labels = []
        for name in names:
            inst, sample = self.c_file.get_inst_and_sample(name)
            if re_str is not None:
                y = re.search(re_str, name)
                try:
                    labels.append(y.group(0))
                except AttributeError:
                    labels.append("no info found")

            elif inst is None and sample is None:
                pass

            else:
                y = re.search(r"[_b\w]{3}[g\d]{2}s([0-9]{3})", name)
                try:
                    # append the sample description if it exists
                    labels.append(sample + y.group(0))
                except AttributeError:
                    # append the first info block in the filename as alternative
                    labels.append(sample + "_" + name.split("_")[2])

        return labels

    def search_in_dir(self, direc, identifiers=None, or_identifiers=None, not_identifiers=None, no_filecheck=False):
        """
        returns list of names in directory, that fulfill conditions

        :param direc: the directory to search (relative to data path)
        :param identifiers: list, All strings have to be in the name
        :param or_identifiers: list, AT LEAST ONE string has to be in the name
        :return: the list of names
        """
        names = []

        # iterate through directory
        for filepath in os.listdir(self.c_file.path + "/" + direc):
            # if path is a directory as well, recall current functions with subdirectory
            if os.path.isdir(self.c_file.path + "/" + direc + "/" + filepath):
                names.extend(self.search_in_dir(direc + "/" + filepath,
                                                identifiers=identifiers,
                                                or_identifiers=or_identifiers,
                                                not_identifiers=not_identifiers,
                                                no_filecheck=no_filecheck))
            # check if conditions are fulfilled
            else:
                # or conditions
                add_name = True
                if or_identifiers is not None:
                    for i in or_identifiers:
                        if i in filepath:
                            add_name = True
                            break
                        else:
                            add_name = False

                # and conditions
                if identifiers is not None:
                    for i in identifiers:
                        if i not in filepath:
                            add_name = False
                            break

                # not condition
                if not_identifiers is not None:
                    for i in not_identifiers:
                        if i in filepath:
                            add_name = False
                            break

                # add name if all conditions are fulfilled
                if add_name and self.c_file.check_filename_format(filepath):
                    names.append(filepath)
                elif no_filecheck and add_name:
                    names.append(filepath)


        return names

    """
    --------------------------------------------------------------------------
    PLOT FUNCTIONS
    """
    def auto_plot_data(self, filename, auto_title=True, **kwargs):
        """
        Extracts data from a given file and plots it according to the configured presets // also does ending check

        :param filename: data source
        :param kwargs: kwargs handed over to the drawing function -> allows for changes
        :return: the diagram
        """

        # update standard settings
        for key in kwargs:
            if key in self.ap_settings:
                kwargs[key] = self.ap_settings[key] | kwargs[key]

        # add ending if needed
        temp = filename
        filename = self.c_file.check_filename_format(filename)

        # check if file is allowed and/or exists
        if filename is False:
            print(f"Skipped file '{temp}', because not plottable (check datatype/existence)!")

        # it exists and can be plotted
        else:
            # get file/savepath for loading and storing
            filepath = self.c_file.get_datafile_path(filename)
            savepath = self.c_file.get_savefile_path(filename)

            # enter path into kwargs if not already given
            if "path" not in kwargs["ax_config"]:
                kwargs["ax_config"]["path"] = savepath

            sp = kwargs["ax_config"]["path"]
            print(f"... Saving plot to '{sp}'.")

            # get instrument and data to plot
            inst = self.c_file.get_inst_and_sample(filename)[0]
            rec_data = self.c_data.auto_read(inst, filepath)

            # add automatic titles (only if neither is given)
            if kwargs["ax_config"]["title"] is None and kwargs["ax_config"]["suptitle"] is None and auto_title:
                kwargs["ax_config"]["suptitle"], kwargs["ax_config"]["title"] = self.title_constructor(filename)

            # make the plot
            return self.c_draw.make_diagram(inst, rec_data, **kwargs)

    def create_combiplot(self, names, outer_format, style):

        #if type(outer_format["ax"]) != list:
        #    outer_format["ax"] = [outer_format["ax"]] * len(names)
        if type(outer_format["inst"]) != list:
            outer_format["inst"] = [outer_format["inst"]] * len(names)
        ax = outer_format["ax"]
        dgs = []
        # print(outer_format["ax"])
        for i, name in enumerate(names):

            config = {}

            for key in style:
                config[key] = {}
                for inner_key in style[key]:
                    if type(style[key][inner_key]) != list:
                        config[key][inner_key] = style[key][inner_key]
                    else:
                        if inner_key == "xbounds" or inner_key == "ybounds":
                            config[key][inner_key] = style[key][inner_key]
                        else:
                            config[key][inner_key] = style[key][inner_key][i]

            filename = self.c_file.check_filename_format(name)
            filepath = self.c_file.get_datafile_path(filename)

            rec_data = self.c_data.auto_read(outer_format["inst"][i], filepath)

            if outer_format["norm"] == "max":
                rec_data[1] = rec_data[1] / np.max(rec_data[1])
            elif outer_format["norm"] == "vector":
                rec_data[1] = rec_data[1] / np.linalg.norm(rec_data[1])

            config["ax_config"]["ax"] = ax

            dgs = dgs + [self.c_draw.make_diagram(outer_format["inst"][i], rec_data, **config)]

        plt.suptitle(outer_format["suptitle"])
        plt.title(outer_format["title"])

        return dgs

    def plot_dir(self, direc, identifiers=None, or_identifiers=None):
        """
        plots all data in directory, that fulfills conditions

        :param direc: the directory to search (relative to data path)
        :param identifiers: list, All strings have to be in the name
        :param or_identifiers: list, AT LEAST ONE string has to be in the name
        """

        # get names that are good :)
        names = self.search_in_dir(direc, identifiers=identifiers, or_identifiers=or_identifiers)

        # plot names
        for name in names:
            self.auto_plot_data(name)
            plt.close()

    def multi_plot(self, names, labels, path, style=None, show_final_plot=False, **kwargs):
        """
        plots multiple data sets of the same instrument in one diagram

        :param names: names of data for the plot
        :param labels: labels for each diagram
        :param path: path to save the final diagram to (will be in prodata directory)
        :param style: should contain lists or entries to overwrite standard plot settings (c, ls, marker...)
        :param kwargs: plot kwargs (norm, title, suptitle)
        :return: the multi diagram
        """

        if style is None:
            style = {}
        for key in style:
            if key in self.mp_settings["style"]:
                style[key] = self.mp_settings["style"][key] | style[key]
        for key in self.mp_settings["style"]:
            if key not in style:
                style[key] = self.mp_settings["style"][key]

        # compare outer_format with kwargs (cant use |, because only predefined keys are allowed)
        outer_format = self.mp_settings["outer_format"]
        for key in kwargs:
            if key in outer_format:
                outer_format[key] = kwargs[key]

        # fully construct style dictionary
        style["plot_kwargs"]["label"] = labels

        # fully construct outer_format dictionary
        fig = plt.figure()
        ax = fig.add_subplot(111)
        outer_format["ax"] = ax
        inst = self.c_file.get_inst_and_sample(names[0])[0]
        outer_format["inst"] = inst

        # call combi_plot to draw diagrams
        self.create_combiplot(names, outer_format, style)

        # adjust plot parameters
        if outer_format["norm"] is not None:
            ax.set_ylabel(self.c_draw.plot_standards[outer_format["inst"]]["norm_ylabel"])
        # ax.grid(True)

        # get save path
        path = self.c_file.prodata_path + "/" + path

        # draw and save plot
        ax.legend()
        plt.savefig(path, dpi=400)

        if show_final_plot:
            plt.show()

    def twin_x_scale_plot(self, names, labels, path, style=None, **kwargs):
        """

        :param names:
        :param labels:
        :param path:

        :param style:
        :param kwargs:
        :return:
        """

        if style is None:
            style = {}
        style = self.tx_settings["style"] | style

        outer_format = self.tx_settings["outer_format"]
        for key in kwargs:
            if key in outer_format:
                outer_format[key] = kwargs[key]

        # get both instruments
        inst_list = []
        for name in names:
            inst_list.append(self.c_file.get_inst_and_sample(name)[0])

        inst1 = inst_list[0]
        inst2 = None
        for inst in inst_list:
            if inst != inst1:
                inst2 = inst
                break
            else:
                inst2 = None

        if inst2 is None:
            raise NameError("You need to provide data from two different instruments! (Consider using multi_plot)")

        # special cases for colors and linestyles
        if "c1" in kwargs and "c2" in kwargs:
            c = []
            for inst in inst_list:
                if inst == inst1:
                    c.append(kwargs["c1"])
                else:
                    c.append(kwargs["c2"])
            style["c"] = c
        
        if "ls1" in kwargs and "ls2" in kwargs:
            ls = []
            for inst in inst_list:
                if inst == inst1:
                    ls.append(kwargs["ls1"])
                else:
                    ls.append(kwargs["ls2"])
            style["ls"] = ls
        
        # construct outer_format
        outer_format["inst"] = inst_list
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twinx()
        axlist = []
        for inst in inst_list:
            if inst == inst1:
                axlist.append(ax1)
            else:
                axlist.append(ax2)
        outer_format["ax"] = axlist

        style["label"] = labels
        print(labels)
        # call combi_plot to draw diagrams
        lns = self.create_combiplot(names, outer_format, style)

        ax2.set_yticks(np.linspace(ax2.get_yticks()[0], ax2.get_yticks()[-1], len(ax1.get_yticks())))

        # configure plots (labels, bound, ticks)
        if style["c"] == self.tx_settings["style"]["c"]:
            c = ["k", "r"]
        else:
            c = ["k", "k"]
        ax1.set_ylabel(self.c_draw.presets[inst1]["ylabel"], color=c[0])
        ax1.set_ybound([0, ax1.get_yticks()[-1]])
        ax1.tick_params(axis="y", labelcolor=c[0])
        ax2.set_ylabel(self.c_draw.presets[inst2]["ylabel"], color=c[1])
        ax2.set_ybound([0, ax2.get_yticks()[-1]])
        ax2.tick_params(axis="y", labelcolor=c[1])
        fig.tight_layout()

        # make legend for entire plot
        ax1.legend(lns, labels)

        # save plot
        path = self.c_file.prodata_path + "/" + path
        plt.savefig(path, dpi=400)

    def draw_by_name(self, name, draw_kwargs=None):
        path = self.c_file.get_datafile_path(name)
        inst = self.c_file.get_inst_and_sample(name)[0]
        data = self.c_data.auto_read(inst, path)
        self.c_draw.make_diagram(inst, data, **draw_kwargs)


def get_inst(path="/run/user/1000/gvfs/sftp:host=sftp.zih.tu-dresden.de/glw/aspabl/Studenten/Baier/Messungen"):
    dr = DiagramMaker()
    # fi = FileManager("C:/Users/baier/OneDrive/Uni/Bachelorarbeit")
    fi = FileManager(path)
    da = DataLoader()

    return Control(dr, fi, da)
