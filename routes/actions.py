
from flask import Blueprint, request, render_template, session, jsonify, Response, redirect, url_for, flash
from data_queries.munro_data_queries import *

from routes.pages import pages_bp 

from dotenv import load_dotenv
import os
import io
from glob import glob

actions_bp = Blueprint("actions", __name__)

load_dotenv()
DB = os.getenv("DB")

@actions_bp.route('/addBag', methods=['POST'])
def add_bag():

    data = request.json
    data["user_id"] = session['user_id']

    munro_coords = add_bag_to_db(data, DB)

    return jsonify(message="OK", coords=munro_coords), 200

@actions_bp.route('/delBag', methods=['POST'])
def del_bag():

    data = request.json
    data["user_id"] = session['user_id']

    munro_coords = del_bag_from_db(data, DB)

    return jsonify(message="OK", coords=munro_coords), 200


@actions_bp.route('/uploadImage', methods=['POST'])
def upload_image():

    file = request.files.get('file')
    user_name = session.get("user_name")

    # Validate file type
    valid_types = {"png", "jpg", "jpeg", "gif"}
    file_type = file.filename.rsplit(".", 1)[-1].lower()

    if file_type not in valid_types:
        flash("Invalid file type. Only PNG, JPG, JPEG, and GIF allowed.", "error")
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

    return redirect(url_for("pages.user_profile_page", user=user_name))

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


@actions_bp.route("/add_team", methods=["POST"])
def create_team():

    team_name = request.form["team_name"]

    print(team_name)

    response = add_team(team_name, DB)

    if response == 200:
        message, color = "New team created!, "#00D100"
    else:
        message, color = "Team name taken!", "#D10000"

    user_name = session["user_name"]
    user_id = session["user_id"]

    log_data, bag_total = get_user_complete_log(user_name, DB)
    all_users = get_all_users(DB)
    other_users = [u for u in all_users if u['user_name'] != user_name]

    user_imgs = return_all_user_images(DB)


    teams = get_user_teams(user_id, DB)

    return render_template("pages.user_profile.html", log_data=log_data, user=user_name, bag_total=bag_total, other_users=other_users, teams=teams, user_imgs=user_imgs,
                           message=message, color=color)