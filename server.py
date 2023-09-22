"""Server for Teamfight Tactics app."""
import os
from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from jinja2 import StrictUndefined
import crud, requests
from datetime import datetime
from api_calls import fetch_match_id
import model

os.system("dropdb Teamfight_Tactics")
os.system("createdb Teamfight_Tactics")

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
    try:
        data = request.get_json()
    
        puuid = data['puuid']
        level = data["summonerLevel"]
        name = data["name"]

        player = crud.create_player(puuid, level, name)
        model.db.session.add(player)
        model.db.session.commit()

        return jsonify({"message": "Data received successfully"})
    except Exception as e:
        #helps for identifying what error i'm receiving
        return jsonify({"error": str(e)})

@app.route('/get_players', methods=['GET'])
def get_players():
    players = crud.get_all_players() 
    #testing whether i've stored the players in the database
    player_data = [{"puuid": player.player_id, "level": player.player_level, "name": player.player_name} for player in players]
    return jsonify(player_data)

@app.route('/store_matches/<player_id>', methods=['GET'])
def fetch_match_info(player_id):
    
    #coming back as none
    matches = fetch_match_id((player_id))
    matches_in_db = []
    
    for match in matches:
        match_id = match["metadata"]["match_id"]
        player_id = match["info"]["participants"][0]["puuid"] #need to fix, getting no puuid and wrong placements
        placement = match["info"]["participants"][0]["placement"]


        db_match = crud.create_match(match_id, player_id, placement)
        matches_in_db.append(db_match)

    model.db.session.add_all(matches_in_db)
    model.db.session.commit()

    return redirect(f'/get_matches/{player_id}')


@app.route('/get_matches/<player_id>', methods=['GET'])
def get_matches_from_db(player_id): #unsure how to use player_id here
    matches = crud.get_all_matches()
    match_data = [{"match id": match.match_id, "player id": match.player_id, "placement": match.placement}for match in matches]
    return jsonify(match_data) 

@app.route('/')
def homepage():
    """Show homepage with search form"""
    
    return render_template("homepage.html")

@app.route('/match_history')
def match_history():
    """show match history for that specific player"""

    return render_template("match_history.html")


if __name__ == "__main__":
    from model import connect_to_db, db
    connect_to_db(app)
    db.create_all()
    app.run(host="0.0.0.0", debug=True)
