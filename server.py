"""Server for Teamfight Tactics app."""
import os
from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from jinja2 import StrictUndefined
import crud, requests
from datetime import datetime
from api_calls import fetch_match_id

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

#API key from secrets file
api_key = os.environ.get('API_KEY')

#routes
#REMEMBER TO UPDATE GET/POST AS NEEDED

@app.route('/api/proxy', methods=['GET'])
def riot_api_proxy():
    proxy_url = request.args.get('url')

    headers = {
        "X-Riot-Token": api_key #riot specific header
    }

    try:
        response = requests.get(proxy_url, headers=headers)
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to proxy the request", "details": str(e)}), 500
    
@app.route('/player_details', methods = ['POST'])
def get_puuid():
    # #will have to add rank later through another api request in app.jsx
    # player_details = requests.get_json()
    
    # player_data_db = []

    # crud.create_player(player_details)

    try:
        data = request.get_json()
        puuid = data['puuid']
        
        return jsonify({"message": "Data received successfully"})
    except Exception as e:
        return None

@app.route('/get_matches/<player_id>', methods=['GET'])
def fetch_match_info(player_id):
    
    matches = fetch_match_id(player_id)

    matches_in_db = []

    for match in matches:
        match_id = match["metadata"]["match_id"]
        player_id = match["info"]["participants"][0]["puuid"] 
        placement = match["info"]["participants"][0]["placement"]
        game_datetime = match["info"]["game_datetime"]

    date_played = datetime.strptime(game_datetime, "%Y-%m-%d")

    db_match = crud.create_match(match_id, player_id, placement, date_played)
    matches_in_db.append(db_match)


    return None


@app.route('/')
def homepage():
    """Show homepage with search form"""
    
    return render_template("homepage.html")


if __name__ == "__main__":
    from model import connect_to_db, db
    connect_to_db(app)
    db.create_all()
    app.run(host="0.0.0.0", debug=True)
