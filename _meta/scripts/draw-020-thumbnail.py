"""Post 20 thumbnail: faded approval stamps in a dim room, one three-sentence sheet leaving through a lit door.

Usage: python draw-020-thumbnail.py docs/assets/images/agent-sdd/020-first-public-preview/thumbnail.png (needs Pillow, Windows Malgun Gothic)."""
import math
import random
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = sys.argv[1]
W, H = 2400, 1260
BOLD = "C:/Windows/Fonts/malgunbd.ttf"
REG = "C:/Windows/Fonts/malgun.ttf"
random.seed(20)


def font(path, size):
    return ImageFont.truetype(path, size)


# room: dark on the left, a little lighter toward the door
img = Image.new("RGB", (W, H))
px = ImageDraw.Draw(img)
for x in range(W):
    t = x / W
    px.line([(x, 0), (x, H)], fill=(int(22 + 20 * t), int(28 + 22 * t), int(42 + 26 * t)))
canvas = img.convert("RGBA")

# floor line
floor_y = 1010
ImageDraw.Draw(canvas).rectangle((0, floor_y, W, H), fill=(18, 23, 34, 255))

# door opening with warm light
door = (1640, 250, 2120, floor_y)
light = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ld = ImageDraw.Draw(light)
ld.polygon([(door[0], floor_y), (door[2], floor_y), (door[2] + 260, H), (door[0] - 520, H)], fill=(255, 214, 120, 70))
ld.polygon([(door[0], door[1]), (door[0], floor_y), (door[0] - 380, floor_y + 40), (door[0] - 380, door[1] + 120)], fill=(255, 214, 120, 26))
light = light.filter(ImageFilter.GaussianBlur(40))
canvas = Image.alpha_composite(canvas, light)
d = ImageDraw.Draw(canvas)
for i in range(door[3] - door[1]):
    t = i / (door[3] - door[1])
    d.line([(door[0], door[1] + i), (door[2], door[1] + i)], fill=(255, int(246 - 40 * t), int(214 - 90 * t), 255))
d.rectangle((door[0] - 22, door[1] - 22, door[2] + 22, door[1]), fill=(58, 66, 86, 255))
d.rectangle((door[0] - 22, door[1], door[0], door[3]), fill=(58, 66, 86, 255))
d.rectangle((door[2], door[1], door[2] + 22, door[3]), fill=(58, 66, 86, 255))
# the open door leaf, swung outward into the light
d.polygon([(door[2], door[1]), (door[2] + 150, door[1] + 70), (door[2] + 150, door[3] - 30), (door[2], door[3])], fill=(44, 52, 70, 255))


# faded approval stamps on the left wall
def stamp(size, alpha, angle):
    s = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(s)
    red = (214, 69, 65, alpha)
    sd.ellipse((8, 8, size - 8, size - 8), outline=red, width=max(6, size // 22))
    sd.ellipse((size * 0.16, size * 0.16, size * 0.84, size * 0.84), outline=red, width=max(3, size // 50))
    f = font(BOLD, int(size * 0.3))
    tw = sd.textlength("승인", font=f)
    sd.text(((size - tw) / 2, size * 0.32), "승인", font=f, fill=red)
    return s.rotate(angle, resample=Image.BICUBIC, expand=True)


spots = [(120, 120), (360, 80), (600, 150), (840, 90), (1080, 170),
         (200, 360), (450, 330), (700, 400), (950, 350),
         (100, 600), (350, 590), (620, 650), (880, 610),
         (230, 800), (500, 820), (780, 830)]
for i, (x, y) in enumerate(spots):
    size = random.randint(170, 230)
    # newer stamps are fainter: approvals pressed out of habit
    alpha = max(26, 170 - i * 8 + random.randint(-12, 12))
    s = stamp(size, alpha, random.uniform(-24, 24))
    canvas.alpha_composite(s, (x, y))

# a key left on the floor, out of reach in the cloud
key = Image.new("RGBA", (360, 140), (0, 0, 0, 0))
kd = ImageDraw.Draw(key)
kc = (150, 160, 182, 200)
kd.ellipse((10, 20, 110, 120), outline=kc, width=14)
kd.rectangle((105, 62, 320, 80), fill=kc)
kd.rectangle((250, 80, 268, 112), fill=kc)
kd.rectangle((292, 80, 310, 104), fill=kc)
canvas.alpha_composite(key.rotate(-8, expand=True), (1040, 870))

# the sheet leaving through the door
sheet_w, sheet_h = 620, 470
sheet = Image.new("RGBA", (sheet_w + 80, sheet_h + 220), (0, 0, 0, 0))
sh = ImageDraw.Draw(sheet)
sh.rounded_rectangle((40, 40, 40 + sheet_w, 40 + sheet_h), 26, fill=(255, 255, 255, 255))
title_f = font(BOLD, 40)
line_f = font(BOLD, 40)
sub_f = font(REG, 30)
sh.text((86, 78), "사람 판단", font=title_f, fill=(43, 53, 80))
sh.line((86, 140, 40 + sheet_w - 46, 140), fill=(220, 225, 234), width=4)
rows = [("1", "멈추고 묻는다"), ("2", "판단 지점은 프로젝트가"), ("3", "결정을 만들지 않는다")]
for i, (n, text) in enumerate(rows):
    y = 172 + i * 100
    sh.ellipse((86, y, 142, y + 56), fill=(47, 158, 91))
    nw = sh.textlength(n, font=line_f)
    sh.text((114 - nw / 2, y + 2), n, font=line_f, fill=(255, 255, 255))
    sh.text((166, y + 2), text, font=line_f, fill=(43, 53, 80))
# hanging tag
tx, ty = 40 + sheet_w - 120, 40 + sheet_h
sh.line((tx, ty, tx + 10, ty + 70), fill=(200, 170, 90), width=5)
sh.rounded_rectangle((tx - 210, ty + 70, tx + 140, ty + 150), 18, fill=(255, 214, 120))
tag_f = font(BOLD, 34)
tw = sh.textlength("v1.0.0-preview.1", font=tag_f)
sh.text((tx - 35 - tw / 2, ty + 88), "v1.0.0-preview.1", font=tag_f, fill=(70, 52, 10))
sheet = sheet.rotate(6, resample=Image.BICUBIC, expand=True)
shadow = Image.new("RGBA", sheet.size, (0, 0, 0, 0))
shadow.paste((0, 0, 0, 110), mask=sheet.split()[3])
shadow = shadow.filter(ImageFilter.GaussianBlur(30))
canvas.alpha_composite(shadow, (1360, 360))
canvas.alpha_composite(sheet, (1330, 320))

# title
d = ImageDraw.Draw(canvas)
title = font(BOLD, 112)
d.text((120, 1000), "방법론을 처음 ", font=title, fill=(240, 243, 248))
w1 = d.textlength("방법론을 처음 ", font=title)
d.text((120 + w1, 1000), "밖에", font=title, fill=(255, 205, 100))
w2 = d.textlength("밖에", font=title)
d.text((120 + w1 + w2, 1000), " 내놓았다", font=title, fill=(240, 243, 248))
d.text((126, 1150), "승인 도장 대신, 세 문장만 들고", font=font(REG, 44), fill=(168, 178, 198))

out = canvas.convert("RGB").quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
out.save(OUT, "PNG", optimize=True)
print("saved", OUT)
