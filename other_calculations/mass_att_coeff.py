import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re
from pprint import pprint

paths = os.scandir("C:/Users/baier/OneDrive/Uni/Bachelorarbeit_2/mass_att_coeff")

daten = {}

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


def mass_fractions(masses, stoch):
    masses = np.array(masses)
    stoch = np.array(stoch)

    a = masses * stoch
    s = np.sum(a)

    return a / s

def linreg(x1, y1, x2, y2, a):

    m = (y2 - y1) / (x2 - x1)
    n = y1 - m * x1

    return m * a + n

def consistency_check(data):

    new_entries = {}

    for key in data:
        new_entries[key] = [np.array([]), np.array([]), np.array([])]

    for key1 in data:
        for key2 in data:
            for ie, e1 in enumerate(data[key1][0]):
                # wenn Eintrag aus 1 nicht in 2, dann wird gespeichert, dass 1 in 2 ergänzt werden muss
                if e1 not in data[key2][0]:
                    new_entries[key2][0] = np.append(new_entries[key2][0], e1)
                    for i in range(len(data[key2][0]) - 1):
                        if data[key2][0][i] < e1 <= data[key2][0][i+1]:
                            new_entries[key2][1] = np.append(new_entries[key2][1],
                                                             linreg(data[key2][0][i], data[key2][1][i],
                                                                    data[key2][0][i+1], data[key2][1][i+1],
                                                                    e1))
                            new_entries[key2][2] = np.append(new_entries[key2][2],
                                                             linreg(data[key2][0][i], data[key2][2][i],
                                                                    data[key2][0][i+1], data[key2][2][i+1],
                                                                    e1))


    s = data.copy()
    for key in s:
        for i in range(3):
            data[key][i] = np.append(data[key][i], new_entries[key][i])

        ind = np.argsort(data[key][0])
        for i in range(3):
            data[key][i] = data[key][i][ind]


    return data

daten = consistency_check(daten)

fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(daten["carbon"][0], daten["carbon"][1] + daten["chlorine"][1],  label="both")
ax.plot(daten["carbon"][0], daten["carbon"][1], label="carbon")
ax.plot(daten["chlorine"][0], daten["chlorine"][1], label="chlorine")

ax.set_yscale('log')
ax.set_xscale('log')

"""ax.set_xlabel("Photonenenergie / MeV")
ax.set_ylabel(r"Verhältnis $(\frac{\mu_{en}}{\rho})_{Detektor}$  /  $(\frac{\mu_{en}}{\rho}_{Gewebe})$")
ax.set_title("Proportionalitätsfaktor zwischen Detektor- und Gewebedosis")"""

ax.legend()
plt.show()
"""
daten["coeff_pu"] = (0.627922665 * daten["coeff_carbon"][2] +
                     0.090842816 * daten["coeff_hydrogen"][2] +
                     0.0505004 * daten["coeff_nitrogen"][2] +
                     0.230734119 * daten["coeff_oxygen"][2])

daten["coeff_epoxy"] = (0.8438475 * daten["coeff_carbon"][2] +
                        0.0758647 * daten["coeff_hydrogen"][2] +
                        0.0802878 * daten["coeff_oxygen"][2])

daten["coeff_pmma"] = (0.59985585 * daten["coeff_carbon"][2] +
                       0.08053401 * daten["coeff_hydrogen"][2] +
                       0.31961015 * daten["coeff_oxygen"][2])

daten["coeff_polyethylene"] = 0

# daten["coeff_salt"] = ()

# ax.plot(daten["coeff_pv"][0], daten["coeff_pv"][2], label="Polyvinyltoulene")
# ax.plot(daten["coeff_ps"][0], daten["coeff_ps"][2], label="Polystyrene")
# ax.plot(daten["coeff_pv"][0], daten["coeff_pu"], label="Polyurethane")

# ax.plot(daten["coeff_tissue"][0], daten["coeff_tissue"][2], label="tissue")

# ax.plot(daten["coeff_tissue"][0], daten["coeff_pu"] / daten["coeff_tissue"][2], label="Polyurethan")
ax.plot(daten["coeff_tissue"][0], daten["coeff_pv"][2] / daten["coeff_tissue"][2], label="Polyvinyl")
ax.plot(daten["coeff_tissue"][0], daten["coeff_epoxy"] / daten["coeff_tissue"][2], label="Epoxidharz")
# ax.plot(daten["coeff_tissue"][0], daten["coeff_pmma"] / daten["coeff_tissue"][2], label="PMMA")


"""
