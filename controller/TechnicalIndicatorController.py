import pandas as pd
from service import StockData as stock_data_service
from strategy import Strategy
import pandas as pd
from multiprocessing import Pool
import time


def compute_technical_indicators(stock_symbol: str):
    try:
        stock_data_service.get_stock_data(stock_symbol=stock_symbol)
        # tech_indicators_df = Strategy.check_and_calculate_tech_indicators(stock_symbol=stock_symbol)
        tech_indicators_df_2 = Strategy.check_and_calculate_tech_indicators_2_0(stock_symbol=stock_symbol)
    except Exception as e:
        raise Exception(f"Error processing {stock_symbol}: {e}")
    
    
def get_symbols_from_csv(file_path):
    df = pd.read_csv(file_path)
    symbols = df['Symbol'].tolist()
    return symbols

def process_symbol(symbol):
    start_time = time.time()
    try:
        execute_main(symbol)
        print(f"Finished processing {symbol}")
    except Exception as e:
        print(f"Error processing {symbol}")
        print(e)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time for {symbol}: {elapsed_time:.2f} seconds")