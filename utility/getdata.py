import csv
import numpy as np
import os
import pandas as pd

"""
Input-Vars:
 - file name / path
 - skip_lines
 - delimiter
 - infos for certain rows (e.g. data type)
 - flip axes
 
returns:
 - data in the csv as nd np array
 
Lösung für das kwargs Problem:
 dict in __init__ festlegen, dann in Funktionen einfach abgleichen
 wenn man keywords für hilfe sehen will, dann einfach help funktion aufrufen -> prettyprinted dictionaries
 
 could add presets in the init class, where data file formats are saved -> needs extra function that is called in case
"""


def update_standards(para, kw):
    for key in kw:
        if key in para:
            para[key] = kw[key]
        else:
            print(f"The keyword {key} does not have a function!")

    return para


class GetData:

    def __init__(self, presets=None):
        self.csv_standards = {
            "skip_lines": 0,
            "delimiter": ";",
            "cols": None,
            "header": None,
            "swap_axes": True
        }

        self.txt_standards = {
            "skip_lines": 0,
            "delimiter": ";",
            "cols": None,
            "header": None,
            "swap_axes": True
        }

        self.presets = presets

    def load_presets(self, presets):
        self.presets = presets

    def auto_read(self, instrument, path, **kwargs):
        if self.presets is None:
            raise ValueError("No presets are set!")
        else:
            if self.presets[instrument]["data_type"] == "txt":
                temp = self.presets[instrument].copy()
                temp.pop("data_type")
                return self.data_from_txt(path, **temp | kwargs)
            if self.presets[instrument]["data_type"] == "csv":
                temp = self.presets[instrument].copy()
                temp.pop("data_type")
                return self.data_from_csv(path, **temp | kwargs)

    def data_from_csv(self, path, **kwargs):

        params = self.csv_standards | kwargs

        if type(path) != str:
            raise TypeError(f"Path must be string-type not {type(path)}! (CODE1)")

        if not path.endswith(".csv"):
            # possibly add relays to different program parts that handle other endings
            if path.endswith(".txt"):
                pass
            else:
                path = path + ".csv"

        if not os.path.isfile(path):
            if os.path.isfile(os.getcwd() + "/" + path):
                path = os.getcwd() + path
            else:
                raise FileNotFoundError(f"There is no file called {path}! (CODE2)")

        data = pd.read_csv(path, sep=params["delimiter"], skiprows=params["skip_lines"], header=params["header"],
                           usecols=params["cols"])

        if params["swap_axes"]:
            return data.to_numpy().swapaxes(0, 1)
        else:
            return data.to_numpy()

    def data_from_txt(self, path, **kwargs):

        params = self.txt_standards | kwargs

        if type(path) != str:
            raise TypeError(f"Path must be string-type not {type(path)}! (CODE3)")

        if not path.endswith(".txt"):
            path = path + ".txt"

        return self.data_from_csv(path, **params)


if __name__ == "__main__":
    a = GetData()
    # x = a.data_from_txt("co57with3hfcomm_histogram", cols=[0, 1], skip_lines=4)
    x = a.auto_read("sev","co57with3hfcomm_histogram")
    print(x[1][0:100])
