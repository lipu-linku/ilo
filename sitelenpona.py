from PIL import Image, ImageDraw, ImageFont
import io

# by jan Tepo
def display(text, font_size):
    STROKE_WIDTH = round(font_size / 133 * 5)
    font = ImageFont.truetype('fonts/linja-sike-5.otf', font_size)
    d = ImageDraw.Draw(Image.new("RGBA", (0, 0), (0,0,0,0)))
    x, y, w, h = d.multiline_textbbox((0, 0), text, stroke_width=STROKE_WIDTH, font=font)
    image = Image.new("RGBA", (x+w+STROKE_WIDTH*2, y+h+STROKE_WIDTH*2), (0,0,0,0))
    d = ImageDraw.Draw(image)
    d.multiline_text((STROKE_WIDTH, STROKE_WIDTH), text, font=font, fill=(0xff,0xff,0xff), stroke_width=STROKE_WIDTH, stroke_fill=(0x36,0x39,0x3f))
    img_out = io.BytesIO()
    image.save(img_out, format='PNG')
    return img_out.getvalue()
