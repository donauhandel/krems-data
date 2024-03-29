import os
import shutil
from datetime import date

import pandas as pd
from config import ORIG_DATA_CSVS
from sqlalchemy import create_engine
from sqlalchemy import inspect

today = date.today()
print(ORIG_DATA_CSVS)
shutil.rmtree(ORIG_DATA_CSVS)
os.makedirs(ORIG_DATA_CSVS, exist_ok=True)

DB_USER = os.environ.get("DB_USER")
DB_PW = os.environ.get("DB_PW")
DB_NAME = os.environ.get("DB_NAME")
DB_HOST = os.environ.get("DB_HOST", "0.0.0.0")
DB_PORT = os.environ.get("DB_PORT", "3307")

db_connection_str = f"mysql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(db_connection_str)
db_connection = create_engine(db_connection_str)
insp = inspect(db_connection)

tables = insp.get_table_names()

for i, x in enumerate(tables):
    i += 1
    if x.startswith("dataface") or x.startswith("help_"):
        continue
    query = f"SELECT * FROM {x}"
    df = pd.read_sql(query, db_connection).fillna("")
    file_name = os.path.join(ORIG_DATA_CSVS, f"{x}.csv")
    print(f"writing table: {x} to {file_name} {i}/{len(tables)}")
    df.to_csv(file_name, index=False)
    with open(file_name, "r") as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace(".0,", ",")
    filedata = filedata.replace(".0\n", "\n")

    # Write the file out again
    with open(file_name, "w") as file:
        file.write(filedata)
