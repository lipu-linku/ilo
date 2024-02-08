from os.path import exists

from ilo.jasima import bundle

FONTDIR = "ijo/nasinsitelen/"
# from repo root

fonts = {
    font["name_short"]: FONTDIR + font["filename"]
    for font in bundle["fonts"].values()
    if "filename" in font
    if exists(FONTDIR + font["filename"])
}
