import pandas as pd
import talib
import numpy as np

def calculate_indicators(stock_data: pd.DataFrame) -> pd.DataFrame:
    # Technical indicators do not exist in the database, calculate and insert them
    rsi = talib.RSI(stock_data['close'], timeperiod=8)
    
    # Calculate Moving Average Convergence Divergence (MACD)
    macd, macdsignal, macdhist = talib.MACD(stock_data['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    
    # Calculate Average Directional Movement Index (ADX)
    adx = talib.ADX(stock_data['high'], stock_data['low'], stock_data['close'])
    
    # # Calculate bollinger band and close price ratio
    # bbands_upper_20, bbands_middle_20, bbands_lower_20 = talib.BBANDS(stock_data['close'], timeperiod=20)
    # bbands_upper, bbands_middle, bbands_lower = bbands_upper_20/stock_data['close'], bbands_middle_20/stock_data['close'], bbands_lower_20/stock_data['close']
    
    # Calculate bollinger band and close price ratio
    bbands_upper_20, bbands_middle_20, bbands_lower_20 = talib.BBANDS(stock_data['close'], timeperiod=20)
    # Convert Decimal object to float
    close_prices = stock_data['close'].astype(float)

    # Divide float by another float
    bbands_upper = np.divide(bbands_upper_20, close_prices)
    bbands_middle = np.divide(bbands_middle_20, close_prices)
    bbands_lower = np.divide(bbands_lower_20, close_prices)
    
    # Calculate Stochastic Oscillator
    stoch, stoch_signal = talib.STOCH(stock_data['high'], stock_data['low'], stock_data['close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    # stoch_15, stoch_signal_15 = talib.STOCH(stock_data['high'], stock_data['low'], stock_data['close'], fastk_period=15, slowk_period=15, slowk_matype=0, slowd_period=15, slowd_matype=0)    
    # stoch, stoch_signal = stoch_5/stoch_15, stoch_signal_5/stoch_signal_15
    
    # Calculate Simple Moving Average (SMA)
    sma_price = talib.SMA(stock_data['close'], timeperiod=5) / talib.SMA(stock_data['close'], timeperiod=20)
    
    # Calculate 200 day exponential moving average
    ema_200 = talib.EMA(stock_data['close'], timeperiod=200)
    
    # Calculate Simple Moving Average (SMA)
    sma_volume = talib.SMA(stock_data['volume'], timeperiod=5) / talib.SMA(stock_data['volume'], timeperiod=20)
    
    # Calculate Average True Range (ATR)
    atr = talib.ATR(stock_data['high'], stock_data['low'], stock_data['close'], timeperiod=5)/talib.ATR(stock_data['high'], stock_data['low'], stock_data['close'], timeperiod=15)

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
    indicator_df['EMA_200'] = ema_200
    
    
    print(indicator_df.tail())

    return indicator_df

def get_data_to_insert(stock_symbol, indicator_df: pd.DataFrame):
        return [(stock_symbol, row['close'], row['date'], row['RSI'], row['MACD'], row['macd_signal_line'], row['ADX'],  
            row['BBands_Upper'], row['BBands_Middle'], row['BBands_Lower'], row['Stoch'], row['SMA_Price'], row['SMA_Volume'], row['ATR'], row['EMA_200'] , row['trade_decision'], row['seven_day_price_diff'], row['seven_day_price_diff_percent']) for index, row in indicator_df.iterrows()]
        
        

        