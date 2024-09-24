import pytest
from csv_reader import read_company_data
import os

def test_read_company_data_sucess(tmpdir):
    # Create a temporary CSV-file with testdata
    csv_file = tmpdir.join("companies.csv")
    csv_file.write("Company,Ticker,Sector\nCompanyA,AAPL,Technology\nCompanyB,GOOGL,Technology")

    # Testing to read CSV-data
    result = read_company_data(str(csv_file))

    assert len(result) == 2, "There should be two companies in the CSV-file"
    assert result[0]['Company'] == "CompanyA", "The Company should be CompanyA"
    assert result[1]['Ticker'] == "GOOGL", "The Company should be GOOGL"

    def test_read_company_data_file_not_found():
        # Test to handel a non existing fil error
        with pytest.raises(FileNotFoundError):
            read_company_data("non_existent_file_csv")