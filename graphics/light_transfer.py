import matplotlib.pyplot as plt
from control import get_inst

c = get_inst("C:/Users/baier/OneDrive/Uni/Bachelorarbeit")

names = c.search_in_dir("data/spec",
                        identifiers=["sr90", "movingavg"],
                        or_identifiers=["eppo1", "ebis110"],
                        not_identifiers=["run24"])
colors = ["xkcd:primary blue", "xkcd:soft purple"]
labels = ["PPO mit POPOP", "PPO"]
ax = c.multi_plot(names, labels, path="", show_final_plot=False, save_final_plot=False,
             ax_config={
                "ybounds": [85, 1200],
                "xbounds": [310, 640]
             },
             plot_kwargs={
                 "color": colors,
                 "lw": 2,
             }
             )


ax.arrow(400, 1000, 60, 0, width=10, head_width=30, head_length=20, color="red", length_includes_head=True)
ax.vlines([400, 460], 0, 1500, colors="red", linestyles="dashed")
ax.text(381, 1080, "Stokes-Shift", color="black", zorder=1000, fontweight="bold")


ax.set_ybound([85, 1200])
ax.set_xbound([310, 640])
# ax.set_title("test")



# plt.show()
plt.savefig("C:/Users/baier/OneDrive/Uni/Bachelorarbeit_2/latex/images/light_transfer.pdf")
