# krems-data
repo to store and convert data from Krems/Aschach Project

## dump sql into csv

* provide DB connection settings via env variables (see `dummy.env`)
* run `scripts/sql_to_csv.py` to dump db-tables into `orig_data/csv/{table_name}.csv`
