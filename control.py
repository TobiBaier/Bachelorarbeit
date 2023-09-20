from utility.getdata import GetData
from utility.drawdiagrams import DrawDiagrams
from utility.filemanager import FileManager
import os
import matplotlib.pyplot as plt

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
        "skipfooter": 32,
        "cols": [0, 1],
    },
}

draw_presets = {
    "spec": {
        "plot_type": "plot",
        "plot_kwargs": {  # NEEDS to contain ALL graphical plot infos
            "ls": "-",
            "marker": "+",
            "c": "blue",
            "mec": "black",
            "ms": 6,
            "label": None
        },
        "xlabel": r"Wellenlänge/nm",
        "ylabel": r"Zählrate/$\frac{1}{s}$",
        "grid": True,
        "ybounds": [0, None],
    },
    "uv-vis": {
        "plot_type": "plot",
        "plot_kwargs": {
            "ls": "-",
            "marker": None,
            "c": "black",
            "label": None,
        },
        "xlabel": r"Wellenlänge/nm",
        "ylabel": "transmission / %",
        "grid": True,
        "ybounds": [0, None],
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

    def auto_plot_data(self, file_name):
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
            print(f"Saving plot to '{save_path}'.")

            # draw and save the plot
            self.curr_draw.make_plot(inst, rec_data, draw=False, save=True, path=save_path, title=file_name.split(".")[0])

    def plot_all_inst_data(self, inst_list=None):
        if inst_list is not None:
            names = self.curr_file.get_file_names(inst_list)
            for name in names:
                self.auto_plot_data(name)

    def plot_dir(self, dir):
        for file_path in os.listdir(self.curr_file.data_path + "/" + dir):
            if os.path.isdir(self.curr_file.data_path + "/" + dir + "/" + file_path):
                print(dir + "/" + file_path)
                self.plot_dir(dir + "/" + file_path)
            else:
                print(file_path)
                self.auto_plot_data(file_path)

    def multi_plot(self, name_list, label_list, path, title=None, clist=["c", "m", "y", "r", "g", "b"]):
        path = self.curr_file.prodata_path + "/" + path

        fig = plt.figure()
        ax = fig.add_subplot(111)

        clist = clist[:len(name_list)]

        for name, c, label in zip(name_list, clist, label_list):
            file_name = self.curr_file.check_ending(name)
            file_path = self.curr_file.check_if_file(file_name)
            print(file_name, file_path)
            if file_path is None:
                raise FileNotFoundError(f"There is no data file called '{file_name}'!")

            inst = file_name.split("_")[0]
            rec_data = self.curr_data.auto_read(inst, file_path)

            self.curr_draw.make_plot(inst, rec_data, ax=ax, draw=False, save=False, title=None, c=c, label=label)

        ax.set_title(title)
        ax.grid()

        plt.savefig(path, dpi=400)

        plt.show()


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
