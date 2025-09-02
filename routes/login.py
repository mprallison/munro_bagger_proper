def get_user(user_name, password):

    import sqlite3
    DB = "database.db"

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(f"SELECT user_id, user_name, password FROM users WHERE user_name = '{user_name}' and password = '{password}'""")
    user = cur.fetchone()
    conn.close()

    return user

def add_user(user_name, password):

    import sqlite3
    DB = "database.db"

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(f"SELECT COUNT(*) FROM users;")
    user_count = cur.fetchone()[0]

    new_user_id  = f"u{user_count:04}"

    insert_user = """
    INSERT INTO users (user_id, user_name, password)
    VALUES (?, ?, ?)
    """

    try:
        cur.execute(insert_user, (
            new_user_id,
            user_name,
            password
            ))
        
        conn.commit()
        response = 200

    except:
        response = 404

    conn.close()

    return response