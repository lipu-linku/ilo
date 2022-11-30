from os.path import exists

from ilo.jasima import bundle

fonts = {
    font["name_short"]: "fonts/" + font["filename"]
    for font in bundle["fonts"].values()
    if "filename" in font
    if exists("fonts/" + font["filename"])
}
