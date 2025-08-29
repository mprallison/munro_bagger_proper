from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape
import sqlite3
from routes.munro_data import *
from routes.login import get_user 

app = Flask(__name__)
app.secret_key = "supersecretkey"
DB = "database.db"

@app.route("/")
def index():

    session.clear()

    locations = get_munro_data()

    return render_template('index.html', locations=locations)

@app.route("/login", methods=["POST"])
def login():

    if "user_id" in session:
        return redirect(url_for("user_profile", user=session["user_name"]))
    
    if request.method == "POST":
            user_name = request.form["user_name"]
            password = request.form["password"]
            user = get_user(user_name, password)

    if user and password:
        session["user_id"] = user[0]
        session["user_name"] = user[1]
        return redirect(url_for("user_profile", user=session["user_name"]))
    else:
        locations = get_munro_data()
        return render_template("index.html", locations=locations, error="Invalid credentials")

#@app.route("/<user>/edit")
#def user_profile(user):
#    if "user_id" not in session:
#        return redirect(url_for("login"))
#    
#    if session["user_name"] != user:
#        return redirect(url_for("user_profile", user=session["user_name"]))
#    
#    locations = get_munro_data()
#
#    return render_template("user_map_edit.html", locations=locations,)

@app.route("/<user>/view")
def user_profile(user):
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    if session["user_name"] != user:
        return redirect(url_for("user_profile", user=session["user_name"]))
    
    log_data, bag_total = get_user_complete_log(user)

    return render_template("user_map_view.html", log_data=log_data, user=user, bag_total=bag_total)














@app.route("/leaderboard")
def build_leaderboard():

    baggers, data = return_table_data()

    return render_template('leaderboard.html', baggers=baggers, data=data)

