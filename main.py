import os

import discord
from dotenv import load_dotenv
from api import API
import json
from tabulate import tabulate
import text_to_image

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
API_URL = os.getenv('API_URL')
OSU_API = os.getenv('OSU_API_KEY')

client = discord.Client()
api = API(API_URL, OSU_API)

def clean_data(raw_data, d_type):
    if (d_type == "plist"):
        # players list
        cols = ["Rank", "ID", "Name", "Avg Score", "Matches", "Elo"]
        data = []
        for player in raw_data:
            cleaned_player = []
            cleaned_player+=[player["player_rank"]]
            cleaned_player+=[player["id"]]
            cleaned_player+=[player["name"]]
            cleaned_player+=[player["average_score"]]
            cleaned_player+=[player["matches_played"]]
            cleaned_player+=[player["elo"]]
            data+=[cleaned_player]
        return cols, data
        


@client.event
async def on_ready():
    print(f'{client.user} has connected to discord!')

MAX_ATTEMPTS = 3

@client.event
async def on_message(message):
    if (message.author == client.user):
        return
    
    if len(message.content) <= 1 or (not message.content.lower().startswith('$')):
        return
    request = message.content[1:]
    command = request.split(" ")
    if command[0] == "players":
        #implement players call
        count = 0
        while (count < MAX_ATTEMPTS):
            players_raw = api.get_all_players()
            if not players_raw:
                count+=1
            else:
                players_raw = players_raw[0:5]
                break
        if count == 3:
            await message.channel.send("Failed to retreive from API. Please try again")
            return
        # need to clean up the data
        cols, players = clean_data(players_raw, "plist")
        table = tabulate(players, headers=cols, tablefmt="fancy_grid", \
            colalign=("left", "center", "left", "center", "center", "right"))
        text_to_image.encode(table, "image.png")
        await message.channel.send("```"+table+"```")
        return
    elif command[0] == "player":
        #implement player call
        pass
    elif command[0] == "matches":
        #implement matches call
        pass
    elif command[0] == "match":
        #implement match call
        pass
    elif command[0] == "elohistory":
        #implement elo history
        pass
    elif command[0] == "help":
        #help im out
        pass
    else:
        #invalid command (tell em!)
        pass
    # await message.channel.send(res)

client.run(TOKEN)