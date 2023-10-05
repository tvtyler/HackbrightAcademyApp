"""Models for Teamfight Tactics app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#relationship between players and matches
class Match_details(db.Model):
    """Match history of a player"""

    __tablename__ = "match_details"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    player_id = db.Column(db.String, db.ForeignKey('players.player_id'))
    match_id = db.Column(db.String, db.ForeignKey('match.match_id')) #unique? #store match IDs as strings
    placement = db.Column(db.Integer)

    match = db.relationship("Match", back_populates="match_details")
    players = db.relationship("Player", back_populates="player_details")
    match_characters = db.relationship("MatchCharacter", back_populates="match_detail")

    def __repr__(self):
        return f"<match_details id={self.id} player_id={self.player_id} match_id={self.match_id}>"
    
class MatchCharacter(db.Model):
    """Association table to establish a many-to-many relationship between Match_details and Character"""

    __tablename__ = "match_character"

    match_character_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    match_detail_id = db.Column(db.Integer, db.ForeignKey("match_details.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("characters.id"))
    
    match_detail = db.relationship("Match_details", back_populates="match_characters")
    character = db.relationship("Character", back_populates="match_characters")
    character_item = db.relationship("Character_item", back_populates="match_characters")

    def __repr__(self):
        return f"<MatchCharacter match_character_id={self.match_character_id} match_detail_id={self.match_detail_id} character_id={self.character_id}"

class Character_item(db.Model):
    """Association table to establish a many-to-many relationship between MatchCharacter and Item"""

    __tablename__ = "character_items"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.item_id"))
    match_character_id = db.Column(db.Integer, db.ForeignKey("match_character.match_character_id"))

    match_characters = db.relationship("MatchCharacter", back_populates="character_item")
    item = db.relationship("Item", back_populates="character_item")

class Player(db.Model):
    """A player"""

    __tablename__ = "players"

    player_id = db.Column(db.String, unique=True, primary_key=True) #puuid
    player_name = db.Column(db.String)
    player_level = db.Column(db.Integer)
    player_icon = db.Column(db.Integer)
    player_rank = db.Column(db.String)

    player_details = db.relationship("Match_details", back_populates="players")

    def __repr__(self):
        return f"<Player player_id={self.player_id} player name={self.player_name}>"
    
class Match(db.Model):
    """Instance of a match"""

    __tablename__ ="match"

    match_id = db.Column(db.String, unique=True, primary_key=True)

    match_details = db.relationship("Match_details", back_populates="match")

    def __repr__(self):
        return f"<MatchID id={self.id} player_id={self.player_id} match_id={self.match_id}>"
    
class Character(db.Model):
    """A character"""

    __tablename__ = "characters"

    id = db.Column(db.Integer, autoincrement = True,  primary_key=True)
    character_name = db.Column(db.String)
    
    match_characters = db.relationship("MatchCharacter", back_populates="character")

    def __repr__(self):
        return f"<Character character_id={self.character_id} character name={self.character_name}>"
    
class Item(db.Model):

    __tablename__ = "items"

    item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    item_name = db.Column(db.String)
    
    character_item = db.relationship("Character_item", back_populates="item")

    def __repr__(self):
        return f"<Item item_id={self.item_id} item name={self.item_name}>"


def connect_to_db(flask_app, db_uri="postgresql:///Teamfight_Tactics", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app, echo = False)