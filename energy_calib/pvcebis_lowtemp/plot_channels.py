import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import scipy.signal as signal

def prepare_listmode(file, xrange=[0,64000]):
    for ch in [0, 1]:
        outfile = file.replace(".txt", f"_channel_{ch}.npy")
        if Path(outfile).exists(): continue
        print(outfile)

        if "part0" in file:
            files = [Path(file.replace("part0", f"part{i}")) for i in range(9)]
            files = [str(file) for file in files if file.exists()]
        else:
            files = [file]

        bins = np.arange(xrange[0], xrange[1]+1, 1)
        all_hist = np.zeros(bins.shape[0]-1)

        for f in files:
            print(f)
            channel, time, energy, risetime = np.loadtxt(f, skiprows=4, unpack = True, delimiter = ";")
            ind = np.where((channel == ch)) #& (energy > 650)) #& (energy < 30000))
            #if energy[ind] >= 1000:
            hist, edges = np.histogram(energy[ind], bins = bins, density=False)
            all_hist += hist

        data = np.array([bins[:-1], all_hist])

        np.savetxt(outfile.replace(".npy", ".txt"), data.transpose(), header = "left_edge count\n 0 0", comments="")
        np.save(outfile, data)

def plot_histogram(file, binwidth = 1, xrange = [0, 64000], plot=None, time = None):
    prepare_listmode(file)
    if plot is None:
        fig, plots = plt.subplots(2, 1, sharex=True, figsize=(10, 6))
    else:
        fig = plot[0]
        plots = plot[1]

    for ch in [0,1]:
        f = str(file).replace(".txt", f"_channel_{ch}.npy")
        data = np.load(f)
        bins = data[0,:]
        hist = data[1,:]
        new_bins = np.arange(xrange[0], xrange[1] + binwidth, binwidth)
        if time is not None: hist = hist / time
        plots[ch].hist(bins, weights=hist, bins=new_bins, histtype="step", label=str(file))
    
    plots[1].set_title("$H'(0.07)$")
    plots[0].set_title("$H^*(10)$")
    
    if plot is None:
        fig.suptitle(str(file))
    else:
        plots[0].legend()
        plots[1].legend()


    if binwidth == 1:
        plots[0].set_ylabel("Ereignissanzahl")
        plots[1].set_ylabel("Ereignissanzahl")
    else:
        plots[0].set_ylabel(f"Ereignissanzahl in {binwidth} Kanälen")
        plots[1].set_ylabel(f"Ereignissanzahl in {binwidth} Kanälen")

    plots[0].set_yscale("log")
    plots[1].set_yscale("log")

    plots[0].grid()
    plots[1].grid()
    plots[1].set_xlabel(f"Pulsintegral / Kanal")

    plots[0].set_xlim([0, 30000])

    if plot is None:
        plt.savefig(f"{str(file)}_hist.pdf")

if __name__ == "__main__":
    plot = plt.subplots(2, 1, sharex=True)

    Export = False

    if Export:
        plot = None

    plot_histogram("../Spektren/sev_ej200_bng2s100_na22_530_15min_80kbins_hist_good.txt", binwidth = 100, plot=plot)


    if not Export:
        plt.show()
