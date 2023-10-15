import pandas as pd
import matplotlib.pyplot as plt
import numpy

calib_data = []
calib_path = "../../../OneDrive/Uni/Bachelorarbeit/data/sev/ej260/sev_ej260_na22_hist_good.txt"
sample_data = []
sample_path = "../../../OneDrive/Uni/Bachelorarbeit/data/sev/ppo5/sev_ppo5_bcg2s067_na22_hist_good.txt"

d = pd.read_csv(calib_path, skiprows=5, sep=";", usecols=[0,1])
calib_data = d.to_numpy().swapaxes(0, 1)

d = pd.read_csv(sample_path, skiprows=5, sep=";", usecols=[0,1])
sample_data = d.to_numpy().swapaxes(0, 1)


def plot_calib_data(channels, counts):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(channels, counts, label="calibration data")
    ax.legend()

    plt.show()

# plot_calib_data(*calib_data)

def energy_scaling_na22(c1, c2, channels, counts, e1=511, e2=1050):
    f = (c2 - c1) / (e2 - e1)

    energy = channels * f

    return energy

calib_energy = energy_scaling_na22(690, 1530, *calib_data)

# plot_calib_data(*sample_data)

sample_energy = energy_scaling_na22(295, 770, *sample_data)

def shift_spectrum(energy, counts, shift):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(energy + (511-shift), counts, label="calibration data")
    ax.legend()

    plt.show()

shift_spectrum(calib_energy, calib_data[1], 1081)
