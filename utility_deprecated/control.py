from getdata import GetData
from drawdiagrams import DrawDiagrams

data_presets = {
            "sev": {
                "data_type": "txt",
                "skip_lines": 5,
                "cols": [0, 1]
            },
            "spectrometer": {
                "data_type": "csv",
                "skip_lines": 0,
            },
}

draw_presets = {
            "spectrometer": {
                "plot_type": "plot",
                "plot_kwargs": {        # NEEDS to contain ALL graphical plot infos
                    "ls": "-",
                    "marker": "+",
                    "c": "blue",
                    "mec": "black",
                    "ms": 6,
                    "label": None
                },
                "xlabel": r"$\lambda$/nm",
                "ylabel": "counts",
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

a = GetData(data_presets)

x = a.auto_read("spectrometer", "combi_scin_1")

b = DrawDiagrams(draw_presets)

b.make_plot("spectrometer", x, save=False, title="testing", label="more testing", c="red")


