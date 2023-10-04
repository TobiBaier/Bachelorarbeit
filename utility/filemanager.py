"""
This program is supposed to be used for a organisation of a large scale prototyping databank, where lots of different
samples are measured with a set of different instruments
"""


import os
import re
import json
import shutil


def load_criteria():
    try:
        with open(os.path.abspath(os.path.dirname(__file__)) + "/config/file_inst.json", "r") as of:
            data = json.load(of)

    except FileNotFoundError:
        raise FileNotFoundError("Could not load config/file_inst.json because file does not exists!")

    return data["crit"]


class FileManager:
    """
    --------------------------------------------------------------------------
    INITIALIZATION
    """
    def __init__(self, root_path):

        # load root directory path
        self.path = root_path

        # load predefined directory paths
        self.data_path = self.path + "/data"
        self.condata_path = self.path + "/condensed_data"
        self.prodata_path = self.path + "/processed_data"
        self.sort_path = self.path + "/sortme"

        # catalogue path/file name
        self.cat_name = "sample_catalogue.txt"

        # load all ids
        self.sample_ids, self.inst_ids = self.load_ids()

        # load file criteria
        self.file_criteria = load_criteria()

    def load_ids(self):
        sample_ids = []
        with open(self.path + "/" + self.cat_name, "r") as idlist:
            lines = idlist.readlines()
            for line in lines:
                # finds all lines of type " id: "[word]""
                x = re.findall(r'[id: "]+[\w]*[-]*[\w]+["]', line)
                if x:
                    # remove "id" with split and "" with strip
                    sample_ids.append(x[0].split(" id: ")[1].strip('\"'))

        try:
            with open(os.path.abspath(os.path.dirname(__file__)) + "/config/file_inst.json", "r") as of:
                inst_ids = json.load(of)["ids"]
        except FileNotFoundError:
            raise FileNotFoundError("Could not load config/file_inst.json because file does not exists!")

        return sample_ids, inst_ids

    """
    --------------------------------------------------------------------------
    UTILITY FUNCTIONS
    """
    def get_inst_and_sample(self, filename):
        """
        extracts the sample and instrument id from a file name

        :param filename: name of the file (may include directory, will get cut)
        :return: inst and sample id (in that order)
        """

        name = filename.split("/")[-1]

        try:
            i_id, s_id = name.split("_")[0], name.split("_")[1]
        except IndexError:
            for ending in self.file_criteria["not_allowed_endings"]:
                if filename.endswith(ending):
                    return None, None
            raise IndexError(f"I do not know how you ended up here, but its probably because of: {filename}")

        if i_id not in self.inst_ids:
            raise NameError(f"Instrument '{i_id}' does not exist!")
        if s_id not in self.sample_ids:
            raise NameError(f"Sample id '{s_id}' does not exist!")

        return i_id, s_id

    def check_filename_format(self, filename):
        """
        checks if filename is allowed and if file exists // will ignore given directory (use check_if_file_exists)

        :param filename: name of the file (with/without dir)
        :return: False if not correct // name with ending if correct
        """

        filename = filename.split("/")[-1]

        for ending in self.file_criteria["not_allowed_endings"]:
            if filename.endswith(ending):
                return False

        inst, sample = self.get_inst_and_sample(filename)

        if inst in self.inst_ids:
            if sample in self.sample_ids:
                if not filename.endswith(self.file_criteria[inst]["ending"]):
                    filename = filename + self.file_criteria[inst]["ending"]
                else:
                    pass

                for ident in self.file_criteria[inst]["contains"]:
                    if ident not in filename:
                        return False

                if os.path.isfile(self.data_path + "/" + inst + "/" + sample + "/" + filename):
                    return filename
                else:
                    return False

        return filename

    def get_datafile_path(self, filename):
        """
        Get the complete path to a file in the data directory

        :param filename: filename with/without ending
        :return: path to filename
        """

        inst, sample = self.get_inst_and_sample(filename)

        filename = self.check_filename_format(filename)

        if os.path.isfile(self.data_path + "/" + inst + "/" + sample + "/" + filename):
            return self.data_path + "/" + inst + "/" + sample + "/" + filename
        else:
            return None

    def get_savefile_path(self, filename):
        """
        Get the complete path to a file in the processed data directory

        :param filename: filename with/without ending
        :return: path to save location
        """
        inst, sample = self.get_inst_and_sample(filename)

        filename = self.check_filename_format(filename)

        if not os.path.isdir(self.prodata_path + "/" + inst + "/" + sample):
            os.makedirs(self.prodata_path + "/" + inst + "/" + sample)

        return self.prodata_path + "/" + inst + "/" + sample + "/" + filename.split(".")[0] + ".png"

    """
    --------------------------------------------------------------------------
    ACTUAL HIGH LEVEL FILE MANAGEMENT
    """
    def sort_to_dirs(self):
        files = []

        for filepath in os.listdir(self.sort_path):
            if os.path.isfile(os.path.join(self.sort_path, filepath)):
                files.append(filepath)

        for file in files:
            inst, sample = self.get_inst_and_sample(file)

            new_path = self.data_path + "/" + inst + "/" + sample

            if not os.path.isdir(new_path):
                os.makedirs(new_path)

            if not os.path.isfile(new_path + "/" + file):
                os.rename(self.sort_path + "/" + file, new_path + "/" + file)
                print(f"Moved from {self.sort_path + '/' + file} to {new_path + '/' + file}")
            else:
                raise FileExistsError(f"A file already exists at {new_path + '/' + file}")

            return files

    def condense_data(self):
        for inst in self.inst_ids:
            for sample in self.sample_ids:
                if os.path.isdir(self.data_path + "/" + inst + "/" + sample):

                    curr_path = self.data_path + "/" + inst + "/" + sample

                    if not os.path.isdir(self.condata_path + "/" + sample):
                        os.makedirs(self.condata_path + "/" + sample)

                    for filepath in os.listdir(curr_path):
                        if os.path.isfile(os.path.join(curr_path, filepath)):

                            file = curr_path + "/" + filepath

                            if not file.endswith("notes.txt"):
                                shutil.copyfile(file, self.condata_path + "/" + sample + "/" + filepath)




