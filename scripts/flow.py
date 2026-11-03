"""How the work moves: discover, map, prove, then a gateway on financial data that ships
lean or guarded, and measure. Two violet pulses run the lean and the guarded route in turn.
Writes assets/flow-{light,dark}.svg. Usage: python3 scripts/flow.py"""
from pathlib import Path

from theme import THEMES, style

ROOT = Path(__file__).resolve().parent.parent
W, H = 1200, 340
MID, TOP, BOT = 170, 92, 248
GATE, END = 630, 1100
# x, title, detail: the steps on the main line
STEPS = [(90, "Discover", "sit with the team"), (270, "Map", "BPMN as-is, to-be"),
         (450, "Prove", "live POC first"), (END, "Measure", "hours returned")]


def lane(y):
    """Main line to the gateway, a soft curve out to the lane at y, and back into Measure."""
    return (f"M90 {MID}H{GATE}C{GATE + 40} {MID} {GATE + 30} {y} {GATE + 80} {y}"
            f"H{END - 170}C{END - 120} {y} {END - 130} {MID} {END - 90} {MID}H{END}")


LEAN, GUARD = lane(TOP), lane(BOT)
T = 7  # seconds per route


def svg(c):
    pen, line = c["pen"], c["line"]
    steps = "".join(
        f'<circle cx="{x}" cy="{MID}" r="7" fill="{pen}"/>'
        f'<text x="{x}" y="{MID + 42}" font-size="22" class="b" text-anchor="middle">{title}</text>'
        f'<text x="{x}" y="{MID + 68}" font-size="15" class="mu mono" text-anchor="middle">{detail}</text>'
        for x, title, detail in STEPS)
    mid = (GATE + END - 90) / 2
    branches = (
        f'<text x="{mid}" y="{TOP - 40}" font-size="22" class="b" text-anchor="middle">Ship lean</text>'
        f'<text x="{mid}" y="{TOP - 16}" font-size="15" class="mu mono" text-anchor="middle">n8n · Power Platform · APIs</text>'
        f'<text x="{mid}" y="{BOT + 42}" font-size="22" class="b" text-anchor="middle">Ship guarded</text>'
        f'<text x="{mid}" y="{BOT + 66}" font-size="15" class="mu mono" text-anchor="middle">MCP agents · tests · telemetry</text>'
        f'<text x="{GATE + 50}" y="{(TOP + MID) / 2 + 2}" font-size="15" class="mu mono">no</text>'
        f'<text x="{GATE + 50}" y="{(BOT + MID) / 2 + 10}" font-size="15" class="mu mono">yes</text>')
    gate = (f'<rect x="{GATE - 13}" y="{MID - 13}" width="26" height="26" fill="{pen}" transform="rotate(45 {GATE} {MID})"/>'
            f'<text x="{GATE - 26}" y="{MID - 22}" font-size="15" class="mu mono" text-anchor="end">financial data?</text>')
    # one route at a time: lean, then guarded, then repeat
    pulses = "".join(
        f'<circle r="11" fill="{pen}" opacity="0.18"><animateMotion path="{p}" dur="{T}s" begin="{b}" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;0.5;1" calcMode="linear"/></circle>'
        f'<circle r="5" fill="{pen}"><animateMotion path="{p}" dur="{T}s" begin="{b}" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;0.5;1" calcMode="linear"/></circle>'
        for p, b in [(LEAN, "0s"), (GUARD, f"{T / 2}s")])
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<title>How the work moves: discover, map in BPMN, prove with a live POC, then ship lean with n8n, Power Platform or APIs, or ship guarded with MCP agents, tests and telemetry when financial data is involved, and measure the hours returned</title>
<style>{style(c)}</style>
<path d="{LEAN}" fill="none" stroke="{line}" stroke-width="2"/>
<path d="{GUARD}" fill="none" stroke="{line}" stroke-width="2"/>
{pulses}
{steps}{branches}{gate}
</svg>
"""


for name, c in THEMES.items():
    p = ROOT / "assets" / f"flow-{name}.svg"
    p.write_text(svg(c))
    print(p.name, round(p.stat().st_size / 1024, 1), "KB")
