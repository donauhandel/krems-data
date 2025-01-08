from config import LISTPLACE, LISTORG
from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import get_xmlid
from acdh_xml_pyutils.xml import NSMAP
import copy


doc = TeiReader(LISTPLACE)
lookup_dict = {}
for x in doc.any_xpath(".//tei:place[@xml:id]"):
    xmlid = get_xmlid(x)
    try:
        geo = x.xpath(".//tei:geo", namespaces=NSMAP)[0]
    except IndexError:
        continue
    lookup_dict[xmlid] = geo


doc = TeiReader(LISTORG)
no_match = set()
for bad in doc.any_xpath(".//tei:geo"):
    bad.getparent().remove(bad)
doc.tree_to_file(LISTORG)

doc = TeiReader(LISTORG)
for x in doc.any_xpath(".//tei:location"):
    key = x.xpath("./tei:placeName/@key", namespaces=NSMAP)[0]
    try:
        geo = lookup_dict[key]
        copy_geo = copy.deepcopy(geo)
        x.insert(1, copy_geo)
    except KeyError:
        print(f"no match for {key}")
doc.tree_to_file(LISTORG)

print(no_match)
