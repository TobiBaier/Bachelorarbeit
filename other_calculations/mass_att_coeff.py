import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re
from pprint import pprint
import locale
import matplotlib.ticker as ticker
locale.setlocale(locale.LC_NUMERIC, "de_DE")
# import matplotlib as mpl
# mpl.use("Qt5Agg")

"""
NOTIZ ZM ADDITIONSSCHEMA:

Even assuming Bragg additivity for the stopping power (that now appears in the denominator of the 
integral), simple additivity for μen/ρ or - as suggested by Attix (1984) 
- for g is formally incorrect. When the numerical values of g are relatively small, 
the errors in μen/ρ incurred by using simple additivity schemes are usually small, a consequence 
partially mitigating the use additivity, particularly for photon energies below 20 MeV. 
However, additivity has not been used in the present work. 
"""

paths = os.scandir("C:/Users/baier/OneDrive/Uni/Bachelorarbeit_2/mass_att_coeff")
# paths = os.scandir("Z:\Studenten\Baier\mass_att_coeffs")
"""
Du dummer Idiot, trag einfach die notwendigen Energien bei NIST ein und hol dir alles fehlende *facepalm*
https://physics.nist.gov/PhysRefData/Xcom/html/xcom1.html
"""

def get_data():
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

    return daten

daten = get_data()

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


daten = consistency_check(daten)

fig = plt.figure()
ax = fig.add_subplot(111)

daten["pu"] = (0.627922665 * daten["carbon"][2] +
                     0.090842816 * daten["hydrogen"][2] +
                     0.0505004 * daten["nitrogen"][2] +
                     0.230734119 * daten["oxygen"][2])
daten["epoxy"] = (0.8438475 * daten["carbon"][2] +
                        0.0758647 * daten["hydrogen"][2] +
                        0.0802878 * daten["oxygen"][2])
daten["pmma"] = (0.59985585 * daten["carbon"][2] +
                       0.08053401 * daten["hydrogen"][2] +
                       0.31961015 * daten["oxygen"][2])
daten["salt"] = (0.3933723 * daten["sodium"][2] +
                 0.6066277 * daten["chlorine"][2])

b = mass_fractions([22.989769, 10.811, 15.999], [2, 4, 7])
daten["borax"] = b[0] * daten["sodium"][2] + b[1] * daten["boron"][2] + b[2] * daten["oxygen"][2]

c = mass_fractions([40.078, 12.011, 15.999], [1,1,3])
daten["caco3"] = c[0] * daten["calcium"][2] + c[1] * daten["carbon"][2] + c[2] * daten["oxygen"][2]

p = mass_fractions([12.011, 1.00784, 35.453], [2, 3, 1])
daten["pvc"] = p[0] * daten["carbon"][2] + p[1] * daten["hydrogen"][2] + p[2] * daten["chlorine"][2]

pf = mass_fractions([12.011, 18.998403], [8, 18])
daten["PF5080"] = pf[0] * daten["carbon"][2] + pf[1] * daten["flourine"][2]

g = mass_fractions([12.011, 1.00784, 15.999], [6, 12, 6])
daten["glucose"] = g[0] * daten["carbon"][2] + g[1] * daten["hydrogen"][2] + g[2] * daten["oxygen"][2]

"""w = mass_fractions([1.00784, 15.999], [2, 1])
daten["water"] = w[0] * daten["hydrogen"][2] + w[1] * daten["oxygen"][2]"""

si = mass_fractions([15.999, 28.0855], [2, 1])
daten["sio2"] = si[0] * daten["oxygen"][2] + si[1] * daten["silicon"][2]

chf = mass_fractions([12.011, 1.00784, 35.453], [1, 1, 3])
daten["chloroform"] = chf[0] * daten["carbon"][2] + chf[1] * daten["hydrogen"][2] + chf[2] * daten["chlorine"][2]

epoa = mass_fractions([12.011, 1.00784, 15.999], [21, 24, 4])
daten["epoa"] = epoa[0] * daten["carbon"][2] + epoa[1] * daten["hydrogen"][2] + epoa[2] * daten["oxygen"][2]

epob = mass_fractions([12.011, 1.00784, 15.999, 14.0067], [6, 16, 1, 2])
daten["epob"] = epob[0] * daten["carbon"][2] + epob[1] * daten["hydrogen"][2] + epob[2] * daten["oxygen"][2] + epob[3] * daten["nitrogen"][2]

daten["epoxy"] = daten["epoa"] * 100/135 + daten["epob"] * 35/135

ppo = mass_fractions([12.011, 1.00784, 14.0067, 15.999], [15, 11, 1, 1])
daten["ppo"] = ppo[0] * daten["carbon"][2] + ppo[1] * daten["hydrogen"][2] + ppo[2] * daten["nitrogen"][2] + ppo[3] * daten["oxygen"][2]

bis = ppo = mass_fractions([12.011, 1.00784], [24, 22])
daten["bis"] = bis[0] * daten["carbon"][2] + bis[1] * daten["hydrogen"][2]

daten["doped_epoxy"] = (15/15.165) * daten["epoxy"] + (0.15/15.165) * daten["ppo"] + (0.015/15.165) * daten["bis"]

baso4 = mass_fractions([55.845, 32.065, 15.999], [1, 1, 4])
daten["baso4"] = baso4[0] * daten["iron"][2] + baso4[1] * daten["sulfur"][2] + baso4[2] * daten["oxygen"][2]

cacl2 = mass_fractions([40.078, 35.453], [1, 2])
daten["cacl2"] = cacl2[0] * daten["calcium"][2] + cacl2[1] * daten["chlorine"][2] # + cacl2[2] * daten["oxygen"][2]

fecl2 = mass_fractions([55.845, 35.453], [1, 2])
daten["fecl2"] = fecl2[0] * daten["iron"][2] + fecl2[1] * daten["chlorine"][2] # + cacl2[2] * daten["oxygen"][2]

crcl2 = mass_fractions([51.9961, 35.453], [1, 2])
daten["crcl2"] = crcl2[0] * daten["chromium"][2] + crcl2[1] * daten["chlorine"][2] # + cacl2[2] * daten["oxygen"][2]

fecl3 = mass_fractions([55.845, 35.453], [1, 3])
daten["fecl3"] = fecl2[0] * daten["iron"][2] + fecl2[1] * daten["chlorine"][2] # + cacl2[2] * daten["oxygen"][2]

# feso4 = mass_fractions([51.9961, 32.065, 15.999], [1, 2])


# ax.plot(daten["tissue"][0], daten["tissue"][2]/daten["tissue"][2], color="xkcd:red")
# ax.plot(daten["tissue"][0], daten["pu"]/daten["tissue"][2], label="Polyurethanharz", color="xkcd:purple")
# ax.plot(daten["tissue"][0], daten["epoxy"]/daten["tissue"][2], label="Epoxidharz", color="xkcd:primary blue")
# ax.plot(daten["tissue"][0], (0.943*daten["epoxy"]+0.057*daten["pvc"])/daten["tissue"][2], label="Epoxidharz mit 5,7% PVC", color="xkcd:baby blue")
# ax.plot(daten["tissue"][0], (0.98*daten["epoxy"]+0.02*daten["salt"])/daten["tissue"][2], label="Epoxidharz mit 2% NaCl", color="xkcd:baby blue")
# ax.plot(daten["tissue"][0], daten["doped_epoxy"]/daten["tissue"][2], label="doped Epoxy")
# ax.plot(daten["tissue"][0], daten["polysterene"][2]/daten["tissue"][2], label="Polystyrol (PS)", color="xkcd:dark green")
# ax.plot(daten["tissue"][0], daten["vinyltoulene"][2]/daten["tissue"][2], label="Polyvinyltoluol (PVT)", color="xkcd:light green")
# ax.plot(daten["tissue"][0], daten["pmma"]/daten["tissue"][2], label="PMMA")
# ax.plot(daten["tissue"][0], (0.7*daten["epoxy"]+0.3*daten["pmma"])/daten["tissue"][2], label="pmma")
# ax.plot(daten["tissue"][0], (0.7*daten["epoxy"]+0.3*daten["borax"])/daten["tissue"][2], label="borax")
# ax.plot(daten["tissue"][0], (0.93*daten["epoxy"]+0.07*daten["caco3"])/daten["tissue"][2], label="mit 7% CaCO3")
# ax.plot(daten["tissue"][0], (0.995*daten["vinyltoulene"][2]+0.005*daten["lead"][2])/daten["tissue"][2], label="PVT mit 0,5% Blei", color="green")
# ax.plot(daten["tissue"][0], (0.935*daten["doped_epoxy"]+0.065*daten["pvc"])/daten["tissue"][2], label="mit 6.5% PVC (doped)")
# ax.plot(daten["tissue"][0], (0.92*daten["epoxy"]+0.08*daten["PF5080"])/daten["tissue"][2], label="PF5080")
# ax.plot(daten["tissue"][0], daten["water"][2]/daten["tissue"][2], label="Wasser", color="blue")
# ax.plot(daten["tissue"][0], (0.9*daten["epoxy"]+0.1*daten["sio2"])/daten["tissue"][2], label="mit 10% SiO2")
# ax.plot(daten["tissue"][0], (0.95*daten["epoxy"]+0.05*daten["chloroform"])/daten["tissue"][2], label="mit 3% Chloroform")
# ax.plot(daten["tissue"][0], daten["air"][2]/daten["tissue"][2], label="Luft", color="black")
ax.plot(daten["tissue"][0], (0.98*daten["epoxy"]+0.02*daten["baso4"])/daten["tissue"][2], label="Epoxidharz mit crcl2", color="xkcd:baby blue")

"""ax.plot(daten["tissue"][0], daten["epoxy"]/daten["tissue"][2], label="Epoxidharz", color="xkcd:primary blue")
ax.plot(daten["tissue"][0], (0.943*daten["epoxy"]+0.057*daten["pvc"])/daten["tissue"][2], label="Epoxidharz mit 5,7% PVC", color="xkcd:sea blue")
ax.plot(daten["tissue"][0], (0.98*daten["epoxy"]+0.02*daten["salt"])/daten["tissue"][2], label="Epoxidharz mit 2% NaCl", color="xkcd:baby blue")
ax.plot(daten["tissue"][0], daten["vinyltoulene"][2]/daten["tissue"][2], label="Polyvinyltoluol (PVT)", color="red")
ax.plot(daten["tissue"][0], (0.995*daten["vinyltoulene"][2]+0.005*daten["lead"][2])/daten["tissue"][2], label="PVT mit 0,5% Blei", color="green")
ax.plot([0.06, 0.06, 0.06, 0.06], [1.3, 0.963, 0.735, 0], "-_", color="black", ms=10)
ax.plot([0.023, 0.023, 0.023, .023], [1.044, 0.901, 0.507, 0], "-_", color="black", ms=10)
ax.text(0.062, 0.325, r"$^{241}$Am " + "\n(60keV)", fontweight="bold")
ax.text(0.02305, 0.325, r"$^{244}$Cm " + "\n(23keV)", fontweight="bold")
ax.text(0.062, 1.05, "1:1,35", fontweight="bold")
ax.text(0.062, 0.82, "1:0,87", fontweight="bold")"""


"""ax.plot(daten["tissue"][0], daten["pu"]/daten["tissue"][2], label="Polyurethanharz", color="xkcd:purple")
ax.plot(daten["tissue"][0], daten["epoxy"]/daten["tissue"][2], label="Epoxidharz", color="xkcd:primary blue")
ax.plot(daten["tissue"][0], (0.943*daten["epoxy"]+0.057*daten["pvc"])/daten["tissue"][2], label="Epoxidharz mit 5,7% PVC", color="xkcd:sea blue")
ax.plot(daten["tissue"][0], daten["vinyltoulene"][2]/daten["tissue"][2], label="Polyvinyltoluol (PVT)", color="red")
ax.plot(daten["tissue"][0], (0.995*daten["vinyltoulene"][2]+0.005*daten["lead"][2])/daten["tissue"][2], label="PVT mit 0,5% Blei", color="green")
ax.plot(daten["tissue"][0], daten["air"][2]/daten["tissue"][2], label="Luft", color="black")"""



"""ax.plot(daten["tissue"][0], daten["pu"]/daten["tissue"][2], label="Polyurethanharz", color="xkcd:purple")
ax.plot(daten["tissue"][0], daten["epoxy"]/daten["tissue"][2], label="Epoxidharz", color="xkcd:primary blue")
ax.plot(daten["tissue"][0], daten["polysterene"][2]/daten["tissue"][2], label="Polystyrol (PS)")
ax.plot(daten["tissue"][0], daten["vinyltoulene"][2]/daten["tissue"][2], label="Polyvinyltoluol (PVT)", color="red")
ax.plot(daten["tissue"][0], (0.995*daten["vinyltoulene"][2]+0.005*daten["lead"][2])/daten["tissue"][2], label="PVT mit 0,5% Blei", color="green")
ax.plot(daten["tissue"][0], daten["pmma"]/daten["tissue"][2], label="PMMA")
"""



"""ax.text(0.062, 0.70, "0,735")
ax.text(0.024, 1.005, "1,044")
ax.text(0.024, 0.865, "0,901")
ax.text(0.024, 0.46, "0,507")"""





ax.set_xlim([0.01, 10])
ax.set_ylim([0.31, 1.35])
ax.ticklabel_format(style="sci", useMathText=True, useLocale=True)
# ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:#.1n}'))
# ax.set_yscale('log')
ax.set_xscale('log')

ax.set_xlabel("Photonenenergie / MeV")
ax.set_ylabel(r"Verhältnis $(\frac{\mu_{en}}{\rho})_{Detektor}$  /  $(\frac{\mu_{en}}{\rho}_{Gewebe})$")
# ax.set_title("Proportionalitätsfaktor zwischen Detektor- und Gewebedosis")

ax.tick_params(which="both", direction="in", top=True, right=True)

ax.grid(visible=True, color="#87878790", zorder=-1, lw=1)

ax.legend(loc="lower right")
# plt.savefig("C:/Users/baier/OneDrive/Uni/Bachelorarbeit_2/Präsentation/images/intro5.svg")
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
