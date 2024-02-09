

def checkMACDSignal(stock_data):
    # macd line crosses signal below 0 and closing price is above 200 day moving average - buy
    if stock_data['macd'][-1] > stock_data['signal'][-1] and stock_data['macd'][-2] < stock_data['signal'][-2] and stock_data['macd'][-1] < 0 and stock_data['close'][-1] > stock_data['sma200'][-1]:
        return 1
    # macd line crosses signal above 0 and closing price is below 200 day moving average - sell
    elif stock_data['macd'][-1] < stock_data['signal'][-1] and stock_data['macd'][-2] > stock_data['signal'][-2] and stock_data['macd'][-1] > 0 and stock_data['close'][-1] < stock_data['sma200'][-1]:
        return -1
    else:
        return 0
 
 
def checkRSISignal(stock_data):
    # rsi is below 30 and closing price is above 200 day moving average - buy
    if stock_data['rsi'][-1] < 30 and stock_data['close'][-1] > stock_data['sma200'][-1]:
        return 1
    # rsi is above 70 and closing price is below 200 day moving average - sell
    elif stock_data['rsi'][-1] > 70 and stock_data['close'][-1] < stock_data['sma200'][-1]:
        return -1
    else:
        return 0