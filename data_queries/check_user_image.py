from glob import glob
import pandas as pd
import sqlite3

def return_user_image(user_name):

    try:
        [user_image] = glob(f"static/images/{user_name}.*")
        user_image = "/" + user_image.replace("\\", "/")
    except:
        user_image = "/static/images/bag.png"
    
    return user_image

def return_all_user_images(DB):

    conn = sqlite3.connect(DB)
    user_df = pd.read_sql_query("SELECT user_name FROM users", conn)
    conn.close()

    user_imgs = {}
    for u in user_df["user_name"]:
        user_imgs[u] = return_user_image(u)

    return user_imgs

