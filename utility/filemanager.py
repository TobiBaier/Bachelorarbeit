import os
import re
import shutil

"""
To-Do:
- Messdaten aus "sortme" in passende Ordner packen -> fertig
- Ordnerstruktur reduzieren -> fertig
- lade alle ids aus dem sample catalogue -> fertig
- eine id ändern 
"""


def plottable(file):
    if file.endswith("notes.txt") or file.endswith(".bin") or file.endswith(".json"):
        return False

    if "sev" in file and "hist" not in file:
        return False

    return True


class FileManager:

    def __init__(self, path="C:/Users/baier/OneDrive/Uni/Bachelorarbeit"):

        self.path = path
        self.data_path = path + "/data"
        self.condata_path = path + "/condensed_data"
        self.prodata_path = path + "/processed_data"
        self.sort_path = path + "/sortme"

        self.ids = self.load_ids()
        self.instrument_names = ["spectrometer", "uv-vis", "sev", "osc"]
        self.instrument_ids = ["spec", "uv-vis", "sev", "osc"]

    def load_ids(self):
        ids = []
        with open(self.path + "/sample_catalogue.txt", "r") as idlist:
            lines = idlist.readlines()
            for line in lines:
                # finds all lines of type " id: "[word]""
                x = re.findall(r'[id: "]*[\w]*["]', line)
                if x:
                    # remove "id" with split and "" with strip
                    ids.append(x[0].split(" id: ")[1].strip('\"'))

        return ids

    def reduce_dir_order(self):
        for i, inst in enumerate(self.instrument_names):
            for sample in self.ids:
                if os.path.isdir(self.data_path + "/" + inst + "/" + sample):

                    # save current path
                    curr_path = self.data_path + "/" + inst + "/" + sample

                    # create target directory if necessary
                    if not os.path.isdir(self.condata_path + "/" + sample):
                        os.makedirs(self.condata_path + "/" + sample)

                    # get list of all files in current directory
                    for file_path in os.listdir(curr_path):
                        if os.path.isfile(os.path.join(curr_path, file_path)):

                            file = curr_path + "/" + file_path

                            if not file.endswith("notes.txt"):
                                shutil.copyfile(file, self.condata_path + "/" + sample + "/" + file_path)

    def save_in_dir(self):
        files = []

        for file_path in os.listdir(self.sort_path):
            if os.path.isfile(os.path.join(self.sort_path, file_path)):
                files.append(file_path)

        for i in files:
            inst, sample = self.filecheck(i)

            new_path = self.data_path + "/" + inst + "/" + sample

            if not os.path.isdir(new_path):
                os.makedirs(new_path)
            else:
                pass

            if not os.path.isfile(new_path + "/" + i):
                os.rename(self.sort_path + "/" + i, new_path + "/" + i)
            else:
                raise FileExistsError(f"A file already exists at {new_path + '/' + i}")

    def filecheck(self, file_name):
        """
        extracts sample and instrument id from file name
        :param file_name:
        :return:
        """
        info = file_name.split("_")
        inst = info[0]
        sample = info[1]

        if inst not in self.instrument_ids:
            raise NameError(f"Instrument '{inst}' does not exist!")
        if sample not in self.ids:
            raise NameError(f"Sample id '{sample}' does not exist!")

        return inst, sample

    def check_if_file(self, file_name):
        """
        REQUIRES ENDING!!! -> check if file at path exists
        :param file_name
        :return: None if file does not exist, path if it does
        """

        inst, sample = self.filecheck(file_name)

        file_path = self.data_path + "/" + inst + "/" + sample + "/" + file_name

        if os.path.isfile(file_path):
            return file_path
        else:
            return None

    def get_save_path(self, file_name):
        """
        REQUIRES ENDING!!!
        :param file_name
        :return: None if file does not exist, path to save to if it does (gets created if necessary)
        """
        inst, sample = self.filecheck(file_name)

        no_ending = file_name.split(".")[0]

        file_path = self.prodata_path + "/" + inst + "/" + sample

        if not os.path.isdir(file_path):
            os.makedirs(file_path)

        return file_path + "/" + no_ending + ".png"

    def get_file_names(self, inst_list):
        names = []
        for inst in inst_list:
            for sample_path in os.listdir(self.data_path + "/" + inst):
                # could add a function, that checks if file is plottable
                for file in os.listdir(self.data_path + "/" + inst + "/" + sample_path):
                    if plottable(file):
                        names.append(file)

        return names

    def check_ending(self, file_name):
        inst, sample = self.filecheck(file_name)

        if inst == "spec" or inst == "uv-vis":
            if not file_name.endswith(".csv"):
                if plottable(file_name):
                    if self.check_if_file(file_name + ".csv") is not None:
                        return file_name + ".csv"

        if inst == "sev":
            if not file_name.endswith(".txt"):
                if plottable(file_name):
                    if self.check_if_file(file_name + ".txt") is not None:
                        return file_name + ".txt"

        return file_name


if __name__ == "__main__":
    a = FileManager()
    a.save_in_dir()
    a.reduce_dir_order()
