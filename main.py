import os

import discord
from dotenv import load_dotenv
from api import API
import json
from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

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
            cleaned_player+=[round(player["average_accuracy"]*100, 2)]
            cleaned_player+=[player["matches_played"]]
            cleaned_player+=[player["elo"]]
            data+=[cleaned_player]
        return cols, data
    elif (d_type == "mlist"):
        #matches list
        cols = ["Match ID", "Match Name", "Start Time"]
        data = []
        for match in raw_data:
            cleaned_match = []
            cleaned_match+=[match["id"]]
            cleaned_match+=[match["name"]]
            cleaned_match+=[match["start_time"][2:10] + " " + match["start_time"][11:16]]
            # cleaned_match+=[match["end_time"][:10] + " " + match["end_time"][11:16]]
            data+=[cleaned_match]
        return cols, data
    elif (d_type == "match"):
        # single match
        cols = ["Name", "Avg Pos", "Avg Score", "Avg Acc", "Elo Change"]
        data = []
        for player in raw_data:
            cleaned_player = []
            cleaned_player+=[player["player_name"]]
            cleaned_player+=[player["average_position"]]
            cleaned_player+=[player["average_score"]]
            cleaned_player+=[round(player["average_accuracy"]*100, 2)]
            cleaned_player+=[str(player["old_elo"])+'-'+str(player['new_elo'])]
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
        img = Image.new('RGB', (540, 240), color = (35, 39, 42))
        d = ImageDraw.Draw(img)
        fnt = ImageFont.truetype('DejaVuSansMono.ttf', 12)
        d.text((10,10), table, fill=(255,255,255), font=fnt)
        img.save('players.png')
        with open('players.png', 'rb') as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)
        # send
        # await message.channel.send("```"+table+"```")
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
        count = 0
        while (count < MAX_ATTEMPTS):
            obj = api.get_player_summary(username)
            if not obj:
                count+=1
            else:
                break
        if count == MAX_ATTEMPTS:
            await message.channel.send("You aren't in the db, or something went wrong...")
        description = \
            "```\u2023 Player ID:        " + str(obj["id"]) + "\n" + \
            "\u2023 Player Rank:      " + str(obj["player_rank"]) + "\n" + \
            "\u2023 Maps Played:      " + str(obj["maps_played"]) + "\n" + \
            "\u2023 Matches Played:   " + str(obj["matches_played"]) + "\n" + \
            "\u2023 Average Score:    " + str(obj["average_score"]) + "\n" + \
            "\u2023 Average Accuracy: " + str(round(obj["average_accuracy"]*100, 2)) + "\n"+ \
            "\u2023 Elo:              " + str(obj["elo"]) + "```"
        player_embed = discord.Embed(title = "nitrawf Profile for "+username, \
            url="https://osu.ppy.sh/users/"+str(obj["id"]), \
                color=discord.Color.magenta(), \
                    description=description)
        player_embed.set_thumbnail(url="https://a.ppy.sh/"+str(obj["id"]))
        await message.channel.send(embed=player_embed)
        pass
    elif command[0] == "matches":
        #implement matches call
        # find which page
        index_page_no = (command.index("-p") + 1) if "-p" in command else len(command)
        if (len(command) > index_page_no) and command[index_page_no].isnumeric():
            page = int(command[index_page_no])
        else:
            page = 1
        #implement matches call
        count = 0
        while (count < MAX_ATTEMPTS):
            matches_raw, max_pg = api.get_all_matches(page)
            if not matches_raw:
                count+=1
            else:
                break
        if count == 3:
            await message.channel.send("Failed to retreive from API. Please try again")
            return
        # need to clean up the data
        cols, matches = clean_data(matches_raw, "mlist")
        ## GET MOST RECENT MATCHES FIRST
        table = tabulate(matches, headers=cols, tablefmt="fancy_grid", \
            colalign=("left", "center", "center"))
        table = table + "\nPage " + (str(page) if page <= max_pg else "1") + " out of " + str(max_pg) 
        img = Image.new('RGB', (500, 245), color = (35, 39, 42))
        d = ImageDraw.Draw(img)
        fnt = ImageFont.truetype('DejaVuSansMono.ttf', 12)
        d.text((10,10), table, fill=(255,255,255), font=fnt)
        img.save('matches.png')
        with open('matches.png', 'rb') as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)
        # await message.channel.send("```"+table+"```")
        return
        pass
    elif command[0] == "match":
        #implement match call
        if len(command) != 2:
            await message.channel.send("Wrong command, ask $help for help")
            return
        match_id = command[1]
        count = 0
        while (count < MAX_ATTEMPTS):
            match_raw = api.get_match_summary(match_id)
            if not match_raw:
                count+=1
            else:
                break
        if count == 3:
            await message.channel.send("Failed to retreive from API. Please try again")
            return
        
        # Need to clean match
        cols, match = clean_data(match_raw, "match")
        match = sorted(match, key=lambda x: x[2], reverse=True)
        table = tabulate(match, headers=cols, tablefmt="fancy_grid", \
            colalign=("left", "center", "center", "center", "center"))
        height_m = len(match)-1
        img = Image.new('RGB', (525, 100+(32*height_m)), color = (35, 39, 42))
        d = ImageDraw.Draw(img)
        fnt = ImageFont.truetype('DejaVuSansMono.ttf', 12)
        d.text((10,10), table, fill=(255,255,255), font=fnt)
        img.save('match.png')
        with open('match.png', 'rb') as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)
        return
        pass
    elif command[0] == "elohistory":
        #implement elo history
        #implement player call
        if len(command) < 2:
            await message.channel.send("Incorrect formatting for command, $help for help")
            return
        if "\"" in request:
            # extract username (has spaces)
            username = request[request.index("\"")+1:request.rindex("\"")]
        else:
            username = command[1]
        count = 0
        while (count < MAX_ATTEMPTS):
            obj = api.get_elo_history(username)
            if not obj:
                count+=1
            else:
                break
        if count ==  MAX_ATTEMPTS:
            await message.channel.send("Player not in database, or I messed up, tee hee!")
        elos = np.array([obj[0]['old_elo']] + [i['new_elo'] for i in obj])
        times = [datetime.strptime(obj[0]['start_time'], '%Y-%m-%dT%H:%M:%S')]+ \
            [datetime.strptime(i['end_time'], '%Y-%m-%dT%H:%M:%S') for i in obj]
        # times = dates.date2num(times)
        x_axis = np.array(list(range(1,len(elos)+1)))
        # plt.plot_date(times, elos)
        plt.plot(x_axis, elos)
        plt.ylabel("Elo Change")
        plt.xlabel("Matches")
        plt.savefig("temp.png")
        plt.close()
        with open('temp.png', 'rb') as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)
        os.remove("temp.png")
        await message.channel.send("Done!")
        pass
    elif command[0] == "help":
        #help im out
        await message.author.send("Refer to https://github.com/kaustubhiyer/nitrawf-stat-bot")
        pass
    else:
        #invalid command (tell em!)
        pass
    # await message.channel.send(res)

client.run(TOKEN)