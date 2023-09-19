from utility.getdata import GetData
from utility.drawdiagrams import DrawDiagrams
from utility.filemanager import FileManager
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

dr = DrawDiagrams(draw_presets)
fi = FileManager()
da = GetData(data_presets)

file_path = "C:/Users/baier/OneDrive/Uni/Bachelorarbeit/data/spec/ppo1/spec_ppo1_sr_1.csv"
save_path = "lel.png"
file_name = "spec_ppo1_r_1.csv"

rec_data = da.auto_read("spec", file_path)


dr.make_plot("spec", rec_data, draw=False, save=True, path=save_path, title=file_name.split(".")[0], ybounds=[0, None])
