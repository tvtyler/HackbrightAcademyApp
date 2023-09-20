from model import db, Player, Character, Trait, Item, Character_item, Match, MatchHistory, connect_to_db #will need to import pairings/charactertraits later

#create operations

def create_player(player_id, summoner_level, name):
        
    player = Player(
        player_id = player_id,
        player_level = summoner_level,
        player_name = name
    )

    return player

def create_character(character_name):
    new_character = Character(character_name=character_name)
    db.session.add(new_character)
    db.session.commit()

    return new_character

def create_trait(trait_name):
    new_trait = Trait(trait_name=trait_name)
    db.session.add(new_trait)
    db.session.commit()

    return new_trait

def create_item(item_name):
    new_item = Item(item_name=item_name)
    db.session.add(new_item)
    db.session.commit()

    return new_item

def create_match(match_id, player_id, placement, date_played):
        
    match = Match(
        match_id = match_id,
        player_id = player_id,
        placement = placement,
        date_played = date_played
    )

    return match


#will need to add the other many-to-many relationships later



#read operations

def get_all_players():
    return Player.query.all()

def get_player_by_id(player_id):
    return Player.query.get(player_id)

def get_all_characters():
    return Character.query.all()

def get_character_by_id(character_id):
    return Character.query.get(character_id)

def get_all_traits():
    return Trait.query.all()

def get_trait_by_id(trait_id):
    return Trait.query.get(trait_id)

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