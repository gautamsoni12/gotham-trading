GET_PREDICTIONS_WITH_VALUE = """
 SELECT predicted_data.stock_symbol, predicted_data.date, predicted_data.trade_decision, predicted_data.predictions, predicted_data.confidence, stock_daily.close
 FROM predicted_data 
 JOIN stock_daily 
 ON predicted_data.stock_symbol=stock_daily.stock_symbol 
 AND predicted_data.date=stock_daily.date 
 WHERE predicted_data.date >='{}'
 AND predicted_data.date <='{}'
 AND stock_daily.close > {}
 AND predictions={}
 ORDER BY confidence 
 DESC LIMIT {};
"""

GET_PREDICTIONS_WITHOUT_VALUE = """
 SELECT predicted_data.stock_symbol, predicted_data.date, predicted_data.trade_decision, predicted_data.predictions, predicted_data.confidence, stock_daily.close
 FROM predicted_data 
 JOIN stock_daily 
 ON predicted_data.stock_symbol=stock_daily.stock_symbol 
 AND predicted_data.date=stock_daily.date 
 WHERE predicted_data.date >='{}'
 AND predicted_data.date <='{}'
 AND stock_daily.close > {}
 ORDER BY confidence 
 DESC LIMIT {};
"""

GET_STOCK_DATA = """
    SELECT stock_symbol, date, close, rsi, macd, macd_signal_line, adx, BBands_Upper, BBands_Middle, BBands_Lower, Stoch, SMA_Price, SMA_Volume, ATR, trade_decision, NULLIF(seven_day_price_diff, 'NaN'), NULLIF(seven_day_price_diff_percent, 'NaN') 
    FROM technical_indicators_two 
    WHERE stock_symbol='{}' 
    ORDER BY date DESC
    LIMIT 30;
"""

GET_PREDICTION_RESULT = """
    SELECT stock_symbol, date, predictions, trade_decision, confidence, seven_day_price_diff, descrepency, actual_return
    FROM stock_data_result
    ORDER BY date DESC
    LIMIT 50;
"""