import discord
from discord.ext import commands


import os, io, json
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


from defines import *
import jasima
import acronym
import sitelenpona
import preferences


bot = commands.Bot(command_prefix="/")


@bot.event
async def on_ready():
    for guild in bot.guilds:
        print("* {}".format(guild.name))

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.author == bot.user:
        if reaction.emoji == "❌":
            await reaction.message.delete()

def to_choices(dictionary):
    return [discord.OptionChoice(name=k, value=v) for k, v in dictionary.items()]
def to_colours(dictionary):
    return {k: discord.Colour.from_rgb(*bytes.fromhex(v)) for k, v in dictionary.items()}

@bot.slash_command(
  name='nimi',
  description=text["DESC_NIMI"],
)
async def slash_nimi(ctx, word: discord.Option(str, text["DESC_NIMI_OPTION"])):
    await nimi(ctx, word)

@bot.slash_command(
  name='n',
  description=text["DESC_NIMI"],
)
async def slash_n(ctx, word: discord.Option(str, text["DESC_NIMI_OPTION"])):
    await nimi(ctx, word)

@bot.slash_command(
  name='lp',
  description=text["DESC_LP"],
)
async def slash_lp(ctx, word: discord.Option(str, text["DESC_LP_OPTION"])):
    await lp(ctx, word)

@bot.slash_command(
  name='sp',
  description=text["DESC_SP"],
)
async def slash_sp(ctx, text: discord.Option(str, text["DESC_SP_OPTION"])):
    await sp(ctx, text)

@bot.slash_command(
  name='ss',
  description=text["DESC_SS"],
)
async def slash_ss(ctx, text: discord.Option(str, text["DESC_SS_OPTION"])):
    await ss(ctx, text)

@bot.slash_command(
  name='preview',
  description=text["DESC_PREVIEW"],
)
async def slash_preview(ctx, text: discord.Option(str, text["DESC_PREVIEW_OPTION"])):
    await preview(ctx, text)

@bot.slash_command(
  name='acro',
  description=text["DESC_ACRO"],
)
async def slash_acro(ctx, text: discord.Option(str, text["DESC_ACRO_OPTION"])):
    await acro(ctx, text)

prefs = bot.create_group(
    "preferences",
    text["DESC_PREFS"]
    )

@prefs.command(
    name="fontsize",
    description=text["DESC_PREFS_FONTSIZE"],
    )
async def preferences_fontsize(ctx, size: discord.Option(int, text["DESC_PREFS_FONTSIZE_OPTION"])):
    if not (size <= 500 and size >= 14):
        await ctx.respond("Font size is limited to the range from 14 to 500.")
    else:
        preferences.set_preference(str(ctx.author.id), "fontsize", size)
        await ctx.respond("Set fontsize preference for **{}** to **{}**.".format(ctx.author.display_name, size))


@prefs.command(
    name="acro",
    description=text["DESC_PREFS_ACRO"],
    )
async def preferences_acro(ctx, book: discord.Option(str, text["DESC_PREFS_ACRO_OPTION"], choices=to_choices(acro_choices))):
    preferences.set_preference(str(ctx.author.id), "acro", book)
    await ctx.respond("Set acronym book preference for **{}** to **{}**.".format(ctx.author.display_name, book))

@prefs.command(
    name="font",
    description=text["DESC_PREFS_FONT"],
    )
async def preferences_font(ctx, font: discord.Option(str, text["DESC_PREFS_FONT_OPTION"], choices=list(fonts))):
    preferences.set_preference(str(ctx.author.id), "font", font)
    await ctx.respond("Set font preference for **{}** to **{}**.".format(ctx.author.display_name, font))

@prefs.command(
    name="reset",
    description=text["DESC_PREFS_RESET"],
    )
async def preferences_reset(ctx):
    preferences.reset_preferences(str(ctx.author.id))
    await ctx.respond("Reset preferences for **{}**.".format(ctx.author.display_name))

language_choices = to_choices(jasima.get_languages_for_slash_commands())

@prefs.command(
    name="language",
    description=text["DESC_PREFS_LANGUAGE"],
    )
async def preferences_language(ctx, lang: discord.Option(str, text["DESC_PREFS_LANGUAGE_OPTION"], choices=language_choices)):
    preferences.set_preference(str(ctx.author.id), "language", lang)
    await ctx.respond("Set language preference for **{}** to **{}**.".format(ctx.author.display_name, lang))


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
@bot.command(name="ss")
async def command_ss(ctx, *, text):
    if text.startswith("text:"):
        text = text.replace("text:", "", 1)
    await ss(ctx, text)
@bot.command(name="preview")
async def command_preview(ctx, *, text):
    if text.startswith("text:"):
        text = text.replace("text:", "", 1)
    await preview(ctx, text)
@bot.command(name="acro")
async def command_acro(ctx, *, text):
    if text.startswith("text:"):
        text = text.replace("text:", "", 1)
    await acro(ctx, text)


async def nimi(ctx, word):
    lang = preferences.get_preference(str(ctx.author.id), "language")

    response = jasima.get_word_entry(word)
    if isinstance(response, str):
        if isinstance(ctx, discord.context.ApplicationContext):
            await ctx.respond(response)
        else:
            await ctx.send(response)
        return
    embed = embed_response(word, lang, response, "concise")
    view = NimiView("expand", word, lang)
    if isinstance(ctx, discord.context.ApplicationContext):
        await ctx.respond(embed=embed, view=view)
    else:
        await ctx.send(embed=embed, view=view)


async def lp(ctx, word):
    response = jasima.get_word_entry(word)
    if isinstance(response, str):
        await ctx.send(response)
        return
    if "luka_pona" in response:
        if "gif" in response["luka_pona"]:
            if isinstance(ctx, discord.context.ApplicationContext):
                await ctx.respond(response["luka_pona"]["gif"])
            else:
                await ctx.send(response["luka_pona"]["gif"])
            return
    if isinstance(ctx, discord.context.ApplicationContext):
        await ctx.respond(f"No luka pona available for **{word}**")
    else:
        await ctx.send(f"No luka pona available for **{word}**")
    

async def sp(ctx, text):
    fontsize = preferences.get_preference(str(ctx.author.id), "fontsize")
    font = preferences.get_preference(str(ctx.author.id), "font")
    if isinstance(ctx, discord.context.ApplicationContext):
        await ctx.respond(file=discord.File(io.BytesIO(sitelenpona.display(text, fonts[font], fontsize)), filename="a.png"))
    else:
        await ctx.send(file=discord.File(io.BytesIO(sitelenpona.display(text, fonts[font], fontsize)), filename="a.png"))


async def ss(ctx, text):
    fontsize = preferences.get_preference(str(ctx.author.id), "fontsize")
    font = "sitelen Latin (ss)"
    if isinstance(ctx, discord.context.ApplicationContext):
        await ctx.respond(file=discord.File(io.BytesIO(sitelenpona.display(text, fonts[font], fontsize)), filename="a.png"))
    else:
        await ctx.send(file=discord.File(io.BytesIO(sitelenpona.display(text, fonts[font], fontsize)), filename="a.png"))


async def preview(ctx, text):
    fontsize = preferences.get_preference(str(ctx.author.id), "fontsize")
    images = []
    for font in fonts:
        images.append(sitelenpona.display(text, fonts[font], fontsize))
    if isinstance(ctx, discord.context.ApplicationContext):
        await ctx.respond(file=discord.File(io.BytesIO(sitelenpona.stitch(images)), filename="a.png"))
    else:
        await ctx.send(file=discord.File(io.BytesIO(sitelenpona.stitch(images)), filename="a.png"))


async def acro(ctx, text):
    book = preferences.get_preference(str(ctx.author.id), "acro")
    if isinstance(ctx, discord.context.ApplicationContext):
        await ctx.respond(acronym.respond(text, book))
    else:
        await ctx.send(acronym.respond(text, book))


"""
@bot.command()
async def reload(ctx):
    jasima.routine()
"""


def embed_response(word, lang, response, embedtype):
    embed = discord.Embed()
    embed.title = response["word"]
    embed.colour = to_colours(colours)[response["book"]]
    description = response["def"][lang] if lang in response["def"] else "(en) {}".format(response["def"]["en"])
    embed.add_field(name="book", value=response["book"])

    if embedtype == "concise":
        embed.add_field(name="description", value=description)

    if embedtype == "verbose":
        embed.add_field(name="description", value=description, inline=False)
        if "etymology" in response or "source_language" in response:
            embed.add_field(name="etymology", value=build_etymology(response), inline=False)
        if "ku_data" in response:
            embed.add_field(name="ku data", value="{} [(source)](http://tokipona.org/nimi_pu.txt)".format(response["ku_data"]), inline=False)
        if "commentary" in response:
            embed.add_field(name="commentary", value=response["commentary"], inline=False)

    if response["book"] not in ("pu", "ku suli"):
        if "see_also" in response:
            embed.add_field(name="see also", value=response["see_also"])
    return embed


class NimiView(discord.ui.View):
    def __init__(self, buttontype, word, lang):
        super().__init__()
        minmax = NimiButton(style=discord.ButtonStyle.primary,
                            label=buttontype,
                            custom_id=f"{buttontype};{word};{lang}")
        self.add_item(minmax)
        url = "https://lipu-linku.github.io/?q={}".format(word)
        moreinfo = discord.ui.Button(style=discord.ButtonStyle.link, label="more info", url=url)
        self.add_item(moreinfo)


class NimiButton(discord.ui.Button):
    async def callback(self, interaction):
        buttontype, word, lang = self.custom_id.split(";")
        if buttontype == "expand":
            embed = embed_response(word, lang, jasima.get_word_entry(word), "verbose")
            view = NimiView("minimise", word, lang)
        if buttontype == "minimise":
            embed = embed_response(word, lang, jasima.get_word_entry(word), "concise")
            view = NimiView("expand", word, lang)
        await interaction.response.edit_message(embed=embed, view=view)


def build_etymology(response):
    etymology = "←"
    if "source_language" in response:
        etymology += " " + response["source_language"]
    if "etymology" in response:
        etymology += " " + response["etymology"]
    return etymology


if __name__ == "__main__":
    bot.run(TOKEN, reconnect=True)
