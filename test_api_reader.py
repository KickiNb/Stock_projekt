import pytest
from api_reader import fetch_stock_data

def test_fetch_stock_data():
    symbol = "TSLA"
    result = fetch_stock_data(symbol)
    assert isinstance(result, dict), "Data should be returned as a dictionary"
    assert 'c' in result, "Response should contain the current stock price"

