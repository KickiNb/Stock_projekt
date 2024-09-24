import pyodbc
import logging

def update_sql_table(data: list, connection_string: str):
    """Update the SQL table with the processed data."""
    conn = None
    try:
        logging.info("Connecting to database...")
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        logging.info("Connection successful.")

        # Insert data in batches
        batch_size = 100
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            cursor.executemany("""
                INSERT INTO StockTable (Company, Ticker, Sector, StockPrice, Currency)
                VALUES (?, ?, ?, ?, ?)
            """, [(item['Company'], item['Ticker'], item['Sector'], item['Stock Price'], item['Currency']) for item in batch])

            conn.commit()
            logging.info(f"Successfully inserted batch {i // batch_size + 1}.")

    except pyodbc.Error as e:
        logging.error(f"Error inserting data into SQL: {e}")
        raise
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed.")