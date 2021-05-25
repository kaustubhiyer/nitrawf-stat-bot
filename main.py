import os

import discord
from dotenv import load_dotenv
from api import API
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
API_URL = os.getenv('API_URL')
OSU_API = os.getenv('OSU_API_KEY')

client = discord.Client()
api = API(API_URL, OSU_API)

@client.event
async def on_ready():
    print(f'{client.user} has connected to discord!')

@client.event
async def on_message(message):
    if (message.author == client.user):
        return
    
    if (message.content.lower().startswith('im')):
        res = "Hi " + message.content[3:] + ", I'm nitrawf-bot"
        await message.channel.send(res)

client.run(TOKEN)