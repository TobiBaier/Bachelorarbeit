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
        "xlabel": r"wavelength/nm",
        "ylabel": r"count rate/$\frac{1}{s}$",
        "norm_ylabel": "normed count rate",
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
        "xlabel": r"wavelength/nm",
        "ylabel": "transmission / %",
        "norm_ylabel": "normed transmission rate",
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
        "norm_ylabel": "normed counts",
        "grid": True,
        "ybounds": [0, None],
        "xbounds": [0, None],
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
        "norm_ylabel": "normed pulse height",
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
    "crit": {
        "not_allowed_endings": [".bin", "notes.txt", ".json"],
        "sev": {
            "ending": ".txt",
            "contains": ["hist"],
        },
        "spec": {
            "ending": ".csv",
            "contains": [],
        },
        "uv-vis": {
            "ending": ".csv",
            "contains": [],
        },
        "osc": {
            "ending": ".txt",
            "contains": ["wave"],
        },

    }
}

'''
    Control presets
'''
control_settings = {
    "multi_plot": {
        "outer_format": {
            "title": None,
            "suptitle": None,
            "ax": None,
            "norm": None,
        },
        "style": {
            "draw": False,
            "save": False,
            "label": None,
            "c": ["c", "m", "y", "r", "g", "b", "gray", "purple"],
            "ls": "-",
        }
    },
    "twin_xscale": {
        "outer_format": {
            "title": None,
            "suptitle": None,
            "ax": None,
            "norm": None,
        },
        "style": {
            "draw": False,
            "save": False,
            "label": None,
            "c": ["k", "r"],
            "ls": "-",
            "draw_label": False,
        }
    },
    "auto_plot": {
        "title": None,
        "suptitle": None,
    }
}

save_to_json(plot_standards, "config/plot_standards.json")
save_to_json(draw_presets, "config/draw_presets.json")
save_to_json(txt_standards, "config/txt_standards.json")
save_to_json(csv_standards, "config/csv_standards.json")
save_to_json(data_presets, "config/data_presets.json")
save_to_json(file_inst, "config/file_inst.json")
save_to_json(control_settings, "config/control_settings.json")
