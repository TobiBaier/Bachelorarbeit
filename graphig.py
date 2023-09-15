import csv
import numpy as np
import matplotlib.pyplot as plt


def load_values(fn):
    draw_arr = []
    with open(fn, "r") as data:
        reader = csv.reader(data, delimiter=";")
        for i in reader:
            draw_arr.append(i)

    return np.array(draw_arr)


data1 = np.swapaxes(load_values("data/first_diphen_cast/own_scin_5.csv"), 0, 1).astype(float)
data2 = np.swapaxes(load_values("data/first_diphen_cast/own_pu_1.csv"), 0, 1).astype(float)

fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(data1[0], data1[1]/np.max(data1[1]), label="scin")
ax.plot(data2[0], data2[1]/np.max(data2[1]), label="pu")

ax.set_xlabel(r"$\lambda$/nm")
ax.set_ylabel("counts")
ax.grid()
plt.legend()
plt.show()