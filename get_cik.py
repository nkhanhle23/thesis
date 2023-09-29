import pandas as pd

link = (
    "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks"
)
df = pd.read_html(link, header=0)[0]

cik = df['CIK'] 

cik.to_csv('cik.csv', index=False)