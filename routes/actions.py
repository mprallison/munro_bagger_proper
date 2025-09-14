
from flask import Blueprint, request, render_template, session, jsonify, Response, redirect, url_for
from data_queries.munro_data_queries import *
from data_queries.user_data_queries import *
from data_queries.user_images import *

from dotenv import load_dotenv
import os
import io
from glob import glob

actions_bp = Blueprint("actions", __name__)

load_dotenv()
DB = os.getenv("DB")

#bag new munro
@actions_bp.route('/addBag', methods=['POST'])
def add_bag():

    data = request.json
    data["user_id"] = session['user_id']

    munro_coords = add_bag_to_db(data, DB)

    return jsonify(message="OK", coords=munro_coords), 200

#delete munro
@actions_bp.route('/delBag', methods=['POST'])
def del_bag():

    data = request.json
    data["user_id"] = session['user_id']

    munro_coords = del_bag_from_db(data, DB)

    return jsonify(message="OK", coords=munro_coords), 200


#upload new icon image
@actions_bp.route('/uploadImage', methods=['POST'])
def upload_image():

    file = request.files.get('file')
    user_name = session.get("user_name")

    # Validate file type
    valid_types = {"png", "jpg", "jpeg", "gif"}
    file_type = file.filename.rsplit(".", 1)[-1].lower()

    if file_type not in valid_types:
        return jsonify({"message": "Fail"})

    upload_folder = "static/images"

    # remove old image if exists
    try:
        [user_image] = glob(f"{upload_folder}/{user_name}.*")
        os.remove(user_image)
    except:
        pass

    filename = f"{user_name}.{file_type}"
    path = os.path.join(upload_folder, filename)
    file.save(path)

    #update session img
    session["user_img"] = get_user_image(session["user_name"])

    return redirect(url_for("pages.user_profile_page", user=user_name))

#download user mbag data as csv
@actions_bp.route('/downloadData')
def download_data():

    user_name = session["user_name"]

    user_data = get_user_data_log(user_name, DB)
    buffer = io.StringIO()
    user_data.to_csv(buffer, index=False)

    csv_data = buffer.getvalue()

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=data.csv"}
        )

#create new team
@actions_bp.route("/createTeam", methods=["POST"])
def create_team():

    team_name = request.form["team_name"]
    user_id= session["user_id"]

    response = add_team_query(team_name, user_id, DB)

    if response == 200:
        message, color = "New team created!", "#00D100"
    else:
        message, color = "Team name taken!", "#D10000"

    print(response)

    return redirect(url_for("pages.user_profile_page", user=session["user_name"], team_message=message, team_color=color))

#quit team
#if team has zero members delete team
@actions_bp.route("/quitTeam", methods=["POST"])
def quit_team():

    team_ids = request.form.getlist("select_team")
    user_id = session["user_id"]

    print(team_ids)

    response = quit_team_query(user_id, team_ids, DB)

    return redirect(url_for("pages.user_profile_page", user=session["user_name"]))

#add users to team
@actions_bp.route("/addToTeam", methods=["POST"])
def add_member():

    user_ids = request.form.getlist("select_user")
    [team_id] = request.form.getlist("select_team")

    print(user_ids)
    print(team_id)

    response = add_user_to_team_query(user_ids, team_id, DB)

    if response == 200:
        message, color = "New members added!", "#00D100"
    else:
        message, color = "A user is already a member!", "#D10000"

    return redirect(url_for("pages.user_profile_page", user=session["user_name"], member_message=message, member_color=color))