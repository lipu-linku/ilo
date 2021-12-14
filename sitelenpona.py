from PIL import Image, ImageDraw, ImageFont
import io

# by jan Tepo
def display(text, font_path, font_size):
    STROKE_WIDTH = round(font_size / 133 * 5)
    font = ImageFont.truetype(font_path, font_size)
    d = ImageDraw.Draw(Image.new("RGBA", (0, 0), (0,0,0,0)))
    x, y, w, h = d.multiline_textbbox((0, 0), text, stroke_width=STROKE_WIDTH, font=font)
    image = Image.new("RGBA", (x+w+STROKE_WIDTH*2, y+h+STROKE_WIDTH*2), (0,0,0,0))
    d = ImageDraw.Draw(image)
    d.multiline_text((STROKE_WIDTH, STROKE_WIDTH), text, font=font, fill=(0xff,0xff,0xff), stroke_width=STROKE_WIDTH, stroke_fill=(0x36,0x39,0x3f))
    img_out = io.BytesIO()
    image.save(img_out, format='PNG')
    return img_out.getvalue()

def stitch(images):
    imgs = [Image.open(io.BytesIO(i)) for i in images]
    min_img_height = min(i.height for i in imgs)

    total_width = 0
    for i, img in enumerate(imgs):
        if img.height > min_img_height:
            imgs[i] = img.resize((int(img.width / img.height * min_img_height), min_img_height), Image.ANTIALIAS)
        total_width += imgs[i].width
    img_merge = Image.new(imgs[0].mode, (total_width, min_img_height), (0,0,0,0))
    x = 0
    for img in imgs:
        img_merge.paste(img, (x, 0))
        x += img.width
    img_out = io.BytesIO()
    img_merge.save(img_out, format='PNG')
    return img_out.getvalue()
