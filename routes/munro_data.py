def get_munro_data():

    import sqlite3
    import pandas as pd

    db_file = "database.db"

    conn = sqlite3.connect("database.db")
    df = pd.read_sql_query(f"SELECT * FROM munros", conn)

    conn.close()

    locations = df.to_dict(orient='records')

    return locations