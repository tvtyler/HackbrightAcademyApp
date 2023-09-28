from model import db, Player, Character, Item, Character_item, Match, Match_details, connect_to_db #will need to import pairings/charactertraits later

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

def create_match_details(player_id, match_id, placement):
    details = Match_details(
        player_id = player_id,
        match_id = match_id,
        placement = placement,
    )
    
    return details
#will need to add the other many-to-many relationships later



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

def get_all_characters():
    return Character.query.all()

def get_character_by_id(character_id):
    return Character.query.get(character_id)

def get_all_items():
    return Item.query.all()

def get_item_by_id(item_id):
    return Item.query.get(item_id)

def get_items_for_character(character_id):
    return db.session.query(Character_item).filter_by(character_id=character_id).all()

def get_characters_for_item(item_id):
    return db.session.query(Character_item).filter_by(item_id=item_id).all()


#MIGHT NEED UPDATE/DELETE OPERATIONS LATER

if __name__ == "__main__":
    from model import connect_to_db
    from server import app

    connect_to_db(app)