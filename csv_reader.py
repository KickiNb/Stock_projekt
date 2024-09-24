import csv
import logging

def read_company_data(csv_file: str) -> list:
    """Read company data from a CSV file and remove duplicates."""
    try:
        with open(csv_file, mode='r') as file:
            csv_reader = csv.DictReader(file)
            company_data = []
            seen_tickers = set()  # To check for duplicates
            row_count = 0
            duplicate_count = 0

            for row in csv_reader:
                if not any(row.values()):  # Skip empty rows
                    continue
                
                ticker = row['Ticker']
                if ticker in seen_tickers:  # Check duplicates
                    logging.warning(f"Duplicate ticker found: {ticker}. Skipping.")
                    duplicate_count += 1
                    continue

                row['Sector'] = row.get('Sector', 'Unknown')  # If Sector is not known use 'Unknown'
                company_data.append(row)
                seen_tickers.add(ticker)  # add unique tickers
                row_count += 1
            
            logging.info(f"Successfully read {row_count} unique rows from CSV.")
            logging.info(f"Skipped {duplicate_count} duplicate rows.")
            return company_data
        
    except FileNotFoundError as e:
        logging.error(f"CSV file not found: {e}")
        raise
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
        raise
