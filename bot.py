import discord
from discord.ext import commands
from discord_slash import SlashCommand

import os, io
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

import dictreader, acronym, sp_renderer

bot = commands.Bot(command_prefix="/")
slash = SlashCommand(bot)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        print("* {}".format(guild.name))

@slash.slash(name="nimi")
async def slash_nimi(ctx, word):
    await nimi(ctx, word)
@slash.slash(name="n")
async def slash_n(ctx, word):
    await nimi(ctx, word)
@slash.slash(name="ss")
async def slash_ss(ctx, word):
    await ss(ctx, word)
@slash.slash(name="sp")
async def slash_sp(ctx, text):
    await sp(ctx, text)

@bot.command(name="nimi")
async def command_nimi(ctx, word):
    if word.startswith("word:"):
        word = word.replace("word:", "", 1)
    await nimi(ctx, word)
@bot.command(name="n")
async def command_n(ctx, word):
    if word.startswith("word:"):
        word = word.replace("word:", "", 1)
    await nimi(ctx, word)
@bot.command(name="ss")
async def command_ss(ctx, word):
    if word.startswith("word:"):
        word = word.replace("word:", "", 1)
    await ss(ctx, word)
@bot.command(name="sp")
async def command_sp(ctx, *, text):
    if text.startswith("text:"):
        text = text.replace("text:", "", 1)
    await sp(ctx, text)


async def nimi(ctx, word):
    response = dictreader.get_word_entry(word)
    if isinstance(response, str):
        await ctx.send(response)
    else:
        embed = discord.Embed(title=response["word"],
                              url="https://lipu-linku.github.io/?q={}".format(word),
                              colour=colours[response["book"]])
        embed.add_field(name="book", value=response["book"])
        embed.add_field(name="description", value=response["def"]["en"])
        await ctx.send(embed=embed)


async def ss(ctx, word):
    response = dictreader.get_word_entry(word)
    if isinstance(response, str):
        await ctx.send(response)
    else:
        embed = discord.Embed(title=response["word"],
                              url="https://lipu-linku.github.io/?q={}".format(word),
                              colour=colours[response["book"]])
        if "sitelen_sitelen" in response:
            embed.set_image(url=response["sitelen_sitelen"])
        else:
            embed.description = "no sitelen sitelen available"
        await ctx.send(embed=embed)


async def sp(ctx, text):
    await ctx.send(file=discord.File(io.BytesIO(sp_renderer.display(text)), filename="a.png"))


@slash.subcommand(base="preferences", name="language")
async def preferences_language(ctx, lang):
    await ctx.send("Hi! You tried to set your lang preference to **{}**. Unfortunately, kala Asi has not implemented that part yet. But as you can see, it does get correctly recognised!".format(lang))


@bot.command()
async def acro(ctx, *args):
    if len(args) == 1:
        await ctx.send(acronym.respond(args[0]))
    else:
        await ctx.send(acronym.respond(args[0], args[1]))


@bot.command()
async def reload(ctx):
    dictreader.routine()


def from_hex(value):
    return int(value, base=16)//256//256, int(value, base=16)//256%256, int(value, base=16)%256
colours = {"pu": discord.Colour.from_rgb(*from_hex("fff882")),
           "ku suli": discord.Colour.from_rgb(*from_hex("42a75a")),
           "ku lili": discord.Colour.from_rgb(*from_hex("1f5666")),
           "none": discord.Colour.from_rgb(*from_hex("0d092a"))
           }

bot.run(TOKEN, reconnect=True)
