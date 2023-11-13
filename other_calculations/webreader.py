import urllib
import re
import mechanize

br = mechanize.Browser()
br.open("https://physics.nist.gov/cgi-bin/Xcom/xcom2?Method=Elem&Output2=Hand")

# br.select_form(name="ZNum=")

a = 0
for form in br.forms():
    form.name = "test"
    a = form

br.select_form(name="test")

a.set_value("14", name="ZNum", kind="text")
control = a.find_control("ZNum", type="text")
print(control.name, control.value, control.type)
