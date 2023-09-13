"""Server for Teamfight Tactics app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, db
from jinja2 import StrictUndefined
import crud, requests, os
import requests

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


@app.route('/')
def homepage():
    """Show homepage with search form"""
    
    return render_template("homepage.html")

@app.route('/player-details')
def show_characters():
    """Show a players details"""
    
    return render_template("player-details.html")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
