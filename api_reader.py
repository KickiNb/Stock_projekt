import requests
import logging
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv('FINNHUB_API_KEY')

def fetch_stock_data(symbol: str, cache: dict) -> dict:
    """Fetch real-time stock data from Finnhub for a given symbol."""
    if symbol in cache:
        logging.info(f"Using cached data for {symbol}.")
        return cache[symbol]
    
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        stock_data = response.json()

        # Check if data contains stock price ('c' is current price)
        if 'c' not in stock_data or stock_data['c'] == 0:
            logging.warning(f"No stock price data for {symbol}. Skipping")
            return None 
        
        logging.info(f"Successfully fetched data for {symbol} from Finnhub.")
        return stock_data
    
    except requests.RequestException as e:
        logging.error(f"Error fetching data from Finnhub API for {symbol}: {e}")
        return None

# Save and load data in cache to avoid duplicates 
def save_cache(data: dict, filename='fetched_data_cache.json'):
    """Save retrieved data in a cache file."""
    with open(filename, 'w') as f:
        json.dump(data, f)
    logging.info("Cached data saved.")

def load_cache(filename='fetched_data_cache.json') -> dict:
    """Read retrieved data from cache file."""
    try:
        with open(filename, 'r') as f:
            data = json.load(f) 
        logging.info("Loaded cached data.")
        return data
    except FileNotFoundError:
        logging.info("No cache found, fetching new data.")
        return {}

