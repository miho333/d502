import os
from pathlib import Path
import requests
import pandas as pd
from src.path_config import RAW_DATA_DIR, PROCESSED_DATA_DIR

#Load cleaned data into dataframes, make sure 
bls = pd.read_csv(PROCESSED_DATA_DIR / 'bls_processed.csv', dtype={'cbsa_code': str})
acs = pd.read_csv(PROCESSED_DATA_DIR / 'acs_processed.csv', dtype={'cbsa_code': str})
bea = pd.read_csv(PROCESSED_DATA_DIR / 'bea_processed.csv', dtype={'cbsa_code': str})

#Merge all three on cbsa_code using outer joins to preserve mismatches
merged = bls.merge(acs, on="cbsa_code", how="outer")
merged = merged.merge(bea, on="cbsa_code", how="outer")

#Identify which rows are present in which dataframes
merged["in_bls"] = merged["cbsa_code"].isin(bls["cbsa_code"])
merged["in_acs"] = merged["cbsa_code"].isin(acs["cbsa_code"])
merged["in_bea"] = merged["cbsa_code"].isin(bea["cbsa_code"])

#Show only those which aren't in all 3
missing = merged[~(merged["in_bls"] & merged["in_acs"] & merged["in_bea"])]
print(missing)

print('Merged.shape: ', merged.shape)

#Consolidate new dataframe of just matching metro areas
merged = merged.drop(columns=["in_bls","in_acs","in_bea"])
merged = merged[~merged['cbsa_code'].isin(missing['cbsa_code'])]

print("Merged dataframe shape:\n", merged.shape)
print("Dataframe info:\n", merged.info())
print("Dataframe head:\n", merged.head())
print("Dataframe descriptions:\n", merged.describe())

#Save to CSV for local use
FILE_OUTPUT = PROCESSED_DATA_DIR / 'merged_processed.csv'
merged.to_csv(FILE_OUTPUT, index=False)