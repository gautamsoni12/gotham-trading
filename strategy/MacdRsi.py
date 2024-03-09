import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from service import PGDatabase as postgres

# from scipy.stats import linregress

def macd_rsi_signal(stock_data, stock_symbol):
    try:
        stock_data['stock_symbol'] = stock_symbol
        # get macd, macd_signal, and 200 day exponential moving average from stock data
        macd_df = macd_signal(stock_data)
        rsi_df = rsi_signal(stock_data)
        
        # merge macd and rsi dataframes
        merged_df = pd.merge(macd_df, rsi_df, on=['stock_symbol', 'date', 'close'], how='inner')
        
        # calculate the final trade decision
        merged_df['final_trade_decision'] = merged_df['macd_trade_decision'] + merged_df['rsi_trade_decision']
        
        # map 2 to 1, -2 to -1, and 0 to 0
        merged_df['final_trade_decision'] = merged_df['final_trade_decision'].map({2: 1, 1: 0, -1: 0, -2: -1, 0: 0})
        
        data_to_insert = get_data_to_insert(stock_symbol, merged_df)
        save_to_postgres(data_to_insert)
        
        return merged_df
    except Exception as e:
        print(e)
        return None


def macd_signal(stock_data):
    # get macd, macd_signal, and 200 day exponential moving average from stock data
    macd_df = stock_data[['stock_symbol','date', 'close', 'MACD', 'macd_signal_line', 'EMA_200' ]].copy()

    # sort the dataframe by date in descending order
    macd_df = macd_df.sort_values(by='date', ascending=True)
    
    # Calculate MACD slope and MACD signal slope for the last 5 days
    macd_df['macd_slope'] = macd_df.groupby('stock_symbol')['MACD'].rolling(window=5).apply(calculate_slope, raw=False).reset_index(level=0, drop=True)
    macd_df['macd_signal_slope'] = macd_df.groupby('stock_symbol')['macd_signal_line'].rolling(window=5).apply(calculate_slope, raw=False).reset_index(level=0, drop=True)

    # check if macd is greater than macd_signal and close price is greater than 200 day exponential moving average
    macd_df['macd_trade_decision'] = (macd_df['MACD'] > macd_df['macd_signal_line']) & (macd_df['close'] < macd_df['EMA_200']) & (macd_df['macd_slope'] > 0) & (macd_df['macd_signal_slope'] > 0)
    
    # map True to 1 and False to -1
    macd_df['macd_trade_decision'] = macd_df['macd_trade_decision'].map({True: 1, False: -1})
    
    print(macd_df)
    
    return macd_df


def rsi_signal(stock_data):
    try:
        # get macd, macd_signal, and 200 day exponential moving average from stock data
        rsi_df = stock_data[['stock_symbol','date', 'close', 'RSI', 'BBands_Lower', 'BBands_Middle', 'BBands_Upper' ]].copy()
        
        rsi_df['rsi_trade_decision'] = 0
        
        rsi_df['rsi_trade_decision'] = rsi_df.apply(rsi_trade_decision, axis=1)
        
        return rsi_df
    except Exception as e:
        print(e)
        return None

def rsi_trade_decision(row):
    try:
        if row['RSI'] < 30 and row['close'] < row['BBands_Lower']:
            return 1
        elif row['RSI'] > 70 and row['close'] > row['BBands_Upper']:
            return -1
        else:
            return 0  # You might want to handle other cases
    except Exception as e:
        print(e)
        return 0
    
def calculate_slope(series):
    x = np.array(range(len(series)))
    slope = ((len(series) * np.sum(x * series)) - (np.sum(x) * np.sum(series))) / ((len(series) * np.sum(x ** 2)) - (np.sum(x) ** 2))
    return slope

def get_data_to_insert(stock_symbol, indicator_df: pd.DataFrame):
        return [(stock_symbol, row['close'], row['date'], row['MACD'], row['macd_signal_line'], row['EMA_200'], row['RSI'],  
            row['BBands_Lower'], row['BBands_Middle'], row['BBands_Upper'], row['macd_slope'], row['macd_signal_slope'], row['macd_trade_decision'], row['rsi_trade_decision'], row['final_trade_decision'] ) for index, row in indicator_df.iterrows()]
        

def save_to_postgres(data_to_insert):
    
    query = """
                INSERT INTO macd_rsi_strategy (stock_symbol, close, date, MACD, macd_signal_line, EMA_200, RSI, BBands_Lower, BBands_Middle, BBands_Upper,  macd_slope, macd_signal_slope, macd_trade_decision, rsi_trade_decision, final_trade_decision)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (stock_symbol, date) DO UPDATE SET
                close = excluded.close,
                RSI = excluded.RSI,
                MACD = excluded.MACD,
                macd_signal_line = excluded.macd_signal_line,
                EMA_200 = excluded.EMA_200,
                BBands_Upper = excluded.BBands_Upper,
                BBands_Middle = excluded.BBands_Middle,
                BBands_Lower = excluded.BBands_Lower,
                macd_slope = excluded.macd_slope,
                macd_signal_slope = excluded.macd_signal_slope
            """
    
    insert_result = postgres.executeMany(query,  data_to_insert)
    print(insert_result)

if __name__ == "__main__":
    # Create a sample dataframe
    data = {
        'stock_symbol': ['AAPL', 'AAPL', 'AAPL', 'AAPL', 'AAPL', 'AAPL', 'AAPL', 'AAPL', 'AAPL', 'AAPL'],
        'date': ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05', '2022-01-06', '2022-01-07', '2022-01-08', '2022-01-09', '2022-01-10'],
        'close': [100, 105, 98, 110, 102, 95, 108, 99, 103, 107],
        'macd': [5, 6, 4, 7, 3, 2, 8, 6, 4, 7],
        'macd_signal': [True, True, False, True, False, True, True, False, True, False],
        'ema_200': [95, 97, 96, 100, 98, 94, 99, 97, 96, 101],
        'rsi': [60, 70, 30, 80, 40, 50, 90, 20, 75, 65],
        'bbands_lower': [90, 95, 85, 100, 95, 90, 105, 80, 95, 90],
        'bbands_middle': [100, 105, 95, 110, 105, 100, 115, 90, 105, 100],
        'bbands_upper': [110, 115, 105, 120, 115, 110, 125, 100, 115, 110]
    }
    stock_data = pd.DataFrame(data)
    
    # Call the macd_signal function with the sample dataframe
    result = macd_rsi_signal(stock_data, 'AAPL')
    
    # Print the result
    print(result)
    
    # # Create a sample dataframe for rsi_signal
    # rsi_data = {
    #     'stock_symbol': ['AAPL', 'AAPL', 'AAPL', 'AAPL', 'AAPL', 'AAPL', 'AAPL', 'AAPL', 'AAPL', 'AAPL'],
    #     'date': ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05', '2022-01-06', '2022-01-07', '2022-01-08', '2022-01-09', '2022-01-10'],
    #     'close': [100, 105, 98, 110, 102, 95, 108, 99, 103, 107],
    #     'rsi': [60, 70, 30, 80, 40, 50, 90, 20, 75, 65],
    #     'bbands_lower': [90, 95, 85, 100, 95, 90, 105, 80, 95, 90],
    #     'bbands_middle': [100, 105, 95, 110, 105, 100, 115, 90, 105, 100],
    #     'bbands_upper': [110, 115, 105, 120, 115, 110, 125, 100, 115, 110]
    # }
    # rsi_df = pd.DataFrame(rsi_data)
    
    # result = rsi_signal(rsi_df)
    
    # print(result)