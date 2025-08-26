from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape
import sqlite3
from routes.munro_data import get_munro_data
from routes.login import get_user 

app = Flask(__name__)
app.secret_key = "supersecretkey"
DB = "database.db"

@app.route("/")
def index():

    locations = get_munro_data()

    return render_template('index.html', locations=locations)

@app.route("/login", methods=["POST"])
def login():

    if "user_id" in session:
        return redirect(url_for("user_profile", user=session["username"]))
    
    if request.method == "POST":
            username = request.form["user"]
            password = request.form["password"]
            user = get_user(username, password)

    if user and password:
        session["user_id"] = user[0]
        session["username"] = user[1]
        return redirect(url_for("user_profile", user=session["username"]))
    else:
        locations = get_munro_data()
        return render_template("index.html", locations=locations, error="Invalid credentials")

@app.route("/<user>")
def user_profile(user):
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    if session["username"] != user:
        return redirect(url_for("user_profile", user=session["username"]))
    
    locations = get_munro_data()

    return render_template("user_map.html", locations=locations,)


@app.route("/leaderboard")
def build_leaderboard():

    baggers, data = return_table_data()

    return render_template('leaderboard.html', baggers=baggers, data=data)

