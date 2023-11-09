import os
import json
import pandas as pd
import numpy as np


class DataLoader:

    def __init__(self):
        self.csv_standards = None
        self.txt_standards = None
        self.presets = None

        self.config()

    def config(self):
        """
        will load csv/txt_standards and data_presets from config/<name>.json in lower directory
        -> file path is mandatory and can not be changed!

        :return: nothing, changes csv/txt_standards and presets globals
        """

        try:
            with open(os.path.abspath(os.path.dirname(__file__)) + "/config/csv_standards.json", "r") as of:
                self.csv_standards = json.load(of)
        except FileNotFoundError:
            raise FileNotFoundError("Could not load config/csv_standards.json because file does not exists!")

        try:
            with open(os.path.abspath(os.path.dirname(__file__)) + "/config/txt_standards.json", "r") as of:
                self.txt_standards = json.load(of)
        except FileNotFoundError:
            raise FileNotFoundError("Could not load config/txt_standards.json because file does not exists!")

        try:
            with open(os.path.abspath(os.path.dirname(__file__)) + "/config/data_presets.json", "r") as of:
                self.presets = json.load(of)
        except FileNotFoundError:
            raise FileNotFoundError("Could not load config/data_presets.json because file does not exists!")

        # Program will not halt if dicts are empty, but will warn the user
        if self.csv_standards is None:
            print("csv standards are empty!")
        if self.txt_standards is None:
            print("txt standards are empty!")
        if self.presets is None:
            print("Draw presets are empty!")

    def auto_read(self, read_preset, path, **kwargs):
        """
        reads data file produced by a specified instrument

        :param read_preset: the instrument/preset that produced the data
        :param path: file path
        :param kwargs: if presets do not apply for this case, they can be updated here
        :return: arrays with the data
        """
        if self.presets is None:
            raise ValueError("No presets are set!")
        else:
            # check if instrument needs txt or csv
            if self.presets[read_preset]["data_type"] == "txt":
                # copy the presets and hand them over to reader function
                temp = self.presets[read_preset].copy()
                temp.pop("data_type")
                return self.data_from_txt(path, **temp | kwargs)
            if self.presets[read_preset]["data_type"] == "csv":
                temp = self.presets[read_preset].copy()
                temp.pop("data_type")
                return self.data_from_csv(path, **temp | kwargs)

    def data_from_csv(self, path, **kwargs):
        """
        read data from a csv file, also checks/adds file ending

        :param path: file path (ending can be missing)
        :param kwargs: keywords for changes in pd.read_csv (only other keyword should be "swap_axes"!)
        :return: the data from the file
        """

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

        # remove swap_axes key, so that rest can be passed to pd.read
        swap_bool = False
        if params["swap_axes"]:
            swap_bool = True
        params.pop("swap_axes")

        # same procedure for bin return
        bin_ret = False
        if "bin_ret" in params:
            bin_ret = params.pop("bin_ret")

        # read data using pandas -> all presets are handed over to the function (might add *params in the future)
        data = pd.read_csv(path, **params)

        # convert data_frame to np arrays and return them
        if swap_bool:
            if not bin_ret:
                return data.to_numpy().swapaxes(0, 1)
            else:
                x, y = data.to_numpy().swapaxes(0, 1)
                bin_width = x[1] - x[0]
                x = x - 0.5 * bin_width
                return y, np.append(x, x[-1]+bin_width)
        else:
            return data.to_numpy()

    def data_from_txt(self, path, **kwargs):
        """
        read data from a txt file, also checks/adds file ending // internally uses data_from_csv

        :param path: file path (ending can be missing)
        :param kwargs: keywords for changes in pd.read_csv (only other keyword should be "swap_axes"!)
        :return: the data from the file
        """

        params = self.txt_standards | kwargs

        if type(path) != str:
            raise TypeError(f"Path must be string-type not {type(path)}! (CODE3)")

        if not path.endswith(".txt"):
            path = path + ".txt"

        # just uses csv reader, as txt files can be handled as such
        return self.data_from_csv(path, **params)

if __name__ == "__main__":
    a = DataLoader()
    # x = a.data_from_txt("co57with3hfcomm_histogram", cols=[0, 1], skip_lines=4)
    x = a.auto_read("sev","C:/Users/baier/OneDrive/Uni/Bachelorarbeit/data/osc/ppo5/osc_ppo5_bcg2s067_waveform_0")
    print(x[1][0:100])