import json
import os
from datetime import date

import jinja2
from acdh_tei_pyutils.tei import TeiReader
from config import LISTPERSON
from config import ORIG_DATA_MERGED

os.makedirs("./data/indices", exist_ok=True)
today = date.today()
context = {"prefix": "wkfm__", "datum": f"{date.today()}"}
templateLoader = jinja2.FileSystemLoader(searchpath="./scripts/templates")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template("listperson.xml")

with open(os.path.join(ORIG_DATA_MERGED, "persons.json"), "r") as f:
    data = f.read()
    data = data.replace("<NA>", "")
    data = json.loads(data)

context["personen"] = []
for key, value in data.items():
    if value["typshort"] in ["piz"]:
        context["personen"].append(value)
    else:
        continue

with open(LISTPERSON, "w") as f:
    f.write(template.render(**context).replace("&", "&amp;"))

doc = TeiReader(LISTPERSON)
doc.tree_to_file(LISTPERSON)
