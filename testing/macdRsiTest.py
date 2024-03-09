import psycopg2
import pandas as pd
import multiprocessing
import numpy as np


def getStockSymbol(date):
        # Query the db - macd_rsi_strategy table from postgres
        query = f"""SELECT * FROM macd_rsi_strategy where date='{date}' and close>10 and close<40 and rsi<30 and macd_trade_decision='1'"""
        
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            host="localhost",
            database="olympus",
            user="postgres",
            password="password"
        )

        # Create a cursor object to execute the query
        cursor = conn.cursor()

        # Execute the query
        cursor.execute(query)

        # Fetch all the rows returned by the query
        rows = cursor.fetchall()
        
        # Get the column names from the cursor description
        column_names = [desc[0] for desc in cursor.description]
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        df = pd.DataFrame(rows, columns=column_names)
        return df['stock_symbol'].to_list()
    

def testMacdRsi(stock_symbol):
    
    try:
        
        date = '2024-02-27'
        # Query the db - macd_rsi_strategy table from postgres
        query = f"""SELECT * FROM macd_rsi_strategy where stock_symbol='{stock_symbol}' and date >= '{date}'"""
        
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            host="localhost",
            database="olympus",
            user="postgres",
            password="password"
        )

        # Create a cursor object to execute the query
        cursor = conn.cursor()

        # Execute the query
        cursor.execute(query)

        # Fetch all the rows returned by the query
        rows = cursor.fetchall()
        
        # Get the column names from the cursor description
        column_names = [desc[0] for desc in cursor.description]
        
        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Convert the rows to a pandas DataFrame
        df = pd.DataFrame(rows, columns=column_names)

        date = pd.to_datetime(date).date()
        # get close value where date = date
        close_value = df[df['date'] == date]['close'].values[0]
        
        # get max of close for next 7 days
        max_close = df[df['date'] > date]['close'].max()
        
        close_diff_percent = ((max_close - close_value) / close_value) * 100
        
        # return close_diff_percent
        
        # if close on the date is less than max of close on next 7 days, then return 1, else 0
        if close_diff_percent > 2:
            return 1
        else:
            return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0
    
    
def getAccuracy(result):
    #return average of array
    return np.mean(result)

if __name__ == "__main__":
    list_of_symbols = getStockSymbol('2024-02-27')
    result = []

    # list_of_symbols = ['AAPL', 'GOOG', 'MSFT', 'TSLA', 'AMZN', 'FB', 'NVDA', 'PYPL', 'ADBE', 'INTC'] 
    # Create a multiprocessing pool with the number of processes equal to the number of symbols
    pool = multiprocessing.Pool(processes=40)

    # # Define a helper function to execute the testMacdRsi function for each symbol
    # def process_symbol(stock_symbol):
    #     value = testMacdRsi( stock_symbol)
    #     return value

    # Use the multiprocessing pool to map the process_symbol function to each symbol in parallel
    result = pool.map(testMacdRsi, list_of_symbols)

    # Close the multiprocessing pool
    pool.close()
    pool.join()

    print(getAccuracy(result))