
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import csv
import time

def load_values():
    fn = input("Please enter a filename: ")
    draw_arr = []
    with open(fn, "r") as data:
        reader = csv.reader(data, delimiter=";")
        for i in reader:
            draw_arr.append(i)

    return np.array(draw_arr)

