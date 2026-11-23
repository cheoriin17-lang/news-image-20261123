#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news front page (1024x1024 PNG).

Fresh build for make.fun news-image-20261123. Everything is drawn with
Pillow primitives; no network, no randomness, no external assets.
Run:  python3 draw_poster.py   ->  writes entry.png next to this file.
"""
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 38
PAPER = (248, 243, 232)
INK = (18, 18, 18)
RED = (158, 27, 27)
BLUE = (31, 58, 95)
GREY = (92, 88, 80)
RULE = (18, 18, 18)
HAIR = (178, 172, 158)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning lines that fit `width` pixels."""
    lines = []
    for chunk in text.split("\n"):
        words, cur = chunk.split(), ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, width, max_lines):
    """Wrap text; shrink the font until it fits in max_lines at width."""
    size = fnt.size
    while size > 10:
        f = font(fnt.path.split("/")[-1], size) if hasattr(fnt, "path") else fnt
        ls = wrap(draw, text, f, width)
        if len(ls) <= max_lines:
            return f, ls
        size -= 1
    return f, ls


def hline(draw, x0, x1, y, width=1, color=RULE):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def draw_globe(draw, cx, cy, r, color=INK):
    """Simple line globe: circle, meridians, equator."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=color, width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=color, width=2)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 200, 340, fill=color, width=2)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 20, 160, fill=color, width=2)


def masthead(draw):
    top = 30
    f_small = font(SANS_B, 15)
    dateline = "MONDAY  \u00b7  23 NOVEMBER 2026  \u00b7  ONE DAY, ONE PAGE"
    tw = draw.textlength(dateline, font=f_small)
    draw.text(((W - tw) / 2, top), dateline, font=f_small, fill=GREY)

    title_f = font(SERIF_B, 72)
    title = "THE DAILY GLOBE"
    tw = draw.textlength(title, font=title_f)
    draw_globe(draw, MARGIN + 34, top + 78, 30)
    draw.text(((W - tw) / 2, top + 34), title, font=title_f, fill=INK)
    draw_globe(draw, W - MARGIN - 34, top + 78, 30)

    tag_f = font(SERIF, 19)
    tag = "The world\u2019s news, summed up in a single page"
    tw = draw.textlength(tag, font=tag_f)
    draw.text(((W - tw) / 2, top + 118), tag, font=tag_f, fill=GREY)

    y = top + 152
    hline(draw, MARGIN, W - MARGIN, y, width=4)
    hline(draw, MARGIN, W - MARGIN, y + 8, width=1)
    return y + 16


def lead(draw, y):
    """Lead story: COP31 collapse, with a cracked-globe motif on the right."""
    x0, x1 = MARGIN, W - MARGIN
    text_w = 640
    f_kick = font(SANS_B, 17)
    draw.text((x0, y), "CLIMATE  \u00b7  ANTALYA, T\u00dcRKIYE", font=f_kick, fill=RED)
    y += 30

    f_head = font(SERIF_B, 54)
    head = "COP31 COLLAPSES AS\nEU WALKS OUT"
    for line in head.split("\n"):
        draw.text((x0, y), line, font=f_head, fill=INK)
        y += 62
    y += 6

    f_deck = font(SANS, 21)
    deck = ("Nearly 200 nations leave the climate summit with no deal "
            "after the draft drops every mention of fossil fuels \u2014 "
            "the longest UN climate talks ever held.")
    for line in wrap(draw, deck, f_deck, text_w):
        draw.text((x0, y), line, font=f_deck, fill=INK)
        y += 28

    # Cracked globe motif, right of the lead text.
    cx, cy, r = 830, 300, 72
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=4)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=BLUE, width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=BLUE, width=2)
    crack = [(cx - 18, cy - r + 8), (cx + 6, cy - 34), (cx - 12, cy + 2),
             (cx + 14, cy + 30), (cx - 4, cy + r - 10)]
    draw.line(crack, fill=RED, width=4, joint="curve")
    f_cap = font(SANS_B, 13)
    cap = "NO DEAL IN ANTALYA"
    tw = draw.textlength(cap, font=f_cap)
    draw.text((cx - tw / 2, cy + r + 12), cap, font=f_cap, fill=RED)
    return 444


def card(draw, x, y, w, kicker, headline, body):
    f_kick = font(SANS_B, 15)
    draw.text((x, y), kicker, font=f_kick, fill=RED)
    y += 24
    f_head, lines = fit_lines(draw, headline, font(SERIF_B, 25), w, 2)
    for line in lines:
        draw.text((x, y), line, font=f_head, fill=INK)
        y += 30
    y += 2
    f_body = font(SANS, 16)
    for line in wrap(draw, body, f_body, w)[:3]:
        draw.text((x, y), line, font=f_body, fill=(52, 50, 46))
        y += 21
    return y


def grid(draw, y0):
    x0, x1 = MARGIN, W - MARGIN
    col_w = (x1 - x0 - 28) // 2
    mid = x0 + col_w + 14
    stories = [
        ("GULF WAR WIDENS",
         "Iran hits US bases in Bahrain; Houthis fire on Saudi Arabia",
         "Two hurt in Bahrain; Riyadh downs Houthi missiles \u2014 yet "
         "Tehran says a deal is still possible."),
        ("BALTIC SEA",
         "Sanctioned Russian freighter burns off Finland",
         "Sparta II, hit by drones en route to Kaliningrad, is towed from "
         "Finnish waters; all 16 crew evacuated safely."),
        ("UKRAINE",
         "14 missing after drone flattens Kyiv flats",
         "Rescuers dig through rubble near Kyiv after a five-storey block "
         "is hit; nine people are pulled out alive."),
        ("INDONESIA",
         "Factory fire near Jakarta kills at least 3",
         "A candy-plant blaze in Banten traps workers overnight; dozens "
         "still missing as families wait outside the gates."),
        ("SOUTH KOREA",
         "Minister quits over AI exam-cheating row",
         "Education chief Choi Kyo-jin resigns two days before the Suneung "
         "after anti-cheating measures spark chaos."),
        ("INDIA \u00b7 NEPAL",
         "Nepal PM begins first visit to Delhi",
         "Rapper-turned-PM Balendra Shah meets Modi on Monday for talks "
         "on trade, energy and flood recovery."),
    ]
    row_h = 154
    for i, (kick, head, body) in enumerate(stories):
        row, col = divmod(i, 2)
        cx = x0 if col == 0 else mid
        cy = y0 + row * row_h
        if row > 0:
            hline(draw, x0, x1, cy - 12, width=1, color=HAIR)
        card(draw, cx, cy, col_w, kick, head, body)
    hline(draw, x0, x1, y0 + 3 * row_h - 12, width=1, color=HAIR)
    draw.line([(mid - 14, y0), (mid - 14, y0 + 3 * row_h - 24)],
              fill=HAIR, width=1)
    return y0 + 3 * row_h


def ticker(draw, y):
    x0, x1 = MARGIN, W - MARGIN
    h = 64
    draw.rectangle([x0, y, x1, y + h], fill=INK)
    f_lab = font(SANS_B, 15)
    label = "ALSO TODAY  \u00b7  "
    draw.text((x0 + 14, y + 22), label, font=f_lab, fill=(232, 196, 90))
    lx = x0 + 14 + draw.textlength(label, font=f_lab)
    f_t = font(SANS, 16)
    items = ("WELLINGTON: India post a record 720/9 in the Test against "
             "New Zealand   \u2022   LONDON: UK and EU agree a post-Brexit "
             "reset deal   \u2022   DHAKA: Deadly protests over exiled ex-leader")
    lines = wrap(draw, items, f_t, x1 - lx - 14)
    ty = y + 12 if len(lines) > 1 else y + 22
    for line in lines[:2]:
        draw.text((lx, ty), line, font=f_t, fill=(248, 243, 232))
        ty += 21
    return y + h + 14


def footer(draw, y):
    f_f = font(SANS, 13)
    note = ("Sources: AP \u00b7 Reuters \u00b7 BBC \u00b7 NPR \u00b7 DW \u00b7 ANI  \u2014  "
            "All stories dated 22\u201323 November 2026")
    tw = draw.textlength(note, font=f_f)
    draw.text(((W - tw) / 2, y), note, font=f_f, fill=GREY)
    hline(draw, MARGIN, W - MARGIN, y - 8, width=1, color=HAIR)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    y = masthead(draw)
    y = lead(draw, y)
    y = grid(draw, y + 8)
    y = ticker(draw, y + 6)
    footer(draw, y + 2)
    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
