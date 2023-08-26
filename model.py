"""Models for Teamfight Tactics app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#classes from data model

class Player(db.Model):
    """A player"""

    #Could need changed later, not sure if player is needed since we only
    #require number of games on an augment, not the players that played them.

    __tablename__ = "players"

    player_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    player_name = db.Column(db.String)


    def __repr__(self):
        return f"<Player player_id={self.player_id} player name={self.player_name}>"

class Character(db.Model):
    """A character"""

    __tablename__ = "characters"

    character_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    character_name = db.Column(db.String)
    
    traits = db.relationship("Trait", secondary="character_traits", back_populates="characters")
    items = db.relationship("Item", secondary="character_item", back_populates="characters")
    character1_pairings = db.relationship("CharacterPairing", foreign_keys="[CharacterPairing.character1_id]", back_populates="character1") #unsure of
    character2_pairings = db.relationship("CharacterPairing", foreign_keys="[CharacterPairing.character2_id]", back_populates="character2")

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

class CharacterPairing(db.Model):
    """Association table to establish a many-to-many relationship between Characters."""

    #come back to after MVP
    __tablename__ = "character_pairings"

    pair_id = db.Column(db.Integer, primary_key = True) #changed from id to pair_id
    character1_id = db.Column(db.Integer, db.ForeignKey("characters.character_id"))
    character2_id = db.Column(db.Integer, db.ForeignKey("characters.character_id"))
    play_rate = db.Column(db.Float)
    win_rate = db.Column(db.Float)

    #should work even if character1 has multiple synergies, as the table will account for that
    character1 = db.relationship("Character", foreign_keys=[character1_id], back_populates="character1_pairings")
    character2 = db.relationship("Character", foreign_keys=[character2_id], back_populates="character2_pairings")

    def __repr__(self):
        return f"<CharacterPairing id={self.pair_id} character1_id={self.character1_id} character2_id={self.character2_id}>"
    
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