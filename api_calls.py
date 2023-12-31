import requests
import os

api_key = os.environ.get('API_KEY')
region = "americas" #routing value

def fetch_match_id(player_id):

        #make another api call using passed player id to receive match id
        url = f"https://{region}.api.riotgames.com/tft/match/v1/matches/by-puuid/{player_id}/ids"
        headers = {
            "X-Riot-Token": api_key
        }
        
        response = requests.get(url, headers=headers)

        all_matches = []

        if response.status_code == 200:
            match_ids = response.json()
            for match_id in match_ids:  #iterate through match_ids and make one more api call for match data based on match id
                url = f"https://{region}.api.riotgames.com/tft/match/v1/matches/{match_id}"
                response = requests.get(url, headers=headers)
                if response.status_code == 200: #append each match data object to a list
                    match_data = response.json()
                    all_matches.append(match_data)
                    #limit the amount of matches we receive to 5, speeds up runtime due to api rate limit
                    if len(all_matches) >= 5:
                         break
            
        return all_matches
