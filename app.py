from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from markupsafe import escape
import sqlite3
from routes.munro_data import *
from routes.login import * 

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
        return render_template("index.html", locations=locations, error="Invalid credentials")
    
@app.route("/signup", methods=["POST"])
def signup():

    if request.method == "POST":

        user_name = request.form["user_name"]
        password = request.form["password"]
       

    response = add_user(user_name, password)
    print(response)
    if response == 200:
        message, color = "Log in and 🏔️→👜", "#00D100"
    else:
        message, color = "Username taken!", "#D10000"
    
    locations = get_munro_data()

    return render_template("index.html", show_signup=True, locations=locations, message=message, color=color)

@app.route("/<user>/edit")
def user_profile_edit(user):
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    if session["user_name"] != user:
        return redirect(url_for("/<user>/edit", user=session["user_name"]))
    
    log_data, bag_total = get_user_complete_log(user)

    return render_template("user_map_edit.html", log_data=log_data, user=user, bag_total=bag_total)

@app.route("/<user>/view")
def user_profile_view(user):

    log_data, bag_total = get_user_complete_log(user)

    return render_template("user_map_view.html", log_data=log_data, user=user, bag_total=bag_total)

@app.route('/addBag', methods=['POST'])
def add_bag():
    data = request.json

    data["user_id"] = session['user_id']

    print(data)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO bags (munro_id, user_id, date, distance, friends, notes)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    cursor.execute(insert_query, (
        data["munro_id"],
        data["user_id"],
        data["date"],
        data["distance"],
        data["friends"],
        data["notes"]
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


@app.route("/leaderboard")
def build_leaderboard():

    baggers, data = return_table_data()

    return render_template('leaderboard.html', baggers=baggers, data=data)