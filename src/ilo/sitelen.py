import io
from typing import Literal, Tuple

from PIL import Image, ImageDraw, ImageFont

BLACK = (0x36, 0x39, 0x3F, 0xFF)
WHITE = (0xF0, 0xF0, 0xF0, 0xFF)
TRANSPARENT = (0, 0, 0, 0)
MINIMUM_BRIGHTNESS = 0x40


def luminance(color: Tuple[int, int, int]) -> float:
    # NOTE: normally luminance is 0.0-1.0, we are going 0.0-255.0
    r, g, b = color
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def get_bg_stroke_colors(
    color: Tuple[int, int, int],
    bgstyle: Literal["outline"] | Literal["background"],
):
    bg_color = BLACK
    stroke_color = BLACK

    # if (sum(color) / len(color)) < MINIMUM_BRIGHTNESS:
    # if luminance(color) < MINIMUM_BRIGHTNESS:
    if all(map(lambda c: c < MINIMUM_BRIGHTNESS, color)):
        bg_color = WHITE
        stroke_color = WHITE

    if bgstyle == "outline":
        bg_color = TRANSPARENT

    return bg_color, stroke_color


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

    bg_color, stroke_color = get_bg_stroke_colors(color, bgstyle)
    font = ImageFont.truetype(font_path, font_size)
    d = ImageDraw.Draw(Image.new("RGBA", (0, 0), (0, 0, 0, 0)))
    x, y, w, h = d.multiline_textbbox(
        (0, 0), text, stroke_width=STROKE_WIDTH, font=font
    )
    image = Image.new(
        mode="RGBA",
        size=(x + w + STROKE_WIDTH * 2, y + h + STROKE_WIDTH * 2 + LINE_SPACING),
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
