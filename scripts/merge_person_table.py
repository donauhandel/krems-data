import os
import pandas as pd
from tqdm import tqdm
from config import ORIG_DATA_CSVS

print("merges some columns from other tables into person.csv")

person_df = pd.read_csv('./orig_data/csvs/personen.csv').convert_dtypes()
konfession_df = pd.read_csv('./orig_data/csvs/konfessionen.csv').convert_dtypes()
type_df = pd.read_csv('./orig_data/csvs/typen.csv').convert_dtypes()
person_df.merge(konfession_df, how='outer', left_on='konfession', right_on="konfessionId").drop(columns=['konfession_x']).rename(columns={"konfession_y": "konfession"})
person_df.merge(konfession_df, how='outer', left_on='konfession', right_on="konfessionId").drop(columns=['konfession_x']).rename(columns={"konfession_y": "konfession"})
new_df = person_df.merge(type_df, how='outer', left_on='typ', right_on="typId").drop(columns=['typ_x']).rename(columns={"typ_y": "typ"})

persons_merged = os.path.join(ORIG_DATA_CSVS, 'persons_merged.csv')
new_df.to_csv(persons_merged, index=False)


df = pd.read_csv('./orig_data/csvs/personen_literatur.csv').convert_dtypes()
literatur = {}
for g, ndf in df.groupby('personenId'):
    literatur[g] = list(ndf['literatur'].values)

df = pd.read_csv('./orig_data/csvs/personen_identisch.csv').convert_dtypes()
doppelt = {}
for g, ndf in df.groupby('personenId1'):
    doppelt[g] = list(ndf['personenId2'].values)

df = pd.read_csv('./orig_data/csvs/personen_ehepartner.csv').convert_dtypes()
ehe = {}
for g, ndf in df.groupby('personenId1'):
    ehe[g] = list(ndf['personenId2'].values)

df = pd.read_csv('./orig_data/csvs/personen_altNachname.csv').convert_dtypes()
alt_nach = {}
for g, ndf in df.groupby('personenId'):
    alt_nach[g] = list(ndf['altNachname'].values)

df = pd.read_csv('./orig_data/csvs/personen_altVorname.csv').convert_dtypes()
alt_vor = {}
for g, ndf in df.groupby('personenId'):
    alt_vor[g] = list(ndf['altVorname'].values)

df = pd.read_csv('./orig_data/csvs/personen_aemter.csv').convert_dtypes()
df1 = pd.read_csv('./orig_data/csvs/aemter.csv').convert_dtypes()
df = df.merge(df1,  how='outer', left_on='amtId', right_on="amtId")
aemter = {}
for g, ndf in df.groupby('personenId'):
    aemter[g] = list(ndf['amt'].values)

df = pd.read_csv('./orig_data/csvs/personen_kaufmannsklasse.csv').convert_dtypes()
df1 = pd.read_csv('./orig_data/csvs/kaufmannsklassen.csv').convert_dtypes()
df = df.merge(df1,  how='outer', left_on='kaufmannsklassenId', right_on="kaufmannsklassenId")
kaufmannsklasse = {}
for g, ndf in df.groupby('personenId'):
    kaufmannsklasse[g] = list(ndf['kaufmannsklasse'].values)

df = pd.read_csv('./orig_data/csvs/persons_merged.csv').convert_dtypes()
items = {}
for i, row in tqdm(new_df.iterrows(), total=len(new_df)):
    item_id = row['personenId']
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
    items[item_id] = item_dict