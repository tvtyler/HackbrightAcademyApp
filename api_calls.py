import requests
import os

api_key = os.environ.get('API_KEY')
region = "americas" #might need to change to americas

def fetch_match_id(player_id):

        url = f"https://{region}.api.riotgames.com/tft/match/v1/matches/by-puuid/{player_id}/ids"
        headers = {
            "X-Riot-Token": api_key
        }
        
        response = requests.get(url, headers=headers)

        all_matches = []

        if response.status_code == 200:
            match_ids = response.json()
            for match_id in match_ids:  #iterate through match_ids
                url = f"https://{region}.api.riotgames.com/tft/match/v1/matches/{match_id}"
                response = requests.get(url, headers=headers)
                if response.status_code == 200: #append each match data object to a list
                    match_data = response.json()
                    all_matches.append(match_data)
            return all_matches
        else:
            # handle request error by returning empty list
            return []
