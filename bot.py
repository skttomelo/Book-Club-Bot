  
from dotenv import load_dotenv
from pathlib import Path
import os
import discord
from discord.ext import commands

# get env
env_path = Path('.') / 'config.env'
load_dotenv(dotenv_path=env_path)

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('Book Club Bot rdy!')

client.run(os.getenv('token'))
