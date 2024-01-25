import os
import pandas as pd
from config import ORIG_DATA_CSVS

ORTE_CSV = os.path.join(ORIG_DATA_CSVS, "orte.csv")

df = pd.read_csv(ORTE_CSV)
df = df[df["aschachId"].notna()]
df["aschachId"].astype("int")

print(df)

# def get_dec(degr):
#     try:
#         dec = int(degr[0]) + (int(degr[1]) / 60 + int(degr[2]) / 3600)
#     except:
#         return None
#     return round(dec, 4)