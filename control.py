from utility.getdata import GetData
from utility.drawdiagrams import DrawDiagrams
from utility.filemanager import FileManager
import os

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
}

draw_presets = {
            "spec": {
                "plot_type": "plot",
                "plot_kwargs": {        # NEEDS to contain ALL graphical plot infos
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
            },
            "uv-vis": {
                "plot_type": "plot",
                "plot_kwargs": {
                    "ls": "-",
                    "marker": None,
                    "c": "black",
                    "label": None,
                },
                "xlabel": r"$\lambda$/nm",
                "ylabel": "transmission / %",
                "grid": True,
            },
            "sev": {
                "plot_type": "plot",
                "plot_kwargs": {
                    "ls": "-",
                    "marker": None,
                    "c": "black",
                    "label": None,
                },
                "xlabel": r"energy/channels",
                "ylabel": "counts",
                "grid": True,
            }
}

"""a = GetData(data_presets)

x = a.auto_read("spectrometer", "combi_scin_1")

b = DrawDiagrams(draw_presets)

b.make_plot("spectrometer", x, save=False, title="testing", label="more testing", c="red")"""

'''
To-Do:
- einzelne Messdatei darstellen
- alle Messdateien gleichzeitig rendern
- Routine, um zwei Plots in einem zu erschaffen
'''


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
        file_path = self.curr_file.check_if_file(file_name)

        if file_path is None:
            raise FileNotFoundError(f"There is no data file called '{file_name}'!")

        # get instrument id
        inst = file_name.split("_")[0]

        rec_data = self.curr_data.auto_read(inst, file_path)

        save_path = self.curr_file.get_save_path(file_name)
        print(f"Saving plot to '{save_path}'.")

        self.curr_draw.make_plot(inst, rec_data, draw=False, save=True, path=save_path, title=file_name.split(".")[0])

    def plot_all_data(self, inst_list=None):
        if inst_list is not None:
            names = self.curr_file.get_file_names(inst_list)
            for name in names:
                self.auto_plot_data(name)


dr = DrawDiagrams()
fi = FileManager()
da = GetData()

a = Control(dr, fi, da)
a.plot_all_data(["spec"])