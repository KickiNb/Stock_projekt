from unittest import mock
from sql_updater import update_sql_table

@mock.patch('pyodbc.connect')
def test_update_sql_table(mock_connect):
    # Mock a SQL connection and cursor
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn 

    # Testdata for SQL-update
    processed_data = [
        {'Company': 'CompanyA', 'Ticker': 'AAPL', 'Sector': 'Technology', 'Stock Price': 200, 'Currency': 'USD'},
        {'Company': 'CompanyB', 'Ticker': 'GOOGL', 'Sector': 'Technology', 'Stock Price': 150, 'Currency': 'USD'}
    ]

    # Call update_sql_table with mocked connection
    update_sql_table(processed_data, "fake_connection_string")

    # Verify that the SQL short commando was called twice (for two companies)
    assert mock_cursor.execute.call_count == 2  # Check that execute is called twice
    mock_conn.commit.assert_called_once()  # Check that commit is called once
    mock_conn.close.assert_called_once()  # Check that connection closed