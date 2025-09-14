from flask import Blueprint, render_template, redirect, url_for, session, request
from werkzeug.routing import BuildError
from data_queries.user_data_queries import *
from data_queries.user_images import *
from data_queries.munro_data_queries import * 
import os
from dotenv import load_dotenv

pages_bp = Blueprint("pages", __name__)

load_dotenv()
os_apikey = os.getenv("OSMAP_APIKEY")
DB = os.getenv("DB")

#user editor page
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
    
#user viewer page
@pages_bp.route("/<user>/view")
def user_profile_view(user, logged_in=False):

    #if user name naot found in db go to lost page
    if check_user_exists(user, DB) == 0:
        return render_template("lost_map.html")
    

    #else return user view page
    else:
        log_data, bag_total = get_user_complete_log(user, DB)
        user_img = get_user_image(user)

        if "user_id" in session:
            logged_in=True
        
        return render_template("map_view.html", log_data=log_data,
                                                os_apikey=os_apikey,
                                                user=user,
                                                user_img=user_img,
                                                bag_total=bag_total,
                                                logged_in=logged_in
                                                )
    
#user profile page
@pages_bp.route("/<user>/profile")
def user_profile_page(user, team_message=None, team_color=None, member_message=None, member_color=None):

    try:
        #redirect to home if no user is logged in
        if "user_id" not in session:
            return redirect(url_for("index"))
        
        else:
            #user data
            user_name = session["user_name"]
            user_id = session["user_id"]
            user_img = session["user_img"]

            log_data, bag_total = get_user_complete_log(user_name, DB)

            #get user teams
            teams = get_user_teams(user_id, DB)

            #get other users and images
            user_imgs = get_all_user_images(DB)
            users = get_all_users(DB)

            users.remove((user_id, user_name))
            users = list(map(lambda x: {"user_id": x[0], "user_name": x[1], "user_img":user_imgs[x[1]]}, users))

            #response to forms
            team_message = request.args.get("team_message")
            team_color = request.args.get("team_color")

            member_message = request.args.get("member_message")
            member_color = request.args.get("member_color")

        return render_template("user_profile.html", log_data=log_data,
                                                    user=user_name,
                                                    user_img=user_img,
                                                    bag_total=bag_total,
                                                    users=users,
                                                    teams=teams,
                                                    team_message=team_message,
                                                    team_color=team_color,
                                                    member_message=member_message,
                                                    member_color=member_color
                                                    )
    
    except BuildError:
        return redirect(url_for("index"))
    
#user viewer page
@pages_bp.route("/<team>/team_view")
def team_view(team):

    #if user name not found in db go to lost page
    if check_team_exists(team, DB) == 0:
        return render_template("lost_map.html")

    #else return user view page
    else:
        #log_data, bag_total = get_user_complete_log(user, DB)
        #user_img = get_user_image(user)
        
        return render_template("index.html")
                                                    