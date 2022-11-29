import io

from PIL import Image, ImageDraw, ImageFont


# by jan Tepo
def display(text, font_path, font_size, color):
    STROKE_WIDTH = round(font_size / 133 * 5)
    font = ImageFont.truetype(font_path, font_size)
    d = ImageDraw.Draw(Image.new("RGBA", (0, 0), (0, 0, 0, 0)))
    x, y, w, h = d.multiline_textbbox(
        (0, 0), text, stroke_width=STROKE_WIDTH, font=font
    )
    image = Image.new(
        "RGBA", (x + w + STROKE_WIDTH * 2, y + h + STROKE_WIDTH * 2), (0, 0, 0, 0)
    )
    d = ImageDraw.Draw(image)
    d.multiline_text(
        (STROKE_WIDTH, STROKE_WIDTH),
        text,
        font=font,
        fill=color,
        stroke_width=STROKE_WIDTH,
        stroke_fill=(0x36, 0x39, 0x3F),
    )
    img_out = io.BytesIO()
    image.save(img_out, format="PNG")
    return img_out.getvalue()


def stitch(images):
    imgs = [Image.open(io.BytesIO(i)) for i in images]
    max_img_width = max(i.width for i in imgs)

    total_height = 0
    for i, img in enumerate(imgs):
        # If the image is larger than the minimum width, resize it
        # if img.width > min_img_width:
        #    imgs[i] = img.resize((min_img_width, int(img.height / img.width * min_img_width)), Image.ANTIALIAS)
        total_height += imgs[i].height

    # I have picked the mode of the first image to be generic. You may have other ideas
    # Now that we know the total height of all of the resized images, we know the height of our final image
    img_merge = Image.new(imgs[0].mode, (max_img_width, total_height))
    y = 0
    for img in imgs:
        img_merge.paste(img, (round((max_img_width - img.width) / 2), y))

        y += img.height
    img_out = io.BytesIO()
    img_merge.save(img_out, format="PNG")
    return img_out.getvalue()
