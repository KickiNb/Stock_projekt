import requests
import csv
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv('FINNHUB_API_KEY')
API_URL = 'https://finnhub.io/api/v1/stock/symbol?exchange=US&token=' + API_KEY

def fetch_company_data():
    response = requests.get(API_URL)
    response.raise_for_status()     # If there are any errors with the API-call
    return response.json()

def save_to_csv(data, filename='companies.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Company', 'Ticker', 'Currency'])  
        for item in data:
            writer.writerow([item['description'], item['symbol'], item['currency']])

def main():
    company_data = fetch_company_data()
    save_to_csv(company_data, filename='C:/Users/kicki/my_stock_projekt/companies.csv')
    print(f"Company information saved in 'companies.csv'.")

if __name__ == '__main__':
    main()