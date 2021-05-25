import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to discord!')

@client.event
async def on_message(message):
    if (message.content.lower().startswith('im')):
        res = "Hi " + message.content[3:] + ", I'm nitrawf-bot"
        await message.channel.send(res)

client.run(TOKEN)