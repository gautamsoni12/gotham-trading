create_technical_indicators_table = """
            CREATE TABLE IF NOT EXISTS technical_indicators_two (
                stock_symbol TEXT,
                date BIGINT,
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
                ON CONFLICT (stock_symbol, date) DO NOTHING;
            """
