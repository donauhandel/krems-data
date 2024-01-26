from acdh_tei_pyutils.tei import TeiReader
from config import LISTORG
from config import LISTPERSON
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
