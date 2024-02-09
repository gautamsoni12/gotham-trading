create_technical_indicators_table = """
            CREATE TABLE IF NOT EXISTS technical_indicators_two (
                stock_symbol TEXT,
                date date,
                close decimal,
                RSI decimal,
                MACD decimal,
                macd_signal_line decimal,
                ADX decimal,
                BBands_Upper decimal,
                BBands_Middle decimal,
                BBands_Lower decimal,
                Stoch decimal,
                SMA_Price decimal,
                SMA_Volume decimal,
                ATR decimal,
                trade_decision INTEGER,
                seven_day_price_diff decimal,
                seven_day_price_diff_percent decimal,
                PRIMARY KEY (stock_symbol, date)
            )
        """
        
update_technical_indicators_table = """
                INSERT INTO technical_indicators_two (stock_symbol, close, date, RSI, MACD, macd_signal_line, ADX, BBands_Upper, BBands_Middle, BBands_Lower, Stoch, SMA_Price, SMA_Volume, ATR, trade_decision, seven_day_price_diff, seven_day_price_diff_percent)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (stock_symbol, date) DO UPDATE SET
                close = excluded.close,
                RSI = excluded.RSI,
                MACD = excluded.MACD,
                macd_signal_line = excluded.macd_signal_line,
                ADX = excluded.ADX,
                BBands_Upper = excluded.BBands_Upper,
                BBands_Middle = excluded.BBands_Middle,
                BBands_Lower = excluded.BBands_Lower,
                Stoch = excluded.Stoch,
                SMA_Price = excluded.SMA_Price,
                SMA_Volume = excluded.SMA_Volume,
                ATR = excluded.ATR,
                trade_decision = excluded.trade_decision,
                seven_day_price_diff = excluded.seven_day_price_diff,
                seven_day_price_diff_percent = excluded.seven_day_price_diff_percent
            """

update_trade_decision = """
            INSERT INTO technical_indicators_two (stock_symbol, date, trade_decision, seven_day_price_diff, seven_day_price_diff_percent)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (stock_symbol, date) DO UPDATE SET
            trade_decision = excluded.trade_decision,
            seven_day_price_diff = excluded.seven_day_price_diff,
            seven_day_price_diff_percent = excluded.seven_day_price_diff_percent
        """