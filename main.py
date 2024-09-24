import concurrent.futures
import requests
import logging
import time
import os
from api_reader import fetch_stock_data, load_cache, save_cache
from csv_reader import read_company_data
from data_processor import process_data  
from sql_updater import update_sql_table
from logger import setup_logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

CSV_FILE = os.getenv('CSV_FILE', 'C:/Users/kicki/my_stock_projekt/companies.csv')
LOG_FILE = os.getenv('LOG_FILE', "C:/Users/kicki/my_stock_projekt/process.log")
DB_CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING')

def main():
    setup_logging(LOG_FILE)
    logging.info("Starting program...")

    # Read company information from CSV
    logging.info("Reading company data from CSV...")
    company_data = read_company_data(CSV_FILE)
    logging.info(f"Read {len(company_data)} companies from CSV.")
    
    # Load cached stock data
    stock_data_cache = load_cache()  
    new_stock_data = {}

    # Fetch data with retries and exponential backoff
    def fetch_with_retries(ticker: str, cache: dict) -> dict:
        max_retries = 5
        retries = 0
        while retries < max_retries:
            try:
                if ticker in cache:
                    logging.info(f"Using cached data for {ticker}")
                    return cache[ticker]
                else:
                    return fetch_stock_data(ticker, cache)
            except requests.RequestException as e:
                if '429' in str(e):
                    delay = min(60, (2 ** retries) * 5)  # Max wait time is capped at 60 seconds
                    logging.warning(f"Rate limit hit for {ticker}. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    retries += 1
                else:
                    logging.error(f"Failed to fetch {ticker}: {e}")
                    retries += 1
        logging.error(f"Max retries exceeded for {ticker}. Skipping.")
        return None

    # Concurrently fetch stock data in batches with exponential backoff
    def fetch_stock_data_concurrently(tickers, cache):
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_ticker = {executor.submit(fetch_with_retries, ticker, cache): ticker for ticker in tickers}
            for future in concurrent.futures.as_completed(future_to_ticker):
                ticker = future_to_ticker[future]
                try:
                    stock_info = future.result()
                    if stock_info is not None:
                        new_stock_data[ticker] = stock_info
                        logging.info(f"Successfully fetched {ticker}")
                    else:
                        logging.warning(f"No stock data for {ticker}")
                except Exception as e:
                    logging.error(f"Error fetching {ticker}: {e}")

    # Fetch data in batches
    batch_size = 100  
    tickers = [company['Ticker'] for company in company_data]
    for i in range(0, len(tickers), batch_size):
        batch_tickers = tickers[i:i + batch_size]
        fetch_stock_data_concurrently(batch_tickers, stock_data_cache)
        logging.info(f"Fetched batch {i // batch_size + 1}/{len(tickers) // batch_size + 1}")

    # Save new data to cache
    total_cache_data = {**stock_data_cache, **new_stock_data}
    save_cache(total_cache_data)
    logging.info(f"Saved {len(new_stock_data)} new stock data entries to cache")

    # Process and update data in SQL
    logging.info("Processing data and updating SQL...")
    batch_data = []
    
    for company in company_data:
        ticker = company['Ticker']
        if ticker in new_stock_data:
            stock_info = new_stock_data[ticker]
            processed_items = process_data([company], {ticker: stock_info})
            batch_data.extend(processed_items)  

        # Update the SQL table when batch is ready
        if len(batch_data) >= batch_size:
            try:
                update_sql_table(batch_data, DB_CONNECTION_STRING)
                logging.info(f"SQL updated for {len(batch_data)} entries")
            except Exception as sql_error:
                logging.error(f"SQL update failed for batch: {sql_error}")
            batch_data.clear()  # Clear the batch after updating

    # Update any remaining data
    if batch_data:
        try:
            update_sql_table(batch_data, DB_CONNECTION_STRING)
            logging.info(f"SQL updated for the last {len(batch_data)} entries")
        except Exception as sql_error:
            logging.error(f"SQL update failed for final batch: {sql_error}")

    logging.info("All stock data fetched and processed.")
    logging.info("Program completed successfully.")

if __name__ == "__main__":
    main()
