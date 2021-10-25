import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

import discord
import dictreader

bot = commands.Bot(command_prefix="/")

@bot.event
async def on_ready():
    for guild in bot.guilds:
        print("* {}".format(guild.name))

@bot.command()
async def mu(ctx, arg):
    await ctx.send(dictreader.get_word_entry(arg))

@bot.command()
async def reload_source(ctx):
    dictreader.build_json()
    dictreader.upload_json_to_github()

bot.run(TOKEN, reconnect=True)
