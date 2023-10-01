"""
Overview of all the presets
-> edit the dictionaries and run the program to update config files
-> run 'consistency_check' to see if saved dictionaries are up-to-date with config
"""


import json


def save_to_json(data, fp):
    j_data = json.dumps(data, indent=4, sort_keys=True, separators=(",", ": "), ensure_ascii=False)
    with open(fp, "w") as of:
        of.write(j_data)


def load_from_json(fp):
    with open(fp, "r") as of:
        data = json.load(of)
    return data


def consistency_check(data, fp):
    j_data = load_from_json(fp)
    return data == j_data


'''
    Diagram presets
'''
# general standards for plots
plot_standards = {
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

# drawing presets for instruments
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

'''
    Data presets
'''
# general standards for certain file types
csv_standards = {
    "skiprows": 0,
    "sep": ";",
    "usecols": None,
    "header": None,
    "swap_axes": True,
    "skipfooter": 0,
    "encoding": "iso-8859-1",
}

txt_standards = {
    "skiprows": 0,
    "sep": ";",
    "usecols": None,
    "header": None,
    "swap_axes": True,
    "skipfooter": 0,
    "encoding": "iso-8859-1",
}

# data presets for instruments
data_presets = {
    "sev": {
        "data_type": "txt",
        "skiprows": 5,
        "usecols": [0, 1]
    },
    "spec": {
        "data_type": "csv",
        "skiprows": 0,
    },
    "uv-vis": {
        "data_type": "csv",
        "skiprows": 2,
        "sep": ",",
        "skipfooter": 2,
        "usecols": [0, 1],
    },
    "osc": {
        "data_type": "txt",
        "skiprows": 5,
        "sep": ";",
        "usecols": [0, 1],
    }
}

'''
    File presets
'''
file_inst = {
    "ids": ["sev", "spec", "osc", "uv-vis"],
}

save_to_json(plot_standards, "config/plot_standards.json")
save_to_json(draw_presets, "config/draw_presets.json")
save_to_json(txt_standards, "config/txt_standards.json")
save_to_json(csv_standards, "config/csv_standards.json")
save_to_json(data_presets, "config/data_presets.json")
save_to_json(file_inst, "config/file_inst.json")
