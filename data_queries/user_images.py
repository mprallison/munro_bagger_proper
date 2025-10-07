from glob import glob
import pandas as pd
import sqlite3

def get_user_image(user_name):

    try:
        [user_image] = glob(f"static/images/{user_name}.*")
        user_image = "/" + user_image.replace("\\", "/")
    except:
        user_image = "/static/images/bag.png"
    
    return user_image

def get_all_user_images(DB):

    with sqlite3.connect(DB) as conn:
        user_df = pd.read_sql_query("SELECT user_name FROM users", conn)

    user_imgs = {}
    for u in user_df["user_name"]:
        user_imgs[u] = get_user_image(u)

    return user_imgs