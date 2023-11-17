import os
import numpy as np
import matplotlib.pyplot as plt
import re
from pprint import pprint

def linreg(x1, y1, x2, y2, a):

    m = (y2 - y1) / (x2 - x1)
    n = y1 - m * x1

    return m * a + n

def get_data(relpath="Z:\Studenten\Baier\mass_att_coeff"):
    daten = {}
    paths = os.scandir(relpath)

    for path in paths:
        if path.name.endswith(".txt"):
            x, y, z = np.array([]), np.array([]), np.array([])
            with open(path, "r") as of:
                for line in of.readlines():
                    s = re.findall(r"[.\d]{5,7}E+[+-]+[\d]{2}", line)
                    x = np.append(x, float(s[0]))
                    y = np.append(y, float(s[1]))
                    z = np.append(z, float(s[2]))

                daten[path.name.split("/")[-1].rstrip(".txt")] = [x, y, z]

    return daten


def consistency_check(data, mode="normal"):

    new_entries = {}

    if mode == "even_better_log":
        for key in data:
            for i in range(3):
                data[key][i] = np.log10(data[key][i])

    for key in data:
        new_entries[key] = [np.array([]), np.array([]), np.array([])]
    for key1 in data:
        # print(key1)
        for key2 in data:
            temp1 = []
            temp2 = []
            temp3 = []
            for ie, e2 in enumerate(data[key2][0]):
                if e2 not in data[key1][0]:
                    for i in range(len(data[key1][0])-1):
                        if data[key1][0][i] < e2 <= data[key1][0][i+1]:
                            a = np.count_nonzero(new_entries[key1][0] == e2)
                            b = np.count_nonzero(data[key2][0] == e2)
                            if a < b:
                                if mode == "normal":
                                    temp1.append(e2)
                                    temp2.append(linreg(data[key1][0][i], data[key1][1][i],
                                                        data[key1][0][i + 1], data[key1][1][i + 1], e2))
                                    temp3.append(linreg(data[key1][0][i], data[key1][2][i],
                                                        data[key1][0][i + 1], data[key1][2][i + 1], e2))

                                if mode == "overlog":
                                    temp1.append(e2)
                                    temp2.append(linreg(np.log10(data[key1][0][i]), np.log10(data[key1][1][i]),
                                                        np.log10(data[key1][0][i+1]), np.log10(data[key1][1][i+1]), np.log10(e2)))
                                    temp3.append(linreg(np.log10(data[key1][0][i]), np.log10(data[key1][2][i]),
                                                        np.log10(data[key1][0][i+1]), np.log10(data[key1][2][i+1]), np.log10(e2)))

                                if mode == "even_better_log":
                                    temp1.append(e2)
                                    temp2.append(linreg(data[key1][0][i], data[key1][1][i],
                                                        data[key1][0][i + 1], data[key1][1][i + 1], e2))
                                    temp3.append(linreg(data[key1][0][i], data[key1][2][i],
                                                        data[key1][0][i + 1], data[key1][2][i + 1], e2))


            new_entries[key1][0] = np.append(new_entries[key1][0], temp1)
            new_entries[key1][1] = np.append(new_entries[key1][1], temp2)
            new_entries[key1][2] = np.append(new_entries[key1][2], temp3)

    s = data.copy()
    for key in s:
        data[key][0] = np.append(data[key][0], new_entries[key][0])
        data[key][1] = np.append(data[key][1], new_entries[key][1])
        data[key][2] = np.append(data[key][2], new_entries[key][2])
        ind = np.argsort(data[key][0], kind="stable")
        for i in range(3):
            data[key][i] = data[key][i][ind]

    return data


def display_data(daten, key, show=True, ax=None):
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    ax.plot(daten[key][0], daten[key][2], label=key)
    ax.set_xscale("log")
    ax.set_yscale("log")
    if show:
        plt.show()
    else:
        return ax


def similar_data():
    x1 = 1e-3
    x2 = 2e-3
    y1 = 5
    y2 = 3

    a = [1.1e-3, 1.2e-3, 1.3e-3, 1.4e-3, 1.5e-3, 1.6e-3, 1.7e-3, 1.8e-3, 1.9e-3]
    b = linreg(np.log10(x1), y1, np.log10(x2), y2, np.log10(a))

    c = linreg(np.log10(x1), 7, np.log10(x2), 5, np.log10(a))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(np.append(a, [x1, x2]), np.append(b, [y1, y2]), label="calc", lw=2)
    ax.plot(np.append(a, [x1, x2]), np.append(c, [7, 5]), label="calc2", lw=2)


    quo = np.append([y1], np.append(b, y2))/np.append([7], np.append(c, 5))
    ax.plot(np.append([x1], np.append(a, x2)), quo, label="quo", lw=2)



    ax.plot([x1, x2], [y1, y2])
    ax.plot([x1, x2], [7, 5])






    ax.set_xscale("log")
    ax.legend()
    plt.show()



if __name__ == "__main__":
    similar_data()
    
    # daten = consistency_check(get_data(), mode="even_better_log")

    # ax = display_data(daten, "tissue", show=False)
    # display_data(daten, "polysterene", ax=ax, show=False)

    # fig1 = plt.figure()
    # ax1 = fig1.add_subplot(111)
    # ax1.set_xscale("log")
    # ax1.plot(daten["tissue"][0], daten["polysterene"][2]/daten["tissue"][2])

    # plt.legend()
    # plt.show()