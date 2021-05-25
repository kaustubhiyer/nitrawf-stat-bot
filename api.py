import os

import requests

class API:

    def __init__(self, url):
        # Constructor initializations
        self.api_url = url
        response = requests.get(url + "/")
        if (response):
            print(response.json())
        else:
            print("Failed to initialize api, api down or incorrect api_url")
        pass

    def getPlayers(self):
        pass

    def getMatches(self):
        pass
