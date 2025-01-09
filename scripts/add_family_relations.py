import json
import lxml.etree as ET

from config import PERSONS_JSON, LISTPERSON
from acdh_tei_pyutils.tei import TeiReader


with open(PERSONS_JSON, "r", encoding="utf-8") as fp:
    data = json.load(fp)

listrelation = ET.Element("{http://www.tei-c.org/ns/1.0}listRelation")
prefix = "#wkfm__"
for key, value in data.items():
    source = key
    source_name = f"{value['nachname']}, {value['vorname']}"
    verwandt = value["verwandtschaft"]
    if isinstance(verwandt, dict):
        for rel_key, rel_value in verwandt.items():
            target_id = str(rel_value["person_id"])
            if target_id.startswith("<NA"):
                print("HALLO")
                continue
            else:
                node = ET.Element("{http://www.tei-c.org/ns/1.0}relation")
                node.attrib["name"] = rel_value["verwandtschaftsverhaeltnis"]
                node.attrib["active"] = f"{prefix}{source}"
                node.attrib["passiv"] = f'{prefix}{rel_value["person_id"]}'
                node.attrib["n"] = (
                    f'{source_name} — {rel_value["verwandtschaftsverhaeltnis"]} — {rel_value["person_name"]}'
                )
                listrelation.append(node)

doc = TeiReader(LISTPERSON)
for bad in doc.any_xpath(".//tei:listRelation"):
    bad.getparent().remove(bad)
body = doc.any_xpath(".//tei:body")[0]
body.insert(1, listrelation)
doc.tree_to_file(LISTPERSON)
