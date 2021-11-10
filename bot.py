import discord
from discord.ext import commands
from discord_slash import SlashCommand

import os, io
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

import jasima, acronym, sitelenpona, preferences

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
@slash.slash(name="acro")
async def slash_acro(ctx, text):
    await acro(ctx, text)

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
@bot.command(name="acro")
async def command_acro(ctx, *, text):
    if text.startswith("text:"):
        text = text.replace("text:", "", 1)
    await acro(ctx, text)


async def nimi(ctx, word):
    lang = preferences.get_preference(str(ctx.author.id), "language", "en")

    response = jasima.get_word_entry(word)
    if isinstance(response, str):
        await ctx.send(response)
    else:
        embed = discord.Embed(title=response["word"],
                              url="https://lipu-linku.github.io/?q={}".format(word),
                              colour=colours[response["book"]])
        embed.add_field(name="book", value=response["book"])
        if lang in response["def"]:
            embed.add_field(name="description", value=response["def"][lang])
        else:
            embed.add_field(name="description", value="(en) {}".format(response["def"]["en"]))
        await ctx.send(embed=embed)


async def ss(ctx, word):
    response = jasima.get_word_entry(word)
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
    fontsize = preferences.get_preference(str(ctx.author.id), "fontsize", 133)
    await ctx.send(file=discord.File(io.BytesIO(sitelenpona.display(text, fontsize)), filename="a.png"))


async def acro(ctx, text):
    book = preferences.get_preference(str(ctx.author.id), "acro", "ku suli")
    await ctx.send(acronym.respond(text, book))


@slash.subcommand(base="preferences", name="language")
async def preferences_language(ctx, lang):
    preferences.set_preference(str(ctx.author.id), "language", lang)
    await ctx.send("Set language preference for **{}** to **{}**.".format(ctx.author.display_name, lang))

@slash.subcommand(base="preferences", name="acro")
async def preferences_acro(ctx, book):
    preferences.set_preference(str(ctx.author.id), "acro", book)
    await ctx.send("Set acronym book preference for **{}** to **{}**.".format(ctx.author.display_name, book))

@slash.subcommand(base="preferences", name="fontsize")
async def preferences_fontsize(ctx, size):
    if not (size <= 500 and size >= 1):
        await ctx.send("Font size is limited to the range from 1 to 500.")
    else:
        preferences.set_preference(str(ctx.author.id), "fontsize", size)
        await ctx.send("Set fontsize preference for **{}** to **{}**.".format(ctx.author.display_name, size))

@slash.subcommand(base="preferences", name="reset")
async def preferences_reset(ctx):
    preferences.reset_preferences(str(ctx.author.id))
    await ctx.send("Reset preferences for **{}**.".format(ctx.author.display_name))


@bot.command()
async def reload(ctx):
    jasima.routine()


def from_hex(value):
    return int(value, base=16)//256//256, int(value, base=16)//256%256, int(value, base=16)%256
colours = {"pu": discord.Colour.from_rgb(*from_hex("fff882")),
           "ku suli": discord.Colour.from_rgb(*from_hex("42a75a")),
           "ku lili": discord.Colour.from_rgb(*from_hex("1f5666")),
           "none": discord.Colour.from_rgb(*from_hex("0d092a"))
           }

bot.run(TOKEN, reconnect=True)
