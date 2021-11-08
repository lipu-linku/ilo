import wand.image
from wand.color import Color
from xml.sax.saxutils import escape
template = """pango:<span size="{}" color="#{}" font_family="{}" font_features="liga">{}</span>"""
def display(text, resolution=133):
    NUM_LINES = len(text.split("\n"))
    WIDTH = resolution*12
    HEIGHT = round(resolution*1.5*(NUM_LINES+1))
    DISK_SIZE = round(resolution*0.042)
    FONT_SIZE = resolution*770
    text = escape(escape(text)) # yes you have to escape twice. blame pango
    with wand.image.Image() as image_text:
        with wand.image.Image() as image_shadow:
            with wand.image.Image(width=WIDTH, height=HEIGHT, background=Color("#36393f")) as image_colour:
                image_text.background_color = Color("transparent")
                image_text.options["pango:align"] = "center"
                image_text.pseudo(width=WIDTH, height=HEIGHT, pseudo=template.format(FONT_SIZE, "ffffff", "linja sike", text))
                image_shadow.background_color = Color("transparent")
                image_shadow.options["pango:align"] = "center"
                image_shadow.pseudo(width=WIDTH, height=HEIGHT, pseudo=template.format(FONT_SIZE, "ffffff", "linja-sike-radius-60", text))
                image_shadow.composite_channel(channel="rgb_channels", image=image_colour, operator="multiply")
                image_shadow.composite_channel(channel="all_channels", image=image_text, operator="over")
                image_shadow.trim()
                return image_shadow.make_blob("png32")
