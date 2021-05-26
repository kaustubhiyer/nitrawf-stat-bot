import os

import requests

class API:

    def __init__(self, url, osu_key):
        # Constructor initializations
        self.api_url = url
        self.osu_key = osu_key

    def get_all_players(self, page):
        response = requests.get(self.api_url + "/api/player/get-all")
        if not response:
            return None, 0
        obj = response.json()
        max_pg = len(obj) // 5 + 1 if len(obj) % 5 != 0 else len(obj) // 5
        if page > max_pg:
            return obj[0:5], max_pg
        elif page == max_pg:
            return obj[(page-1)*5:], max_pg
        return obj[(page-1)*5:(page)*5], max_pg

    def get_player_summary(self, username):
        # Need the id of the player with that username to fetch it from the api, so we need to reference osu's api
        osu_res = requests.get(f'https://osu.ppy.sh/api/get_user?k={self.osu_key}&u={username}')
        
        if osu_res.status_code != 200:
            print('\rSomething went wrong getting info for', username)
            return None
        user_obj = osu_res.json()
        user_id = user_obj[0]['user_id']
        response = requests.get(self.api_url + "/api/player/"+ user_id + "/summary")
        if not response:
            print('\r Something went wrong interacting with the api to get details of', username)
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

    def get_all_matches(self, page):
        response = requests.get(self.api_url + "/api/match/get-all")
        if not response:
            print(response.status_code)
            return None, 0
        obj = response.json()
        max_pg = len(obj) // 5 + 1 if len(obj) % 5 != 0 else len(obj) // 5
        if page > max_pg:
            return obj[0:5], max_pg
        elif page == max_pg:
            return obj[(page-1)*5:], max_pg
        return obj[(page-1)*5:(page)*5], max_pg
    
    def get_match_summary(self, match_id):
        response = requests.get(self.api_url + '/api/match/get-summary/' + match_id)
        if not response:
            print(response.status_code)
            return None
        return response.json()
    
    def get_elo_history(self, username):
        # Need the id of the player with that username to fetch it from the api, so we need to reference osu's api
        osu_res = requests.get(f'https://osu.ppy.sh/api/get_user?k={self.osu_key}&u={username}')
        
        if osu_res.status_code != 200:
            print('\rSomething went wrong getting info for', username)
            return None
        user_obj = osu_res.json()
        user_id = user_obj[0]['user_id']
        response = requests.get(self.api_url + "/api/player/"+ user_id + "/elo-history")
        if not response:
            print('\r Something went wrong interacting with the api to get details of', username)
            return None
        return response.json()


