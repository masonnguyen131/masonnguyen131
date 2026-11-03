"""Profile header: a contribution graph whose cells spell MASON, then fade and redraw.
Writes assets/header-{light,dark}.svg. Usage: python3 scripts/header.py"""
import random
from pathlib import Path

from theme import THEMES, style

ROOT = Path(__file__).resolve().parent.parent
COLS, ROWS, PITCH, CELL = 53, 7, 20, 16
X0, Y0 = 70, 96
W, H = 1200, 300
T = 12  # seconds per loop
GLYPHS = {
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
}
MONTHS = ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"]


def letters(word="MASON"):
    start = (COLS - (len(word) * 6 - 1)) // 2
    lit = {}
    rng = random.Random(7)
    for i, ch in enumerate(word):
        for r, row in enumerate(GLYPHS[ch]):
            for k, bit in enumerate(row):
                if bit == "1":
                    lit[(start + i * 6 + k, r)] = rng.choice([3, 4, 4, 4])
    return lit, start


def svg(c):
    d = c["dots"]
    lit, start = letters()
    rng = random.Random(42)
    cells = []
    for col in range(COLS):
        for row in range(ROWS):
            x, y = X0 + col * PITCH, Y0 + row * PITCH
            if (col, row) in lit:
                on = (0.4 + (col - start) * 0.06) / T
                off = (10.4 + (col - start) * 0.02) / T
                lv = d[lit[(col, row)]]
                anim = (f'<animate attributeName="fill" values="{d[0]};{d[0]};{lv};{lv};{d[0]};{d[0]}" '
                        f'keyTimes="0;{on:.3f};{on + 0.03:.3f};{off:.3f};{off + 0.03:.3f};1" dur="{T}s" repeatCount="indefinite"/>')
                cells.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{lv}">{anim}</rect>')
            else:
                lv = rng.choices([0, 1], [93, 7])[0]
                cells.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{d[lv]}"/>')
    months = "".join(f'<text x="{X0 + i * 4.42 * PITCH:.0f}" y="{Y0 - 12}" class="mu" font-size="12">{m}</text>'
                     for i, m in enumerate(MONTHS))
    days = "".join(f'<text x="{X0 - 12}" y="{Y0 + r * PITCH + 12}" class="mu" font-size="12" text-anchor="end">{n}</text>'
                   for r, n in [(1, "Mon"), (3, "Wed"), (5, "Fri")])
    legend_x = X0 + COLS * PITCH - 4 - 5 * 15 - 34
    legend = "".join(f'<rect x="{legend_x + i * 15}" y="{H - 44}" width="11" height="11" rx="2" fill="{d[i]}"/>' for i in range(5))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<title>Mason Nguyen: applied AI and automation, Melbourne</title>
<style>{style(c)}</style>
<text x="8" y="22" font-size="16"><tspan class="b">5 of 5</tspan> automation POCs shipped to production in the last four months</text>
<rect x="0.5" y="40.5" width="{W - 1}" height="{H - 41}" rx="6" fill="{c['bg']}" stroke="{c['border']}"/>
{months}{days}
{''.join(cells)}
<text x="{X0 - 30}" y="{H - 34}" class="mu" font-size="12">Mason Nguyen · Applied AI and automation · Melbourne, Australia</text>
<text x="{legend_x - 6}" y="{H - 34}" class="mu" font-size="12" text-anchor="end">Less</text>
{legend}
<text x="{legend_x + 5 * 15 + 2}" y="{H - 34}" class="mu" font-size="12">More</text>
</svg>
"""


for name, c in THEMES.items():
    p = ROOT / "assets" / f"header-{name}.svg"
    p.write_text(svg(c))
    print(p.name, round(p.stat().st_size / 1024), "KB")
