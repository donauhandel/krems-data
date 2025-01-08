from config import LISTPLACE, LISTORG
from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import get_xmlid
from acdh_xml_pyutils.xml import NSMAP


doc = TeiReader(LISTPLACE)

lookup_dict = {}
for x in doc.any_xpath(".//tei:place[@xml:id]"):
    xmlid = get_xmlid(x)
    print(xmlid)
    try:
        geo = x.xpath(".//tei:geo", namespaces=NSMAP)[0]
    except IndexError:
        continue
    lookup_dict[xmlid] = geo


doc = TeiReader(LISTORG)
for x in doc.any_xpath(".//tei:location"):
    try:
        key = x.xpath("./tei:placeName/@key", namespaces=NSMAP)[0]
    except IndexError:
        continue
    try:
        geo = lookup_dict[key]
    except KeyError:
        continue
    x.append(geo)
doc.tree_to_file(LISTORG)
