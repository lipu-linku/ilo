from discord import Colour


def discord_colours(dictionary):
    return {k: Colour.from_rgb(*tuple(bytes.fromhex(v))) for k, v in dictionary.items()}


colours = discord_colours(
    {
        "core": "f4ef7c",
        "common": "d94f3c",
        "uncommon": "972765",
        "obscure": "4d0d6a",
        "sandbox": "07041c",
    }
)
