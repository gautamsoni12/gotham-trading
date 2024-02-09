import pandas as pd
import psycopg2
import numpy as np
from service import PGDatabase as postgres

    
DAYS_AGO = 12

STOCKS_TO_TRADE = 4


def calculate_volatility(returns: list) -> float:
    volatility = np.std(returns)
    return volatility   


def get_data():
    # Connect to Postgres database
    conn = psycopg2.connect(database="olympus", user="postgres", password="password", host="127.0.0.1", port="5432")
    cur = conn.cursor()

    # Get data from predicted_data_two table
    cur.execute("SELECT stock_symbol, date, predictions, confidence FROM predicted_data WHERE date = current_date - interval '{} days' order by confidence desc".format(DAYS_AGO))
    data = cur.fetchall()

    # Store data in a dataframe
    df = pd.DataFrame(data, columns=['stock_symbol', "date", 'predictions', 'confidence'])

    # Pick top 10 for trade_decision 1 and top 10 for trade decision -1
    df = df.sort_values(by=['confidence'], ascending=False)
    df1 = df[df['predictions'] == 1].head(STOCKS_TO_TRADE)
    df2 = df[df['predictions'] == -1].head(STOCKS_TO_TRADE)
    
    df = pd.concat([df1, df2])
    print(df.head(20))

    # Get data from technical_indicators_two table
    stock_symbols = ','.join(["'" + symbol + "'" for symbol in df['stock_symbol'].unique()])
    cur.execute("SELECT stock_symbol, date, trade_decision, seven_day_price_diff_percent FROM technical_indicators WHERE stock_symbol IN ({}) AND date = current_date - interval '{} days'".format(stock_symbols, DAYS_AGO))
    data = cur.fetchall()

    # Store data in a dataframe
    df_ti = pd.DataFrame(data, columns=['stock_symbol', 'date', 'trade_decision', 'seven_day_price_diff_percent'])
    print(df_ti.head(20))

    # Merge dataframes
    df = pd.merge(df, df_ti, on='stock_symbol')

    # Create another column called "descrepency"
    df['descrepency'] = df.apply(lambda row: 1 if row['predictions'] == row['trade_decision'] else -1, axis=1)

    # Multiply descrepency and seven_day_price_diff_percent for each row and store it in column called actual return
    df['actual_return'] = df['descrepency'] * abs(df['seven_day_price_diff_percent'])
    
    print(df.head(20))
    
    
    for index, row in df.iterrows():
        cur.execute(
        """
            INSERT INTO stock_data_result (stock_symbol, date, predictions, trade_decision, confidence, seven_day_price_diff, descrepency, actual_return)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (stock_symbol, date) 
            DO UPDATE SET
                predictions = EXCLUDED.predictions,
                trade_decision = EXCLUDED.trade_decision,
                confidence = EXCLUDED.confidence,
                seven_day_price_diff = EXCLUDED.seven_day_price_diff,
                descrepency = EXCLUDED.descrepency,
                actual_return = EXCLUDED.actual_return;
            """,
            (row['stock_symbol'], row['date_x'], row['predictions'], row['trade_decision'], row['confidence'], row['seven_day_price_diff_percent'], row['descrepency'], row['actual_return'])
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Predictions saved to the 'predicted_data' table.")
    
    # Calculate average of actual return and print it
    avg_return = df['actual_return'].mean()
    print("Average return: ", avg_return)
    
    average_volatility = calculate_volatility(df['actual_return'].to_list())
    print("Average volatility: ", average_volatility)
    
    avd_descrepency = df['descrepency'].mean()
    print("Average descrepency: ", avd_descrepency)

    # Close database connection
    cur.close()
    conn.close()


if __name__ == "__main__":
    get_data()

