import mechanize
from mechanize import urlopen
import os
import numpy as np
import matplotlib.pyplot as plt
import re
import json
import pandas as pd
import csv
from pprint import pprint


np.set_printoptions(suppress=True,
   formatter={'float_kind':'{:f}'.format})


def retrieve_xcom_data(br):
    i = 0
    for form in br.forms():
        form.name = f"form{i}"
        i += 1
        if form.name == "form1":
            a = form

    input = {
        "photoelectric": ["on"],
        "coherent": ["on"],
        "incoherent": ["on"],
        "nuclear": ["on"],
        "electron": ["on"],
        "with": ["on"],
    }

    for key in input:
        a[key] = input[key]

    answer = urlopen(a.click()).read().decode()

    answer = answer[re.search("\n\n", answer).end():-1]
    df = pd.DataFrame([x.split(' ') for x in answer.split('\n')])

    df_array = df.to_numpy()
    new_array = 0
    for i, line in enumerate(df_array):
        df_array[i] = line[:-1]

    return df_array


def get_element_data_from_xcom(elements, energies):
    str_energies = np.array2string(energies, separator="\n")[1:-1].replace(" ", "")
    print(str_energies)

    for element in elements:
        br = mechanize.Browser()
        br.open("https://physics.nist.gov/cgi-bin/Xcom/xcom2?Method=Elem&Output2=Hand")
        for form in br.forms():
            form.name = "test"
            a = form
        br.select_form(name="test")
        input = {
            "Graph0": [],
            "Graph1": ["on"],
            "Graph2": ["on"],
            "Graph3": ["on"],
            "Graph4": ["on"],
            "Graph5": ["on"],
            "Graph6": ["on"],
            "Graph7": [],
            "ZSym": element,
            "Energies": str_energies
        }
        for key in input:
            a[key] = input[key]
        br.open(a.click())

        ret_arr = retrieve_xcom_data(br)

        print(ret_arr)

        # np.savetxt("data/" + element + ".txt", ret_arr, delimiter=";")


energies = np.logspace(-3, 3, 100)
get_element_data_from_xcom(["C"], energies)


def get_compound_data_from_xcom(compound, energies):
    pass






