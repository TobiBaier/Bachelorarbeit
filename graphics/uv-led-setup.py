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
mirror_ax = ax.twinx()

p = []

filter = c.search_in_dir("data/spec/uv-led", identifiers=["_filter_good"])[0]
filter_data = c.c_data.auto_read("spec", c.c_file.get_datafile_path(filter))
#filter_data[1] = filter_data[1]/np.max(filter_data[1]) - 0.009
#filter_data[1] = filter_data[1]/np.max(filter_data[1])
a = ax.plot(*filter_data, c="xkcd:deep purple", label="UV-LED mit Pass-Filter")

nofilter = c.search_in_dir("data/spec/uv-led", identifiers=["nofilter"])[0]
nofilter_data = c.c_data.auto_read("spec", c.c_file.get_datafile_path(nofilter))
#nofilter_data[1] = nofilter_data[1]/np.max(nofilter_data[1])
b = ax.plot(*nofilter_data, c="xkcd:neon purple", label="UV-LED ohne Pass-Filter")

transfilter = c.search_in_dir("data/uv-vis/uv-filter")[0]
transfilter_data = c.c_data.auto_read("uv-vis", c.c_file.get_datafile_path(transfilter))
transfilter_data[1] = transfilter_data[1]/np.max(transfilter_data[1]) * 100
c = mirror_ax.plot(*transfilter_data, c="xkcd:electric blue", label="Transmissionsspektrum des Pass-Filters", ls="--")

labels = ["UV-LED mit Pass-Filter", "UV-LED ohne Pass-Filter", "Transmissionsspektrum des Pass-Filters"]

ax.legend(a+b+c, labels)


def add_subplot_axes(ax,rect,facecolor='w'):
    fig = plt.gcf()
    box = ax.get_position()
    width = box.width
    height = box.height
    inax_position  = ax.transAxes.transform(rect[0:2])
    transFigure = fig.transFigure.inverted()
    infig_position = transFigure.transform(inax_position)
    x = infig_position[0]
    y = infig_position[1]
    width *= rect[2]
    height *= rect[3]  # <= Typo was here
    subax = fig.add_axes([x,y,width,height],facecolor=facecolor)  # matplotlib 2.0+
    # subax = fig.add_axes([x,y,width,height],axisbg=axisbg)
    x_labelsize = subax.get_xticklabels()[0].get_size()
    y_labelsize = subax.get_yticklabels()[0].get_size()
    x_labelsize *= rect[2]**0.5
    y_labelsize *= rect[3]**0.5
    subax.xaxis.set_tick_params(labelsize=x_labelsize)
    subax.yaxis.set_tick_params(labelsize=y_labelsize)
    return subax

rect = [0.4,0.25,0.4,0.45]
ax2 = add_subplot_axes(ax, rect)
#print(len(filter_data[0]))
ax2.plot(filter_data[0][30:55], filter_data[1][30:55], c="xkcd:deep purple")
ax2.plot(nofilter_data[0][30:55], nofilter_data[1][30:55], c="xkcd:neon purple")
"""ax3 = ax2.twinx()
ax3.plot(transfilter_data[0][57:81], transfilter_data[1][57:81], "--", c="xkcd:electric blue")
ax3.set_ybound([0, None])"""
ax2.set_xbound([400, 520])
ax2.set_ybound([0, None])
ax2.grid(visible=True, color="#87878790", zorder=-1, lw=1)
ax2.tick_params(axis="both", labelsize=10)

ax.plot([408,400], [0.26,0], "--", color="gray")
ax.plot([570,520], [0.26,0], "--", color="gray")

ax.set_xlabel(r"$\lambda$/nm")
ax.set_xbound([250, 650])
ax.tick_params(axis="both", labelcolor="black", direction="in", top=True)
ax.ticklabel_format(axis="y", useLocale=True)
ax.set_ylabel("gezaehlte Ereignisse", color="black")
ax.set_ybound([0, None])

def formatter(y, pos):
    if y == 0:
        return 0
    # Find the number of decimal places required
    decimalplaces = int(np.log10(y))  # =0 for numbers >=1
    # Insert that number into a format string
    a = np.int_(np.floor(y/(10**decimalplaces)))
    print(np.round(y/(10**decimalplaces), 1))
    b = np.int_((np.round(y/(10**decimalplaces), 1) - np.floor(y/(10**decimalplaces))) * 10)
    formatstring = r'{},{}$\cdot 10^{{{}}}$'.format(a, b, decimalplaces)
    # Return the formatted tick label
    return formatstring


ax.yaxis.set_major_formatter(ticker.FuncFormatter(formatter))

mirror_ax.tick_params(axis="y", labelcolor="xkcd:electric blue", direction="in", top=True)
mirror_ax.set_ylabel("Transmission / %", color="xkcd:electric blue")
mirror_ax.set_ybound([0, None])

ax.grid(visible=True, color="#87878790", zorder=-1, lw=1)

plt.savefig("Z:/Studenten/Baier/Latex/images/uv-led_filter_comparison.pdf")


