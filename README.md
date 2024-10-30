# krems-data
repo to store and convert data from Krems/Aschach Project

## dump sql into csv

* provide DB connection settings via env variables (see `dummy.env`)
* run `scripts/sql_to_csv.py` to dump db-tables into `orig_data/csv/{table_name}.csv`


## how to ge a dump

* go to https://webdatenbank-admin.univie.ac.at/
* connect to
  * HOST: donauhandj87mysql15.mysql.univie.ac.at
  * USER: donauhandj87
  * PW: verysecret

### ASCHACH
https://webdatenbank-admin.univie.ac.at/index.php?route=/database/structure&server=1&db=donauhandj87mysql15
* angaben | angaben_1625 | angaben_bemerkungen

### KREMS
https://webdatenbank-admin.univie.ac.at/index.php?route=/database/structure&server=1&db=donauhandj87mysql11
* aemter | alphabet | bearbeitet | codesAktuell
