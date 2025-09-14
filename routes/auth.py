from flask import Blueprint, request, render_template, redirect, url_for, session
from data_queries.user_data_queries import *
from data_queries.user_images import *
from data_queries.munro_data_queries import * 
import os
from dotenv import load_dotenv
from glob import glob

auth_bp = Blueprint("auth", __name__)

load_dotenv()
os_apikey = os.getenv("OSMAP_APIKEY")
DB = os.getenv("DB")

@auth_bp.route("/login", methods=["POST"])
def login():

    #if user already logged in then ignore request
    if "user_id" in session:
        return redirect(url_for("pages.user_profile_edit", user=session["user_name"]))
    
    #get user data from db
    user_name = request.form["user_name"]
    password = request.form["password"]
    user = get_user(user_name, password, DB)

    #if valid create session and go to edit page
    if user and password:
        
        session["user_id"] = user[0]
        session["user_name"] = user[1]
        session["user_img"] = get_user_image(session["user_name"])

        return redirect(url_for("pages.user_profile_edit", user=session["user_name"]))
    
    #else return error mesage
    else:
        return redirect(url_for("index", message="Invalid credentials!", color="#D10000"))
    
@auth_bp.route("/signup", methods=["POST"])
def signup():

    #add user if username is novel
    user_name = request.form["user_name"]
    password = request.form["password"]
    
    response = add_user(user_name, password, DB)

    if response == 200:
        message, color = "Log in and 🏔️→👜", "#00D100"
    else:
        message, color = "Username taken!", "#D10000"
    
    return redirect(url_for("index", message=message, color=color))

@auth_bp.route('/logout')
def logout():

    return redirect(url_for("index"))

@auth_bp.route('/delUser', methods=['POST'])
def deleteUser():

    delete_user_data(session["user_id"], DB)

    try:
        [user_image] = glob(f"static/images/{session["user_name"]}.*")
        os.remove(user_image)
    except:
        pass

    session.clear()

    return render_template("lost_map.html")