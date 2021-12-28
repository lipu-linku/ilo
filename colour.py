from discord import Colour

def discord_colours(dictionary):
    return {k: Colour.from_rgb(rgb_tuple(v)) for k, v in dictionary.items()}

def rgb_tuple(value):
    return tuple(bytes.fromhex(value))

def is_colour(value):
    try:
        value = rgb_tuple(value)
        if len(value) == 3:
            return True
    except ValueError:
        return False
