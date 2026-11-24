#!/usr/bin/env python3
"""Draw the news-image-20261123 variant front page (v2, hero-led layout).

A one-page newspaper front page for 23 November 2026: a full-width
illustrated hero of the COP31 walkout in Antalya, a centred lead
headline, then six stories in a three-column grid, a black ticker
strip and a sources footer. All stories are the verified 22-23 Nov
2026 facts from the live entry; only the layout and artwork differ.

Render: python3 draw_poster.py  -> writes entry.png (1024x1024).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (246, 241, 229)
INK = (17, 17, 17)
RED = (163, 22, 33)
NAVY = (31, 58, 95)
GREY = (85, 85, 85)
RULE = (60, 60, 60)
HALL = (143, 168, 160)
HALL_DARK = (110, 138, 130)
FLOOR = (107, 93, 79)
TABLE = (250, 248, 242)
GOLD = (212, 175, 55)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    if not os.path.exists(path):
        path = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
    return ImageFont.truetype(path, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SERIF_I = lambda s: font("DejaVuSerif-Italic.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=fill)


def globe(draw, cx, cy, r, outline=INK, line_w=2):
    """Small wireframe globe glyph."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=outline,
                 width=line_w)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=outline, width=1)
    draw.line([cx - r, cy, cx + r, cy], fill=outline, width=1)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             start=200, end=340, fill=outline, width=1)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             start=20, end=160, fill=outline, width=1)


def hero_walkout(draw, x0, y0, x1, y1):
    """Antalya negotiation hall after the walkout: long empty table,
    a cracked globe, delegates heading for the exit door."""
    draw.rectangle([x0, y0, x1, y1], fill=HALL)
    # back wall panels
    for px in range(x0, x1, 116):
        draw.line([px, y0, px, y1 - 78], fill=HALL_DARK, width=2)
    # floor
    draw.rectangle([x0, y1 - 78, x1, y1], fill=FLOOR)
    # red carpet
    draw.rectangle([x0, y1 - 26, x1, y1], fill=RED)
    # exit door, right side
    dx0, dx1 = x1 - 118, x1 - 28
    draw.rectangle([dx0, y0 + 26, dx1, y1 - 78], fill=(52, 52, 52))
    draw.rectangle([dx0 + 8, y0 + 30, dx1 - 8, y0 + 52], fill=RED)
    centered(draw, (dx0 + dx1) // 2, y0 + 33, "EXIT", SANS_B(13),
             fill=(255, 255, 255))
    # long negotiation table with white cloth (stops short of the door)
    ty0, ty1 = y1 - 138, y1 - 26
    draw.rectangle([x0 + 26, ty0, x1 - 210, ty1], fill=TABLE,
                   outline=(200, 196, 188), width=2)
    draw.line([x0 + 26, ty0 + 16, x1 - 210, ty0 + 16],
              fill=(200, 196, 188), width=1)
    # empty chair backs behind the table, touching its top edge
    for cx in (x0 + 110, x0 + 250, x0 + 390, x0 + 530, x0 + 660):
        draw.rounded_rectangle([cx - 24, ty0 - 40, cx + 24, ty0 + 2],
                               radius=10, fill=(58, 74, 70))
        draw.rectangle([cx - 24, ty0 - 40, cx + 24, ty0 - 24],
                       fill=(74, 92, 88))
    # cracked globe on the table, centre-left
    gx, gy, gr = x0 + 440, ty0 + 52, 30
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr],
                 fill=(178, 205, 225), outline=NAVY, width=3)
    draw.ellipse([gx - gr * 0.45, gy - gr, gx + gr * 0.45, gy + gr],
                 outline=NAVY, width=2)
    draw.line([gx - gr, gy, gx + gr, gy], fill=NAVY, width=2)
    draw.line([gx - 6, gy - gr + 4, gx + 10, gy - 6, gx - 4, gy + 8,
               gx + 12, gy + gr - 6], fill=RED, width=4)
    # name plates and papers left on the table
    for px in (x0 + 70, x0 + 190, x0 + 300, x0 + 590, x0 + 690):
        draw.rectangle([px, ty0 + 30, px + 56, ty0 + 46], fill=(255, 255, 255),
                       outline=(180, 176, 168), width=1)
    # walking delegates: dark silhouettes on the floor, heading for the door
    for dx, s in ((x1 - 190, 1.0), (x1 - 152, 0.92)):
        draw.ellipse([dx - 11 * s, 268, dx + 11 * s,
                      290 * s + 268 * (1 - s)], fill=INK)
        draw.polygon([(dx - 13 * s, 290), (dx + 13 * s, 290),
                      (dx + 9 * s, 368), (dx - 9 * s, 368)],
                     fill=INK)
    # one tipped-over chair on the floor by the table's end
    draw.rounded_rectangle([x1 - 268, 348, x1 - 210, 368],
                           radius=8, fill=(58, 74, 70))
    # caption strip
    draw.rectangle([x0, y1 - 26, x1, y1], fill=(20, 20, 20))
    centered(draw, (x0 + x1) // 2, y1 - 22,
             "EMPTY CHAIRS IN ANTALYA  —  DELEGATES WALK OUT AS TALKS COLLAPSE",
             SANS_B(15), fill=(255, 255, 255))


def story_cell(draw, x, y, w, kicker, headline, deck):
    draw.text((x, y), kicker, font=SANS_B(15), fill=RED)
    y += 21
    hf = SERIF_B(21)
    lines = wrap(draw, headline, hf, w)
    for ln in lines[:2]:
        draw.text((x, y), ln, font=hf, fill=INK)
        y += 26
    y += 3
    df = SERIF(15)
    for ln in wrap(draw, deck, df, w)[:2]:
        draw.text((x, y), ln, font=df, fill=(40, 40, 40))
        y += 19
    return y


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # dateline
    centered(d, W // 2, 26, "MONDAY  ·  23 NOVEMBER 2026  ·  ONE DAY, ONE PAGE",
             SANS_B(19), fill=GREY)
    # masthead (no side glyphs: the 78pt nameplate spans the full width)
    mast = SERIF_B(78)
    centered(d, W // 2, 56, "THE DAILY GLOBE", mast, fill=INK)
    # tagline
    centered(d, W // 2, 148, "The world's news, summed up in a single page",
             SERIF_I(22), fill=GREY)
    # double rule
    d.line([40, 182, W - 40, 182], fill=RULE, width=3)
    d.line([40, 188, W - 40, 188], fill=RULE, width=1)

    # hero illustration
    hero_walkout(d, 40, 200, W - 40, 380)

    # lead kicker + headline + deck (centred)
    centered(d, W // 2, 394, "CLIMATE  ·  ANTALYA, TÜRKIYE", SANS_B(20),
             fill=RED)
    centered(d, W // 2, 422, "COP31 COLLAPSES AS", SERIF_B(58), fill=INK)
    centered(d, W // 2, 484, "EU WALKS OUT", SERIF_B(58), fill=INK)
    deck = ("Nearly 200 nations leave the summit with no deal after the draft "
            "drops every mention of fossil fuels — the longest UN climate "
            "talks ever held.")
    y = 556
    for ln in wrap(d, deck, SERIF(23), 880):
        centered(d, W // 2, y, ln, SERIF(23), fill=(40, 40, 40))
        y += 30

    # rule above the grid
    d.line([40, 624, W - 40, 624], fill=RULE, width=2)

    stories = [
        ("GULF WAR WIDENS",
         "Iran hits US bases in Bahrain",
         "Houthis fire on Saudi Arabia; two hurt in Bahrain as Riyadh "
         "downs missiles."),
        ("BALTIC SEA",
         "Sanctioned Russian freighter burns off Finland",
         "Sparta II, hit by drones, is towed from Finnish waters; all 16 "
         "crew safe."),
        ("UKRAINE",
         "14 missing after drone flattens Kyiv flats",
         "Rescuers dig through rubble after a five-storey block is hit; "
         "nine survive."),
        ("INDONESIA",
         "Factory fire near Jakarta kills at least 3",
         "A candy-plant blaze in Banten traps workers overnight; dozens "
         "missing."),
        ("SOUTH KOREA",
         "Minister quits over AI exam-cheating row",
         "Education chief Choi Kyo-jin resigns two days before the Suneung."),
        ("INDIA · NEPAL",
         "Nepal PM begins first visit to Delhi",
         "Rapper-turned-PM Balendra Shah meets Modi for trade and energy."),
    ]
    col_w = 296
    col_x = [40, 364, 688]
    # vertical dividers
    d.line([352, 640, 352, 916], fill=(180, 176, 168), width=1)
    d.line([676, 640, 676, 916], fill=(180, 176, 168), width=1)
    # horizontal divider between rows
    d.line([40, 774, W - 40, 774], fill=(180, 176, 168), width=1)
    for i, (kick, head, deck_txt) in enumerate(stories):
        row, col = divmod(i, 3)
        story_cell(d, col_x[col], 640 + row * 140, col_w, kick, head, deck_txt)

    # ticker strip
    d.rectangle([40, 930, W - 40, 976], fill=INK)
    d.text((56, 940), "ALSO TODAY", font=SANS_B(16), fill=GOLD)
    ticker = ("WELLINGTON: India post a record 720/9 in the Test against "
              "New Zealand  ·  LONDON: UK and EU agree a post-Brexit reset "
              "deal  ·  DHAKA: Deadly protests over exiled ex-leader")
    tlines = wrap(d, ticker, SANS(15), 1024 - 40 - 56 - 150)
    d.text((206, 941), tlines[0] if tlines else "", font=SANS(15),
           fill=(255, 255, 255))
    if len(tlines) > 1:
        d.text((56, 958), tlines[1], font=SANS(15), fill=(255, 255, 255))

    # footer
    centered(d, W // 2, 986,
             "Sources: AP · Reuters · BBC · NPR · DW · ANI  —  "
             "All stories dated 22–23 November 2026",
             SANS(14), fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
