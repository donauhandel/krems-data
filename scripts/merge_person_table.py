import os
import json
import pandas as pd
from tqdm import tqdm
from slugify import slugify
from config import ORIG_DATA_CSVS, ORIG_DATA_MERGED
from utils import MyEncoder


print("merges some columns from other tables into person.csv")

person_df = pd.read_csv(f'{ORIG_DATA_CSVS}/personen.csv').convert_dtypes()
konfession_df = pd.read_csv(f'{ORIG_DATA_CSVS}/konfessionen.csv').convert_dtypes()
type_df = pd.read_csv(f'{ORIG_DATA_CSVS}/typen.csv').convert_dtypes()
person_df.merge(konfession_df, how='outer', left_on='konfession', right_on="konfessionId")
new_df = person_df.merge(type_df, how='outer', left_on='typ', right_on="typId").drop(columns=['typ_x']).rename(columns={"typ_y": "typ"})

persons_merged = os.path.join(ORIG_DATA_CSVS, 'persons_merged.csv')
new_df.to_csv(persons_merged, index=False)


df = pd.read_csv(f'{ORIG_DATA_CSVS}/personen_literatur.csv').convert_dtypes()
literatur = {}
for g, ndf in df.groupby('personenId'):
    literatur[g] = list(ndf['literatur'].values)

df = pd.read_csv(f'{ORIG_DATA_CSVS}/personen_identisch.csv').convert_dtypes()
doppelt = {}
for g, ndf in df.groupby('personenId1'):
    doppelt[g] = list(ndf['personenId2'].values)

df = pd.read_csv(f'{ORIG_DATA_CSVS}/personen_ehepartner.csv').convert_dtypes()
ehe = {}
for g, ndf in df.groupby('personenId1'):
    ehe[g] = list(ndf['personenId2'].values)

df = pd.read_csv(f'{ORIG_DATA_CSVS}/personen_altNachname.csv').convert_dtypes()
alt_nach = {}
for g, ndf in df.groupby('personenId'):
    alt_nach[g] = list(ndf['altNachname'].values)

df = pd.read_csv(f'{ORIG_DATA_CSVS}/personen_altVorname.csv').convert_dtypes()
alt_vor = {}
for g, ndf in df.groupby('personenId'):
    alt_vor[g] = list(ndf['altVorname'].values)

df = pd.read_csv(f'{ORIG_DATA_CSVS}/personen_aemter.csv').convert_dtypes()
df1 = pd.read_csv(f'{ORIG_DATA_CSVS}/aemter.csv').convert_dtypes()
df = df.merge(df1,  how='outer', left_on='amtId', right_on="amtId")
aemter = {}
for g, ndf in df.groupby('personenId'):
    aemter[g] = list(ndf['amt'].values)

df = pd.read_csv(f'{ORIG_DATA_CSVS}/personen_kaufmannsklasse.csv').convert_dtypes()
df1 = pd.read_csv(f'{ORIG_DATA_CSVS}/kaufmannsklassen.csv').convert_dtypes()
df = df.merge(df1,  how='outer', left_on='kaufmannsklassenId', right_on="kaufmannsklassenId")
kaufmannsklasse = {}
for g, ndf in df.groupby('personenId'):
    kaufmannsklasse[g] = list(ndf['kaufmannsklasse'].values)

print("fetching person-place relations")
df = pd.read_csv(f'{ORIG_DATA_CSVS}/personen_orte.csv').convert_dtypes()
df1 = pd.read_csv(f'{ORIG_DATA_CSVS}/ortsarten.csv').convert_dtypes()
df = df.merge(df1,  how='outer', left_on='ortsartId', right_on="ortartenId")
df1 = pd.read_csv(f'{ORIG_DATA_CSVS}/orte.csv').convert_dtypes()
df = df.merge(df1,  how='outer', left_on='ortsId', right_on="ortsId")
orte = {}
for g, ndf in tqdm(df.groupby('personenId')):
    orte[g] = {}
    for i, row in ndf.iterrows():
        try:
            rel_type = slugify(row['art'])
        except TypeError:
            continue
        item = {}
        item['art'] = row['art']
        item['orts_id'] = row['ortsId']
        item['orts_name'] = row['ortsname']
        orte[g][rel_type] = item

df = pd.read_csv(f'{ORIG_DATA_CSVS}/persons_merged.csv').convert_dtypes()
items = {}
for i, row in tqdm(new_df.iterrows(), total=len(new_df)):
    item_id = row['personenId']
    if isinstance(item_id, int):
        pass
    else:
        continue
    item_dict = row.to_dict()
    try:
        lit = literatur[item_id]
    except:
        lit = []
    item_dict['literatur'] = lit
    try:
        lit = doppelt[item_id]
    except:
        lit = []
    item_dict['doppelt'] = lit
    try:
        lit = aemter[item_id]
    except:
        lit = []
    item_dict['aemter'] = lit
    try:
        lit = kaufmannsklasse[item_id]
    except:
        lit = []
    item_dict['kaufmannsklasse'] = lit
    try:
        lit = ehe[item_id]
    except:
        lit = []
    item_dict['ehe'] = lit
    try:
        lit = alt_vor[item_id]
    except:
        lit = []
    item_dict['alt_vor'] = lit
    try:
        lit = alt_nach[item_id]
    except:
        lit = []
    item_dict['alt_nach'] = lit
    try:
        lit = orte[item_id]
    except:
        lit = []
    item_dict['orte'] = lit
    items[item_id] = item_dict

print(f"writing person.jsons into {ORIG_DATA_MERGED}")

os.makedirs(ORIG_DATA_MERGED, exist_ok=True)
with open(f'{ORIG_DATA_MERGED}/persons.json', 'w') as f:
    json.dump(items, f, ensure_ascii=False, cls=MyEncoder, default=str, indent=2)