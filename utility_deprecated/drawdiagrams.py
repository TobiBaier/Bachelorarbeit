import matplotlib.pyplot as plt
from pprint import pprint


def config_window(params):

    if params["ax"] is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    else:
        ax = params["ax"]

    if params["title"]:
        # ax.set_title(params["title"])
        plt.title(params["title"], fontsize="small")
    if params["suptitle"]:
        # ax.set_suptitle(params["suptitle"])
        plt.suptitle(params["suptitle"])
    if params["grid"]:
        ax.grid()

    ax.set_xlabel(params["xlabel"])
    ax.set_ylabel(params["ylabel"])

    return ax


def save_draw(params):
    if params["plot_kwargs"]["label"] is not None and params["draw_label"]:
        plt.legend()

    if params["save"]:
        if params["path"] is None:
            plt.savefig(params["title"] + ".png", dpi=params["dpi"])
            print("Done Saving!")
        else:
            plt.savefig(params["path"], dpi=params["dpi"])
            print("Done Saving!")

    if params["draw"]:
        plt.show()



class DrawDiagrams:

    def __init__(self, presets=None):
        self.plot_standards = {
            "ax": None,  # possible to add plot to existing frame
            "plot_kwargs": {
                "fmt": "-+",
                "c": "blue",
                "mec": "black",
                "ms": 6
            },
            "draw": False,
            "save": True,
            "path": None,
            "dpi": 400,
            "title": None,
            "suptitle": None,
            "xlabel": "x",
            "ylabel": "y",
            "xbounds": None,
            "ybounds": None,
            "grid": False,
        }

        self.scatter_standards = {

        }

        self.errorbar_standards = {

        }

        self.presets = presets

    def load_presets(self, presets):
        self.presets = presets

    def make_plot(self, plot_preset, data, **kwargs):
        if self.presets is None:
            raise ValueError("No presets are set!")
        else:
            if self.presets[plot_preset]["plot_type"] == "plot":
                temp = self.presets[plot_preset].copy()
                temp.pop("plot_type")
                return self.draw_plot(data, **temp | kwargs)
            elif self.presets[plot_preset]["plot_type"] == "scatter":
                temp = self.presets[plot_preset].copy()
                temp.pop("plot_type")
                return self.draw_scatter(data, **temp | kwargs)
            elif self.presets[plot_preset]["plot_type"] == "errorbar":
                temp = self.presets[plot_preset].copy()
                temp.pop("plot_type")
                return self.draw_errorbar(data, **temp | kwargs)
            else:
                print(f"There is no preset called {plot_preset}! Consider using draw_plot or draw_scatter directly!")

    def draw_plot(self, data, **kwargs):

        params = self.plot_standards | kwargs

        # pprint(params)

        ax = config_window(params)

        for key in params:
            if key in params["plot_kwargs"]:
                params["plot_kwargs"][key] = params[key]

        diagram = ax.plot(*data, **params["plot_kwargs"])

        if params["xbounds"] is not None:
            ax.set_xbound(params["xbounds"])
        if params["ybounds"] is not None:
            ax.set_ybound(params["ybounds"])

        save_draw(params)

        return diagram

    def draw_scatter(self, data, **kwargs):
        pass

    def draw_errorbar(self, data, **kwargs):
        pass
