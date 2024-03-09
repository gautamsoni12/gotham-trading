from service import StockData as stock_data_service
from strategy import MacdRsi as macd_rsi_strategy
from strategy import Strategy
import pandas as pd
from multiprocessing import Pool
import time


def execute_main(stock_symbol: str):
    stock_data_service.get_stock_data(stock_symbol=stock_symbol)
    # tech_indicators_df = Strategy.check_and_calculate_tech_indicators(stock_symbol=stock_symbol)
    tech_indicators_df_2 = Strategy.check_and_calculate_tech_indicators_2_0(stock_symbol=stock_symbol)
    macd_rsi_strategy_result = macd_rsi_strategy.macd_rsi_signal(stock_data=tech_indicators_df_2, stock_symbol=stock_symbol)
    
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
    list_of_symbols = get_symbols_from_csv('stock_exchange/nasdaq_screener_1709687949672.csv')
    # list_of_symbols.reverse()
    # list_of_symbols = [ 'AAPL']
    # print(list_of_symbols)
    with Pool(processes=40) as pool:
        pool.map(process_symbol, list_of_symbols)
