from flask import Blueprint, render_template, redirect, url_for, session
from werkzeug.routing import BuildError
from data_queries.user_data_queries import *
from data_queries.check_user_image import *
from data_queries.munro_data_queries import * 
import os
from dotenv import load_dotenv

pages_bp = Blueprint("pages", __name__)

load_dotenv()
os_apikey = os.getenv("OSMAP_APIKEY")
DB = os.getenv("DB")

@pages_bp.route("/<user>/edit")
def user_profile_edit(user):

    try:
        #redirect to home if no user is logged in
        if "user_id" not in session:
            return redirect(url_for("index"))    
        else:
            #if user is logged in, redirect to user edit page for any input user
            user = session["user_name"]
            user_img = session["user_img"]

            log_data, bag_total = get_user_complete_log(user, DB)

        return render_template("user_map_edit.html", log_data=log_data,
                                                    os_apikey=os_apikey,
                                                    user=user,
                                                    user_img=user_img,
                                                    bag_total=bag_total
                                                    )
    
    except BuildError as e:
        print(e)
        return redirect(url_for("index"))
    
@pages_bp.route("/<user>/view")
def user_profile_view(user):

    count = check_user_exists(user, DB)

    if count == 0:
        return render_template("lost_map.html")

    log_data, bag_total = get_user_complete_log(user, DB)
    user_img = return_user_image(user)
    
    return render_template("user_map_view.html", log_data=log_data,
                                                os_apikey=os_apikey,
                                                user=user,
                                                user_img=user_img,
                                                bag_total=bag_total
                                                )
    

@pages_bp.route("/<user>/profile")
def user_profile_page(user):

    try:
        #redirect to home if no user is logged in
        if "user_id" not in session:
            return redirect(url_for("index"))
        
        else:
            #if user is logged in, redirect to user edit page for any input user
            user_name = session["user_name"]
            user_id = session["user_id"]
            user_img = session["user_img"]

            log_data, bag_total = get_user_complete_log(user_name, DB)
            all_users = get_all_users(DB)
            other_users = [u for u in all_users if u['user_name'] != user_name]

            user_imgs = return_all_user_images(DB)

            teams = get_user_teams(user_id, DB)

        return render_template("user_profile.html", log_data=log_data,
                                                    user=user_name,
                                                    user_img=user_img,
                                                    bag_total=bag_total,
                                                    other_users=other_users,
                                                    teams=teams,
                                                    user_imgs=user_imgs
                                                    )
    
    except BuildError:
        return redirect(url_for("index"))