from control import get_inst
import re
from pprint import pprint

c = get_inst()

# c.c_file.sort_to_dirs()
# c.plot_dir("data/spec/uv-led")
# c.plot_dir("data/uv-vis/ej260")
# c.plot_dir("data/spec")

"""names = c.search_in_dir("data/spec", identifiers=["2step"])
pprint(names)
style = {"c": ["xkcd:pale green", "xkcd:electric blue", "xkcd:lime", "xkcd:light cyan", "xkcd:neon blue", "xkcd:cobalt blue", "xkcd:dark blue", "gray"]}
labels = c.extract_labels_from_path(names)
c.multi_plot(names, labels, "zz_spec_combis/all_samples_highres.png", title="all samples measured (same circumstances)", style=style)"""

"""names = c.search_in_dir("data/spec", identifiers=["good"])
labels = c.extract_labels_from_path(names)
uv_names = []
for label in labels:
    print(label)
    uv_names.extend(c.search_in_dir("data/uv-vis", identifiers=[label, "good", "survey"]))

for name, uv_name, label in zip(names, uv_names, labels):
    print(name, uv_name)
    sample = c.c_file.get_inst_and_sample(name)[1]
    c.twin_x_scale_plot([name, uv_name], ["spec", "uv-vis"], "zz_spec_uv/with_popop_bis/"+sample+".png", title=sample)"""

c.plot_dir("data/sev")





