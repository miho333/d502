import sqlite3
import os
from pathlib import Path
import requests
import pandas as pd
from src.path_config import DB_PATH, RAW_DATA_DIR, PROCESSED_DATA_DIR

#Load cleaned data into dataframes, make sure codes come in as strings
bls = pd.read_csv(PROCESSED_DATA_DIR / 'bls_processed.csv', dtype={'cbsa_code': str})
acs = pd.read_csv(PROCESSED_DATA_DIR / 'acs_processed.csv', dtype={'cbsa_code': str})
bea = pd.read_csv(PROCESSED_DATA_DIR / 'bea_processed.csv', dtype={'cbsa_code': str})

#Launch sqlite and ingest cleaned data into sql tables
conn = sqlite3.connect(DB_PATH)
bls.to_sql('bls_wages', conn, if_exists='replace', index=False)
acs.to_sql('acs_education', conn, if_exists='replace', index=False)
bea.to_sql('bea_rpp', conn, if_exists='replace', index=False)

#Join all tables together on cbsa_code
query = """
SELECT 
    a.cbsa_code,
    a.metro_name,
    a.bachelors_or_higher_pct,
    b.employment,
    b.median_wage,
    r.rpp
FROM acs_education AS a
INNER JOIN bls_wages AS b
    ON a.cbsa_code = b.cbsa_code
INNER JOIN bea_rpp AS r
    ON a.cbsa_code = r.cbsa_code
"""
joined_df = pd.read_sql(query,conn)
print("\nDataframe of joined data:\n", joined_df.head())

#Save joined table to new master record in sql
joined_df.to_sql('workforce_master', conn, if_exists='replace',index=False)

#Verify all 3 source tables and master table are present
tables = pd.read_sql("""
                     SELECT name
                     FROM sqlite_master
                     WHERE type='table'
                     """, conn)
print("\nCreated tables:\n", tables)

#Close connection to db
conn.close()