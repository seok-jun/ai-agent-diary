"""Post 21 thumbnail: a thin box shipped at 02:23, a full box shipped at 04:26.

Usage: python draw-021-thumbnail.py <out.png>  (needs Pillow and Windows Malgun Gothic)
"""
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = sys.argv[1]
W, H = 2400, 1260
BOLD = "C:/Windows/Fonts/malgunbd.ttf"
REG = "C:/Windows/Fonts/malgun.ttf"
INK = (31, 42, 68)
SUB = (96, 104, 124)
BLUE = (47, 111, 219)
KRAFT = (214, 172, 120)
KRAFT_DARK = (186, 142, 92)


def font(path, size):
    return ImageFont.truetype(path, size)


# pale night on the left, early light on the right
canvas = Image.new("RGBA", (W, H))
g = ImageDraw.Draw(canvas)
left, right = (228, 233, 250), (255, 237, 220)
for x in range(W):
    t = x / (W - 1)
    g.line([(x, 0), (x, H)], fill=tuple(int(left[i] + (right[i] - left[i]) * t) for i in range(3)) + (255,))
d = ImageDraw.Draw(canvas)


def shadow(box, radius, strength=30, blur=20, offset=12):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle(
        (box[0], box[1] + offset, box[2], box[3] + offset), radius, fill=(40, 50, 80, strength))
    return layer.filter(ImageFilter.GaussianBlur(blur))


def paste(card, xy, angle):
    global canvas, d
    rotated = card.rotate(angle, resample=Image.BICUBIC, expand=True)
    canvas.alpha_composite(rotated, xy)
    d = ImageDraw.Draw(canvas)


def sheet(w, h):
    s = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(s)
    sd.rounded_rectangle((0, 0, w - 1, h - 1), 14, fill=(255, 255, 255, 255), outline=(214, 220, 232, 255), width=3)
    for i in range(4):
        y = 40 + i * 34
        sd.line((28, y, w - 28 - (i % 2) * 40, y), fill=(200, 207, 222, 255), width=8)
    return s


def label_card(w, h, color, text, size):
    c = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cd = ImageDraw.Draw(c)
    cd.rounded_rectangle((0, 0, w - 1, h - 1), 18, fill=color + (255,))
    f = font(BOLD, size)
    tw = cd.textlength(text, font=f)
    cd.text(((w - tw) / 2, 22), text, font=f, fill=(255, 255, 255, 255))
    return c


def box(x0, y0, x1, y1):
    global canvas, d
    canvas = Image.alpha_composite(canvas, shadow((x0, y0, x1, y1), 16))
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle((x0, y0, x1, y1), 16, fill=KRAFT + (255,))
    d.rectangle((x0, y0, x1, y0 + 26), fill=KRAFT_DARK + (255,))
    # tape strip
    cx = (x0 + x1) // 2
    d.rectangle((cx - 40, y0, cx + 40, y0 + 70), fill=(236, 214, 172, 255))


def tag(x, y, text):
    d.line((x, y - 40, x + 30, y), fill=(120, 110, 90), width=5)
    f = font(BOLD, 50)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle((x - 20, y, x + tw + 50, y + 84), 20, fill=(34, 139, 84))
    d.ellipse((x - 2, y + 30, x + 22, y + 54), fill=(255, 255, 255))
    d.text((x + 36, y + 10), text, font=f, fill=(255, 255, 255))


# title
t1 = font(BOLD, 116)
d.text((130, 110), "방법론을 처음 내놓고,", font=t1, fill=INK)
d.text((130, 262), "두 시간 만에", font=t1, fill=BLUE)
w_a = d.textlength("두 시간 만에 ", font=t1)
d.text((130 + w_a, 262), "다시 냈다", font=t1, fill=INK)
d.text((136, 440), "Agent SDD 개발 일지 · 21편", font=font(REG, 44), fill=SUB)

# preview.1: a thin box with three sheets
for i, (dx, ang) in enumerate([(-70, 6), (0, -2), (70, -8)]):
    paste(sheet(200, 230), (470 + dx, 640 - i * 6), ang)
box(380, 780, 760, 1000)
tag(410, 890, "preview.1")

# preview.2: a wider box with four labelled cards standing side by side
cards = [
    ((60, 110, 200), "실행 절차", 480),
    ((128, 82, 200), "Skill 4개", 530),
    ((214, 120, 40), "eval 30개", 505),
    ((34, 139, 84), "설치 도구", 550),
]
x = 1282
for color, text, top in cards:
    paste(label_card(206, 340, color, text, 42), (x, top), 0)
    x += 206 + 14
box(1260, 760, 2160, 1000)
tag(1290, 870, "preview.2")

# timeline
ty = 1110
d.line((200, ty, 2200, ty), fill=(150, 158, 178), width=6)
for cx, label in [(570, "02:23"), (1710, "04:26")]:
    d.ellipse((cx - 18, ty - 18, cx + 18, ty + 18), fill=INK)
    f = font(BOLD, 56)
    tw = d.textlength(label, font=f)
    d.text((cx - tw / 2, ty + 30), label, font=f, fill=INK)
# the two-hour span
d.line((640, ty - 50, 1640, ty - 50), fill=BLUE, width=6)
d.polygon([(1640, ty - 66), (1672, ty - 50), (1640, ty - 34)], fill=BLUE)
span = font(BOLD, 48)
tw = d.textlength("두 시간", font=span)
d.rounded_rectangle((1140 - tw / 2 - 30, ty - 86, 1140 + tw / 2 + 30, ty - 14), 30, fill=(255, 255, 255))
d.text((1140 - tw / 2, ty - 84), "두 시간", font=span, fill=BLUE)

out = canvas.convert("RGB").quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
out.save(OUT, "PNG", optimize=True)
print("saved", OUT)
