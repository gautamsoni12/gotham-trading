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

    # Generate trading signals based on technical indicators
    indicator_df = pd.DataFrame()

    indicator_df['close'] = stock_data['close']
    indicator_df['date'] = stock_data['date']
    indicator_df['RSI'] = rsi
    indicator_df['MACD'] = macd
    indicator_df['MACD_Signal'] = macdsignal
    indicator_df["macd_signal_line"] = macdsignal
    indicator_df['ADX'] = adx
    indicator_df['BBands_Upper'] = bbands_upper
    indicator_df['BBands_Middle'] = bbands_middle
    indicator_df['BBands_Lower'] = bbands_lower
    indicator_df['Stoch'] = stoch
    indicator_df['Stoch_Signal'] = stoch_signal

    indicator_df['RSI_Signal'] = 0
    indicator_df.loc[rsi > 70, 'RSI_Signal'] = -1  # overbought, sell signal
    indicator_df.loc[rsi < 30, 'RSI_Signal'] = 1   # oversold, buy signal

    indicator_df['MACD_Signal'] = 0
    # bullish crossover, buy signal
    indicator_df.loc[macd > macdsignal, 'MACD_Signal'] = 1  # bullish crossover, buy signal
    indicator_df.loc[macd < macdsignal, 'MACD_Signal'] = -1  # bearish crossover, sell signal

    indicator_df['ADX_Signal'] = 0
    indicator_df.loc[adx > 25, 'ADX_Signal'] = 1  # trend strength, buy signal
    indicator_df.loc[adx < 20, 'ADX_Signal'] = -1  # trend weakness, sell signal

    indicator_df['BBands_Signal'] = 0
    indicator_df.loc[indicator_df['close']< bbands_lower, 'BBands_Signal'] = 1  # oversold, buy signal
    indicator_df.loc[indicator_df['close']> bbands_upper, 'BBands_Signal'] = -1  # overbought, sell signal


    indicator_df['Stoch_Signal'] = 0
    indicator_df.loc[(stoch > 80) & (stoch_signal > 80), 'Stoch_Signal'] = -1  # overbought, sell signal
    indicator_df.loc[(stoch < 20) & (stoch_signal < 20), 'Stoch_Signal'] = 1  # oversold, buy signal

    # # Combine the signals to generate a final trading signal
    # indicator_df['Signal'] = indicator_df['RSI_Signal'] + indicator_df['MACD_Signal']
    return indicator_df


def get_data_to_insert(stock_symbol, indicator_df: pd.DataFrame):
        return [(stock_symbol, row['close'], row['date'], row['RSI'], row['MACD'], row['macd_signal_line'], row['ADX'],  
            row['BBands_Upper'], row['BBands_Middle'], row['BBands_Lower'], row['Stoch'], row['SMA_Price'], row['SMA_Volume'], row['ATR'], row['trade_decision'], row['seven_day_price_diff'], row['seven_day_price_diff_percent']) for index, row in indicator_df.iterrows()]
        