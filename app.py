from flask import Flask, render_template, redirect, url_for, session
from data_queries.munro_data_queries import get_munro_data
from routes.auth import auth_bp
from routes.pages import pages_bp
from routes.actions import actions_bp 

from werkzeug.exceptions import MethodNotAllowed
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv("FLASK_SECRET_KEY")
os_apikey = os.getenv("OSMAP_APIKEY")
DB = os.getenv("DB")

app.register_blueprint(auth_bp)
app.register_blueprint(pages_bp)
app.register_blueprint(actions_bp)

@app.route("/")
def index():

    session.clear()
    locations = get_munro_data(DB)

    return render_template('index.html', locations=locations, os_apikey=os_apikey)

@app.errorhandler(MethodNotAllowed)
def handle_405(e):

    return redirect(url_for("index"))

@app.errorhandler(404)
def page_not_found(error):

    return "<div style='font-family: Courier New'; letter-spacing: 0.02em;'>" \
    "<h1 style='text-align: center;'>404</h1><p style='text-align: center;'>" \
    "The page you are looking for does not exist. Do you exist?</p>" \
    "<br><br><br><br><br>&nbsp;&nbsp;&nbsp;........... " \
    "splash! Silence again.", 404

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response