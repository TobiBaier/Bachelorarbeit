"""
utility_deprecated program that implements a class for easier and automated diagram production
features:
-

needs to be added:
- support for scatter and errorbar plots
"""

import matplotlib.pyplot as plt
import json
import os
import matplotlib as mpl
from pprint import pprint
import locale

# mpl.use('Qt5Agg')
locale.setlocale(locale.LC_ALL, "")

def create_window(params: dict):
    """
    utility_deprecated function that will configure certain presets for a plot window (or better: a subplot)
    will set: a subplot (if not existing), title, suptitle, grid, x/y-label

    :param params: dictionary containing plot information
    :return: the diagram (ax) object
    """

    # create or load subplot
    if params["ax_config"]["ax"] is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    else:
        ax = params["ax_config"]["ax"]

    """# set title, suptitle, grid if given
    # title is BELOW suptitle and therefore smaller
    if params["title"]:
        plt.title(params["title"], fontsize="small")
    if params["suptitle"]:
        plt.suptitle(params["suptitle"], fontsize="medium")
    if params["grid"]:
        ax.grid()

    # configure axis labels
    ax.set_xlabel(params["xlabel"])
    ax.set_ylabel(params["ylabel"])"""

    # return configured plot
    return ax

def config_window(ax, params: dict):
    """
    scrolls through dict and uses contents to call predetermined functions

    :return: a formatted window
    """

    ax_config = params["ax_config"]

    if "title" in ax_config:
        plt.title(ax_config["title"], fontsize="small")
    if "suptitle" in ax_config:
        plt.suptitle(ax_config["suptitle"], fontsize="medium")

    if "grid" in ax_config:
        ax.grid(**params["grid_kwargs"])

    if "xlabel" in ax_config:
        ax.set_xlabel(ax_config["xlabel"])
    if "ylabel" in ax_config:
        ax.set_ylabel(ax_config["ylabel"])

    if "xscale" in ax_config:
        ax.set_xscale(ax_config["xscale"])
    if "yscale" in ax_config:
        ax.set_yscale(ax_config["yscale"])

    if "xbounds" in ax_config:
        ax.set_xbound(ax_config["xbounds"])
    if "ybounds" in ax_config:
        ax.set_ybound(ax_config["ybounds"])

    if "tick_kwargs" in params:
        ax.tick_params(**params["tick_kwargs"])
    try:
        if "ticklabel_kwargs" in params:
            ax.ticklabel_format(**params["ticklabel_kwargs"])
    except AttributeError:
        path = ax_config["path"]
        print(f"Falling back to normal notation for image with path: {path}")

    return ax

def save_draw(params: dict):
    """
    Utility funtion that draws/saves a window
    Will also configure legend

    :param params: dictionary containing plot information
    """
    ax_config = params["ax_config"]

    if params["plot_kwargs"]["label"] is not None and ax_config["draw_label"]:
        plt.legend()

    if ax_config["save"]:
        if ax_config["path"] is None:
            plt.savefig(ax_config["title"] + ".png", dpi=ax_config["dpi"])
            print("Done Saving!")
        else:
            plt.savefig(ax_config["path"], dpi=ax_config["dpi"])
            print("Done Saving!")

    if ax_config["draw"]:
        plt.show()


class DiagramMaker:

    def __init__(self):
        self.plot_standards = None
        self.errorbar_standards = None
        self.scatter_standards = None
        self.hist_standards = None
        self.presets = None

        self.config()

    def config(self):
        """
        will load plot_standards and draw_presets from config/<name>.json in lower directory
        -> file path is mandatory and can not be changed!

        :return: nothing, changes plot_standards and presets globals
        """

        try:
            with open(os.path.abspath(os.path.dirname(__file__)) + "/config/plot_standards.json", "r") as of:
                self.plot_standards = json.load(of)
        except FileNotFoundError:
            raise FileNotFoundError("Could not load config/plot_standards.json because file does not exists!")

        try:
            with open(os.path.abspath(os.path.dirname(__file__)) + "/config/hist_standards.json", "r") as of:
                self.hist_standards = json.load(of)
        except FileNotFoundError:
            raise FileNotFoundError("Could not load config/plot_standards.json because file does not exists!")

        try:
            with open(os.path.abspath(os.path.dirname(__file__)) + "/config/draw_presets.json", "r") as of:
                self.presets = json.load(of)
        except FileNotFoundError:
            raise FileNotFoundError("Could not load config/draw_presets.json because file does not exists!")

        # Program will not halt if dicts are empty, but will warn the user
        if self.plot_standards is None:
            print("Plot standards are empty!")
        if self.hist_standards is None:
            print("Hist standards are empty!")
        if self.presets is None:
            print("Draw presets are empty!")

    def make_diagram(self, plot_preset: str, data, **kwargs):
        """
        Makes a plot with preset parameters
        // requires presets to be not None

        :param plot_preset: string, instrument that produced the data
        :param data: tupel of two or more arrays
        :param kwargs: keywords that will overwrite presets and standards if given (will also work for plot_kwargs)
        :return: Diagram object with plotted data
        """

        # check for presets
        if self.presets is None:
            raise ValueError("No presets are set!")
        else:
            # choose plot type
            if self.presets[plot_preset]["plot_type"] == "plot":
                # make copy of presets
                temp = self.presets[plot_preset].copy()
                # remove 'plot_type' key from preset-copy-dictionary
                temp.pop("plot_type")
                for key in kwargs:
                    kwargs[key] = temp[key] | kwargs[key]
                # call according plot function and return the return (overwrites presets here)
                return self.draw_plot(data, **temp | kwargs)

            # same as above
            elif self.presets[plot_preset]["plot_type"] == "scatter":
                temp = self.presets[plot_preset].copy()
                temp.pop("plot_type")
                for key in kwargs:
                    kwargs[key] = temp[key] | kwargs[key]
                return self.draw_scatter(data, **temp | kwargs)

            elif self.presets[plot_preset]["plot_type"] == "errorbar":
                temp = self.presets[plot_preset].copy()
                temp.pop("plot_type")
                for key in kwargs:
                    kwargs[key] = temp[key] | kwargs[key]
                return self.draw_errorbar(data, **temp | kwargs)

            elif self.presets[plot_preset]["plot_type"] == "hist":
                temp = self.presets[plot_preset].copy()
                temp.pop("plot_type")
                for key in kwargs:
                    kwargs[key] = temp[key] | kwargs[key]
                return self.draw_hist(data, **temp | kwargs)

            # raise error, if plot type does not exist
            else:
                print(f"There is no preset called {plot_preset}! Consider using draw_plot or draw_scatter directly!")

    def draw_plot(self, data, **kwargs):
        """
        Makes a plot of the provided data using plt.plot(...)

        :param data: tupel of two or more arrays
        :param kwargs: plot parameters that will be set by the program (overwrites standards)
        :return: Diagram object with plotted data
        """

        # overwrite the standards with provided kwargs (final parameters)
        params = {}
        for key in self.plot_standards:
            if key in kwargs:
                params[key] = self.plot_standards[key] | kwargs[key]
            else:
                params[key] = self.plot_standards[key]

        # configure the window with according utility_deprecated function
        ax = create_window(params)

        # draw diagram
        diagram = ax.plot(*data, **params["plot_kwargs"])

        ax = config_window(ax, params)

        # save/draw/both diagram
        save_draw(params)

        # return the resulting object
        return diagram

    def draw_hist(self, data, **kwargs):
        # overwrite the standards with provided kwargs (final parameters)
        params = {}
        for key in self.hist_standards:
            if key in kwargs:
                # print(self.plot_standards[key], kwargs[key])
                params[key] = self.hist_standards[key] | kwargs[key]
            else:
                # print(key)
                params[key] = self.hist_standards[key]

        # configure the window with according utility_deprecated function
        ax = create_window(params)
        # print(data)
        pprint(params["plot_kwargs"])
        diagram = ax.stairs(*data, **params["plot_kwargs"])

        ax = config_window(ax, params)

        save_draw(params)

        return diagram

    def draw_scatter(self, data, **kwargs):
        pass

    def draw_errorbar(self, data, **kwargs):
        pass


