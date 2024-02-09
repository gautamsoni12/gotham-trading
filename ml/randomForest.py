import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error
import psycopg2
from datetime import datetime, timedelta
from sklearn.model_selection import GridSearchCV
import pickle
import multiprocessing as mp
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
strategy_table = "technical_indicators_two"

def get_symbols_from_csv(file_path):
    df = pd.read_csv(file_path)
    symbols = df['Symbol'].tolist()
    return symbols

def get_stock_list():
    query = "SELECT DISTINCT(stock_symbol) FROM stock_daily"
    stock_data = pd.read_sql_query(query, conn)
    list_of_stocks = stock_data['stock_symbol'].tolist()
    return list_of_stocks



def train_and_test(stock, rf_model):
    
    try:
        # with open('random_forest_model.pkl', 'rb') as f:
        #     rf_model = pickle.load(f)
        
        # Query to fetch data from the table
        query = "SELECT * FROM {} WHERE stock_symbol = %s AND date <= %s".format(strategy_table)
        six_months_ago = datetime.today().date() - timedelta(days=20)

        # Split the data into training and testing sets
        X_train = []
        y_train = []
        
        train_data = pd.read_sql_query(query, conn, params=(stock, six_months_ago))
        # print(train_data.head() )
        train_data = train_data.drop(columns=['stock_symbol', 'date' , 'close', 'seven_day_price_diff', 'seven_day_price_diff_percent'])
        train_data.dropna(inplace=True)
        X_train = train_data.drop(columns=['trade_decision'])
        y_train = train_data['trade_decision']

        # Load the test data from PostgreSQL
        query = "SELECT * FROM {} WHERE stock_symbol = %s AND date > %s".format(strategy_table)
        test_data = pd.read_sql_query(query, conn, params=(stock, six_months_ago))
        test_data.dropna(inplace=True) 
        # Split the test data into features and target
        X_test = test_data.drop(columns=['stock_symbol', 'date', 'close', 'seven_day_price_diff', 'seven_day_price_diff_percent'])
        X_test = X_test.drop(columns=['trade_decision'])
        y_test = test_data['trade_decision']

        # Create and train the Random Forest model
        rf_model.fit(X_train, y_train)

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
        
        with open('random_forest_model.pkl', 'wb+') as f:
            pickle.dump(rf_model, f)
    
    except Exception as e:
        print(f"Error processing {stock}")
        error_stocks.append(stock)
        print(e)


if __name__ == "__main__":
    # Define a list of stocks for which you want to stream data    
    stocks = get_stock_list()
    
    rf = RandomForestClassifier(
        n_estimators=42, criterion='gini',
        max_depth=5, min_samples_split=2,
        min_samples_leaf=1, max_features='auto',
        bootstrap=True, oob_score=False, n_jobs=1,
        random_state=None, verbose=0)
    
    
    for i in range(len(stocks)): 
        print(i)
        train_and_test(stocks[i], rf)
    
    # with open('random_forest_model.pkl', 'wb+') as f:
    #         pickle.dump(rf, f)
    # # Create a multiprocessing pool with the number of processes equal to the number of CPUs
    # pool = mp.Pool(processes=20)

    # # Map the train_and_test function to the list owith Pool(processes=20) as pool:
    # pool.map(train_and_test, stocks)
    
    with open('random_forest_model.pkl', 'wb+') as f:
            pickle.dump(rf, f)

    # # Close the multiprocessing pool
    # pool.close()
    # pool.join()  # Wait for all processes to finish
    
    print(error_stocks)
    with open('error_stocks.txt', 'w+') as f:
        for stock in error_stocks:
            f.write(stock + '\n')