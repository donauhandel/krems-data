import os
import pandas as pd
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

