def get_user(username, password):

    import sqlite3
    DB = "database.db"

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT id, user, password FROM users WHERE user = ? and password = ?", (username, password))
    user = cur.fetchone()
    conn.close()

    return user