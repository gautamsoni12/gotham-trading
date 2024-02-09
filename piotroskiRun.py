import pandas as pd
import psycopg2
from datetime import datetime, timedelta
import time
from strategy import Piotroski as piotroski


def get_shortlisted_stocks(decision: int)-> list:
    
    try:
        conn = psycopg2.connect(database="olympus", user="postgres", password="password", host="127.0.0.1", port="5432")
        # Query to fetch data from the table
        _decision = str(decision)
        query = "Select * from predicted_data_two where predictions={} and date = (SELECT MAX(date) FROM predicted_data_two) order by confidence desc limit 5;".format(_decision)
        
        result = pd.read_sql_query(query, conn)
        conn.commit()

        conn.close()
        stocks = result['stock_symbol'].tolist()
        return stocks
    except Exception as e:
        print(e)
        return []


def get_piotroski(stocks):
    try:
        conn = psycopg2.connect(database="olympus", user="postgres", password="password", host="127.0.0.1", port="5432")
        cursor = conn.cursor()

        for stock in stocks:
            score = piotroski.get_piotroski_score(stock)
            update_query = """
                UPDATE predicted_data_two
                SET piotroski_score={}
                WHERE stock_symbol='{}';
                """.format(score, stock)
            cursor.execute(update_query)
            conn.commit()
            time.sleep(20)
            
        cursor.close()
        conn.close()
    except Exception as e:      
        print(e)
        return []

if __name__ == "__main__":
    # Define a list of stocks for which you want to stream data

    long_stocks = get_shortlisted_stocks(1)
    short_stocks = get_shortlisted_stocks(-1)
    all_stocks = long_stocks + short_stocks
    all_stocks = list(set(all_stocks))
    
    # all_stocks = ['AAPL']
    
    get_piotroski(all_stocks)
