from service.database import postgres
from datetime import datetime, timedelta
import pandas as pd
import talib
from constants import sql_queries as sq
from psycopg2 import sql
from scipy import stats
from constants import  sql_tech_indicators as sti
import time

def calculate_indicators(stock_data: pd.DataFrame) -> pd.DataFrame:
    # Technical indicators do not exist in the database, calculate and insert them
    rsi = talib.RSI(stock_data['close'], timeperiod=14)
    macd, macdsignal, macdhist = talib.MACD(
            stock_data['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    adx = talib.ADX(
            stock_data['high'], stock_data['low'], stock_data['close'])
    bbands_upper, bbands_middle, bbands_lower = talib.BBANDS(
            stock_data['close'], timeperiod=20)
    stoch, stoch_signal = talib.STOCH(stock_data['high'], stock_data['low'], stock_data['close'],
                                          fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    
    # Calculate Simple Moving Average (SMA)
    sma_price = talib.SMA(stock_data['close'], timeperiod=20)
    sma_volume = talib.SMA(stock_data['volume'], timeperiod=20)
    
    # Calculate Average True Range (ATR)
    atr = talib.ATR(stock_data['high'], stock_data['low'], stock_data['close'], timeperiod=14)

    # Generate trading signals based on technical indicators
    indicator_df = pd.DataFrame()

    indicator_df['close'] = stock_data['close']
    indicator_df['date'] = stock_data['date']
    indicator_df['RSI'] = rsi
    indicator_df['MACD'] = macd
    indicator_df["macd_signal_line"] = macdsignal
    indicator_df['ADX'] = adx
    indicator_df['BBands_Upper'] = bbands_upper
    indicator_df['BBands_Middle'] = bbands_middle
    indicator_df['BBands_Lower'] = bbands_lower
    indicator_df['Stoch'] = stoch
    indicator_df['SMA_Price'] = sma_price
    indicator_df['SMA_Volume'] = sma_volume
    indicator_df['ATR'] = atr

    return indicator_df

def get_data_to_insert(stock_symbol, indicator_df: pd.DataFrame):
        return [(stock_symbol, row['close'], row['date'], row['RSI'], row['MACD'], row['macd_signal_line'], row['ADX'],  
            row['BBands_Upper'], row['BBands_Middle'], row['BBands_Lower'], row['Stoch'], row['SMA_Price'], row['SMA_Volume'], row['ATR'], row['trade_decision'], row['seven_day_price_diff'], row['seven_day_price_diff_percent']) for index, row in indicator_df.iterrows()]