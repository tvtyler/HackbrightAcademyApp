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
    try:
        data = request.get_json()
    
        puuid = data['puuid']
        level = data["summonerLevel"]
        name = data["name"]
        icon = data['icon']

        player = crud.create_player(puuid, level, name, icon)
        model.db.session.add(player)
        model.db.session.commit()

        matches = fetch_match_id((puuid))
        match_characters_db = []
        player = crud.get_player_by_id(puuid)
        try:
            for match in matches:
                #get the index of the player and find data about them using that index
                puuid_index = match["metadata"]["participants"].index(puuid)

                match_id = match["metadata"]["match_id"]
                placement = match["info"]["participants"][puuid_index]["placement"]

                db_match = crud.create_match(match_id)
                match_details = crud.create_match_details(puuid, match_id, placement)
                # match_details.players = player
                model.db.session.add(db_match)
                model.db.session.add(match_details)
                model.db.session.commit()
                #iterate through each unit in the match, adding to database and associating with each match_details
                for unit in match["info"]["participants"][puuid_index]["units"]:
                    character = crud.create_character(unit["character_id"])
                    model.db.session.add(character)
                    model.db.session.commit()
                    match_character = crud.create_match_characters(match_details.id, character.id)
                    model.db.session.add(match_character)
                    model.db.session.commit()
                    if unit["itemNames"] != []:
                        for i in unit["itemNames"]:
                             #need to store in DB
                            item = crud.create_item(i)
                            print(item.item_name)
                            model.db.session.add(item)
                            model.db.session.commit()
                            character_item = crud.create_character_item(match_character.match_character_id, item.item_id)
                            model.db.session.add(character_item)
                            model.db.session.commit()

            print("ID CHECK:", character_item.item_id, " ", character_item.match_character_id)
        except Exception as e:
            return jsonify({"error": str(e)})
        return jsonify({"message": "Data received successfully"})
    except Exception as e:
        #helps for identifying what error i'm receiving
        return jsonify({"error": str(e)})

@app.route('/rank_details', methods=["POST"])
def rank_details():
    try:
        data = request.get_json()

        puuid = data['puuid']
        rank = data['rank']

        player = crud.get_player_by_id(puuid)
        player.player_rank = rank
        #session add?
        db.session.commit()

        return jsonify({"message": "Rank received successfully"})
    except Exception as e:
        #helps for identifying what error i'm receiving
        return jsonify({"error": str(e)})



@app.route('/get_players', methods=['GET'])
def get_players():
    players = crud.get_all_players() 
    #testing whether i've stored the players in the database
    player_data = [{"puuid": player.player_id, "level": player.player_level, "name": player.player_name} for player in players]
    return jsonify(player_data)

@app.route('/get_matches/<player_id>', methods=['GET'])
def get_matches_from_db(player_id): #unsure how to use player_id here
    matches = crud.get_match_details_by_player_id(player_id) #changed to details
    player_name = crud.get_player_by_id(player_id).player_name
    match_data = [{"match id": match.match_id, "player id": match.player_id, "placement": match.placement, "Name": player_name, "player": match.players.player_name }for match in matches]
    return jsonify(match_data) 

@app.route('/')
def homepage():
    """Show homepage with search form"""
    
    return render_template("homepage.html")

@app.route('/match_history/<string:puuid>', methods = ['POST', 'GET'])
def match_history(puuid):
    """show match history for that specific player"""

    player = crud.get_player_by_id(puuid)
    matches = crud.get_match_details_by_player_id(puuid)
    match_characters = crud.get_match_characters_by_match_details_id(matches[0].id) #will need to iterate through later for each match
    character_items = []
    for character in match_characters:
        items = crud.get_character_items_by_match_character_id(character.match_character_id)
        if items != []:
            character_items.append(items)
    if character_items == []:
        print("LIST IS EMPTY DUUUUUUUUDE")
    icon_link = f"http://ddragon.leagueoflegends.com/cdn/13.17.1/img/profileicon/{player.player_icon}.png"


    return render_template("match_history.html", player = player, matches = matches, icon_link = icon_link, match_characters = match_characters, character_items = character_items)


if __name__ == "__main__":
    from model import connect_to_db, db
    connect_to_db(app)
    db.create_all()
    app.run(host="0.0.0.0", debug=True)
