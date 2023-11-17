import matplotlib.pyplot as plt
from control import get_inst
import locale
import numpy as np
import matplotlib as mpl
import matplotlib.ticker as ticker
mpl.use('Qt5Agg')

locale.setlocale(locale.LC_ALL, "")

c = get_inst("Z:\Studenten\Baier\Messungen")

fig = plt.figure()
ax = fig.add_subplot(111)
miax = ax.twinx()

pu_spec = c.search_in_dir("data/spec/pu", identifiers=["good"])[0]
pu_spec_data = c.c_data.auto_read("spec", c.c_file.get_datafile_path(pu_spec))
a = ax.plot(*pu_spec_data, c="xkcd:black", label="Emissionsspektrum Polyurethan")

pu_uvvis = c.search_in_dir("data/uv-vis/pu", identifiers=["good", "fast"])[0]
pu_uvvis_data = c.c_data.auto_read("uv-vis", c.c_file.get_datafile_path(pu_uvvis))
b = miax.plot(*pu_uvvis_data, c="xkcd:blue", label="Transmissionsspektrum Polyurethan")

ax.set_xlabel(r"$\lambda$/nm")
ax.set_xbound([250, 750])
ax.tick_params(axis="both", labelcolor="black", direction="in", top=True)
ax.ticklabel_format(axis="y", useLocale=True)
ax.set_ylabel("gezaehlte Ereignisse", color="black")
ax.set_ybound([0, None])

miax.tick_params(axis="y", labelcolor="black", direction="in", top=True)
miax.set_ylabel("Transmission / %", color="black")
miax.set_ybound([0, None])

# miax.grid(visible=True, color="#87878790", zorder=-1, lw=1)
ax.grid(visible=True, color="#87878790", zorder=-1, lw=1)
labels = ["Emissionsspektrum Polyurethan", "Transmissionsspektrum Polyurethan"]
ax.legend(a+b, labels, loc="center right")

# plt.savefig("Z:/Studenten/Baier/Latex/images/pu_spec_uvvis.pdf")
# plt.show()


name = c.search_in_dir("data/sev/pu", identifiers=["na22", "hist"])[0]
print(name)
c.auto_plot_data(name, auto_title=False,
                 ax_config={
                     "save": True,
                     "path": "Z:/Studenten/Baier/Latex/images/pu_sev.pdf",
                     "dpi": None,
                     "draw": True,
                     "yscale": "log",
                     "xlabel": "Kanäle",
                     "xbounds": [0, 750]
                 }
)

name = c.search_in_dir("data/spec/pu", identifiers=["good", "hist"])[0]
print(name)
c.auto_plot_data(name, auto_title=False,
                 ax_config={
                     "save": True,
                     "path": "Z:/Studenten/Baier/Latex/images/pu_sev.pdf",
                     "dpi": None,
                     "draw": True,
                     "yscale": "log",
                     "xlabel": "Kanäle",
                     "xbounds": [0, 750]
                 }
)
