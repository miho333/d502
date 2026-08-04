import os
from pathlib import Path
import requests
import pandas as pd
import json
from src.path_config import RAW_DATA_DIR, PROCESSED_DATA_DIR
from dotenv import load_dotenv

#Import API key
load_dotenv(Path(__file__).parent.parent / "keys.env")
BEA_API_KEY = os.getenv("BEA_API_KEY")

#Pull data from BEA source
url = "https://apps.bea.gov/api/data"
params = {
    "UserID": BEA_API_KEY,
    "method": "GetData",
    "datasetname": "Regional",
    "TableName": "MARPP",
    "LineCode": 1,
    "GeoFips": "MSA",
    "Year":"2024",
    "ResultFormat": "JSON"
}
response = requests.get(url, params=params)
data = response.json()

#Save raw data before processing
RAW_OUPUT = RAW_DATA_DIR / "bea_raw.csv"
with open(RAW_DATA_DIR / "bea_raw.json", "w") as f:
    json.dump(data, f, indent=2)

#Process data
rows = data['BEAAPI']['Results']['Data']
bea_df = pd.DataFrame(rows)

#Clean to only contain CBSA code, Metro Name, RPP
df = bea_df[['GeoFips','GeoName','DataValue']].copy()

#Rename columns for clarity and to match other datasets
df = df.rename(columns={
    'GeoFips': 'cbsa_code',
    'GeoName': 'metro_name',
    'DataValue': 'rpp'
})
df["cbsa_code"] = df["cbsa_code"].astype(str).str.strip()

#Quick sanity check for dataframe
print('Cleaned dataframe shape: ')
print(df.shape)
print(df.head())
print('TYPES', print(df.info()))

#Save cleaned dataframe 
output_path = PROCESSED_DATA_DIR / 'bea_processed.csv'
df.to_csv(output_path, index=False)