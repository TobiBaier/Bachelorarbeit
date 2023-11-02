import matplotlib.pyplot as plt
from utility.dataloader import DataLoader
from utility.diagrammaker import DiagramMaker

d = DataLoader()

data = d.data_from_txt("tissue_cross_section.txt", sep=" ")

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


ax.legend()
ax.grid()



plt.savefig("C:/Users/baier/OneDrive/Uni/Bachelorarbeit_2/latex/images/tissue_cross_section.pdf")
# plt.show()