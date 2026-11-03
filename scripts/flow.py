"""How the work moves: the BPMN flow drawn on a contribution grid, with a snake that
runs it twice per loop, once down the lean branch and once down the guarded one.
Writes assets/flow-{light,dark}.svg. Usage: python3 scripts/flow.py"""
from pathlib import Path

from theme import EMBER, THEMES, style

ROOT = Path(__file__).resolve().parent.parent
PITCH, CELL, COLS, ROWS = 20, 16, 60, 16
W, H = COLS * PITCH, ROWS * PITCH
STEP = 0.11  # seconds per cell, like the snake's pace
SNAKE = [4, 4, 3, 3, 2, 2, 1]  # head to tail, as contribution levels

MAIN, TOP, BOT = 8, 3, 13
GATE = 37
# name: (col, row, width, title, subtitle)
NODES = {
    "discover": (4, MAIN, 140, "Discover", "sit with the team"),
    "map": (14, MAIN, 150, "Map in BPMN", "as-is to to-be"),
    "prove": (26, MAIN, 170, "Prove it live", "POC before the build"),
    "lean": (47, TOP, 190, "Ship lean", "n8n · Power Platform"),
    "guarded": (47, BOT, 230, "Ship guarded", "MCP agents · tests · telemetry"),
    "measure": (55, MAIN, 150, "Measure", "hours returned"),
}


def centre(col, row):
    return col * PITCH + PITCH / 2, row * PITCH + PITCH / 2


def walk(points):
    """Cells visited moving orthogonally through the given (col, row) corners."""
    cells = [points[0]]
    for (c1, r1) in points[1:]:
        c0, r0 = cells[-1]
        while (c0, r0) != (c1, r1):
            c0 += (c1 > c0) - (c1 < c0)
            if c0 == cells[-1][0]:
                r0 += (r1 > r0) - (r1 < r0)
            cells.append((c0, r0))
    return cells


LEAN = walk([(4, MAIN), (GATE, MAIN), (GATE, TOP), (55, TOP), (55, MAIN)])
GUARD = walk([(4, MAIN), (GATE, MAIN), (GATE, BOT), (55, BOT), (55, MAIN)])
LOOP = LEAN + GUARD
T = len(LOOP) * STEP


def inside(cell):
    x, y = centre(*cell)
    for col, row, w, *_ in NODES.values():
        nx, ny = centre(col, row)
        if abs(x - nx) < w / 2 + 4 and abs(y - ny) < 30:
            return True
    return False


def flash(times, base):
    """Discrete stroke animation: ember for a beat each time the snake's head arrives."""
    keys, vals = [0.0], [base]
    for t in sorted(times):
        a, b = t / len(LOOP), min((t + 10) / len(LOOP), 0.999)
        keys += [a, b]
        vals += [EMBER, base]
    return (f'<animate attributeName="stroke" values="{";".join(vals)}" keyTimes="{";".join(f"{k:.4f}" for k in keys)}" '
            f'calcMode="discrete" dur="{T:.2f}s" repeatCount="indefinite"/>')


def svg(c):
    d = c["dots"]
    track = set(LEAN) | set(GUARD)
    grid = "".join(
        f'<rect x="{col * PITCH + 2}" y="{row * PITCH + 2}" width="{CELL}" height="{CELL}" rx="3" fill="{d[1] if (col, row) in track else d[0]}"/>'
        for col in range(COLS) for row in range(ROWS) if not inside((col, row)))

    snake = []
    for i, lv in reversed(list(enumerate(SNAKE))):
        seq = [LOOP[(t - i) % len(LOOP)] for t in range(len(LOOP))]
        vals = ";".join(f"{col * PITCH + 2} {row * PITCH + 2}" for col, row in seq)
        snake.append(f'<rect width="{CELL}" height="{CELL}" rx="3" fill="{d[lv]}">'
                     f'<animateTransform attributeName="transform" type="translate" values="{vals}" calcMode="discrete" dur="{T:.2f}s" repeatCount="indefinite"/></rect>')

    nodes = []
    for key, (col, row, w, title, sub) in NODES.items():
        x, y = centre(col, row)
        hits = [t for t, cell in enumerate(LOOP) if cell == (col, row)]
        nodes.append(
            f'<rect x="{x - w / 2}" y="{y - 26}" width="{w}" height="52" rx="6" fill="{c["bg"]}" stroke="{c["border"]}" stroke-width="1.5">{flash(hits, c["border"])}</rect>'
            f'<text x="{x}" y="{y - 3}" font-size="14" class="b" text-anchor="middle">{title}</text>'
            f'<text x="{x}" y="{y + 15}" font-size="12" class="mu" text-anchor="middle">{sub}</text>')
    gx, gy = centre(GATE, MAIN)
    gate_hits = [t for t, cell in enumerate(LOOP) if cell == (GATE, MAIN)]
    nodes.append(
        f'<rect x="{gx - 15}" y="{gy - 15}" width="30" height="30" rx="4" fill="{c["bg"]}" stroke="{c["border"]}" stroke-width="1.5" transform="rotate(45 {gx} {gy})">{flash(gate_hits, c["border"])}</rect>'
        f'<text x="{gx}" y="{gy + 5}" font-size="14" class="b" text-anchor="middle">?</text>'
        f'<text x="{gx - 30}" y="{gy - 26}" font-size="12" class="mu" text-anchor="end">Touches financial data?</text>'
        f'<text x="{gx + 18}" y="{centre(0, TOP + 2)[1] + 4}" font-size="12" class="mu mono">no</text>'
        f'<text x="{gx + 18}" y="{centre(0, BOT - 2)[1] + 4}" font-size="12" class="mu mono">yes</text>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<title>How the work moves: discover, map in BPMN, prove it live, then ship lean or guarded depending on financial data, and measure the hours returned</title>
<style>{style(c)}</style>
{grid}
{''.join(snake)}
{''.join(nodes)}
</svg>
"""


for name, c in THEMES.items():
    p = ROOT / "assets" / f"flow-{name}.svg"
    p.write_text(svg(c))
    print(p.name, round(p.stat().st_size / 1024), "KB", f"loop {T:.1f}s")
