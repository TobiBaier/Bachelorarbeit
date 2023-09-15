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
"""


def update_standards(para, kw):
    for key in kw:
        if key in para:
            para[key] = kw[key]
        else:
            print(f"The keyword {key} does not have a function!")

    return para


class GetData:

    def __init__(self):
        self.csv_standards = {
            "skip_lines": 0,
            "delimiter": ";",
            "cols": None,
            "header": None,
            "swap_axes": True
        }

    def data_from_csv(self, path, **kwargs):

        params = update_standards(self.csv_standards, kwargs)

        if type(path) != str:
            raise TypeError(f"Path must be string-type not {type(path)}! (CODE1)")

        if not path.endswith(".csv"):
            # possibly add relays to different program parts that handle other endings
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









if __name__ == "__main__":
    a = GetData()
    x = a.data_from_csv("spectrum", cols=[0, 1])
    print(x[0])

