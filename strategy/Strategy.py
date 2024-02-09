from strategy import Helper, StrategyUno as CurrentStrategy
from strategy import StrategyDos
from queries import TradingSignalQueries, StrategyUnoQueries as CurrentStrategyQueries
from queries import StrategyDosQueries
from service import PGDatabase as postgres
import pandas as pd


def check_and_calculate_tech_indicators(stock_symbol: str) -> pd.DataFrame:
    # Only include the last 120 rows of data
    stock_data = Helper.get_stock_data(stock_symbol)

    indicator_df = CurrentStrategy.calculate_indicators(stock_data)
    indicator_df = Helper.trade_decision(indicator_df)
    
    # update_trade_decision(stock_symbol, indicator_df)
    
    try:
        result = postgres.executeQuery(CurrentStrategyQueries.create_technical_indicators_table, "CREATE")
    except Exception as e:
        print(f"Error creating table: {e}")
        
    data_to_insert = CurrentStrategy.get_data_to_insert(stock_symbol, indicator_df)
    try:
        insert_result = postgres.executeMany(CurrentStrategyQueries.update_technical_indicators_table, data_to_insert)
    except Exception as e:
        print(f"Error inserting data: {e}")

    # indicator_df = calculateSignal(stock_symbol, indicator_df)

    return indicator_df


def check_and_calculate_tech_indicators_2_0(stock_symbol: str) -> pd.DataFrame:
    # Only include the last 120 rows of data
    stock_data = Helper.get_stock_data(stock_symbol)

    indicator_df_2 = StrategyDos.calculate_indicators(stock_data)
    indicator_df_2 = Helper.trade_decision(indicator_df_2)
    
    update_trade_decision_2_0(stock_symbol, indicator_df_2)
    
    try:
        result = postgres.executeQuery(StrategyDosQueries.create_technical_indicators_table, "CREATE")
    except Exception as e:
        print(f"Error creating table: {e}")
        
    data_to_insert = StrategyDos.get_data_to_insert(stock_symbol, indicator_df_2)
    try:
        insert_result = postgres.executeMany(StrategyDosQueries.update_technical_indicators_table, data_to_insert)
    except Exception as e:
        print(f"Error inserting data: {e}")

    # indicator_df_2 = calculateSignal(stock_symbol, indicator_df_2)

    return indicator_df_2



def get_trade_decision_data_to_insert(stock_symbol, indicator_df: pd.DataFrame):
        return [(stock_symbol, row['date'], row['trade_decision'], row['seven_day_price_diff'], row['seven_day_price_diff_percent']) for index, row in indicator_df.iterrows()]


def update_trade_decision(stock_symbol: str, indicator_df: pd.DataFrame ):
    try:
        insert_result = postgres.executeMany(CurrentStrategyQueries.update_trade_decision, get_trade_decision_data_to_insert(stock_symbol, indicator_df))
    except Exception as e:
        print("Error making trade decision and saving to the database.")
        print(e)
        
def update_trade_decision_2_0(stock_symbol: str, indicator_df: pd.DataFrame ):
    try:
        insert_result = postgres.executeMany(StrategyDosQueries.update_trade_decision, get_trade_decision_data_to_insert(stock_symbol, indicator_df))
    except Exception as e:
        print("Error making trade decision and saving to the database.")
        print(e)