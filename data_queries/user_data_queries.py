
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

def add_user(user_name, password, DB):
    
    try:
        with sqlite3.connect(DB) as conn:
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO users (user_id, user_name, password) VALUES (?, ?, ?)",
                (None, user_name, password)
            )
            numeric_id = cur.lastrowid
            new_user_id = f"u{numeric_id:04}"


            cur.execute(
                "UPDATE users SET user_id = ? WHERE id = ?",
                (new_user_id, numeric_id)
            )

            conn.commit()
            return 200 

    except sqlite3.IntegrityError as e:
        print(f"Integrity error: {e}")
        return 404
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 404

def check_user_exists(user_name, DB):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users WHERE user_name = ?;", (user_name,))
    count = cur.fetchone()[0]

    conn.commit()
    conn.close()

    return count


def check_team_exists(team_name, DB):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM teams WHERE team_name = ?;", (team_name,))
    count = cur.fetchone()[0]

    conn.commit()
    conn.close()

    return count

def delete_user_data(user_id, DB):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    cur.execute("DELETE FROM bags WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()

def get_all_users(DB):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT user_id, user_name FROM users")
    all_users = cur.fetchall()

    return all_users

def get_user_teams(user_id, DB):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    user_team_query = """SELECT t.team_id, t.team_name
                        FROM members m
                        LEFT JOIN teams t
                        ON m.team_id = t.team_id
                        WHERE m.user_id =  ?;
                        """
    
    
    user_teams_df  = pd.read_sql(user_team_query, conn, params=(user_id,))

    user_teams = user_teams_df.to_dict(orient='records')

    return user_teams

def add_team_query(team_name, user_id, DB):

    try:
        with sqlite3.connect(DB) as conn:
            cur = conn.cursor()

        cur.execute("INSERT INTO teams (team_id, team_name) VALUES (?, ?)", (None, team_name))

        numeric_id = cur.lastrowid
        new_team_id = f"t{numeric_id:04}"

        cur.execute("UPDATE teams SET team_id = ? WHERE id = ?", (new_team_id, numeric_id))
        
        insert_member_query = """INSERT INTO members (team_id, user_id)
                                VALUES (?, ?)
                            """
        
        cur.execute(insert_member_query, (new_team_id, user_id,))

        conn.commit()
        response = 200

    except:
        response = 404

    return response

def quit_team_query(user_id, team_ids, DB):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    try:

        # Prepare list of (user_id, team_id) tuples for executemany
        params = [(user_id, team_id) for team_id in team_ids]

        # Delete members for all (user_id, team_id) pairs
        cur.executemany(
            "DELETE FROM members WHERE user_id = ? AND team_id = ?",
            params
        )

        # Delete empty teams
        for team_id in team_ids:
            cur.execute("SELECT COUNT(*) FROM members WHERE team_id = ?", (team_id,))
            count = cur.fetchone()[0]
            if count == 0:
                cur.execute("DELETE FROM teams WHERE team_id = ?", (team_id,))

        conn.commit()
        return 200
    
    except Exception as e:
        return 404
    finally:
        conn.close()

def add_user_to_team_query(user_ids, team_id, DB):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    members = []
    for user in user_ids:
        members.append((team_id, user))

    try:
        cur.executemany("INSERT INTO members (team_id, user_id) VALUES (?, ?);", members)
        conn.commit()
        conn.close()
        
        return 200
    
    except:
        return 404
    
    finally:
        conn.close()