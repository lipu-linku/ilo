import discord
from discord.ext import commands
from discord_slash import SlashCommand

import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

import dictreader, acronym

bot = commands.Bot(command_prefix="/")
slash = SlashCommand(bot)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        print("* {}".format(guild.name))

@slash.slash(name="nimi")
async def nimi(ctx, word):
    print(word)
    await ctx.send(dictreader.get_word_entry(word))

@bot.command(name="acro")
async def acro(ctx, *args):
    if len(args) == 1:
        await ctx.send(acronym.respond(args[0]))
    else:
        await ctx.send(acronym.respond(args[0], args[1]))

@bot.command(name="reload")
async def reload(ctx):
    dictreader.build_json()
    dictreader.upload_json_to_github()

bot.run(TOKEN, reconnect=True)
