import os
import json
import matplotlib.pyplot as plt
import numpy as np

p_data ={}
for path in os.scandir("../energy_calib"):
    if os.path.isdir(path):
        for sub_path in os.scandir("../energy_calib/" + path.name):
            if "Peaks.json" in sub_path.name:
                p_data[path.name] = json.load(open("../energy_calib/"+path.name+"/"+sub_path.name))

l_data = json.load(open("../energy_calib/calibration.json"))




def plot_calib_curve(point_data, line_data):

    colors = {
        "22Na": "blue",
        "133Ba": "green",
        "241Am": "red",
        "244Cm": "orange"
    }
    labels = {
        "22Na": "Natrium-22",
        "133Ba": "Barium-133",
        "241Am": "Americium-241",
        "244Cm": "Curium-244"
    }

    fig = plt.figure()
    ax = fig.add_subplot(111)

    h10_data = point_data["H^*(10)"]
    for key in h10_data:

        energies = []
        channels = []
        for entry in h10_data[key]:
            if entry["Kanal"] is not None:
                energies.append(entry["Energie"])
                channels.append(entry["Kanal"])

        if energies != []:
            ax.plot(channels, energies, "o", ms=3, color=colors[key], label=labels[key])

    lin_poly = np.polynomial.Polynomial(line_data["linear"])
    quad_poly = np.polynomial.Polynomial(line_data["quadratic"])
    switch = line_data["switch"]

    x = np.linspace(0, switch, 10)
    ax.plot(x, lin_poly(x), label="Kalibrierkurve", color="black")
    x = np.linspace(switch, np.max(h10_data["22Na"][3]["Kanal"]), 1000)
    ax.plot(x, quad_poly(x), color="black")



plot_calib_curve(p_data["ebis110_lowtemp"], l_data["ebis110"]["lowtemp"])
plt.legend()
plt.show()











