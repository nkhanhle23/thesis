import requests
import pandas as pd
from tqdm import tqdm
import json

# Define metrics
metrics = ['NetIncomeLoss','RevenueFromContractWithCustomerExcludingAssessedTax',
           'EarningsPerShareDiluted', 'NetCashProvidedByUsedInContinuingOperations',
           'NetCashProvidedByUsedInFinancingActivities', 
           'NetCashProvidedByUsedInInvestingActivities']

start_year = 2006
end_year = 2022

# Define base URL and header
base_url = "https://data.sec.gov/api/xbrl/frames/us-gaap"
header = {'Accept': "application/json", 'User-Agent': "s_nguyenk22@stud.hwr-berlin.de"}

# Create an empty list to store the results
all_data = []

# Loop through metrics and years
for metric in metrics: 
    metric_data = []  # Create a list for data related to the current metric
    for year in tqdm(range(start_year, end_year + 1), desc=f"Fetching {metric}"):
        url = f"{base_url}/{metric}/USD/CY{year}.json"
        try:
            data = requests.get(url, headers=header).json()
            df = pd.DataFrame(data['data'])
            df['year'] = year
            
            df['metric'] = metric

            metric_data.append(df)
        except json.JSONDecodeError as e:
            print(f"Skipping {url} due to JSONDecodeError: {e}")

    # Concatenate all the dataframes related to the current metric
    if metric_data:
        all_data.extend(metric_data)

# Concatenate all the dataframes into one
final_df = pd.concat(all_data, ignore_index=True)

# Rename the columns
final_df['metric'] = final_df['metric'].replace({
    'NetIncomeLoss': 'Net Income (Loss)',
    'RevenueFromContractWithCustomerExcludingAssessedTax': 'Revenue',
    'EarningsPerShareDiluted': 'Diluted Earnings per share',
    'NetCashProvidedByUsedInContinuingOperations': 'Net Cash from Operating Activities',
    'NetCashProvidedByUsedInFinancingActivities': 'Net Cash from Financing Activities',
    'NetCashProvidedByUsedInInvestingActivities': 'Net Cash from Investing Activities'
})



# Save the concatenated dataframe to a CSV file
final_df.to_csv('datasets/financial_data.csv', index=False)

# Print a completion message
print("Done")