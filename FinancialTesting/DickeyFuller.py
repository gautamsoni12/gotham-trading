from __future__ import print_function
import statsmodels.tsa.stattools as ts
from datetime import datetime
import pandas as pd
import psycopg2
from numpy import cumsum, log, polyfit, sqrt, std, subtract
from numpy.random import randn

conn = psycopg2.connect(database="olympus", user="postgres", password="password", host="127.0.0.1", port="5432")
query = "SELECT * FROM stock_daily WHERE stock_symbol = %s"

def hurst(data_ts):
    """Returns the Hurst Exponent of the time series vector ts"""
    
    print(data_ts)
    # Create the range of lag values
    lags = range(2, 100)
    # Calculate the array of the variances of the lagged differences
    tau = [sqrt(std(subtract(data_ts[lag:], data_ts[:-lag]))) for lag in lags]
    # Use a linear fit to estimate the Hurst Exponent
    poly = polyfit(log(lags), log(tau), 1)
    # Return the Hurst exponent from the polyfit output
    return poly[0]*2.0

def getDickeyFullerScore(data_ts):

    # Output the results of the Augmented Dickey-Fuller test for Amazon
    # with a lag order value of 1
    return ts.adfuller(data_ts, 1)
    
    

if __name__ == "__main__":
    symbol = "AMZN"
    
    stock_data = pd.read_sql_query(query, conn, params=(symbol,))
    stock_data = pd.DataFrame(stock_data, columns=['stock_symbol', 'adj_close', 'close', 'date', 'high', 'low', 'open', 'volume'])
    # Create a Gometric Brownian Motion, Mean-Reverting and Trending Series
    
    print(stock_data.tail(10))
    
    adj_close = stock_data['adj_close'].reset_index(drop=True)
    
    result = getDickeyFullerScore(adj_close)
    
    
    gbm = log(cumsum(randn(100000))+1000)
    mr = log(randn(100000)+1000)
    tr = log(cumsum(randn(100000)+1)+1000)
    # Output the Hurst Exponent for each of the above series
    # and the price of Amazon (the Adjusted Close price) for
    # the ADF test given above in the article
    print("Hurst(GBM): %s" % hurst(gbm))
    print("Hurst(MR): %s" % hurst(mr))
    print("Hurst(TR): %s" % hurst(tr))

    # Assuming you have run the above code to obtain ’amzn’!
    print("Hurst(AMZN): %s" % hurst(adj_close.tolist()))