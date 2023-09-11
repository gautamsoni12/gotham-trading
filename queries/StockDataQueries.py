CREATE_TABLE_IF_NOT_QUERY = """
    CREATE TABLE IF NOT EXISTS stock_daily (
        stock_symbol TEXT,
        adj_close decimal,
        close decimal,
        date date,
        high decimal,
        low decimal,
        open decimal,
        volume BIGINT,
        PRIMARY KEY (stock_symbol, date)
    )
"""

INSERT_NEW_DATA = """INSERT INTO stock_daily (date, stock_symbol, adj_close, close, high, low, open, volume)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (stock_symbol, date) DO NOTHING;"""