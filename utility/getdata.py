import csv
import numpy as np
import os
import pandas as pd
from pprint import pprint

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


class GetData:
    """
    can take data from a specified file
    features:
        - csv/txt reader function, that feeds pandas command with information
        - autoread, allowing for presets if reading from a specified instrument
    """

    def __init__(self, presets=None):
        """
        Initialise the standard settings for reading csv/txt files
        :param presets: dictionary with "inst" keys containing dictionaries with updated standards
        """
        self.csv_standards = {
            "skip_lines": 0,
            "delimiter": ";",
            "cols": None,
            "header": None,
            "swap_axes": True,
            "skipfooter": 0,
        }

        self.txt_standards = {
            "skip_lines": 0,
            "delimiter": ";",
            "cols": None,
            "header": None,
            "swap_axes": True,
            "skipfooter": 0,
        }

        self.presets = presets

    def load_presets(self, presets):
        self.presets = presets

    def auto_read(self, instrument, path, **kwargs):
        """
        reads data file produced by a specified instrument
        :param instrument: the instrument/preset that produced the data
        :param path: file path
        :param kwargs: if presets do not apply for this case, they can be updated here
        :return: arrays with the data
        """
        if self.presets is None:
            raise ValueError("No presets are set!")
        else:
            # check if instrument needs txt or csv
            if self.presets[instrument]["data_type"] == "txt":
                # copy the presets and hand them over to reader function
                temp = self.presets[instrument].copy()
                temp.pop("data_type")
                return self.data_from_txt(path, **temp | kwargs)
            if self.presets[instrument]["data_type"] == "csv":
                temp = self.presets[instrument].copy()
                temp.pop("data_type")
                return self.data_from_csv(path, **temp | kwargs)

    def data_from_csv(self, path, **kwargs):

        # update the standards with provided presets/kwargs
        params = self.csv_standards | kwargs

        # error handling if path is no string
        if type(path) != str:
            raise TypeError(f"Path must be string-type not {type(path)}! (CODE1)")

        # add ending to file path (if not there already)
        if not path.endswith(".csv"):
            # possibly add relays to different program parts that handle other endings
            if path.endswith(".txt"):
                pass
            else:
                path = path + ".csv"

        # check if path does actually exist
        if not os.path.isfile(path):
            if os.path.isfile(os.getcwd() + "/" + path):
                path = os.getcwd() + path
            else:
                raise FileNotFoundError(f"There is no file called {path}! (CODE2)")

        # read data using pandas -> all presets are handed over to the function (might add *params in the future)
        data = pd.read_csv(path, sep=params["delimiter"], skiprows=params["skip_lines"], header=params["header"],
                           usecols=params["cols"], skipfooter=params["skipfooter"])

        # convert data_frame to np arrays and return them
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

        # just uses csv reader, as txt files can be handled as such
        return self.data_from_csv(path, **params)


if __name__ == "__main__":
    a = GetData()
    # x = a.data_from_txt("co57with3hfcomm_histogram", cols=[0, 1], skip_lines=4)
    x = a.auto_read("sev","co57with3hfcomm_histogram")
    print(x[1][0:100])
