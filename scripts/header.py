"""GitHub profile header: a still from the portfolio hero.

Same palette and type as masonportfolio.vercel.app (fonts embedded so GitHub renders them),
faint drifting contour lines, and one ember dot travelling a contour.
Usage: python3 scripts/header.py   (writes assets/header-dark.svg and assets/header-light.svg)
"""
import base64
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
out = ROOT / "assets"
FONTS = {
    "Geist": ROOT / "assets/fonts/geist.woff2",
    "GeistMono": ROOT / "assets/fonts/geist-mono.woff2",
    "Serif": ROOT / "assets/fonts/instrument-serif-italic.woff2",
}
font_css = "".join(
    f"@font-face{{font-family:'{name}';src:url(data:font/woff2;base64,{base64.b64encode(p.read_bytes()).decode()}) format('woff2');}}"
    for name, p in FONTS.items()
)

THEMES = {
    "dark": dict(bg="#0A0A0B", fg="#EDE8DF", mute="#8B867D", line="#EDE8DF"),
    "light": dict(bg="#EFEAE1", fg="#151413", mute="#6D685F", line="#151413"),
}
EMBER = "#FF5B1F"
W, H = 1200, 400


def contour(i):
    pts = []
    for x in range(-200, W + 201, 20):
        y = 18 + i * 26
        y += 16 * math.sin(x / 190 + i * 0.22) + 8 * math.sin(x / 83 + i * 0.35)
        y -= 70 * math.exp(-(((x - 900) / 210) ** 2)) * math.exp(-(((i - 7) / 5) ** 2))  # a hill on the right
        pts.append(f"{x},{y:.1f}")
    return "M" + " L".join(pts)


def svg(c):
    lines = "\n".join(
        f'<path id="c{i}" d="{contour(i)}" fill="none" stroke="{c["line"]}" stroke-width="{1.2 if i % 5 == 0 else 0.8}" opacity="{0.22 if i % 5 == 0 else 0.1}"/>'
        for i in range(17)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<title>Mason Nguyen: Applied AI and automation</title>
<style>{font_css}
.mono{{font-family:'GeistMono',ui-monospace,monospace;font-size:13px;letter-spacing:1.2px;fill:{c['mute']}}}
.big{{font-family:'Geist',system-ui,sans-serif;font-weight:500;fill:{c['fg']}}}
.serif{{font-family:'Serif',Georgia,serif;font-style:italic;fill:{c['fg']}}}
</style>
<defs>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  <linearGradient id="fade" x1="0" x2="1"><stop offset="0.25" stop-color="{c['bg']}" stop-opacity="0.92"/><stop offset="0.65" stop-color="{c['bg']}" stop-opacity="0"/></linearGradient>
  <radialGradient id="glow"><stop offset="0" stop-color="{EMBER}" stop-opacity="0.55"/><stop offset="1" stop-color="{EMBER}" stop-opacity="0"/></radialGradient>
</defs>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="{c['bg']}"/>
  <g>
    <animateTransform attributeName="transform" type="translate" values="0 0; -60 6; 0 0" dur="40s" repeatCount="indefinite"/>
    {lines}
    <circle r="22" fill="url(#glow)"><animateMotion dur="14s" repeatCount="indefinite" rotate="auto"><mpath xlink:href="#c7"/></animateMotion></circle>
    <circle r="4.5" fill="{EMBER}"><animateMotion dur="14s" repeatCount="indefinite"><mpath xlink:href="#c7"/></animateMotion></circle>
  </g>
  <rect width="{W}" height="{H}" fill="url(#fade)"/>
  <g>
    <animate attributeName="opacity" from="0" to="1" dur="1.2s"/>
    <text x="56" y="70" class="mono">(01) APPLIED AI &amp; AUTOMATION</text>
    <text x="50" y="204" class="big" font-size="128" letter-spacing="-7">Mason</text>
    <text x="150" y="320" class="serif" font-size="132" letter-spacing="-2">Nguyen</text>
    <text x="56" y="366" class="mono">MELBOURNE  ·  NOW AT REDBRIDGE CAPITAL  ·  5 OF 5 POCS LIVE</text>
  </g>
  <circle cx="{W - 64}" cy="66" r="4" fill="{EMBER}"><animate attributeName="opacity" values="1;0.15;1" dur="1.6s" calcMode="discrete" keyTimes="0;0.5;1" repeatCount="indefinite"/></circle>
  <text x="{W - 78}" y="70" class="mono" text-anchor="end">SC 01 · OPENING</text>
</g>
</svg>
"""


out.mkdir(parents=True, exist_ok=True)
for name, c in THEMES.items():
    (out / f"header-{name}.svg").write_text(svg(c))
    print(name, round((out / f"header-{name}.svg").stat().st_size / 1024), "KB")
