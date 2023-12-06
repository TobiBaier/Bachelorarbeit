import numpy as np
from numpy.polynomial import Polynomial
import matplotlib.pyplot as plt
import json
import re
import matplotlib as mpl

def plot_fit(peaks, fit, linear_cutoff):
    for ch, kanal in enumerate(fit):
        fig, plot = plt.subplots(1,1)

        x_max = 0
        y_max = 0

        colors = {
            "Na": "blue",
            "Ba": "green",
            "Am": "purple",
            "Cm": "orange"
        }

        for isotop in peaks[kanal]:
            if len(peaks[kanal][isotop]["Energie"]) != 0:
                x_max = max(x_max, np.max(peaks[kanal][isotop]["Kanal"]))
                y_max = max(y_max, np.max(peaks[kanal][isotop]["Energie"]))
                m = re.search(r"(\d{1,3})([A-Z][a-z]{0,2})", isotop)
                label = "$^{" + m.group(1) + "}$" + m.group(2)
                plot.errorbar(peaks[kanal][isotop]["Kanal"], peaks[kanal][isotop]["Energie"],
                              xerr=peaks[kanal][isotop]["Breite"], label=label, fmt="o", color=colors[m.group(2)])

        x = np.linspace(0, x_max * 1.1, 1000)
        for i, p in enumerate(fit[kanal]):
            tangente = Polynomial(
                [p(linear_cutoff[ch]) - p.deriv()(linear_cutoff[ch]) * linear_cutoff[ch], p.deriv()(linear_cutoff[ch])])
            energy = p(x)  # keV
            ind = np.where(x < linear_cutoff[ch])
            energy[ind] = tangente(x[ind])

            plt.plot(x, energy, marker="", linestyle="solid", label=f"Polynom {p.degree()}. grades", color="red")
            plt.axvline(linear_cutoff[ch], color="black")

        # plot.set_title(f"Kalibrierfunktion ${kanal}$")
        plot.set_xlabel("Pulsintegral / Kanal")
        plot.set_ylabel("Pulsenergie / keV")

        plot.tick_params(direction="in", top=True, right=True)
        plot.ticklabel_format(style="sci", useMathText=False, useLocale=True)

        plot.grid(visible=True, color="#87878790", zorder=-1, lw=1)

        plot.set_xlim(0, x_max * 1.1)
        plot.set_ylim(0, y_max * 1.1)
        # plot.grid()
        plot.legend()

        kanal = kanal.replace("^*", "").replace("'", "")
        plt.savefig("C:/Users/baier\OneDrive/Uni\Bachelorarbeit_2\latex\images/ecalib_ebis_high.pdf")
        break
    # plt.show()

def print_fit(peaks, fit, linear_cutoff):
    f = open("Energiekalibrierung.txt", "w")

    def print_save(line, end="\n"):
        print(line, end=end)
        f.write(f"{line}{end}")

    for kanal in peaks:
        print_save(f"\n\n{kanal}")
        print_save("  Peaks:")
        for isotop in peaks[kanal]:
            if len(peaks[kanal][isotop]["Energie"]) != 0:
                print_save(f"    {isotop}")
                for i in range(len(peaks[kanal][isotop]["Energie"])):
                    fehler = []
                    for j in range(len(fit[kanal])):
                        energie_fit = fit[kanal][j](peaks[kanal][isotop]['Kanal'][i])
                        fehler.append((energie_fit - peaks[kanal][isotop]['Energie'][i]) / peaks[kanal][isotop]['Energie'][i])

                    print_save(f"      Kanal {peaks[kanal][isotop]['Kanal'][i]:5}   {peaks[kanal][isotop]['Energie'][i]:4} keV  Breite: {peaks[kanal][isotop]['Breite'][i]:4}", end="")
                    print_save(("{:10.1%}" * len(fehler)).format(*fehler))

        print_save("  Fit:")
        for i, p in enumerate(fit[kanal]):
            print_save(f"    E(x) = {p.convert()}, Unterhalb von Kanal {linear_cutoff} Linear fortgesetzt.".replace("\n", " "))

    f.close()

def fit_line(peaks, linear_cutoff):
    fit = dict()
    p = dict()

    for i, ch in enumerate(peaks):
        cutoff = linear_cutoff[i]
        fit[ch] = list()
        p[ch] = list()

        kanal = []
        energie = []
        breite = []

        for isotop in peaks[ch]:
            energie.extend(peaks[ch][isotop]["Energie"])
            kanal.extend(peaks[ch][isotop]["Kanal"])
            breite.extend(peaks[ch][isotop]["Breite"])

        energie = np.array(energie, dtype=np.int64)
        kanal = np.array(kanal, dtype=np.int64)
        breite = np.array(breite, dtype=np.int64)

        lin = np.where(kanal < cutoff)
        quad = np.where(kanal >= cutoff)

        energie_lin = energie[lin]
        kanal_lin = kanal[lin]
        breite_lin = breite[lin]

        energie = energie[quad]
        kanal = kanal[quad]
        breite = breite[quad]

        tangente = Polynomial.fit(kanal_lin, energie_lin, 1, w=1/breite_lin, domain=[-1, 1], window=[-1, 1])

        const_t = tangente.coef[0]
        lin_t = tangente.coef[1]

        quad = Polynomial.fit(kanal - cutoff, energie - tangente(kanal), [2], w=1/breite, domain=[-1, 1], window=[-1, 1]).coef[2]

        lin = -2 * cutoff * quad
        const = -1 * (lin * cutoff + quad * cutoff**2)

        print(repr(tangente))

        fit[ch].append(Polynomial([const + const_t, lin + lin_t, quad]))

    return fit


def comptonkante(full_energy):
    epsilon = full_energy / 510.998950
    kante = 2 * epsilon / (1 + 2 * epsilon) * full_energy
    return kante


def reverse_comptonkante(kante):
    a = kante / 510.998950
    epsilon = a / 2 + np.sqrt(a**2/4+a/2)
    E_gamma = (1 + 2 * epsilon) / (2 * epsilon) * kante
    return E_gamma


def load_peaks(file):
    data = json.load(open(file, "r"))
    peaks = dict()

    for channel in data:
        peaks[channel] = dict()
        for isotop in data[channel]:
            peaks[channel][isotop] = {
                "Typ": [],
                "Energie": [],
                "Kanal": [],
                "Breite": []
                }

            for peak in data[channel][isotop]:
                if peak["Kanal"] is not None:
                    peaks[channel][isotop]["Typ"    ].append(peak["Typ"])
                    peaks[channel][isotop]["Energie"].append(peak["Energie"])
                    peaks[channel][isotop]["Kanal"  ].append(peak["Kanal"])
                    peaks[channel][isotop]["Breite" ].append(peak["Breite"])
    return peaks

if __name__ == "__main__":
    peaks = load_peaks("Peaks.json")
    linear_cutoff = [300, 300]
    fit = fit_line(peaks, linear_cutoff)
    print_fit(peaks, fit, linear_cutoff)
    plot_fit(peaks, fit, linear_cutoff)
