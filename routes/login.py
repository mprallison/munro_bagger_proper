def get_user(user_name, password):

    import sqlite3
    DB = "database.db"

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(f"SELECT user_id, user_name, password FROM users WHERE user_name = '{user_name}' and password = '{password}'""")
    user = cur.fetchone()
    conn.close()

    return user