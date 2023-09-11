from service import StockData as stock_data_service
from strategy import Strategy
import pandas as pd
from multiprocessing import Pool
import time

def execute_main(stock_symbol: str):
    stock_data_service.get_stock_data(stock_symbol=stock_symbol)
    tech_indicators_df = Strategy.check_and_calculate_tech_indicators(stock_symbol=stock_symbol)
    # piotroski_score = fundamental_indicator_service.get_piotroski_score(stock_symbol=stock_symbol)
    

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


if __name__ == '__main__':
    list_of_symbols = get_symbols_from_csv('stock_exchange/nasdaq_screener.csv')
    list_of_symbols.reverse()
    with Pool(processes=20) as pool:
        pool.map(process_symbol, list_of_symbols)
