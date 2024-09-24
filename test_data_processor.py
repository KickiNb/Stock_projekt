from data_processor import process_data

def test_process_data():
    company_data = [
        {'Company': 'CompanyA', 'Ticker': 'AAPL', 'Sector': 'Technology' },
        {'Company': 'CompanyB', 'Ticker': 'GOOGL', 'Sector': 'Technology' }
    ]

    stock_data = {
        'AAPL': {'c': 200},
        'GOOGL': {'c': 150}
    }

    # Run process_data function
    result = process_data(company_data, stock_data)

    assert len(result) == 2, "There sholud be two companies in the result"
    assert result[0]['Stock Price'] == 200, "AAPL:s stockprice should be 200"
    assert result[1]['Stock Price'] == 150, "GOOGL:s stockprice should be 150"