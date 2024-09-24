import logging

def process_data(company_data: list, stock_data: dict) -> list:
    """Combine and process stock and company data."""
    processed_data = []
    for company in company_data:
        ticker = company.get('Ticker')
        stock_info = stock_data.get(ticker)

        if stock_info:
            combined_data = {
                'Company': company['Company'],
                'Ticker': ticker,
                'Sector': company.get('Sector', 'Unknown'),
                'Stock Price': stock_info.get('c', 0),  # 'c' is current price in Finnhub API
                'Currency': 'USD'  # Assuming USD for now, adjust as needed
            }
            processed_data.append(combined_data)
            logging.info(f"Processed data for {ticker}")

    return processed_data
