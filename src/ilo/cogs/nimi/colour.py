from discord import Colour


def discord_colours(dictionary):
    return {k: Colour.from_rgb(*tuple(bytes.fromhex(v))) for k, v in dictionary.items()}


colours = discord_colours({
  "core": "f4ef7c",
  "widespread": "fa990a",
  "common": "d94f3c",
  "uncommon": "972765",
  "rare": "4d0d6a",
  "obscure": "07041c"
})
