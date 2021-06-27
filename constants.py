import discord
from discord.ext import commands
import json

with open("data/roles.json") as f:
    role_messages = json.load(f)
