import json
import inspect
from pprint import pprint

class Test:

    def __init__(self):
        self.seq_name = None
        self.seq = []

    def some_func(self, arg1, arg2, kwarg1=None, kwarg2=None, **kwargs):

        # NEEDED----
        if "kwargs" in kwargs:
            kwargs = kwargs["kwargs"]
        # ----

        print("arg1: " + str(arg1))
        print("arg2: " + str(arg2))

        print("kwarg1: " + str(kwarg1))
        print("kwarg2: " + str(kwarg2))
        print("kwargs: ")
        pprint(kwargs)

        # NEEDED----
        a = locals()
        a.pop("self")
        a["func_name"] = inspect.stack()[0][3]
        self.seq.append(a)
        # ----

    def clear_seq(self):
        self.seq = []
        self.seq_name = None

    def jsonize(self, name):
        print(self.seq)
        if not self.seq:
            raise ValueError("Sequence can not be empty!")

        with open("seq.json", "r") as of:
            j = json.load(of)

        j[name] = self.seq

        with open("seq.json", "w") as of:
            jf = json.dumps(j, indent=4, sort_keys=True, separators=(",", ": "), ensure_ascii=False)
            of.write(jf)

        self.seq = []
        self.seq_name = None

    def load_seq(self, name):
        with open("seq.json", "r") as of:
            j = json.load(of)[name]


        for i in j:
            print(i)
            func_name = i.pop("func_name")
            if func_name == "some_func":
                self.some_func(**i)




a = {
    "test": [1, 2, 3],
    "kei": 123,
    "f": 23,
}

for key in a:
    a["test"] = 1



#t = Test()
"""t.some_func(1,2, kwarg1="test", kwarg2="ahjj", more_kwarg="asdfkj")
t.some_func(11,21, kwarg1="test1", kwarg2="ahjj1", more_kwarg="asdfkj1")

t.jsonize("test2")

t.some_func(1,2, kwarg1="test", kwarg2="ahjj", more_kwarg="asdfkj")

t.jsonize("test")"""

#t.load_seq("test2")

# args = r.pop("args")
# print(args)

