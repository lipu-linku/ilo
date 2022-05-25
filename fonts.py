from os.path import exists
from jasima import bundle

fonts = {font["name_short"]: "fonts/" + font["filename"]
         for font in bundle["fonts"].values()
         if exists("fonts/" + font["filename"])}
