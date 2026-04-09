import io
import logging
import re

from PIL import Image, ImageDraw, ImageFont

from ilo.cog_utils import BgStyle, Color, ColorAlpha
from ilo.ucsur import chars

LOG = logging.getLogger("ilo")

BLACK: ColorAlpha = (0x36, 0x39, 0x3F, 0xFF)
WHITE: ColorAlpha = (0xF0, 0xF0, 0xF0, 0xFF)
TRANSPARENT: ColorAlpha = (0, 0, 0, 0)

def subpixel_luminance(num: int) -> float:
    srgb = num / 255
    if srgb <= 0.04045:
        return srgb / 12.92
    return ((srgb + 0.055) / 1.055) ** 2.4


def relative_luminance(color: Color) -> float:
    r = subpixel_luminance(color[0])
    g = subpixel_luminance(color[1])
    b = subpixel_luminance(color[2])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(color1: Color, color2: Color) -> float:
    luminance1 = relative_luminance(color1)
    luminance2 = relative_luminance(color2)
    minimum = min(luminance1, luminance2)
    maximum = max(luminance1, luminance2)
    return (maximum + 0.05) / (minimum + 0.05)


def passes_aa(color: Color, bg_color: Color, font_size: int) -> bool:
    # https://www.w3.org/WAI/WCAG2AA-Conformance
    minimum_ratio = None
    if font_size < 20:
        minimum_ratio = 4.5
    else:
        minimum_ratio = 3

    return minimum_ratio <= contrast_ratio(color, bg_color)


# def midpoint(a: int, b: int) -> int:
#     return round((a + b) / 2)


# def midpoint_color(color1: Color, color2: Color) -> Color:
#     return (
#         midpoint(color1[0], color2[0]),
#         midpoint(color1[1], color2[1]),
#         midpoint(color1[2], color2[2]),
#     )


# def get_bg_stroke_colors(
#     color: Color, bgstyle: BgStyle, font_size: int
# ) -> tuple[ColorAlpha, ColorAlpha]:
#     if bgstyle == "outline":
#         passes_on_dark = passes_aa(color, BLACK, font_size)
#         passes_on_light = passes_aa(midpoint_color(color, BLACK), WHITE, font_size)
#         if passes_on_dark and passes_on_light:
#             return TRANSPARENT, BLACK

#     if passes_aa(color, BLACK, font_size):
#         return BLACK, BLACK
#     return WHITE, WHITE

def wrap_text(text:str, font: ImageFont.FreeTypeFont, line_width: int):
    lines = text.splitlines()
    wrapped_text = ""
    for line in lines:
        if font.getlength(line) < line_width:
            wrapped_text += line+"\n"
            continue
        
        split_line = re.sub(rf"({"|".join(chars)})", r"\g<0> ", line) # insert space after every uscur character
        split_line = split_line.split(" ")
        current_line_segment = ""
        for word in split_line: 
            newline = current_line_segment + word
            if font.getlength(newline) < line_width:
                current_line_segment += word
            else:
                wrapped_text += current_line_segment + "\n"
                current_line_segment = word
        wrapped_text += current_line_segment + "\n"
    return(wrapped_text)

# by jan Tepo
def display(text: str, font_path: str, font_size: int, color: Color, bgstyle: BgStyle, linewrap:bool, linewidth:int):
    STROKE_WIDTH = round((font_size / 133) * 5)
    LINE_SPACING = round((font_size / 2.5))
    PAD = round(font_size / 25)

    stroke_color = BLACK if passes_aa(color, BLACK, font_size) else WHITE
    bg_color = stroke_color if bgstyle == "background" else TRANSPARENT

    font = ImageFont.truetype(font_path, font_size)

    if linewrap:
        text = wrap_text(text, font, linewidth)

    d = ImageDraw.Draw(Image.new("RGBA", (0, 0), (0, 0, 0, 0)))
    x, y, w, h = d.multiline_textbbox(
        (0, 0),
        text=text,
        font=font,
        spacing=LINE_SPACING,
        stroke_width=STROKE_WIDTH,
        font_size=font_size,
    )
    
    if linewrap:
        w = max(w, linewidth) # mobile sometimes expands images to the screen's width, so this helps keep the characters displayi   ng at a constant size

    image = Image.new(
        mode="RGBA",
        size=(w + PAD, h + PAD + 25),
        # NOTE: +20px is a buffer for alt text button on desktop
        color=bg_color,
    )
    d = ImageDraw.Draw(image)
    d.multiline_text(
        (PAD // 2, PAD // 2),
        text,
        font=font,
        fill=color,
        spacing=LINE_SPACING,
        stroke_width=STROKE_WIDTH,
        stroke_fill=stroke_color,
    )
    img_out = io.BytesIO()
    image.save(img_out, format="PNG")
    return img_out.getvalue()
