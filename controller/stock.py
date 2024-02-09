import datetime
from service import PGDatabase as pg
from queries import UIQueries as ui_queries
import json
import pandas as pd

def getStockPredictions(max_results, filterValue, maxPrice, startDate, endDate):
    if filterValue!=0:
        query = ui_queries.GET_PREDICTIONS_WITH_VALUE.format(startDate, endDate, maxPrice, filterValue, max_results  )
    else:
        query = ui_queries.GET_PREDICTIONS_WITHOUT_VALUE.format(startDate, endDate, maxPrice, max_results)
    stocks = pg.executeQueryWithReturn(query, 'SELECT')
    return stocks

def getStockData(symbol):
    try:
        query = ui_queries.GET_STOCK_DATA.format(symbol)
        stockData = pg.executeQueryWithReturn(query, 'SELECT')
        return stockData
    except Exception as e:
        print(e)
    
def getPredictionResults():
    try:
        query = ui_queries.GET_PREDICTION_RESULT
        # Execute the query and fetch the results
        predictions = pg.executeQueryWithReturn(query, 'SELECT')

        # Convert the result set into a DataFrame
        df = pd.DataFrame(predictions)

        # Drop columns with NaN values
        df = df.dropna(axis=0)

        # Convert the DataFrame back into a list of dictionaries
        predictions = df.to_dict('records')
        return predictions

    except Exception as e:
        print(e)
        
        
def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()