import os
import json
import jinja2
from datetime import date

from config import ORIG_DATA_MERGED

os.makedirs('./data/indices', exist_ok=True)
today = date.today()
context = {
    "prefix": "wkfm__",
    "datum": f"{date.today()}"
}
templateLoader = jinja2.FileSystemLoader(searchpath="./scripts/templates")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template('listperson.xml')

with open(os.path.join(ORIG_DATA_MERGED, 'persons.json'), 'r') as f:
    data = f.read()
    data = data.replace('<NA>', "")
    data = json.loads(data)

context['personen'] = []
for key, value in data.items():
    if value['typshort'] in ['piz']:
        context['personen'].append(value)
    else:
        continue

with open("./data/indices/listperson.xml", 'w') as f:
    f.write(template.render(**context).replace('&', '&amp;'))
