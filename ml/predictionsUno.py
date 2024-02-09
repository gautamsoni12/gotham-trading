import pandas as pd
import psycopg2
import pickle
from datetime import datetime, timedelta
import multiprocessing as mp
import numpy as np

import warnings
warnings.filterwarnings('ignore')

prediction_table = "predicted_data"
strategy_table = "technical_indicators"

# Load the trained model from the pickle file
def get_symbols_from_csv(file_path):
    df = pd.read_csv(file_path)
    symbols = df['Symbol'].tolist()
    return symbols


# Define a function to make predictions and save them to the database
def make_predictions_and_save(stock):
    try:
            # Connect to the PostgreSQL database
        conn = psycopg2.connect(database="olympus", user="postgres", password="password", host="127.0.0.1", port="5432")
        # Calculate the date 2 days ago
        two_days_ago = datetime.today().date() - timedelta(days=10)

        # Query to fetch data from the "technical_indicators" table
        query = """
            SELECT *
            FROM {}
            WHERE stock_symbol = %s AND date > %s
        """.format(strategy_table)

        # Fetch prediction data from PostgreSQL
        prediction_data = pd.read_sql_query(query, conn, params=(stock, two_days_ago,))


        with open('random_forest_model.pkl', 'rb') as f:
            rf_model = pickle.load(f)

        selected_columns = ['rsi_signal', 'macd_signal', 'stoch_signal', 'bbands_signal']
        X_pred = prediction_data[selected_columns]
        X_pred = X_pred.dropna()

        # predicted_class_probabilities = rf_model.predict_proba(X_pred)
        predicted_class_probabilities = np.max(rf_model.predict_proba(X_pred), axis=1)

        
        predictions = rf_model.predict(X_pred)
        
        print(predictions)

        prediction_data.reset_index(drop=True, inplace=True)
        prediction_data['predictions'] = predictions

        # Add predictions to the DataFrame
        
        # Create a new column called 'trade_decision' based on the 'predictions' column
        prediction_data['trade_decision'] = 0
        prediction_data.loc[prediction_data['predictions'] > 0, 'trade_decision'] = 1
        prediction_data.loc[prediction_data['predictions'] < 0, 'trade_decision'] = -1
        
        # Create a new table "predicted_data" to store the predictions
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS {} (
                stock_symbol TEXT,
                date DATE,
                trade_decision NUMERIC,
                predictions NUMERIC,
                confidence NUMERIC,
                PRIMARY KEY (stock_symbol, date)
            )
        """.format(prediction_table))
    
        # Insert the prediction data into the "predicted_data" table
        for index, row in prediction_data.iterrows():
            
            print(row['predictions'], predicted_class_probabilities[index])
            
            cursor.execute(
            """
                INSERT INTO {} (stock_symbol, date, trade_decision, predictions, confidence) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (stock_symbol, date) DO UPDATE SET trade_decision = excluded.trade_decision, predictions = excluded.predictions, confidence = excluded.confidence;""".format(prediction_table),
                (stock, row['date'], row['trade_decision'], row['predictions'], predicted_class_probabilities[index])
            )

        conn.commit()
        cursor.close()
        conn.close()
        print("Predictions saved to the 'predicted_data' table.")

    except Exception as e:
        print("Error making predictions and saving to the database.")
        print(e)

if __name__ == "__main__":
    # Define a list of stocks for which you want to stream data
    
    stocks = get_symbols_from_csv('stock_exchange/nasdaq_screener.csv')

    # stocks = ["AAPL", "GOOG", "MSFT", "TSLA", "AKAM", "T"]

    # Create a multiprocessing pool with the number of processes equal to the number of CPUs
    pool = mp.Pool(processes=20)

    # Map the train_and_test function to the list owith Pool(processes=20) as pool:
    pool.map(make_predictions_and_save, stocks)

    # Close the multiprocessing pool
    pool.close()
    pool.join()  # Wait for all processes to finish
    # Call the function to make predictions and save them to the database

    # Close the database connection
    
