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
from pprint import pprint


def title_constructor(filename):
    t_str = None
    st_str = "Diagramm zu Daten aus: " + filename

    y = re.search(r"_b+[\w]+g[\w]+s+([0-9]{3})", filename)
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


class Control:
    c_draw: DiagramMaker
    c_file: FileManager
    c_data: DataLoader

    def __init__(self, c_draw: DiagramMaker, c_file: FileManager, c_data: DataLoader):
        self.c_data = c_data
        self.c_file = c_file
        self.c_draw = c_draw

    """
    --------------------------------------------------------------------------
    UTILITY FUNCTIONS
    """
    def extract_labels_from_path(self, names):
        """
        takes list of filenames and returns their labels (either sample description or info text)

        :param names: list of filenames (can include filepath)
        :return: labels
        """

        labels = []
        for name in names:
            inst, sample = self.c_file.get_inst_and_sample(name)
            if inst is None and sample is None:
                pass
            else:
                y = re.search(r"_b+[\w]+g[\w]+s+([0-9]{3})", name)
                try:
                    # append the sample description if it exists
                    labels.append(sample + y.group(0))
                except AttributeError:
                    # append the first info block in the filename as alternative
                    labels.append(sample + "_" + name.split("_")[2])

        return labels

    def search_in_dir(self, direc, identifiers=None, or_identifiers=None, not_identifiers=None):
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
                                                not_identifiers=not_identifiers))
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

        return names

    """
    --------------------------------------------------------------------------
    PLOT FUNCTIONS
    """
    def auto_plot_data(self, filename, **kwargs):
        """
        Extracts data from a given file and plots it according to the configured presets // also does ending check

        :param filename: data source
        :param kwargs: kwargs handed over to the drawing function -> allows for changes
        :return: the diagram
        """
        if "title" not in kwargs:
            kwargs["title"] = None
        if "suptitle" not in kwargs:
            kwargs["suptitle"] = None

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
            if "path" not in kwargs:
                kwargs["path"] = savepath

            print(f"... Saving plot to '{savepath}'.")

            # get instrument and data to plot
            inst = self.c_file.get_inst_and_sample(filename)[0]
            rec_data = self.c_data.auto_read(inst, filepath)

            # add automatic titles (only if neither is given)
            if kwargs["title"] is None and kwargs["suptitle"] is None:
                kwargs["suptitle"], kwargs["title"] = title_constructor(filename)

            # make the plot
            return self.c_draw.make_diagram(inst, rec_data, **kwargs)

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

    def multi_plot(self, names, labels, path, title=None, clist=None, lslist=None, norm=False, **kwargs):
        """
        plots multiple data sets of the same instrument in one diagram

        :param names: names of data for the plot
        :param labels: labels for each diagram
        :param path: path to save the final diagram to (will be in prodata directory)
        :param title: optional plot title
        :param clist: optional color list (standard: ["c", "m", "y", "r", "g", "b", "gray", "purple"])
        :param lslist: list of linestyles (can be int -> n-1 position will be dashed)
        :param norm: norm all plots to their maximum y-value if True
        :param kwargs: plot kwargs
        :return: the multi diagram
        """

        # plot settings need to be updated, so that one plot and not many are produced
        standards = {
            "ax": None, "draw": False, "save": False, "title": None, "label": None
        }
        kwargs = standards | kwargs

        # update color list if necessary
        if clist is None:
            clist = ["c", "m", "y", "r", "g", "b", "gray", "purple"]

        # check lslist len, if given
        if lslist is not None:
            if type(lslist) != int:
                if len(names) != len(lslist):
                    print("lslist length does not match names list -> setting ls='-'!")
                    lslist = None
            else:
                sp = lslist
                lslist = []
                for i in range(len(names)):
                    if i == sp:
                        lslist.append("--")
                    else:
                        lslist.append("-")
        if lslist is None:
            lslist = []
            for i in range(len(names)):
                lslist.append("-")

        # get save path
        path = self.c_file.prodata_path + "/" + path

        # configure window
        fig = plt.figure()
        ax = fig.add_subplot(111)
        kwargs["ax"] = ax

        # cut color list to needed length
        clist = clist[:len(names)]

        # iterate over plots
        for name, label, color, ls in zip(names, labels, clist, lslist):
            # get filename and path
            filename = self.c_file.check_filename_format(name)
            filepath = self.c_file.get_datafile_path(name)

            if filepath is None:
                raise FileNotFoundError(f"There is no data file called '{filename}'!")

            # load data
            inst = self.c_file.get_inst_and_sample(filename)[0]
            rec_data = self.c_data.auto_read(inst, filepath)

            # norm data
            if norm:
                rec_data[1] = rec_data[1] / np.max(rec_data[1])

            # update kwargs
            kwargs["label"] = label
            kwargs["c"] = color
            kwargs["ls"] = ls

            # draw one diagram
            self.c_draw.make_diagram(inst, rec_data, **kwargs)

        # configure plot
        ax.set_title(title)
        ax.grid(True)

        # change ax label, if norm
        if norm:
            ax.set_ylabel("normierte Zählrate")

        # save/show plot
        plt.savefig(path, dpi=400)
        # plt.show()

    def twin_x_scale_plot(self, names, labels, path, style=None, **kwargs):
        """
        plots data from two different instruments in one diagram (uses same x-axis)
        you can provide style options in a dictionary

        :param names: names of data for the plot
        :param labels: labels for each diagram
        :param path: path to save the final diagram to (will be in prodata directory)
        :param style: dict of type {"ls1": "-", "ls2": "-", "c1": "k", "c2": "r",}
                    -> can also take (correctly sized !!!!) arrays as input
        :param kwargs: plot kwargs
        :return: the twin diagram
        """

        # plot settings need to be updated, so that one plot and not many are produced
        standards = {
            "ax": None, "draw": False, "save": False, "title": None, "label": None, "draw_label": False,
        }
        kwargs = standards | kwargs

        # update the style settings
        standard_style = {
            "ls1": "-",
            "ls2": "-",
            "c1": "k",
            "c2": "r",
        }
        using_standards = False
        if style is None:
            style = standard_style
            using_standards = True
        else:
            style = standard_style | style

        # isolate the two instruments used
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

        # create the plot space
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twinx()

        # save diagrams and labels to build a legend later on
        labs = []
        lns = []

        # iterate over all names etc.
        for name, label, inst in zip(names, labels, inst_list):
            # get filename and path
            print(name)
            file_name = self.c_file.check_filename_format(name)
            file_path = self.c_file.get_datafile_path(file_name)

            # load data
            rec_data = self.c_data.auto_read(inst, file_path)

            # switch to correct color, linestyle and plot space
            if inst == inst1:
                ax = ax1
                inst_str = "1"
            else:
                ax = ax2
                inst_str = "2"

            # switch to the according linestyle for the instrument
            ci = style["c" + inst_str]
            if type(ci) == list:
                style["c" + inst_str] = ci[1:]
                ci = ci[0]
            lsi = style["ls" + inst_str]
            if type(lsi) == list:
                style["ls" + inst_str] = lsi[1:]
                lsi = lsi[0]

            # update plot kwargs
            kwargs["label"] = label + f" ({inst})"
            kwargs["c"] = ci
            kwargs["ax"] = ax
            # print(lsi)
            kwargs["ls"] = lsi

            # append resulting diagram and label (for later legend construction)
            labs.append(kwargs["label"])
            lns = lns + self.c_draw.make_diagram(inst, rec_data, **kwargs)

        # calculate tick distance, so that grids overlay
        ax2.set_yticks(np.linspace(ax2.get_yticks()[0], ax2.get_yticks()[-1], len(ax1.get_yticks())))

        # configure plots (labels, bound, ticks)
        if using_standards:
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
        ax1.legend(lns, labs)

        # save plot
        path = self.c_file.prodata_path + "/" + path
        plt.savefig(path, dpi=400)
        plt.show()

    def math_plot(self, names, labels, path, **kwargs):
        # plot settings need to be updated, so that one plot and not many are produced
        standards = {
            "ax": None, "draw": False, "save": False, "title": None, "label": None
        }
        kwargs = standards | kwargs

        # get save path
        path = self.c_file.prodata_path + "/" + path

        # configure window
        fig = plt.figure()
        ax = fig.add_subplot(111)
        kwargs["ax"] = ax

        data = []
        for name, label in zip(names, labels):
            filename = self.c_file.check_filename_format(name)
            filepath = self.c_file.get_datafile_path(name)

            if filepath is None:
                raise FileNotFoundError(f"There is no data file called '{filename}'!")

            # load data
            inst = self.c_file.get_inst_and_sample(filename)[0]
            rec_data = self.c_data.auto_read(inst, filepath)

            # update kwargs
            kwargs["label"] = label

            rec_data[1] = rec_data[1]/np.linalg.norm(rec_data[1])
            data.append(rec_data)

            # draw one diagram

        d = []
        print(data[0])
        d.append(data[0][0])
        d.append(data[0][1] - data[1][1])

        self.c_draw.make_diagram(inst, d, **kwargs)

        # configure plot
        ax.set_title(kwargs["title"])
        ax.grid(True)

        # save/show plot
        plt.savefig(path, dpi=400)
        plt.show()


def get_inst():
    dr = DiagramMaker()
    fi = FileManager("C:/Users/baier/OneDrive/Uni/Bachelorarbeit")
    da = DataLoader()

    return Control(dr, fi, da)
