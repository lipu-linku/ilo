import io
from typing import Literal, Tuple

from PIL import Image, ImageDraw, ImageFont

BLACK = (0x36, 0x39, 0x3F, 0xFF)
WHITE = (0xF0, 0xF0, 0xF0, 0xFF)
TRANSPARENT = (0, 0, 0, 0)

def subpixel_luminance(num: int) -> float:
    srgb = num / 255
    if srgb <= 0.04045:
        return srgb / 12.92
    else:
        return ((srgb + 0.055) / 1.055) ** 2.4 

def relative_luminance(color: Tuple[int, int, int]) -> float:
    r = subpixel_luminance(color[0])
    g = subpixel_luminance(color[1])
    b = subpixel_luminance(color[2])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast_ratio(color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> float:
    luminance1 = relative_luminance(color1)
    luminance2 = relative_luminance(color2)
    minimum = min(luminance1, luminance2)
    maximum = max(luminance1, luminance2)
    return (maximum + 0.05) / (minimum + 0.05)

def passes_aa(color: Tuple[int, int, int], bg_color: Tuple[int, int, int], font_size: int) -> bool:
    minimum_ratio = None
    if font_size < 20:
        minimum_ratio = 4.5
    else:
        minimum_ratio = 3

    return minimum_ratio <= contrast_ratio(color, bg_color)

def midpoint(a: int, b: int) -> int:
    return round((a + b) / 2)

def midpoint_color(color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> Tuple[int, int, int]:
    return (
        midpoint(color1[0], color2[0]),
        midpoint(color1[1], color2[1]),
        midpoint(color1[2], color2[2]),
    )

def get_bg_stroke_colors(
     color: Tuple[int, int, int],
     bgstyle: Literal["outline"] | Literal["background"],
     font_size: int,
):
    if bgstyle == "outline":
        passes_on_dark = passes_aa(color, BLACK, font_size)
        passes_on_light = passes_aa(midpoint_color(color, BLACK), WHITE, font_size)
        if passes_on_dark and passes_on_light:
            return TRANSPARENT, BLACK

    if passes_aa(color, BLACK, font_size):
        return BLACK, TRANSPARENT
    else:
        return WHITE, TRANSPARENT

# by jan Tepo
def display(
    text: str,
    font_path: str,
    font_size: int,
    color: Tuple[int, int, int],
    bgstyle: Literal["outline"] | Literal["background"],
):
    STROKE_WIDTH = round((font_size / 133) * 5)
    LINE_SPACING = round((font_size / 11) * 2)

    bg_color, stroke_color = get_bg_stroke_colors(color, bgstyle, font_size)
    font = ImageFont.truetype(font_path, font_size)
    d = ImageDraw.Draw(Image.new("RGBA", (0, 0), (0, 0, 0, 0)))
    x, y, w, h = d.multiline_textbbox(
        (0, 0), text, stroke_width=STROKE_WIDTH, font=font
    )
    image = Image.new(
        mode="RGBA",
        size=(
            x + w + STROKE_WIDTH * 2,
            y + h + STROKE_WIDTH * 2 + (LINE_SPACING * text.count("\n")),
        ),
        color=bg_color,
    )
    d = ImageDraw.Draw(image)
    d.multiline_text(
        (STROKE_WIDTH, STROKE_WIDTH),
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
