import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pprint import pprint

paths = os.scandir("C:/Users/baier/OneDrive/Uni/Bachelorarbeit_2/mass_att_coeff")

daten = {}

for path in paths:
    if path.name.endswith(".txt"):
        with open(path, "r") as of:
            data = pd.read_csv(of, skiprows=0, header=None, sep="  ")

        x = data.to_numpy().swapaxes(0, 1)

        daten[path.name.split("/")[-1].rstrip(".txt")] = x

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

fig = plt.figure()
ax = fig.add_subplot(111)

# ax.plot(daten["coeff_pv"][0], daten["coeff_pv"][2], label="Polyvinyltoulene")
# ax.plot(daten["coeff_ps"][0], daten["coeff_ps"][2], label="Polystyrene")
# ax.plot(daten["coeff_pv"][0], daten["coeff_pu"], label="Polyurethane")

# ax.plot(daten["coeff_tissue"][0], daten["coeff_tissue"][2], label="tissue")

ax.plot(daten["coeff_tissue"][0], daten["coeff_pu"] / daten["coeff_tissue"][2], label="Polyurethan")
ax.plot(daten["coeff_tissue"][0], daten["coeff_pv"][2] / daten["coeff_tissue"][2], label="Polyvinyl")
ax.plot(daten["coeff_tissue"][0], daten["coeff_epoxy"] / daten["coeff_tissue"][2], label="Epoxidharz")
ax.plot(daten["coeff_tissue"][0], daten["coeff_pmma"] / daten["coeff_tissue"][2], label="PMMA")

# ax.set_yscale('log')
ax.set_xscale('log')

ax.set_xlabel("Photonenenergie / MeV")
ax.set_ylabel(r"Verhältnis $(\frac{\mu_{en}}{\rho})_{Detektor}$  /  $(\frac{\mu_{en}}{\rho}_{Gewebe})$")
ax.set_title("Proportionalitätsfaktor zwischen Detektor- und Gewebedosis")

ax.legend()
plt.show()
