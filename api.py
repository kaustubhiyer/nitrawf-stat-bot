import os

import requests

class API:

    def __init__(self, url, osu_key):
        # Constructor initializations
        self.api_url = url
        self.osu_key = osu_key
        response = requests.get(url + "/")
        if (response):
            print(response.json())
        else:
            print("Failed to initialize api, api down or incorrect api url")
        pass

    def get_all_players(self):
        response = requests.get(self.api_url + "/api/player/get-all")
        if not response:
            return None
        return response.json()

    def get_player_summary(self, username):
        # Need the id of the player with that username to fetch it from the api, so we need to reference osu's api
        osu_res = requests.get(f'https://osu.ppy.sh/api/get_user?k={self.osu_key}&u={username}')
        
        if osu_res.status_code != 200:
            print('\rSomething went wrong getting info for', username)
            return None
        
        user_id = osu_res.json()[0]['user_id']
        response = requests.get(self.api_url + "/api/player/"+ user_id + "/summary")
        if not response:
            return None
        return response.json()
    
    def get_player_matches(self, username):
        # Need the id of the player with that username to fetch it from the api, so we need to reference osu's api
        osu_res = requests.get(f'https://osu.ppy.sh/api/get_user?k={self.osu_key}&u={username}')
        
        if osu_res.status_code != 200:
            print('\rSomething went wrong getting info for', username)
            return None
        
        user_id = osu_res.json()[0]['user_id']
        response = requests.get(self.api_url + "/api/player/"+ user_id + "/matches")
        if not response:
            return None
        return response.json()

    def get_all_matches(self):
        response = requests.get(self.api_url + "/api/match/get-all")
        if not response:
            print(response.status_code)
            return None
        return response.json()
    
    def get_match_summary(self, match_id):
        response = requests.get(self.api_url + '/api/match/get-summary/' + match_id)
        if not response:
            print(response.status_code)
            return None
        return response.json()
    
    
