from strategy import Helper, StrategyUno, StrategyDos
from queries import TradingSignalQueries, StrategyUnoQueries, StrategyDosQueries
from service import PGDatabase as postgres
import pandas as pd



def check_and_calculate_tech_indicators(stock_symbol: str) -> pd.DataFrame:
    # Only include the last 120 rows of data
    stock_data = Helper.get_stock_data(stock_symbol)

    indicator_df = StrategyUno.calculate_indicators(stock_data)
    indicator_df = Helper.trade_decision(indicator_df)
    try:
        result = postgres.executeQuery(StrategyUnoQueries.create_technical_indicators_table, "CREATE")
    except Exception as e:
        print(f"Error creating table: {e}")
    
    # data_to_insert = [(stock_symbol,) + tuple(row) for index, row in indicator_df.iterrows()]
    
    data_to_insert = StrategyUno.get_data_to_insert(stock_symbol, indicator_df)

    try:
        insert_result = postgres.executeMany(StrategyUnoQueries.update_technical_indicators_table, data_to_insert)
    except Exception as e:
        print(f"Error inserting data: {e}")

    indicator_df = calculateSignal(indicator_df)

    return indicator_df



def calculateSignal(stock_symbol:str, indicator_df: pd.DataFrame) -> pd.DataFrame:
    # Replace NaN values with 0
    indicator_df.fillna(0, inplace=True)

    # Reset the index of indicator_df
    indicator_df.reset_index(inplace=True)

    indicator_df['Signal'] = indicator_df['RSI_Signal'] + indicator_df['MACD_Signal']
    signals_df = pd.DataFrame()
    signals_df['stock_symbol'] = [stock_symbol] * len(indicator_df)
    signals_df['date'] = indicator_df['date']
    signals_df['buy_signal'] = (indicator_df['Signal'] == 2) & (indicator_df['RSI'] < 30)
    signals_df['sell_signal'] = (indicator_df['Signal'] == -2) & (indicator_df['RSI'] > 70)

    try:
        result = postgres.executeQuery(TradingSignalQueries.create_trading_signals_table, "CREATE")
    except Exception as e:
        print(f"Error creating table: {e}")
    
    data = [(row['stock_symbol'], row['date'], row['buy_signal'], row['sell_signal']) for index, row in signals_df.iterrows()]
    try:
        insert_result = postgres.executeMany(TradingSignalQueries.update_trading_signals_table, data)
    except Exception as e:
        print(f"Error inserting data: {e}")

    return indicator_df
