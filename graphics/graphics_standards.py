import matplotlib.pyplot as plt
from control import get_inst
import locale
import numpy as np
import matplotlib as mpl

"""
Worauf zu achten ist:
 - Ticks innen 
 - Ticks auf allen vier Seiten
 - Gitter in grau mit Stärke 1
 - Linien mit Stärke 1 und Legende, wenn Multiplot
 - Kommas und Punkte in Achsenbeschriftung
 - Histogramme aus DAQ sind nicht richtig gebinnt, verschiebe um die Hälfte und füge einen hinzu

"""

mpl.use('Qt5Agg')

locale.setlocale(locale.LC_ALL, "")

c = get_inst("Z:\Studenten\Baier\Messungen")
file_name = c.search_in_dir("data/sev", identifiers=["ej200", "hist"])[0]
data = c.c_data.auto_read("sev", c.c_file.get_datafile_path(file_name), bin_ret=True)

fig = plt.figure()
ax = fig.add_subplot()

ax.grid(visible=True, color="#87878790", zorder=-1, lw=1)

bin_size = data[0][1] - data[0][0]
ax.stairs(*data, zorder=100, label="EJ200")

ax.set_xbound([np.min(data[0]), np.max(data[0])])
ax.set_xbound([0, 1250])
ax.set_ybound([0, None])

ax.set_xlabel(r"Energie / keV")
ax.set_ylabel(r"gezählte Ereignisse in 15 min")
ax.set_title("Irgendeine Messung von sonstwas")

ax.set_yscale("linear")

ax.tick_params(direction="in", top=True, right=True)
ax.ticklabel_format(style="sci", useMathText=False, useLocale=True)

plt.legend()
plt.savefig("test.png", dpi=400)
plt.show()








