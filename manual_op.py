from control import get_inst

c = get_inst()


c.c_file.sort_to_dirs()
c.plot_dir("data/spec/ppo5", identifiers=["uv"])
c.plot_dir("data/spec/3hf1", identifiers=["uv"])

# print(c.search_in_dir("data/spec", identifiers=["uv", "4600"]))






