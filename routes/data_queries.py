import sqlite3
import pandas as pd

def get_munro_data():

    db_file = "database.db"

    conn = sqlite3.connect("database.db")
    loc_df = pd.read_sql_query(f"SELECT * FROM munros", conn)

    conn.close()

    locations = loc_df.to_dict(orient='records')

    return locations


def get_user_complete_log(user_name):

    db_file = "database.db"

    conn = sqlite3.connect("database.db")
    
    complete_log_query = f"""SELECT m.munro_id, m.name, m.region, m.height, m.description, m.whl_url, m.latitude, m.longitude, 
                        b.user_id, b.date, b.distance, b.friends, b.notes, b.private
                        FROM munros m
                        LEFT JOIN users u
                        ON u.user_name = '{user_name}'
                        LEFT JOIN bags b
                        ON m.munro_id = b.munro_id
                        AND b.user_id = u.user_id;
                """

    bags_df  = pd.read_sql(complete_log_query, conn)

    conn.close()

    bag_data = bags_df.to_dict(orient='records')
    bag_total = str(len(bags_df[~bags_df["date"].isnull()]))

    return bag_data, bag_total

def get_users():

    db_file = "database.db"

    conn = sqlite3.connect("database.db")
    user_df = pd.read_sql_query(f"SELECT user_name FROM users", conn)

    conn.close()

    all_users = user_df.to_dict(orient='records')

    return all_users

def get_user_data_log(user_name):

    db_file = "database.db"

    conn = sqlite3.connect("database.db")
    
    user_data_query = f"""SELECT m.name, b.date, b.distance, b.friends, b.notes, b.private
                        FROM munros m
                        LEFT JOIN users u
                        ON u.user_name = '{user_name}'
                        LEFT JOIN bags b
                        ON m.munro_id = b.munro_id
                        AND b.user_id = u.user_id
                        WHERE
                        b.date IS NOT NULL;
                """
    
    user_data  = pd.read_sql(user_data_query, conn)

    conn.close()

    return user_data

def delete_user_data(user_id):

    db_file = "database.db"

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM bags WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()