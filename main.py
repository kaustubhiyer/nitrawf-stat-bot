import os

import discord
from dotenv import load_dotenv
from api import API
import json
from tabulate import tabulate

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
API_URL = os.getenv('API_URL')
OSU_API = os.getenv('OSU_API_KEY')
PREFIX = "$"
MAX_ATTEMPTS = 3

client = discord.Client()
api = API(API_URL, OSU_API)

def clean_data(raw_data, d_type):
    if (d_type == "plist"):
        # players list
        cols = ["Rank", "Name", "Avg Score", "Avg Acc", "Matches", "Elo"]
        data = []
        for player in raw_data:
            cleaned_player = []
            cleaned_player+=[player["player_rank"]]
            cleaned_player+=[player["name"]]
            cleaned_player+=[player["average_score"]]
            cleaned_player+=[player["average_accuracy"]*100]
            cleaned_player+=[player["matches_played"]]
            cleaned_player+=[player["elo"]]
            data+=[cleaned_player]
        return cols, data
        


@client.event
async def on_ready():
    print(f'{client.user} has connected to discord!')


@client.event
async def on_message(message):
    if (message.author == client.user):
        return
    
    if len(message.content) <= 1 or (not message.content.lower().startswith('$')):
        return
    request = message.content[1:]
    command = request.split(" ")
    if command[0] == "players":
        # find which page
        index_page_no = (command.index("-p") + 1) if "-p" in command else len(command)
        if (len(command) > index_page_no) and command[index_page_no].isnumeric():
            page = int(command[index_page_no])
        else:
            page = 1
        #implement players call
        count = 0
        while (count < MAX_ATTEMPTS):
            players_raw, max_pg = api.get_all_players(page)
            if not players_raw:
                count+=1
            else:
                break
        if count == 3:
            await message.channel.send("Failed to retreive from API. Please try again")
            return
        # need to clean up the data
        cols, players = clean_data(players_raw, "plist")
        table = tabulate(players, headers=cols, tablefmt="fancy_grid", \
            colalign=("left", "left", "center", "center", "center", "right"))
        table = table + "\nPage " + (str(page) if page <= max_pg else "1") + " out of " + str(max_pg) 
        await message.channel.send("```"+table+"```")
        return
    elif command[0] == "player":
        #implement player call
        if len(command) < 2:
            await message.channel.send("Incorrect formatting for command, $help for help")
            return
        if "\"" in request:
            # extract username (has spaces)
            username = request[request.index("\"")+1:request.rindex("\"")]
        else:
            username = command[1]
        obj = api.get_player_summary(username)
        description = \
            "**\u2023 Player ID:**\t" + str(obj["id"]) + "\n" + \
            "**\u2023 Player Rank:**\t" + str(obj["player_rank"]) + "\n" + \
            "**\u2023 Maps Played:**\t" + str(obj["maps_played"]) + "\n" + \
            "**\u2023 Matches Played:**\t" + str(obj["matches_played"]) + "\n" + \
            "**\u2023 Average Score:**\t" + str(obj["average_score"]) + "\n" + \
            "**\u2023 Average Accuracy:**\t" + str(obj["average_accuracy"]*100) + "\n"+ \
            "**\u2023 Elo:**\t" + str(obj["elo"]) + "\n"
        player_embed = discord.Embed(title = "nitrawf Profile for "+username, \
            url="https://osu.ppy.sh/users/"+str(obj["id"]), \
                color=discord.Color.magenta(), \
                    description=description)
        player_embed.set_thumbnail(url="https://a.ppy.sh/"+str(obj["id"]))
        print(obj)
        await message.channel.send(embed=player_embed)
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