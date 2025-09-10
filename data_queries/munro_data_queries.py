import sqlite3
import pandas as pd

def get_munro_data(DB):

    conn = sqlite3.connect(DB)
    loc_df = pd.read_sql_query("SELECT * FROM munros", conn)

    conn.close()

    locations = loc_df.to_dict(orient='records')

    return locations

def get_user_complete_log(user_name, DB):

    conn = sqlite3.connect(DB)
    
    complete_log_query = """SELECT m.munro_id, m.name, m.region, m.height, m.description, m.whl_url, m.latitude, m.longitude, 
                        b.user_id, b.date, b.distance, b.friends, b.notes, b.private
                        FROM munros m
                        LEFT JOIN users u
                        ON u.user_name = ?
                        LEFT JOIN bags b
                        ON m.munro_id = b.munro_id
                        AND b.user_id = u.user_id;
                        """

    bags_df  = pd.read_sql(complete_log_query, conn, params=(user_name,))

    conn.close()

    bag_data = bags_df.to_dict(orient='records')
    bag_total = str(len(bags_df[~bags_df["date"].isnull()]))

    return bag_data, bag_total

def get_user_data_log(user_name, DB):

    conn = sqlite3.connect(DB)
    
    user_data_query = """SELECT m.name, b.date, b.distance, b.friends, b.notes, b.private
                        FROM munros m
                        LEFT JOIN users u
                        ON u.user_name = ?
                        LEFT JOIN bags b
                        ON m.munro_id = b.munro_id
                        AND b.user_id = u.user_id
                        WHERE
                        b.date IS NOT NULL;
                        """

    user_data  = pd.read_sql(user_data_query, conn, params=(user_name,))

    conn.close()

    return user_data

def add_bag_to_db(data, DB):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    insert_bag_query = """INSERT INTO bags (munro_id, user_id, date, distance, friends, notes, private)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """

    cursor.execute(insert_bag_query, (
                data["munro_id"],
                data["user_id"],
                data["date"],
                data["distance"],
                data["friends"],
                data["notes"],
                data["private"]
                ))
    
    get_coords_query = """SELECT latitude, longitude
                        FROM munros
                        WHERE munro_id = ?
                        """

    cursor.execute(get_coords_query, (data["munro_id"],))

    munro_coords = cursor.fetchone() 

    conn.commit()
    conn.close()

    return munro_coords

def del_bag_from_db(data, DB):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    del_bag_query = """DELETE FROM bags
                WHERE munro_id = ? AND user_id = ?;
                """

    cursor.execute(del_bag_query, (
                                data["munro_id"],
                                data["user_id"],
                                ))

    get_coords_query = """SELECT latitude, longitude
                        FROM munros
                        WHERE munro_id = ?
                        """

    cursor.execute(get_coords_query, (data["munro_id"],))

    munro_coords = cursor.fetchone() 

    conn.commit()
    conn.close()

    return munro_coords