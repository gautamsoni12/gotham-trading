from service import PGDatabase as postgres
import pandas as pd

def get_stock_data(stock_symbol: str) -> pd.DataFrame:
    query = "SELECT * FROM stock_daily WHERE stock_symbol = %s"
    stock_data = postgres.executeQuery(query, "SELECT", (stock_symbol,))
    stock_data = pd.DataFrame(stock_data, columns=['stock_symbol', 'adj_close', 'close', 'date', 'high', 'low', 'open', 'volume'])
    return stock_data


def trade_decision(indicator_df: pd.DataFrame) -> pd.DataFrame:
    
    # indicator_df = indicator_df.sort_values(by='date', ascending=False)
    # Use last 2 days to determine buy or sell decision
    indicator_df['7_day_close'] = indicator_df['close'].shift(-7)
    indicator_df['seven_day_price_diff'] = indicator_df['7_day_close'] - indicator_df['close']

    # Convert Decimal to float before performing the multiplication
    indicator_df['seven_day_price_diff_percent'] = (
        ((indicator_df['7_day_close'] - indicator_df['close']).astype(float) / indicator_df['close'].astype(float)) * 100)

    indicator_df['seven_day_price_diff_percent'] = indicator_df['seven_day_price_diff_percent'].round(2)
    # Create a new column 'trade_decision' based on the comparison of 'close' and 'next_day_close'
    indicator_df['trade_decision'] = 0  # Default decision

    # Set buy decision based on the condition
    indicator_df.loc[indicator_df['seven_day_price_diff_percent'] > 2, 'trade_decision'] = 1
    indicator_df.loc[indicator_df['seven_day_price_diff_percent'] < -2, 'trade_decision'] = -1

    # Drop the 'next_day_close' column if you don't need it anymore
    indicator_df.drop(columns=['7_day_close'], inplace=True)
    
    return indicator_df


