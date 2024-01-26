import lxml.etree as ET
from acdh_tei_pyutils.tei import TeiReader
from config import LISTORG
from config import LISTPERSON
from config import LISTPLACE
from tqdm import tqdm

person_xml = TeiReader(LISTPERSON)
org_xml = TeiReader(LISTORG)
nsmap = person_xml.nsmap

print("make org-dict")
orgs = {}
for x in tqdm(org_xml.any_xpath(".//tei:org[@xml:id]")):
    xmlid = x.attrib["{http://www.w3.org/XML/1998/namespace}id"]
    name = x.xpath("./tei:orgName/text()", namespaces=nsmap)[0]
    orgs[xmlid] = {"key": f"#{xmlid}", "name": name}

print(f"writing orgNames from {LISTORG} into {LISTPERSON}")
for x in tqdm(person_xml.any_xpath(".//tei:affiliation/tei:orgName[@key]")):
    key = x.attrib["key"][1:]
    try:
        name = orgs[key]["name"]
    except KeyError:
        continue
    x.text = name
person_xml.tree_to_file(LISTPERSON)
person_xml = TeiReader(LISTPERSON)

place_xml = TeiReader(LISTPLACE)
places = {}
print(f"collecting data from {LISTPLACE}")
for x in tqdm(place_xml.any_xpath(".//tei:place[@xml:id]")):
    xmlid = x.attrib["{http://www.w3.org/XML/1998/namespace}id"]
    try:
        location = x.xpath("./tei:location/tei:geo", namespaces=nsmap)[0]
    except IndexError:
        continue
    places[xmlid] = {
        "location": location.text,
    }

for x in tqdm(person_xml.any_xpath(".//tei:residence")):
    try:
        key = x.xpath(".//tei:placeName/@key", namespaces=nsmap)[0][1:]
    except IndexError:
        continue
    try:
        location = places[key]["location"]
    except KeyError:
        continue
    loc_node = ET.Element("{http://www.tei-c.org/ns/1.0}location")
    loc_node.attrib["type"] = "coords"
    geo_node = ET.Element("{http://www.tei-c.org/ns/1.0}geo")
    geo_node.text = location
    loc_node.append(geo_node)
    x.append(loc_node)
person_xml.tree_to_file(LISTPERSON)
