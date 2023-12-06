import urllib
import re
import mechanize
from mechanize import urlopen
import pandas as pd
from pprint import pprint

br = mechanize.Browser()
br.open("https://physics.nist.gov/cgi-bin/Xcom/xcom2?Method=Elem&Output2=Hand")

# br.select_form(name="ZNum=")

a = 0
for form in br.forms():
    form.name = "test"
    a = form

br.select_form(name="test")

input = {
    "Graph0": [],
    "Graph1": ["on"],
    "Graph2": ["on"],
    "Graph3": ["on"],
    "Graph4": ["on"],
    "Graph5": ["on"],
    "Graph6": ["on"],
    "Graph7": [],
    "ZNum": "13",
    "Energies": "0.023"
}

for key in input:
    a[key] = input[key]

br.open(a.click())

i = 0
for form in br.forms():
    form.name = f"form{i}"
    i += 1
    if form.name == "form1":
        a = form

input = {
    "photoelectric": ["on"],
    "coherent": ["on"],
    "incoherent": ["on"],
    "nuclear": ["on"],
    "electron": ["on"],
    "with": ["on"],
}

for key in input:
    a[key] = input[key]

answer = urlopen(a.click()).read().decode()

answer = answer[re.search("\n\n", answer).end():-1]
df = pd.DataFrame([x.split(' ') for x in answer.split('\n')])

nda = df.to_numpy()
print(nda)
