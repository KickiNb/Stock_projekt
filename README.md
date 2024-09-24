# My Stock Project

## Description
This project automates the retrieval of stock data from the Finnhub API and updates an SQL table with that data. The project uses Python and efficiently handles errors and data caching to optimize API requests.

## Features
- Fetches company data from the Finnhub API and saves it to a CSV file.
- Retrieves stock information for companies and stores it in an SQL database.
- Cache functionality to avoid fetching the same data multiple times.
- Automatic logging and error handling.
- Multi-threaded data processing for faster data retrieval.

## Installation

### Requirements
- Python 3.7+
- Finnhub API key
- SQL Server

### Environment Variables
To run this project, you need to configure the following environment variables in a .env file:
```plaintext
FINNHUB_API_KEY=your_finnhub_api_key
DB_CONNECTION_STRING="DRIVER={ODBC Driver 17 for SQL Server};SERVER=YOUR_SERVER;DATABASE=YOUR_DATABASE;Trusted_Connection=yes;"
CSV_FILE="C:/Users/kicki/my_stock_projekt/companies.csv"
LOG_FILE="C:/Users/kicki/my_stock_projekt/process.log"
