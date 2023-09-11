import psycopg2

def executeMany(query, values):
    conn = psycopg2.connect(database="olympus", user="postgres", password="password", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    try:
        cur.executemany(query, values)
        conn.commit()
        print("Query executed successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error executing query: {e}")
    finally:
        cur.close()
        conn.close()

print("Database opened successfully")

def executeQuery(query: str, type: str, params: tuple = None):
    con = psycopg2.connect(database="olympus", user="postgres", password="password", host="127.0.0.1", port="5432")
    try:
        cur = con.cursor()
        print("Query: ", query)
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        result = []
        print("Query executed successfully")
        if type == 'SELECT':
            result = cur.fetchall()
        con.commit()
        return result
    except Exception as e:
        print(e)
        return []


