from control import get_inst
import re
from pprint import pprint

c = get_inst()

c.c_file.sort_to_dirs()
c.plot_dir("data/spec", identifiers=["ap1000"])
# c.plot_dir("data/uv-vis/ej260")
# c.plot_dir("data/spec/ppo1")

#names = c.search_in_dir("data/spec", identifiers=["uv"], or_identifiers=["led", "masked"])
#labels = c.extract_labels_from_path(names)
#pprint(names)
#c.multi_plot(names, labels, "zz_spec_combis/all_samples_norm.png", title="All samples so far", norm=True)

"""names = c.search_in_dir("data/spec", identifiers=["uv", "masked"])
labels = c.extract_labels_from_path(names)
uv_name = c.search_in_dir("data/spec/uv-led", identifiers=["uv"])

for name, label in zip(names, labels):
    a = [name]
    a.extend(uv_name)
    b = [label]
    b.append("uv-led")
    sample = c.c_file.get_inst_and_sample(name)[1]
    print(b)
    try:
        t = re.search(r"_b+[\w]+g[\w]+s+([0-9]{3})", name).group(0)
    except AttributeError:
        t = ""
    print("zz_spec_combis/" + sample + "_and_uv.png", sample + t + " irradiated by uv-led")
    c.multi_plot(a, b, "zz_spec_combis/" + sample + "_and_uv_normed.png", title=sample + t + " irradiated by uv-led", norm=True)
"""

#names = ["uv-vis_ppo5_bcg2s067_trans_fast_1", "spec_uv-led_4600mV", "spec_ppo5_bcg2s067_uv_4600mV_masked_5step"]
#names = ["uv-vis_ppo5_bcg2s067_trans_fast_1", "spec_ppo5_bcg2s067_uv_4600mV_masked_5step"]

"""
names = c.search_in_dir("data/spec", identifiers=["uv", "masked"], not_identifiers=["ej260"])
labels = c.extract_labels_from_path(names)
for name, label in zip(names, labels):
    sample = c.c_file.get_inst_and_sample(name)[1]
    t = re.search(r"_b+[\w]+g[\w]+s+([0-9]{3})", name).group(0)
    uv_name = c.search_in_dir("data/uv-vis", identifiers=[sample, "_good", "survey", t])

    a = [name]
    a.extend(uv_name)
    # a.append("spec_uv-led_4600mV")
    b = [label]
    b.append(label)
    # b.append("uv-led")

    #style = {
    #    "ls1": ["-", "--"]
    #}

    c.twin_x_scale_plot(a, b, "zz_spec_uv/" + sample + ".png", title=sample + t + " in spec and cary",)
"""

"""
names = c.search_in_dir("data/spec", identifiers=["uv_4600"], or_identifiers=["combi14", "combi92"])
names.append("spec_uv-led_4600mV")
labels = c.extract_labels_from_path(names)
c.multi_plot(names, labels, "zz_spec_combis/combi_samples.png", title="Combi Proben", lslist=2, norm=False)

"""
"""
names = c.search_in_dir("data/spec/ppo1", identifiers=["107mW"])
print(names)
labels = []
for name in names:
    labels.append(re.search(r"[\d]+mm", name).group(0))

title = "ppo1_bcg2s022 illuminated by uv-led at different distances (normed)"
c.multi_plot(names, labels, path="zz_spec_combis/ppo1_diff_distances_norm.png", title=title, norm=True)"""
"""
names = c.search_in_dir("data/spec", identifiers=["7mm", "17mW"])
labels = c.extract_labels_from_path(names)
print(names)
c.math_plot(names, labels, path="zz_spec_combis/uv-diff.png", title="Spektrum der UV-LED von ppo1-Messung abgezogen", ybounds=None)
"""
"""
names_spec = ["spec_ej260_sr_5step", "spec_ej260_uv_4600mV_masked_5step"]
labels_spec = ["EJ260 (Sr)", "EJ260 (UV)"]
titles_spec = ["Emissionsspektrum von EJ260 stimuliert mit Strontium", "Emissionsspektrum von EJ260 stimuliert mit UV-LED"]
paths_spec = ["zz_vortrag/ej260_spec_sr", "zz_vortrag/ej260_spec_uv"]

name_uvv = "uv-vis_ej260_trans_fast"

c.auto_plot_data(name_uvv, label=None, suptitle="Transmissionsspektrum von EJ260", path=c.c_file.prodata_path + "/" + "zz_vortrag/uv-vis_ej260",
                     xbounds=[200, 750])

for i in range(len(names_spec)):
    c.auto_plot_data(names_spec[i], label=None, suptitle=titles_spec[i], path=c.c_file.prodata_path + "/" + paths_spec[i],
                     xbounds=[300, 750])

    c.twin_x_scale_plot([names_spec[i], name_uvv], [labels_spec[i], "EJ260 transmission"], path=paths_spec[i] + "_with_transmission",
                        xbounds=[300, 750])
"""

"""names = c.search_in_dir("data/spec/uv-led", identifiers=["aprun"])
labels = c.extract_labels_from_path(names)
path = "zz_spec_combis/uv_tube_aperture.png"
c.multi_plot(names, labels, path, title="Verschiedene Blendenöffnungen vor der LED", norm=True)
"""
