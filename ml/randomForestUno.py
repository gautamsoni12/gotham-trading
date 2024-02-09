import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error
import psycopg2
from datetime import datetime, timedelta
from sklearn.model_selection import RandomizedSearchCV as RSCV
import pickle
import multiprocessing as mp
import numpy as np
import csv
import psycopg2
import warnings


error_stocks = []
database="olympus"
user="postgres"
password="password"
host="127.0.0.1"
port="5432"


warnings.filterwarnings('ignore')
conn = psycopg2.connect(database="olympus", user="postgres", password="password", host="127.0.0.1", port="5432")
strategy_table = "technical_indicators"


def get_stock_list():
    query = "SELECT DISTINCT(stock_symbol) FROM stock_daily"
    stock_data = pd.read_sql_query(query, conn)
    list_of_stocks = stock_data['stock_symbol'].tolist()
    return list_of_stocks


def train_model(stock, rf_model):
    try:
        # with open('random_forest_model.pkl', 'rb') as f:
        #     rf_model = pickle.load(f)
        
        # Query to fetch data from the table
        query = "SELECT * FROM {} WHERE stock_symbol = %s AND date <= %s".format(strategy_table)
        six_months_ago = datetime.today().date() - timedelta(days=30)

        # Split the data into training and testing sets
        X_train = []
        y_train = []
        
        
        indicators_data_train = pd.read_sql_query(query, conn, params=(stock, six_months_ago))
        selected_columns = ['rsi_signal', 'macd_signal', 'stoch_signal', 'bbands_signal', 'trade_decision']
        
        train_data = indicators_data_train[selected_columns]
        train_data.dropna(inplace=True)
        X_train = train_data.drop(columns=['trade_decision'])
        y_train = indicators_data_train['trade_decision']
        
        print(train_data.tail())
        print(len(train_data))

        # Create and train the Random Forest model
        rf_model.fit(X_train, y_train)
    
    except Exception as e:
        print(f"Error processing {stock}")
        error_stocks.append(stock)
        print(e)


def test_model(stock, rf_model):
    try:

        six_months_ago = datetime.today().date() - timedelta(days=30)
        # Load the test data from PostgreSQL
        query = "SELECT * FROM {} WHERE stock_symbol = %s AND date > %s".format(strategy_table)
        indicators_data_test = pd.read_sql_query(query, conn, params=(stock, six_months_ago))
        indicators_data_test.dropna(inplace=True) 
        
        # Split the test data into features and target
        selected_columns = ['rsi_signal', 'macd_signal', 'stoch_signal', 'bbands_signal', 'trade_decision']
        X_test = indicators_data_test[selected_columns]
        X_test = X_test.drop(columns=['trade_decision'])
        y_test = indicators_data_test['trade_decision']
        
        print(indicators_data_test.tail())
        print(len(indicators_data_test))

        # Test the model
        y_pred = rf_model.predict(X_test)
        
        accuracy = rf_model.score(X_test, y_test)
        print(f"Accuracy for {stock}: {accuracy}")

        # Calculate the mean squared error (MSE) as a measure of model performance
        mse = mean_squared_error(y_test, y_pred)
        print(f"Mean Squared Error for {stock}: {mse}")
        with open('mse.csv', mode='a+') as mse_file:
            mse_writer = csv.writer(mse_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            mse_writer.writerow([stock, mse, accuracy])

    except Exception as e:
        print(f"Error processing {stock}")
        error_stocks.append(stock)
        print(e)


# def train_and_test(stock, rf_model):
    
#     try:
#         # with open('random_forest_model.pkl', 'rb') as f:
#         #     rf_model = pickle.load(f)
        
#         # Query to fetch data from the table
#         query = "SELECT * FROM {} WHERE stock_symbol = %s AND date <= %s".format(strategy_table)
#         six_months_ago = datetime.today().date() - timedelta(days=10)

#         # Split the data into training and testing sets
#         X_train = []
#         y_train = []
        
#         indicators_data_train = pd.read_sql_query(query, conn, params=(stock, six_months_ago))
#         selected_columns = ['rsi_signal', 'macd_signal', 'stoch_signal', 'bbands_signal', 'trade_decision']
#         train_data = indicators_data_train[selected_columns]
#         train_data.dropna(inplace=True)
#         X_train = train_data.drop(columns=['trade_decision'])
#         y_train = indicators_data_train['trade_decision']

#         # Load the test data from PostgreSQL
#         query = "SELECT * FROM {} WHERE stock_symbol = %s AND date > %s".format(strategy_table)
#         indicators_data_test = pd.read_sql_query(query, conn, params=(stock, six_months_ago))
#         indicators_data_test.dropna(inplace=True) 
        
#         # Split the test data into features and target
#         X_test = indicators_data_test[selected_columns]
#         X_test = X_test.drop(columns=['trade_decision'])
#         y_test = indicators_data_test['trade_decision']

#         # Create and train the Random Forest model
#         rf_model.fit(X_train, y_train)

#         # Test the model
#         y_pred = rf_model.predict(X_test)
        
#         accuracy = rf_model.score(X_test, y_test)
#         print(f"Accuracy for {stock}: {accuracy}")

#         # Calculate the mean squared error (MSE) as a measure of model performance
#         mse = mean_squared_error(y_test, y_pred)
#         print(f"Mean Squared Error for {stock}: {mse}")
#         with open('mse.csv', mode='a+') as mse_file:
#             mse_writer = csv.writer(mse_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#             mse_writer.writerow([stock, mse, accuracy])
        
#         with open('random_forest_model.pkl', 'wb+') as f:
#             pickle.dump(rf_model, f)
    
#     except Exception as e:
#         print(f"Error processing {stock}")
#         error_stocks.append(stock)
#         print(e)


if __name__ == "__main__":
    # Define a list of stocks for which you want to stream data    
    stocks = get_stock_list()
    # stocks = ['AAPL', 'GOOG', 'MSFT', 'TSLA', 'AKAM', 'T']
    
    param_grid = {'n_estimators':np.arange(50,100,15),
              'max_features':np.arange(0.1, 1, 0.1),
              'max_depth': [3, 5, 7, 9],
              'max_samples': [0.3, 0.5, 0.8]}

    # rf = RSCV(RandomForestClassifier(), param_grid, n_iter = 2)
    
    rf = RandomForestClassifier(
        n_estimators=100, criterion='gini',
        max_depth=7, min_samples_split=2,
        min_samples_leaf=2, max_features='auto',
        bootstrap=True, oob_score=True, n_jobs=-1,
        random_state=None, verbose=0)
    
    
    for i in range(len(stocks)): 
        train_model(stocks[i], rf)
        
    # rf = rf.best_estimator_
    
    with open('random_forest_model.pkl', 'wb+') as f:
            pickle.dump(rf, f)
        
    for i in range(len(stocks)): 
        print(i)
        test_model(stocks[i], rf)
    
    print(error_stocks)
    with open('error_stocks.txt', 'w+') as f:
        for stock in error_stocks:
            f.write(stock + '\n')