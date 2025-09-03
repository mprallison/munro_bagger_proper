from flask import Flask, render_template, request, redirect, url_for, session, jsonify
#from markupsafe import escape
import sqlite3
from routes.munro_data import *
from routes.login import * 
from werkzeug.routing import BuildError
from werkzeug.exceptions import MethodNotAllowed
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY")
os_apikey = os.getenv("OSMAP_APIKEY")

DB = "database.db"

@app.route("/")
def index():

    session.clear()

    locations = get_munro_data()

    return render_template('index.html', locations=locations, os_apikey=os_apikey)

@app.route("/login", methods=["POST"])
def login():

    if "user_id" in session:
        return redirect(url_for("user_profile_edit", user=session["user_name"]))
    
    if request.method == "POST":
            user_name = request.form["user_name"]
            password = request.form["password"]
            user = get_user(user_name, password)

    if user and password:
        session["user_id"] = user[0]
        session["user_name"] = user[1]
        return redirect(url_for("user_profile_edit", user=session["user_name"]))
    else:
        locations = get_munro_data()
        return render_template("index.html", locations=locations, os_apikey=os_apikey, error="Invalid credentials")

@app.route("/signup", methods=["POST"])
def signup():

    if request.method == "POST":
        user_name = request.form["user_name"]
        password = request.form["password"]
       
    response = add_user(user_name, password)

    if response == 200:
        message, color = "Log in and 🏔️→👜", "#00D100"
    else:
        message, color = "Username taken!", "#D10000"
    
    locations = get_munro_data()

    return render_template("index.html", show_signup=True, locations=locations, os_apikey=os_apikey, message=message, color=color)

@app.route('/logout')
def logout():

    session.clear()
    return redirect(url_for("index"))

@app.route("/<user>/edit")
def user_profile_edit(user):

    try:
        #redirect to home if no user is logged in
        if "user_id" not in session:
            return redirect(url_for("login"))
        
        else:
            #if user is logged in, redirect to user edit page for any input user
            user=session["user_name"]
            log_data, bag_total = get_user_complete_log(user)
        
        return render_template("user_map_edit.html", log_data=log_data,  os_apikey=os_apikey, user=user, bag_total=bag_total)
    
    except BuildError:
        return redirect(url_for("index"))

@app.route("/<user>/view")
def user_profile_view(user):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(f"""SELECT COUNT(*) FROM users WHERE user_name = '{user}';""")
    count = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    if count == 0:
        return render_template("lost_map.html")

    log_data, bag_total = get_user_complete_log(user)

    return render_template("user_map_view.html", log_data=log_data,  os_apikey=os_apikey, user=user, bag_total=bag_total)

@app.route('/addBag', methods=['POST'])
def add_bag():

    data = request.json

    print(data)

    data["user_id"] = session['user_id']

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    insert_query = """
                   INSERT INTO bags (munro_id, user_id, date, distance, friends, notes, private)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   """

    cursor.execute(insert_query, (
                data["munro_id"],
                data["user_id"],
                data["date"],
                data["distance"],
                data["friends"],
                data["notes"],
                data["private"]
            ))

    cursor.execute(f"""
                    SELECT latitude, longitude
                    FROM munros
                    WHERE munro_id = '{data["munro_id"]}'
                    """)

    munro_coords = cursor.fetchone() 

    conn.commit()
    conn.close()

    return jsonify(message="OK", coords=munro_coords), 200

@app.route('/delBag', methods=['POST'])
def del_bag():

    data = request.json

    data["user_id"] = session['user_id']

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    del_query = """
                DELETE FROM bags
                WHERE munro_id = ? AND user_id = ?;
                """

    cursor.execute(del_query, (
        data["munro_id"],
        data["user_id"],
    ))

    cursor.execute(f"""
                    SELECT latitude, longitude
                    FROM munros
                    WHERE munro_id = '{data["munro_id"]}'
                    """)

    munro_coords = cursor.fetchone() 

    conn.commit()
    conn.close()

    return jsonify(message="OK", coords=munro_coords), 200

@app.errorhandler(MethodNotAllowed)
def handle_405(e):

    return redirect(url_for("index"))

@app.errorhandler(404)
def page_not_found(error):

    return "<h1 style='text-align: center;'>404</h1><p style='text-align: center;'>The page you are looking for does not exist. Do you exist?</p><br><br><br><pre>       splash! Silence again.", 404