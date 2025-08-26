from flask import Flask, render_template
from routes.munro_data import get_munro_data

app = Flask(__name__)

@app.route("/")
def login_page():

    locations = get_munro_data()

    return render_template('login.html', locations=locations)

@app.route("/leaderboard")
def build_leaderboard():

    baggers, data = return_table_data()

    return render_template('leaderboard.html', baggers=baggers, data=data)

@app.route("/map")
def build_map():

    locations = return_map_data()

    return render_template('map.html', locations=locations)

if __name__ == '__main__':
    app.run(debug=True) 