from control import get_inst
import re
from pprint import pprint

c = get_inst()

# c.c_file.sort_to_dirs()

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
    uv_name = c.search_in_dir("data/uv-vis", identifiers=[sample, "_good", "fast", t])

    a = [name]
    a.extend(uv_name)
    a.append("spec_uv-led_4600mV")
    b = [label]
    b.append(label)
    b.append("uv-led")

    style = {
        "ls1": ["-", "--"]
    }

    c.twin_x_scale_plot(a, b, "zz_spec_uv/" + sample + "_with_uv.png", title=sample + t + " in spec and cary", style=style)

"""

names = c.search_in_dir("data/spec", identifiers=["uv_4600"], or_identifiers=["combi14", "combi92"])
names.append("spec_uv-led_4600mV")
labels = c.extract_labels_from_path(names)
c.multi_plot(names, labels, "zz_spec_combis/combi_samples.png", title="Combi Proben", lslist=2, norm=False)




