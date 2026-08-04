import os
from pathlib import Path
import requests
import pandas as pd
from src.path_config import RAW_DATA_DIR, PROCESSED_DATA_DIR

#Pull data from BLS source
'''
OWES metro wage and employment data were obtained from BLS OEWS data web tool. This is a 
*much* simpler/more direct path to the data than their API. This has been saved as an .xlsx 
file, included in the ETL pipeline as the raw BLS source dataset in /data/raw/MSA_M2025_dl.xlsx

I also included the matching file definitions in /data/raw/file_descriptions.xslx
'''

file_path = RAW_DATA_DIR / 'MSA_M2025_dl.xlsx'
bls_df=pd.read_excel(file_path, engine='openpyxl',dtype={'OCC_CODE':str})

#Clean to only contain CBSA Metro Name, Employment, Median Wage
df = bls_df[bls_df['OCC_CODE'] == '00-0000'][['AREA','AREA_TITLE','TOT_EMP','A_MEDIAN']].copy()

#Rename columns to match other datasets where applicable
df = df.rename(columns={
    'AREA': 'cbsa_code',
    'AREA_TITLE': 'metro_name',
    'TOT_EMP': 'employment',
    'A_MEDIAN': 'median_wage'
})

#Quick sanity check for dataframe
print('Cleaned dataframe shape: ')
print(df.shape)
print(df.head())

#Save cleaned dataframe 
output_path = PROCESSED_DATA_DIR / 'bls_processed.csv'
df.to_csv(output_path, index=False)