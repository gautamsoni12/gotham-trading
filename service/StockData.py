from service import PGDatabase
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
from queries import StockDataQueries as sdq


def get_stock_data(stock_symbol: str) -> pd.DataFrame:
    result = PGDatabase.executeQuery(sdq.CREATE_TABLE_IF_NOT_QUERY, "CREATE")
    # Get the latest date in the database
    SELECT_MAX_DATE_QUERY = "SELECT MAX(date) from stock_daily where stock_symbol='{}'".format(
        stock_symbol)
    max_date_int = PGDatabase.executeQuery(SELECT_MAX_DATE_QUERY, "SELECT")
    max_date_int = (max_date_int[0][0])
    if (max_date_int == None):
        start_date = datetime.now() - timedelta(1095)
        start_date = start_date.date()
    else:
        start_date = max_date_int
    # Get historical data from yfinance
    stock_data = yf.download(stock_symbol, start=start_date)
    # print(stock_data.tail(10))
    
    data_to_insert = [(index.date(), stock_symbol,) + tuple(row) for index, row in stock_data.iterrows()]
    
    PGDatabase.executeMany(sdq.INSERT_NEW_DATA, data_to_insert)
    