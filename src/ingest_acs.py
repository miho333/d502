import os
from pathlib import Path
import requests
import pandas as pd
import json
from src.path_config import RAW_DATA_DIR, PROCESSED_DATA_DIR
from dotenv import load_dotenv

#Import API key
load_dotenv(Path(__file__).parent.parent / "keys.env")
CENSUS_API_KEY = os.getenv("CENSUS_API_KEY")

'''
Important note for API call - Per official documentation S1501 is the relevant table for education data:
"S1501_C02_015E: Estimate!!Percent!!AGE BY EDUCATIONAL ATTAINMENT!! Population 25 years and over!!Bachelor's degree or higher"
'''

#Pull data from Census API
url = "https://api.census.gov/data/2024/acs/acs5/subject"
params = {
    'get':'NAME,S1501_C02_015E',
    'for':'metropolitan statistical area/micropolitan statistical area:*',
    'key': CENSUS_API_KEY
}
response = requests.get(url,params=params)
data = response.json()

#Save raw data before processing
with open(RAW_DATA_DIR / "acs_raw.json", "w") as f:
    json.dump(data, f, indent=1)

#Convert response to dataframe
df = pd.DataFrame(data[1:], columns=data[0])
#Process data
df = df.rename(
    columns={
        "NAME": "metro_name",
        "S1501_C02_015E": "bachelors_or_higher_pct",
        "metropolitan statistical area/micropolitan statistical area": "cbsa_code"        
})
df['bachelors_or_higher_pct'] = pd.to_numeric(df['bachelors_or_higher_pct'])
df["cbsa_code"] = df["cbsa_code"].astype(str).str.strip()

#Drop micropolitan areas
df = df[~df['metro_name'].str.contains('micro area', case=False, na=False)].copy()

#Quick sanity check for dataframe
print('Cleaned dataframe shape: ')
print(df.shape)
print(df.head())
print('TYPES', print(df.info()))

#Save to CSV for local use
PROCESSED_OUTPUT = PROCESSED_DATA_DIR / 'acs_processed.csv'
df.to_csv(PROCESSED_OUTPUT, index=False)