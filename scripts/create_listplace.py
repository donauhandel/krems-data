import os
from datetime import date
from xml.sax.saxutils import escape

import jinja2
import pandas as pd
from acdh_tei_pyutils.tei import TeiReader
from AcdhArcheAssets.uri_norm_rules import get_normalized_uri
from config import LISTPLACE
from config import ORIG_DATA_CSVS
from utils import convert_coordinates

os.makedirs("./data/indices", exist_ok=True)
today = date.today()
context = {"prefix": "wkfm-place__", "datum": f"{date.today()}"}
templateLoader = jinja2.FileSystemLoader(searchpath="./scripts/templates")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template("listplace.xml")

ORTE_CSV = os.path.join(ORIG_DATA_CSVS, "orte.csv")
df = pd.read_csv(ORTE_CSV)
df = df[df["aschachId"].notna()]
df["aschachId"].astype("int")
df["latitude"] = df.apply(lambda row: convert_coordinates(row["latitude"]), axis=1)
df["longitude"] = df.apply(lambda row: convert_coordinates(row["longitude"]), axis=1)

normdata = pd.read_csv(os.path.join(ORIG_DATA_CSVS, "orte_verknuepfungen.csv"))
norm_dict = {}
for g, ndf in normdata.groupby("ortsId"):
    norm_dict[g] = []
    for i, row in ndf.iterrows():
        try:
            if "d-nb" in row["eintrag"]:
                item = {"domain": "gnd", "uri": get_normalized_uri(row["eintrag"].strip())}
                norm_dict[g].append(item)
            if "geonames" in row["eintrag"]:
                item = {"domain": "geonames", "uri": get_normalized_uri(row["eintrag"].strip())}
                norm_dict[g].append(item)
        except TypeError:
            continue

lit = pd.read_csv(os.path.join(ORIG_DATA_CSVS, "orte_literatur.csv"))
lit_dict = {}
for g, ndf in lit.groupby("ortsId"):
    lit_dict[g] = []
    for i, row in ndf.iterrows():
        try:
            lit_dict[g].append(escape(row["literatur"].strip()))
        except AttributeError:
            continue

context["objects"] = []
for i, row in df.iterrows():
    item = row.to_dict()
    if isinstance(item["verkehrsanbindung"], str):
        item["verkehrsanbindung"] = escape(item["verkehrsanbindung"])
    else:
        item["verkehrsanbindung"] = ""
    try:
        item["normdata"] = norm_dict[row["ortsId"]]
    except KeyError:
        item["normdata"] = []
    try:
        item["literatur"] = lit_dict[row["ortsId"]]
    except KeyError:
        item["literatur"] = []
    context["objects"].append(item)

with open(LISTPLACE, "w") as f:
    f.write(template.render(**context).replace("&", "&amp;"))

doc = TeiReader(LISTPLACE)

print(f"saving {LISTPLACE}")
