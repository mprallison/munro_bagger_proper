
import sqlite3
import pandas as pd

def get_user(user_name, password, DB):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    get_user_query = """SELECT user_id, user_name, password 
                        FROM users 
                        WHERE user_name = ? and password = ?
                        """
    
    cur.execute(get_user_query, (user_name, password, ))
    
    user = cur.fetchone()
    conn.close()

    return user

def add_user(user_name, password, DB):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM users;")
    user_count = cur.fetchone()[0]

    new_user_id  = f"u{user_count:04}"

    insert_user = """INSERT INTO users (user_id, user_name, password)
                     VALUES (?, ?, ?)
                  """

    try:
        cur.execute(insert_user, (new_user_id, user_name, password))
        conn.commit()
        response = 200

    except:
        response = 404

    conn.close()

    return response

def get_all_users(DB):

    conn = sqlite3.connect(DB)
    user_df = pd.read_sql_query("SELECT user_name FROM users", conn)

    conn.close()

    all_users = user_df.to_dict(orient='records')

    return all_users

def add_team(team_name, DB):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM teams;")
    team_count = cursor.fetchone()[0]

    new_team_id  = f"u{team_count:04}"

    insert_team_query = """INSERT INTO teams (team_id, team_name)
                            VALUES (?, ?)
                        """
    
    try:
        cursor.execute(insert_team_query, (new_team_id, team_name))
        conn.commit()
        response = 200

    except:
        response = 404

    conn.close()

    return response

def delete_user_data(user_id, DB):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM bags WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()

def check_user_exists(user_name, DB):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE user_name = ?;", (user_name,))
    count = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return count

def add_user_to_team(data, DB):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    insert_member_query = """INSERT INTO members (team_id, user_id)
                            VALUES (?, ?)
                        """

    cursor.execute(insert_member_query, (
                                data["team_id"],
                                data["user_id"]
                                ))
    
    conn.commit()
    conn.close()


def get_user_teams(user_id, DB):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    user_team_query = """SELECT t.team_id, t.team_name
                        FROM members m
                        LEFT JOIN teams t
                        ON m.team_id = t.team_id
                        WHERE
                        m.user_id =  ?;
                        """
    
    
    user_teams_df  = pd.read_sql(user_team_query, conn, params=(user_id,))

    user_teams = user_teams_df.to_dict(orient='records')

    return user_teams














