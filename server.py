"""Server for Teamfight Tactics app."""

from flask import Flask
from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
from jinja2 import StrictUndefined
import crud, requests, os

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

#API info
api_key = os.environ.get('API_KEY')
routing_value = os.environ.get('ROUTING_VALUE')

#routes
#REMEMBER TO UPDATE GET/POST AS NEEDED
@app.route('/')
def homepage():
    """Show homepage"""

    return render_template("homepage.html")

@app.route('/characters')
def show_characters():
    """Show characters that you want to see the best items for"""
    

    return render_template("characters.html")

@app.route('/item/<id>')
def show_character_items(id):
    """A page for showing a characters best items"""

    return render_template("character_items.html")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
