create_technical_indicators_table = """
            CREATE TABLE IF NOT EXISTS technical_indicators (
                stock_symbol TEXT,
                date date,
                close decimal,
                RSI decimal,
                RSI_Signal decimal,
                MACD decimal,
                MACD_Signal decimal,
                macd_signal_line decimal,
                ADX decimal,
                ADX_Signal decimal,
                BBands_Upper decimal,
                BBands_Middle decimal,
                BBands_Lower decimal,
                BBands_Signal decimal,
                Stoch decimal,
                Stoch_Signal decimal,
                trade_decision INTEGER,
                seven_day_price_diff decimal,
                seven_day_price_diff_percent decimal,
                PRIMARY KEY (stock_symbol, date)
            )
        """
        
update_technical_indicators_table = """
                INSERT INTO technical_indicators (stock_symbol, close, date, RSI, MACD, MACD_Signal, macd_signal_line, ADX, BBands_Upper, BBands_Middle, BBands_Lower, Stoch, Stoch_Signal, RSI_Signal, ADX_Signal, BBands_Signal, trade_decision, seven_day_price_diff, seven_day_price_diff_percent)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (stock_symbol, date) DO NOTHING;
            """
            
            
update_trade_decision = """
            INSERT INTO technical_indicators (stock_symbol, date, trade_decision, seven_day_price_diff, seven_day_price_diff_percent)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (stock_symbol, date) DO UPDATE SET
            trade_decision = excluded.trade_decision,
            seven_day_price_diff = excluded.seven_day_price_diff,
            seven_day_price_diff_percent = excluded.seven_day_price_diff_percent
        """