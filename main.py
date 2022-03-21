from logging import exception
import discord
from discord.ext import commands
import json
import os

CONFIG_PATH = "config.json"

def read_config():
      with open(CONFIG_PATH) as file:
        return json.load(file)

config = read_config()

from cogs import events
from cogs import support

intents = discord.Intents.all()
client = commands.Bot(command_prefix=commands.when_mentioned_or(config["prefix"]), intents=intents)

client.add_cog(events.events(client, config))
client.add_cog(support.support(client, config))

if config["token"] is not None: 
  token = config["token"]
elif os.environ['token'] is not None:
  token = os.environ['token']
else:
  print("No token found")

client.run(token)