import os
import json
from datetime import datetime

import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
load_dotenv()

import constants

intents = discord.Intents.default()
intents.members = True

prefixes = ["gda ", "gda", "GDA ", "GDA", "Gda ", "Gda "]
bot = commands.Bot(command_prefix=prefixes, case_insensitive=True, intents=intents)
#TODO: get the bot to work with mentions

statuses = [
    "It's dangerous to go alone. Take this!",
    "Cheers love! GDA Bot is here!",
    "All your base are belong to us.",
    "The cake is a lie.",
    "Your bot is in another castle.",
    "Press F to pay respects.",
    "It's super effective!",
    "A new challenger approaches!"
]

SAY_HI_CHANNEL_ID = 756246179565797408
WELCOME_CHANNEL_ID = 521957837937704969

@bot.event
async def on_ready():
    print(datetime.now())
    print("GDA Bot: Ready to rumble!")
    i = 0
    while True:
        name = f"gda help | {statuses[i]}"
        await bot.change_presence(activity=discord.Game(name=name))
        i += 1
        i %= len(statuses)
        await asyncio.sleep(60)

@bot.event
async def on_member_join(member):
    say_hi_channel = member.guild.get_channel(SAY_HI_CHANNEL_ID)
    welcome_channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
    if say_hi_channel is None or welcome_channel is None:
        print(f"Error with finding channels:")
        print(f"say_hi_channel: {say_hi_channel}")
        print(f"welcome_channel: {welcome_channel}")
        return
    await say_hi_channel.send(
        f"Hey, {member.mention}! Feel free to introduce yourself here, and "
        f"check out {welcome_channel.mention} to unlock the rest of the server."
    )

def load_extensions(bot):
    """Loads all extensions found in the cogs folder."""
    os.chdir("cogs")
    if __name__ == "__main__":
        for path in os.listdir():
            if os.path.isfile(path):
                cog = os.path.splitext(path)[0]
                if cog != "__init__":
                    try:
                        bot.load_extension(f"cogs.{cog}")
                        print(f"{cog} sucessfully loaded.")
                    except Exception as Ex:
                        print(f"{cog} could not be loaded because {Ex}")
    os.chdir("..")
load_extensions(bot)

@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    guild = channel.guild
    member = await guild.fetch_member(payload.user_id)
    if member.bot:
        return
    if str(payload.emoji) != "✅":
        return
    role_id = constants.role_messages.get(str(payload.message_id))
    if role_id is not None:
        await member.add_roles(guild.get_role(role_id))

@bot.event
async def on_raw_reaction_remove(payload):
    channel = bot.get_channel(payload.channel_id)
    guild = channel.guild
    member = await guild.fetch_member(payload.user_id)
    if member.bot:
        return
    if str(payload.emoji) != "✅":
        return
    role_id = constants.role_messages.get(str(payload.message_id))
    if role_id is not None:
        await member.remove_roles(guild.get_role(role_id))

@bot.event
async def on_raw_message_delete(payload):
    id = str(payload.message_id)
    if id in constants.role_messages:
        constants.role_messages.pop(id)
        with open("data/roles.json", "w") as f:
            json.dump(constants.role_messages, f, indent=4)

bot.run(os.getenv(key='DISCORD_BOT_TOKEN'))
