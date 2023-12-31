"""Server for Teamfight Tactics app."""
import os
from flask import (Flask, render_template, request, jsonify, redirect)
from jinja2 import StrictUndefined
import crud, requests
from api_calls import fetch_match_id
import model

#create and drop the database so it is fresh each time the server is booted
os.system("dropdb Teamfight_Tactics")
os.system("createdb Teamfight_Tactics")

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

#API key from shell script
api_key = os.environ.get('API_KEY')

#routes

#proxy server to avoid CORS error
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
        #receive data from frontend
        data = request.get_json()
    
        puuid = data['puuid']
        level = data["summonerLevel"]
        name = data["name"]
        icon = data['icon']

        #store recieved data in database as player
        player = crud.create_player(puuid, level, name, icon)
        model.db.session.add(player)
        model.db.session.commit()

        #call function from api_calls that gets the players matches based on player id
        matches = fetch_match_id((puuid))
        player = crud.get_player_by_id(puuid)

        #save the publicly available item data from riots api docs
        response = requests.get("https://ddragon.leagueoflegends.com/cdn/13.18.1/data/en_US/tft-item.json")
        item_response = response.json()
        item_data = item_response.get("data", {})

        try:
            #iterate through match details where most of the information is retrieved
            for match in matches:
                #get the index of the player and find data about them using that index
                puuid_index = match["metadata"]["participants"].index(puuid)

                match_id = match["metadata"]["match_id"]
                placement = match["info"]["participants"][puuid_index]["placement"]

                db_match = crud.create_match(match_id)

                match_details = crud.create_match_details(puuid, match_id, placement)

                #Commiting one object at a time since commiting them all at once caused them to save in tables as None.
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
                    #If unit has an item equipped, add it to the association table. This is where line 59 is used.
                    if unit["itemNames"] != []:
                        for i in unit["itemNames"]:
                            item = crud.create_item(i)
                            print(item.item_name)
                            model.db.session.add(item)
                            model.db.session.commit()
                            for item_key, item_info in item_data.items():
                                if item_info["id"] == item.item_name:
                                    item.item_short_name = item_info["name"]
                            character_item = crud.create_character_item(match_character.match_character_id, item.item_id)
                            model.db.session.add(character_item)
                            model.db.session.commit()

        except Exception as e:
            return jsonify({"error": str(e)})
        return jsonify({"message": "Data received successfully"})
    except Exception as e:
        #identify the error I'm receiving
        return jsonify({"error": str(e)})

@app.route('/rank_details', methods=["POST"])
def rank_details():
    try:
        #after a player is stored in the database, store their rank
        data = request.get_json()

        puuid = data['puuid']
        rank = data['rank']

        player = crud.get_player_by_id(puuid)
        player.player_rank = rank
        db.session.commit()

        return jsonify({"message": "Rank received successfully"})
    except Exception as e:
        #error handling
        return jsonify({"error": str(e)})


@app.route('/')
def homepage():
    """Show homepage with search form"""
    
    return render_template("homepage.html")

@app.route('/match_history/<string:puuid>', methods = ['POST', 'GET'])
def match_history(puuid):
    """show match history for that specific player"""
    #get correct player by querying the database
    player = crud.get_player_by_id(puuid)
    if player == None:
        return redirect("/")
    
    #get correct matches from association table by using player id
    matches = crud.get_match_details_by_player_id(puuid)
    match_character_list = []

    #iterate through match details to get the characters that were used
    for match in matches:
        match_characters = crud.get_match_characters_by_match_details_id(match.id)
        for match_character in match_characters:
            match_character_list.append(match_character)
    character_items = []

    #iterate through the characters items if they have any and add them to a list that will be passed to the template
    for character in match_character_list:
        items = crud.get_character_items_by_match_character_id(character.match_character_id)
        if items != []:
            character_items.append(items)
    icon_link = f"http://ddragon.leagueoflegends.com/cdn/13.17.1/img/profileicon/{player.player_icon}.png"

    #access riots publicly available data that we will use for each champion to assign image and name
    response = requests.get("http://ddragon.leagueoflegends.com/cdn/13.18.1/data/en_US/tft-champion.json")
    data = response.json()

    champion_data = data.get("data", {})

    image_dict = {}
    #iterate over the data to get the images that correspond the characters.
    for champion_key, champion_info in champion_data.items():
        if "image" in champion_info:
            champion_id = champion_info["id"]
            #use list comprehension to iterate through the characters in the match and add them to a list if they are equal to a character in the dictionary
            matching_characters = [character for character in match_character_list if character.character.character_id.lower() == champion_id.lower()]
            #assign the name that is seen in the game to each matching character. (Or else names will display as TFT9_CharacterName)
            for character in matching_characters:
                character.character.character_name = champion_info["name"]
                if character.character.character_id == "tft9_reksai": #the only character that doesn't follow the naming standard in the json, manually corrected
                    character.character.character_id = "TFT9_RekSai"
            #finally, assign the correct image for each character
            if matching_characters:
                image_info = champion_info["image"]
                image_url = image_info["full"]
                image_dict[champion_id] = image_url
    
    #return all these list to be rendered by jinja template
    return render_template("match_history.html", player = player, matches = matches, icon_link = icon_link, match_character_list = match_character_list, character_items = character_items, image_dict = image_dict)


if __name__ == "__main__":
    from model import connect_to_db, db
    connect_to_db(app)
    db.create_all()
    app.run(host="0.0.0.0", debug=True)
