#!/usr/bin/env python3
"""Render the 23 November 2026 world-news front page (1024x1024 PNG).

Rewritten from scratch in this session for make.fun news-image-20261123.
Everything is drawn with Pillow primitives: no network, no randomness,
no external assets. Deterministic output.

Usage:  python3 draw_poster.py   ->  writes entry.png next to this file.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- page setup
PAGE = 1024
PAD = 38
LEFT = PAD
RIGHT = PAGE - PAD
CONTENT_W = RIGHT - LEFT

PAPER = (248, 243, 232)      # warm newsprint
INK = (18, 18, 18)           # near-black
RED = (158, 27, 27)          # kicker red
NAVY = (31, 58, 95)          # globe blue
BODY = (52, 50, 46)          # body grey-black
MUTED = (92, 88, 80)         # dateline / footer grey
HAIRLINE = (178, 172, 158)   # light rule
GOLD = (232, 196, 90)        # ticker label
TICKER_BG = INK

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SERIF_BOLD = "DejaVuSerif-Bold.ttf"
SERIF_REG = "DejaVuSerif.ttf"
SANS_BOLD = "DejaVuSans-Bold.ttf"
SANS_REG = "DejaVuSans.ttf"

# ------------------------------------------------------------------- stories
DATELINE = "MONDAY  \u00b7  23 NOVEMBER 2026  \u00b7  ONE DAY, ONE PAGE"
MASTHEAD = "THE DAILY GLOBE"
TAGLINE = "The world\u2019s news, summed up in a single page"

LEAD_KICKER = "CLIMATE  \u00b7  ANTALYA, T\u00dcRKIYE"
LEAD_HEAD = ["COP31 COLLAPSES AS", "EU WALKS OUT"]
LEAD_DECK = (
    "Nearly 200 nations leave the climate summit with no deal after the "
    "draft drops every mention of fossil fuels \u2014 the longest UN "
    "climate talks ever held."
)
LEAD_CAPTION = "NO DEAL IN ANTALYA"

# (kicker, headline, body) — two columns, three rows.
STORIES = [
    (
        "GULF WAR WIDENS",
        "Iran hits US bases in Bahrain; Houthis fire on Saudi Arabia",
        "Two hurt in Bahrain; Riyadh downs Houthi missiles \u2014 yet "
        "Tehran says a deal is still possible.",
    ),
    (
        "BALTIC SEA",
        "Sanctioned Russian freighter burns off Finland",
        "Sparta II, hit by drones en route to Kaliningrad, is towed from "
        "Finnish waters; all 16 crew evacuated safely.",
    ),
    (
        "UKRAINE",
        "14 missing after drone flattens Kyiv flats",
        "Rescuers dig through rubble near Kyiv after a five-storey block "
        "is hit; nine people are pulled out alive.",
    ),
    (
        "INDONESIA",
        "Factory fire near Jakarta kills at least 3",
        "A candy-plant blaze in Banten traps workers overnight; dozens "
        "still missing as families wait outside the gates.",
    ),
    (
        "SOUTH KOREA",
        "Minister quits over AI exam-cheating row",
        "Education chief Choi Kyo-jin resigns two days before the Suneung "
        "after anti-cheating measures spark chaos.",
    ),
    (
        "INDIA \u00b7 NEPAL",
        "Nepal PM begins first visit to Delhi",
        "Rapper-turned-PM Balendra Shah meets Modi on Monday for talks "
        "on trade, energy and flood recovery.",
    ),
]

TICKER_LABEL = "ALSO TODAY  \u00b7  "
TICKER_ITEMS = (
    "WELLINGTON: India post a record 720/9 in the Test against New "
    "Zealand   \u2022   LONDON: UK and EU agree a post-Brexit reset deal   "
    "\u2022   DHAKA: Deadly protests over exiled ex-leader"
)

FOOTER = (
    "Sources: AP \u00b7 Reuters \u00b7 BBC \u00b7 NPR \u00b7 DW \u00b7 ANI  "
    "\u2014  All stories dated 22\u201323 November 2026"
)


# ------------------------------------------------------------------- helpers
def load_font(filename, size):
    return ImageFont.truetype(str(FONT_DIR / filename), size)


def wrap_text(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines fitting max_width px."""
    out = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        current = ""
        for word in words:
            trial = f"{current} {word}".strip()
            if not current or draw.textlength(trial, font=font) <= max_width:
                current = trial
            else:
                out.append(current)
                current = word
        if current:
            out.append(current)
    return out


class FrontPage:
    """A newspaper front page drawn top to bottom with a moving cursor."""

    def __init__(self):
        self.image = Image.new("RGB", (PAGE, PAGE), PAPER)
        self.draw = ImageDraw.Draw(self.image)
        self.y = 0  # cursor: top of the next block

    # -- generic drawing -------------------------------------------------
    def rule(self, y, weight=1, colour=INK, x0=LEFT, x1=RIGHT):
        self.draw.line([(x0, y), (x1, y)], fill=colour, width=weight)

    def centred(self, text, y, font, colour=INK):
        width = self.draw.textlength(text, font=font)
        self.draw.text(((PAGE - width) / 2, y), text, font=font, fill=colour)

    def globe(self, cx, cy, radius, colour=INK, weight=3):
        d = self.draw
        d.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                  outline=colour, width=weight)
        d.ellipse([cx - radius // 2, cy - radius,
                   cx + radius // 2, cy + radius], outline=colour, width=2)
        d.line([(cx - radius, cy), (cx + radius, cy)], fill=colour, width=2)
        box = [cx - radius, cy - radius // 2, cx + radius, cy + radius // 2]
        d.arc(box, 200, 340, fill=colour, width=2)
        d.arc(box, 20, 160, fill=colour, width=2)

    # -- sections --------------------------------------------------------
    def masthead(self):
        self.y = 30
        self.centred(DATELINE, self.y, load_font(SANS_BOLD, 15), MUTED)
        title_font = load_font(SERIF_BOLD, 72)
        title_y = self.y + 34
        self.globe(LEFT + 34, title_y + 48, 30)
        self.globe(RIGHT - 34, title_y + 48, 30)
        self.centred(MASTHEAD, title_y, title_font)
        self.centred(TAGLINE, self.y + 118, load_font(SERIF_REG, 19), MUTED)
        rule_y = self.y + 152
        self.rule(rule_y, weight=4)
        self.rule(rule_y + 8, weight=1)
        self.y = rule_y + 16

    def lead_story(self):
        top = self.y
        text_width = 640
        self.draw.text((LEFT, top), LEAD_KICKER,
                       font=load_font(SANS_BOLD, 17), fill=RED)
        head_font = load_font(SERIF_BOLD, 54)
        hy = top + 30
        for line in LEAD_HEAD:
            self.draw.text((LEFT, hy), line, font=head_font, fill=INK)
            hy += 62
        deck_font = load_font(SANS_REG, 21)
        dy = hy + 6
        for line in wrap_text(self.draw, LEAD_DECK, deck_font, text_width):
            self.draw.text((LEFT, dy), line, font=deck_font, fill=INK)
            dy += 28

        # Cracked-globe motif to the right of the lead text.
        cx, cy, r = 830, 300, 72
        d = self.draw
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=4)
        d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r],
                  outline=NAVY, width=2)
        d.line([(cx - r, cy), (cx + r, cy)], fill=NAVY, width=2)
        crack = [(cx - 18, cy - r + 8), (cx + 6, cy - 34), (cx - 12, cy + 2),
                 (cx + 14, cy + 30), (cx - 4, cy + r - 10)]
        d.line(crack, fill=RED, width=4, joint="curve")
        caption_font = load_font(SANS_BOLD, 13)
        caption_w = self.draw.textlength(LEAD_CAPTION, font=caption_font)
        self.draw.text((cx - caption_w / 2, cy + r + 12), LEAD_CAPTION,
                       font=caption_font, fill=RED)
        self.y = 444

    def story_card(self, x, y, width, kicker, headline, body):
        d = self.draw
        d.text((x, y), kicker, font=load_font(SANS_BOLD, 15), fill=RED)
        hy = y + 24
        # Shrink the headline until it fits in two lines.
        size = 25
        while size > 12:
            head_font = load_font(SERIF_BOLD, size)
            lines = wrap_text(d, headline, head_font, width)
            if len(lines) <= 2:
                break
            size -= 1
        for line in lines:
            d.text((x, hy), line, font=head_font, fill=INK)
            hy += 30
        body_font = load_font(SANS_REG, 16)
        by = hy + 2
        for line in wrap_text(d, body, body_font, width)[:3]:
            d.text((x, by), line, font=body_font, fill=BODY)
            by += 21
        return by

    def story_grid(self):
        y0 = self.y + 8
        gutter = 28
        col_w = (CONTENT_W - gutter) // 2
        divider_x = LEFT + col_w + gutter // 2
        row_h = 154
        for index, (kicker, headline, body) in enumerate(STORIES):
            row, col = divmod(index, 2)
            x = LEFT if col == 0 else divider_x + gutter // 2
            cy = y0 + row * row_h
            if row > 0:
                self.rule(cy - 12, weight=1, colour=HAIRLINE)
            self.story_card(x, cy, col_w, kicker, headline, body)
        bottom = y0 + 3 * row_h
        self.rule(bottom - 12, weight=1, colour=HAIRLINE)
        self.draw.line([(divider_x, y0), (divider_x, bottom - 24)],
                       fill=HAIRLINE, width=1)
        self.y = bottom

    def ticker_strip(self):
        top = self.y + 6
        height = 64
        self.draw.rectangle([LEFT, top, RIGHT, top + height], fill=TICKER_BG)
        label_font = load_font(SANS_BOLD, 15)
        self.draw.text((LEFT + 14, top + 22), TICKER_LABEL,
                       font=label_font, fill=GOLD)
        label_w = self.draw.textlength(TICKER_LABEL, font=label_font)
        text_font = load_font(SANS_REG, 16)
        lines = wrap_text(self.draw, TICKER_ITEMS, text_font,
                          RIGHT - (LEFT + 14 + label_w) - 14)
        ty = top + 12 if len(lines) > 1 else top + 22
        for line in lines[:2]:
            self.draw.text((LEFT + 14 + label_w, ty), line,
                           font=text_font, fill=PAPER)
            ty += 21
        self.y = top + height + 14

    def footer(self):
        self.rule(self.y - 8, weight=1, colour=HAIRLINE)
        self.centred(FOOTER, self.y + 2, load_font(SANS_REG, 13), MUTED)

    def render(self):
        self.masthead()
        self.lead_story()
        self.story_grid()
        self.ticker_strip()
        self.footer()
        return self.image


def main():
    page = FrontPage()
    image = page.render()
    out = Path(__file__).resolve().parent / "entry.png"
    image.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
