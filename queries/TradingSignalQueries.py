create_trading_signals_table = """
CREATE TABLE IF NOT EXISTS trading_signals (
                stock_symbol TEXT,
                date BIGINT,
                buy_signal BOOLEAN,
                sell_signal BOOLEAN,
                PRIMARY KEY (stock_symbol, date)
            )
        """
        
update_trading_signals_table = """
INSERT INTO trading_signals (stock_symbol, date, buy_signal, sell_signal)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (stock_symbol, date) DO NOTHING;
            """