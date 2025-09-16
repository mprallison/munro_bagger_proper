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
    
    complete_log_query = """SELECT m.munro_id, m.name, m.region, m.height, m.whl_url, m.latitude, m.longitude, 
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
    cur = conn.cursor()

    insert_bag_query = """INSERT INTO bags (munro_id, user_id, date, distance, friends, notes, private)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """

    cur.execute(insert_bag_query, (
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

    cur.execute(get_coords_query, (data["munro_id"],))

    munro_coords = cur.fetchone() 

    conn.commit()
    conn.close()

    return munro_coords

def del_bag_from_db(data, DB):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    del_bag_query = """DELETE FROM bags
                WHERE munro_id = ? AND user_id = ?;
                """

    cur.execute(del_bag_query, (
                                data["munro_id"],
                                data["user_id"],
                                ))

    get_coords_query = """SELECT latitude, longitude
                        FROM munros
                        WHERE munro_id = ?
                        """

    cur.execute(get_coords_query, (data["munro_id"],))

    munro_coords = cur.fetchone() 

    conn.commit()
    conn.close()

    return munro_coords

def get_team_data_log(team_name, DB):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    #get all bags for team members
    team_bags_query = """SELECT user_id, munro_id
                    FROM bags 
                    WHERE user_id IN (
                        SELECT user_id 
                        FROM members 
                        WHERE team_id = (
                            SELECT team_id 
                            FROM teams 
                            WHERE team_name = ?
                        ));
                    """

    #group users by munro
    team_df = pd.read_sql(team_bags_query, conn, params=(team_name,))
    team_df = team_df.groupby("munro_id")["user_id"].agg(list).reset_index()

    #join on munro data
    munro_df = pd.read_sql("SELECT * FROM munros", conn)
    team_data_df = munro_df.merge(team_df, how="left", on="munro_id")
    team_data_df["user_id"] = team_data_df["user_id"].apply(lambda x: x if isinstance(x, list) else [])

    #get team members count
    cur.execute("""SELECT COUNT(*) FROM members
                LEFT JOIN teams ON members.team_id = teams.team_id
                WHERE teams.team_name = ?""", (team_name,))
    
    member_count = cur.fetchone()[0]

    #get team members
    cur.execute("""SELECT users.user_id, user_name 
                FROM users
                LEFT JOIN members ON members.user_id = users.user_id
                LEFT JOIN teams ON members.team_id = teams.team_id
                WHERE teams.team_name = ?""", (team_name,))
    
    team_users = cur.fetchall()

    #add user name
    user_df = pd.read_sql("SELECT * FROM users", conn)

    conn.commit()
    conn.close()

    user_name_dict = dict(zip(user_df["user_id"], user_df["user_name"]))
    team_data_df["user_name"] = team_data_df["user_id"].apply(lambda lst: [user_name_dict.get(x, None) for x in lst])
    team_data_df["user_name"] = team_data_df["user_name"].apply(lambda x: ", ".join(x))


    #count of bags per munro
    team_data_df["count"] = team_data_df["user_id"].apply(lambda x: len(x))

    #drop user_id
    team_data_df = team_data_df.drop(columns="user_id")

    return team_data_df, member_count, team_users