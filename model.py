"""Models for Teamfight Tactics app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#classes from data model

class Player(db.Model):
    """A player"""

    __tablename__ = "players"

    player_id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String)
    player_level = db.Column(db.Integer)


    def __repr__(self):
        return f"<Player player_id={self.player_id} player name={self.player_name}>"

class Character(db.Model):
    """A character"""

    __tablename__ = "characters"

    character_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    character_name = db.Column(db.String)
    
    traits = db.relationship("Trait", secondary="character_traits", back_populates="characters")
    items = db.relationship("Item", secondary="character_item", back_populates="characters")

    def __repr__(self):
        return f"<Character character_id={self.character_id} character name={self.character_name}>"
    
class Trait(db.Model):

    __tablename__ = "traits"
    
    trait_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trait_name = db.Column(db.String)
    
    characters = db.relationship("Character", secondary="character_traits", back_populates="traits")

    def __repr__(self):
        return f"<Trait trait_id={self.trait_id} trait name={self.trait_name}>"
    
class Item(db.Model):

    __tablename__ = "items"

    item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    item_name = db.Column(db.String)
    
    characters = db.relationship("Character", secondary="character_item", back_populates="items")


    def __repr__(self):
        return f"<Item item_id={self.item_id} item name={self.item_name}>"
    
#NEW TABLES CHECK SAT

class AveragePlacement(db.Model):
    """Average placement of a player in their last 10 games"""

    __tablename__ = "average_placements"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id'))
    placement = db.Column(db.Float)  # assuming this is a float value
    
    player = db.relationship("Player", backref="average_placements")

    def __repr__(self):
        return f"<AveragePlacement id={self.id} player_id={self.player_id} placement={self.placement}>"

class MatchHistory(db.Model):
    """Match history of a player"""

    __tablename__ = "match_history"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id'))
    match_id = db.Column(db.String)  #store match IDs as strings
    placement = db.Column(db.Integer)  
    date_played = db.Column(db.DateTime)

    player = db.relationship("Player", backref="match_history")

    def __repr__(self):
        return f"<MatchHistory id={self.id} player_id={self.player_id} match_id={self.match_id} placement={self.placement}>"


class MatchDetails(db.Model):
    """Details of individual matches"""

    __tablename__ = "match_details"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    match_id = db.Column(db.String, db.ForeignKey('match_history.match_id'))
    # Add additional fields for champions, items, and outcome

    match = db.relationship("MatchHistory", backref="match_details")

    def __repr__(self):
        return f"<MatchDetails id={self.id} match_id={self.match_id}>"

    
#Association tables from data model for many to many relationships

class Character_item(db.Model):
    """Association table to establish a many-to-many relationship between Character and Item"""

    __tablename__ = "character_item"

    character_item_id = db.Column(db.Integer, autoincrement = True, primary_key = True) #autoincrement?
    character_id = db.Column(db.Integer, db.ForeignKey("characters.character_id"), nullable = False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.item_id"), nullable=False)
    num_items = db.Column(db.Integer)
    play_rate = db.Column(db.Float)
    win_rate = db.Column(db.Float)

    def __repr__(self):
        return f"<Character_item_id={self.character_item_id} character_id={self.character_id} item_id={self.item_id}>"
    
class CharacterTraits(db.Model):
    """Association table to establish a many-to-many relationship between Character and Trait."""

    #come back to after MVP
    __tablename__ = "character_traits"

    character_id = db.Column(db.Integer, db.ForeignKey("characters.character_id"), primary_key=True)
    trait_id = db.Column(db.Integer, db.ForeignKey("traits.trait_id"), primary_key=True)


    def __repr__(self):
        return f"<CharacterTraits character_id={self.character_id} trait_id={self.trait_id}>"

def connect_to_db(flask_app, db_uri="postgresql:///teamfight_tactics", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app, echo = False)