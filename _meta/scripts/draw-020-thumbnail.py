"""Post 20 thumbnail: approval request cards pile up while their check marks fade.

Usage: python draw-020-thumbnail.py <out.png>  (needs Pillow and Windows Malgun Gothic)
"""
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = sys.argv[1]
W, H = 2400, 1260
BOLD = "C:/Windows/Fonts/malgunbd.ttf"
REG = "C:/Windows/Fonts/malgun.ttf"
INK = (31, 42, 68)
SUB = (110, 118, 135)
BLUE = (47, 111, 219)
GREEN = (34, 139, 84)
PAPER = (250, 247, 241)


def font(path, size):
    return ImageFont.truetype(path, size)


canvas = Image.new("RGBA", (W, H), PAPER + (255,))
d = ImageDraw.Draw(canvas)


def drop_shadow(box, radius, strength=26, blur=22, offset=12):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle(
        (box[0], box[1] + offset, box[2], box[3] + offset), radius, fill=(40, 50, 80, strength))
    return layer.filter(ImageFilter.GaussianBlur(blur))


# title
t1 = font(BOLD, 128)
d.text((130, 150), "승인을 늘릴수록", font=t1, fill=INK)
w_a = d.textlength("승인은 ", font=t1)
d.text((130, 310), "승인은 ", font=t1, fill=INK)
d.text((130 + w_a, 310), "가벼워졌다", font=t1, fill=BLUE)
d.text((136, 498), "Agent SDD 개발 일지 · 20편", font=font(REG, 44), fill=SUB)

# the stack of approval requests: higher cards, fainter checks
card_w, card_h = 640, 116
base_x, base_y = 1540, 1060
n = 8
for i in range(n):
    x = base_x + (i % 2) * 26 - i * 6
    y = base_y - (i + 1) * (card_h - 14)
    box = (x, y, x + card_w, y + card_h)
    canvas = Image.alpha_composite(canvas, drop_shadow(box, 18, strength=18, blur=14, offset=8))
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle(box, 18, fill=(255, 255, 255, 255), outline=(222, 226, 234, 255), width=3)
    d.text((x + 40, y + 30), "승인 요청", font=font(BOLD, 46), fill=(60, 70, 96))
    d.text((x + 270, y + 40), f"#{101 + i}", font=font(REG, 36), fill=(160, 166, 180))
    # check box with a mark that fades as the pile grows
    cb = (x + card_w - 120, y + 26, x + card_w - 56, y + 90)
    d.rounded_rectangle(cb, 10, outline=(196, 202, 214, 255), width=4)
    alpha = max(0, 255 - i * 38)
    if alpha:
        mark = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        md = ImageDraw.Draw(mark)
        md.line([(cb[0] + 12, cb[1] + 34), (cb[0] + 28, cb[1] + 50), (cb[0] + 54, cb[1] + 12)],
                fill=GREEN + (alpha,), width=11, joint="curve")
        canvas = Image.alpha_composite(canvas, mark)
        d = ImageDraw.Draw(canvas)

# side note above the faded top of the pile
note_f = font(REG, 42)
d.text((1540, 118), "쌓일수록 확인은 흐려졌다", font=note_f, fill=SUB)
d.line([(2060, 182), (2060, 218)], fill=(170, 176, 190), width=4)
d.polygon([(2048, 214), (2060, 236), (2072, 214)], fill=(170, 176, 190))

# what replaced it
box = (130, 700, 1180, 1010)
canvas = Image.alpha_composite(canvas, drop_shadow(box, 30))
d = ImageDraw.Draw(canvas)
d.rounded_rectangle(box, 30, fill=(232, 245, 237, 255), outline=(150, 205, 172, 255), width=4)
d.text((180, 742), "이제 사람에게 묻는 때", font=font(BOLD, 44), fill=GREEN)
d.text((180, 820), "구조가 바뀌거나", font=font(BOLD, 64), fill=INK)
d.text((180, 905), "문제가 생겼을 때만", font=font(BOLD, 64), fill=INK)

out = canvas.convert("RGB").quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
out.save(OUT, "PNG", optimize=True)
print("saved", OUT)
