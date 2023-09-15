import csv
import numpy as np
import matplotlib.pyplot as plt


def load_values():
    fn = input("Please enter a filename: ")
    # fn = "data/uvlamp2.csv"
    draw_arr = []
    with open(fn, "r") as data:
        reader = csv.reader(data, delimiter=";")
        for i in reader:
            draw_arr.append(i)

    return np.array(draw_arr)


draw_arr = load_values()
draw_arr = np.swapaxes(draw_arr, 0, 1)
draw_arr = draw_arr.astype(float)

wl = draw_arr[0]
counts = draw_arr[1]

fig = plt.figure()
ax = fig.add_subplot(111)


ax.plot(wl, counts, "-+", c="blue", mec="black", ms=6)

ax.set_xlabel(r"$\lambda$/nm")
ax.set_ylabel("counts")

ax.grid()

# plt.savefig("data/image.png", dpi=400)
plt.show()



