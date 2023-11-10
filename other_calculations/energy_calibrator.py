import numpy as np
from control import get_inst
import matplotlib as mpl
import matplotlib.pyplot as plt


c = get_inst("Z:\Studenten\Baier\Messungen")

def Energy_Calib(ch):
    E = np.zeros((len(ch)))
    for i, channel in enumerate(ch):
        if channel < 800:
            E[i] = 7.61706783 + 0.0809628 * channel
        else:
            E[i] = 67.17851564179762 - 0.0679408186449754*channel**1 + 9.306476220015559e-05*channel**2


    return E


file_name = c.search_in_dir("data/sev/ebis110", identifiers=["cm244", "100s", "hist", "hight", "1000K"])[0]
data = c.c_data.auto_read("sev", c.c_file.get_datafile_path(file_name), bin_ret=True)
calib_data = [data[0], Energy_Calib(data[1])]

fig = plt.figure()
ax = fig.add_subplot(111)

ax.stairs(*calib_data, zorder=1000)

ax.set_xbound([0, 400])
ax.set_xlabel("Energie / keV")
ax.set_ylabel("gezählte Ereignisse in 15 min")
ax.set_title(r"$^{241}$Am gemessen mit Epoxidharzszintillator (ohne PVC)")

ax.grid(visible=True, color="#87878790", zorder=-1, lw=1)
ax.tick_params(direction="in", top=True, right=True)
ax.ticklabel_format(style="sci", useMathText=False, useLocale=True)
ax.set_yscale("log")

plt.show()






