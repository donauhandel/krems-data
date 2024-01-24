import os
import json
import jinja2
from datetime import date

from config import ORIG_DATA_MERGED


def org_filter(item):
    _, value = item
    if value["typId"] == 2:
        return True
    else:
        return False


os.makedirs('./data/indices', exist_ok=True)
today = date.today()
context = {
    "prefix": "wkfm__",
    "datum": f"{date.today()}"
}
templateLoader = jinja2.FileSystemLoader(searchpath="./scripts/templates")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template('listorg.xml')

with open(os.path.join(ORIG_DATA_MERGED, 'persons.json'), 'r') as f:
    data = f.read()
    data = data.replace('<NA>', "")
    data = json.loads(data)

data = dict(filter(org_filter, data.items()))

context['objects'] = []
for key, value in data.items():
    context["objects"].append(value)

with open("./data/indices/listorg.xml", 'w') as f:
    f.write(template.render(**context).replace('&', '&amp;'))
