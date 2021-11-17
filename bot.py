import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle

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
@slash.slash(name="lp")
async def slash_lp(ctx, word):
    await lp(ctx, word)
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
@bot.command(name="lp")
async def command_lp(ctx, word):
    if word.startswith("word:"):
        word = word.replace("word:", "", 1)
    await lp(ctx, word)
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
        return
    embed = embed_response(word, lang, response, "concise")
    components = build_action_row(word, lang, "expand")
    await ctx.send(embed=embed, components=components)


async def ss(ctx, word):
    lang = preferences.get_preference(str(ctx.author.id), "language", "en")

    response = jasima.get_word_entry(word)
    if isinstance(response, str):
        await ctx.send(response)
        return
    embed = embed_response(word, lang, response, "image")
    await ctx.send(embed=embed)


async def lp(ctx, word):
    response = jasima.get_word_entry(word)
    if isinstance(response, str):
        await ctx.send(response)
        return
    if "luka_pona" in response:
        if "gif" in response["luka_pona"]:
            await ctx.send(response["luka_pona"]["gif"])
            return
    await ctx.send(f"No luka pona available for **{word}**")


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


@bot.event
async def on_component(ctx):
    # you may want to filter or change behaviour based on custom_id or message
    buttontype, word, lang = ctx.custom_id.split(";")
    if buttontype == "expand":
        embed = embed_response(word, lang, jasima.get_word_entry(word), "verbose")
        components = build_action_row(word, lang, "minimise")
    if buttontype == "minimise":
        embed = embed_response(word, lang, jasima.get_word_entry(word), "concise")
        components = build_action_row(word, lang, "expand")
    await ctx.edit_origin(embed=embed, components=components)

def embed_response(word, lang, response, embedtype):
    embed = discord.Embed()
    embed.title = response["word"]
    embed.colour = colours[response["book"]]
    description = response["def"][lang] if lang in response["def"] else "(en) {}".format(response["def"]["en"])
    embed.add_field(name="book", value=response["book"])

    if embedtype == "concise":
        embed.add_field(name="description", value=description)

    if embedtype == "verbose":
        embed.add_field(name="description", value=description, inline=False)
        if "etymology" in response or "source_language" in response:
            embed.add_field(name="etymology", value=build_etymology(response), inline=False)
        if "ku_data" in response:
            embed.add_field(name="ku data", value=response["ku_data"], inline=False)
        if "commentary" in response:
            embed.add_field(name="commentary", value=response["commentary"], inline=False)

    if embedtype == "image":
        if "sitelen_sitelen" in response:
            embed.set_image(url=response["sitelen_sitelen"])
        else:
            embed.description = "no sitelen sitelen available"
    return embed

def build_action_row(word, lang, buttontype):
    url = "https://lipu-linku.github.io/?q={}".format(word)
    buttons = [create_button(style=ButtonStyle.blue, label=f"{buttontype}", custom_id=f"{buttontype};{word};{lang}"),
               create_button(style=ButtonStyle.URL, label="more info", url=url)]
    return [create_actionrow(*buttons)]

def build_etymology(response):
    etymology = "←"
    if "source_language" in response:
        etymology += " " + response["source_language"]
    if "etymology" in response:
        etymology += " " + response["etymology"]
    return etymology


def from_hex(value):
    return int(value, base=16)//256//256, int(value, base=16)//256%256, int(value, base=16)%256
colours = {"pu": discord.Colour.from_rgb(*from_hex("fff882")),
           "ku suli": discord.Colour.from_rgb(*from_hex("42a75a")),
           "ku lili": discord.Colour.from_rgb(*from_hex("1f5666")),
           "none": discord.Colour.from_rgb(*from_hex("0d092a"))
           }

bot.run(TOKEN, reconnect=True)
