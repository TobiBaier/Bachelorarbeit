import matplotlib.pyplot as plt
from utility.dataloader import DataLoader
from utility.diagrammaker import DiagramMaker
import matplotlib.ticker
import numpy as np

d = DataLoader()

data = d.data_from_txt("tissue_cross_section2.txt", sep=" ")

fig = plt.figure()
ax = fig.add_subplot(111)

labels = [
    "kohärent",
    "inkohärent",
    "Photoeffekt",
    "Paarerzeugung (Kern)",
    "Paarerzeugung (Hülle)",
    "gesamt"
]

ax.plot(data[0], data[1], lw=1, label="kohärent")
ax.plot(data[0], data[2], lw=1, label="inkohärent")
ax.plot(data[0], data[3], lw=1, label="Photoeffekt")
ax.plot(data[0][40:], data[4][40:], lw=1, label="Paarerzeugung (Kern)")
ax.plot(data[0][43:], data[5][43:], lw=1, label="Paarerzeugung (Hülle)")
ax.plot(data[0], data[6], lw=2.5, c="black", label="gesamt")


ax.set_xlabel(r"Photonenenergie / MeV")
ax.set_ylabel(r"$(\mu / \rho)$ / cm$^2$ g$^{-1}$")
ax.set_xscale("log")
ax.set_yscale("log")

"""locmaj = matplotlib.ticker.LogLocator(base=10,numticks=12)
ax.xaxis.set_major_locator(locmaj)
# ax.yaxis.set_major_locator(locmaj)

locmin = matplotlib.ticker.LogLocator(base=10.0,subs=(0.2,0.4,0.6,0.8),numticks=12)
ax.xaxis.set_minor_locator(locmin)
ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())

# ax.yaxis.set_minor_locator(locmin)
# ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())

ax.tick_params(which="both", direction="in", top=True, right=True, )
# ax.ticklabel_format(style="sci", useMathText=False, useLocale=True)"""

locmajx = matplotlib.ticker.LogLocator(base=10,numticks=100)
locminx = matplotlib.ticker.LogLocator(base=10,subs=np.arange(2, 10) * .1,numticks=100) # subs=(0.2,0.4,0.6,0.8)
locmajy = matplotlib.ticker.LogLocator(base=10,numticks=8)
locminy = matplotlib.ticker.LogLocator(base=10,subs=np.arange(2, 10) * .1,numticks=24) # subs=(0.2,0.4,0.6,0.8)

ax.yaxis.set_major_locator(locmajy)
ax.yaxis.set_minor_locator(locminy)
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())

ax.xaxis.set_major_locator(locmajx)
ax.xaxis.set_minor_locator(locminx)
ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())

ax.tick_params(which="both", direction="in", top=True, right=True, )
# ax.ticklabel_format(style="sci", useMathText=False, useLocale=True)

ax.set_xbound([np.min(data[0]), np.max(data[0])])

ax.legend()
ax.grid()

plt.savefig("Z:\Studenten/Baier/Latex/images/tissue_cross_section.pdf")
plt.show()