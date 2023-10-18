from model import *

#create operations

def create_player(player_id, summoner_level, name, icon):
        
    player = Player(
        player_id = player_id,
        player_level = summoner_level,
        player_name = name,
        player_icon = icon
    )

    return player

def create_match(match_id):
        
    match = Match(
        match_id = match_id,
    )

    return match

def create_item(item_name):
    item = Item(item_name = item_name)

    return item

def create_match_details(player_id, match_id, placement):
    details = Match_details(
        player_id = player_id,
        match_id = match_id,
        placement = placement
    )
    
    return details

def create_match_characters(match_detail_id, character_id):
    match_character = MatchCharacter(
        match_detail_id = match_detail_id,
        character_id = character_id
    )
    
    return match_character

def create_character(character_id):
    character = Character(character_id = character_id)

    return character

def create_character_item(match_character_id, item_id):
    character_item = Character_item(
        match_character_id = match_character_id,
        item_id = item_id
    )

    return character_item

#read operations

def get_all_players():
    return Player.query.all()

def get_player_by_id(player_id):
    return Player.query.get(player_id)

def get_all_matches():
    return Match.query.all()

def get_all_match_details():
    return Match_details.query.all()

def get_match_details_by_player_id(player_id):
    return Match_details.query.filter(Match_details.player_id == player_id).all()

def get_match_characters_by_match_details_id(match_detail_id):
    return MatchCharacter.query.filter(MatchCharacter.match_detail_id == match_detail_id).all()

def get_all_characters():
    return Character.query.all()

def get_character_by_id(character_id):
    return Character.query.get(character_id)

def get_all_items():
    return Item.query.all()

def get_item_by_id(item_id):
    return Item.query.get(item_id)

def get_character_items_by_match_character_id(match_character_id):
    return Character_item.query.filter(Character_item.match_character_id == match_character_id).all()


#MIGHT NEED UPDATE/DELETE OPERATIONS LATER

if __name__ == "__main__":
    from model import connect_to_db
    from server import app

    connect_to_db(app)