import os
import re
import json
import shutil

class FileManager:

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

        self.ids, self.inst_ids = self.load_ids()

    def load_ids(self):
        ids = []
        with open(self.path + "/" + self.cat_name, "r") as idlist:
            lines = idlist.readlines()
            for line in lines:
                # finds all lines of type " id: "[word]""
                x = re.findall(r'[id: "]*[\w]*["]', line)
                if x:
                    # remove "id" with split and "" with strip
                    ids.append(x[0].split(" id: ")[1].strip('\"'))

        try:
            with open("config/file_inst.json", "r") as of:
                inst_ids = json.load(of)["ids"]
        except FileNotFoundError:
            raise FileNotFoundError("Could not load config/file_inst.json because file does not exists!")

        return ids, inst_ids

    def reduce_dir_order(self):
        for inst in self.inst_ids:
            for sample in self.ids:
                if os.path.isdir(self.data_path + "/" + inst + "/" + sample):
                    pass

a = FileManager("C:/Users/baier/OneDrive/Uni/Bachelorarbeit")
a.reduce_dir_order()

