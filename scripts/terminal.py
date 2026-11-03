"""Profile hero: a terminal session that types out who I am, the proof, and today's line
from how I work. Reprinted every morning by GitHub Actions so the date and line stay fresh.
Standard library only. Usage: python3 scripts/terminal.py <out_dir>"""
import datetime as dt
import sys
from pathlib import Path
from xml.sax.saxutils import escape
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
from theme import THEMES, style  # noqa: E402

TZ = ZoneInfo("Australia/Melbourne")
PROMPT = "mason@melbourne ~ %"
# value, what it measured, where (the same proof as the portfolio's Capabilities)
PROOF = [
    ("5/5", "POCs taken to production in my first four months", "redbridge"),
    ("-40%", "operations time per task, before and after go-live", "redbridge"),
    ("-20%", "working time once an agentic workflow replaced manual escalation", "thermomix"),
    ("-35%", "order fulfilment time from the Redshift ETL pipelines", "thermomix"),
    ("+25%", "revenue from the Python and SQL segmentation models", "myer"),
    ("2x", "mid-tier churn the brief missed, found with a cohort model", "myer"),
]
LINES = [
    "Sit with the person closest to the problem.",
    "Draw it before building it.",
    "Show it working before proposing the build.",
    "The tool follows the risk.",
    "Telemetry goes in before go-live.",
    "Count the hours returned, not the features shipped.",
    "Keep asking until the real bottleneck shows.",
    "Accuracy is non-negotiable.",
]
W, LH, X = 1200, 34, 4
STEP = 0.2  # seconds between printed lines


def svg(c, rows):
    out, t = [], 0.2
    for i, row in enumerate(rows):
        y = 30 + i * LH
        out.append(f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>'
                   f'<text x="{X}" y="{y}" font-size="20" class="mono" xml:space="preserve">{row}</text></g>')
        t += STEP * (2.4 if row.startswith(f'<tspan class="mu">{PROMPT}') else 1)
    y = 30 + len(rows) * LH
    cursor = (f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>'
              f'<text x="{X}" y="{y}" font-size="20" class="mono"><tspan class="mu">{PROMPT}</tspan> '
              f'<tspan class="pen">█<animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/></tspan></text></g>')
    H = y + 18
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<title>whoami: Mason Nguyen, applied AI and automation. Proof: {'; '.join(f'{v} {w}' for v, w, _ in PROOF)}.</title>
<style>{style(c)}</style>
{''.join(out)}
{cursor}
</svg>
"""


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now(TZ)
    line = LINES[now.timetuple().tm_yday % len(LINES)]
    cmd = lambda s: f'<tspan class="mu">{PROMPT}</tspan> <tspan class="b">{escape(s)}</tspan>'
    rows = [cmd("whoami"),
            'Mason Nguyen <tspan class="mu">·</tspan> applied AI &amp; automation <tspan class="mu">·</tspan> Redbridge Capital',
            "",
            cmd("cat proof.log")]
    rows += [f'<tspan class="pen b">{v:>5}</tspan>  {escape(w)}  <tspan class="mu">{where}</tspan>' for v, w, where in PROOF]
    rows += ["", cmd("echo $TODAY"),
             f'<tspan class="mu">{now:%a} {now.day} {now:%b %Y}</tspan>  “{escape(line)}”']
    for name, c in THEMES.items():
        (out / f"terminal-{name}.svg").write_text(svg(c, rows))
    print(f"{now:%a} {now.day} {now:%b %Y}", "|", line)


main()
