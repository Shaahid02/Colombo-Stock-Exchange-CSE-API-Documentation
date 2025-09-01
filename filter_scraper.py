import pandas as pd
import json
import os

os.makedirs("company_training_data", exist_ok=True)

company_data = []

try:
    with open('company_data/data.json', 'r', encoding='utf-8') as f:
        company_data = json.load(f)
except FileNotFoundError:
    company_data = []
    

for company in company_data:
    df = pd.read_csv('training_data/daily_market_capitalization.csv')
    filtered_df = df[df["name"].str.contains(company["name"], na=False)]
    filtered_df.to_csv(f'company_training_data/{company["symbol"].replace(" ", "_")}.csv', index=False)


""" df = pd.read_csv('training_data/daily_market_capitalization(1).csv')

filtered_df = df[df["name"].str.contains("ABANS ELECTRICALS", na=False)]

filtered_df.to_csv('training_data/abans_electricals.csv', index=False) """