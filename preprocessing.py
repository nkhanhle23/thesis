import os
import json
import pandas as pd

# Extract metadata from filings

data_source = 'datasets/FILINGS_METADATA.csv'
metadata = pd.read_csv(data_source)

metadata = metadata[['CIK', 'Company', 'Period of Report', 'State of Inc', 'State location', 'Fiscal Year End']]

print(metadata.head())

metadata.to_csv('datasets/metadata.csv', index=False)

print('Done! Check datasets/metadata.csv')

# Extract financial metrics from item 8

## For this we need a list of synonyms for each metric to automate the process



