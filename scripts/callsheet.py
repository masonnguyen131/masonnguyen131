"""Daily call sheet: a cinema-ticket SVG rebuilt every morning by GitHub Actions.

Melbourne weather and golden hour (Open-Meteo, no key), the day of the year,
tonight's moon, and a rotating line from how I work.
Standard library only. Usage: python3 scripts/callsheet.py <out_dir>
"""
import base64
import datetime as dt
import hashlib
import json
import sys
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
USER = "masonnguyen131"
TZ = ZoneInfo("Australia/Melbourne")
EMBER = "#FF5B1F"
THEMES = {
    "dark": dict(bg="#0A0A0B", card="#111113", fg="#EDE8DF", mute="#8B867D", line="#2A2927"),
    "light": dict(bg="#EFEAE1", card="#F6F2EA", fg="#151413", mute="#6D685F", line="#D6D0C4"),
}
SCENES = [
    "Sit with the person closest to the problem.",
    "Draw it before building it.",
    "Show it working before proposing the build.",
    "The tool follows the risk.",
    "Telemetry goes in before go-live.",
    "Count the hours returned, not the features shipped.",
    "Keep asking until the real bottleneck shows.",
    "Accuracy is non-negotiable.",
]
WEATHER = {0: "Clear", 1: "Mostly clear", 2: "Partly cloudy", 3: "Overcast", 45: "Fog", 48: "Fog",
           51: "Drizzle", 53: "Drizzle", 55: "Drizzle", 61: "Rain", 63: "Rain", 65: "Heavy rain",
           80: "Showers", 81: "Showers", 82: "Heavy showers", 95: "Thunderstorm", 96: "Thunderstorm", 99: "Thunderstorm"}


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def weather():
    try:
        d = get_json("https://api.open-meteo.com/v1/forecast?latitude=-37.81&longitude=144.96"
                     "&daily=weather_code,temperature_2m_max,sunset&timezone=Australia%2FMelbourne&forecast_days=1")["daily"]
        sunset = dt.datetime.fromisoformat(d["sunset"][0])
        golden = (sunset - dt.timedelta(hours=1)).strftime("%H:%M")
        return f"{round(d['temperature_2m_max'][0])}° · {WEATHER.get(d['weather_code'][0], 'Mixed')}", f"{golden} to {sunset:%H:%M}"
    except Exception:
        return "Melbourne · four seasons", "Check the sky"


def moon(now):
    """Tonight's moon phase, for the night shoot. Days since a known new moon, mod the synodic month."""
    age = ((now - dt.datetime(2000, 1, 6, 18, 14, tzinfo=dt.timezone.utc)).total_seconds() / 86400) % 29.530588853
    names = ["New moon", "Waxing crescent", "First quarter", "Waxing gibbous",
             "Full moon", "Waning gibbous", "Last quarter", "Waning crescent"]
    return names[int((age / 29.530588853) * 8 + 0.5) % 8]


def fonts():
    files = {"Geist": "geist.woff2", "GeistMono": "geist-mono.woff2", "Serif": "instrument-serif-italic.woff2"}
    return "".join(
        f"@font-face{{font-family:'{n}';src:url(data:font/woff2;base64,{base64.b64encode((ROOT / 'assets/fonts' / f).read_bytes()).decode()}) format('woff2');}}"
        for n, f in files.items()
    )


def barcode(seed, x0, y0, width, height, color):
    bits = hashlib.sha256(seed.encode()).digest()
    bars, x = [], x0
    for b in bits:
        w = 1 + b % 4
        if x + w > x0 + width:
            break
        if b % 3:
            bars.append(f'<rect x="{x}" y="{y0}" width="{w}" height="{height}" fill="{color}"/>')
        x += w + 1 + (b >> 5) % 3
    return "".join(bars)


def svg(c, f, today, doy, total, wx, golden, take, scene):
    W, H, STUB = 1200, 380, 900
    e = escape
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<title>Call sheet for {e(today)}</title>
<style>{f}
.m{{font-family:'GeistMono',ui-monospace,monospace;font-size:13px;letter-spacing:1.2px;fill:{c['mute']}}}
.v{{font-family:'Geist',system-ui,sans-serif;font-size:22px;fill:{c['fg']}}}
.s{{font-family:'Serif',Georgia,serif;font-style:italic;fill:{c['fg']}}}
</style>
<defs><mask id="notch"><rect width="{W}" height="{H}" fill="#fff"/><circle cx="{STUB}" cy="0" r="18" fill="#000"/><circle cx="{STUB}" cy="{H}" r="18" fill="#000"/></mask></defs>
<g mask="url(#notch)">
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="{c['card']}" stroke="{c['line']}"/>
</g>
<line x1="{STUB}" y1="26" x2="{STUB}" y2="{H - 26}" stroke="{c['line']}" stroke-width="2" stroke-dasharray="2 8" stroke-linecap="round"/>

<text x="48" y="58" class="m">CALL SHEET</text>
<circle cx="168" cy="53" r="4" fill="{EMBER}"><animate attributeName="opacity" values="1;0.15;1" keyTimes="0;0.5;1" calcMode="discrete" dur="1.6s" repeatCount="indefinite"/></circle>
<text x="{STUB - 48}" y="58" class="m" text-anchor="end">DAY {doy} / {total}</text>
<text x="44" y="138" class="s" font-size="64">{e(today)}</text>
<text x="48" y="172" class="m">ON LOCATION · MELBOURNE, AUSTRALIA</text>

<line x1="48" y1="200" x2="{STUB - 48}" y2="200" stroke="{c['line']}"/>
<text x="48" y="232" class="m">WEATHER</text><text x="48" y="262" class="v">{e(wx)}</text>
<text x="330" y="232" class="m">GOLDEN HOUR</text><text x="330" y="262" class="v">{e(golden)}</text>
<text x="600" y="232" class="m">NIGHT SHOOT</text><text x="600" y="262" class="v">{e(take)}</text>
<line x1="48" y1="290" x2="{STUB - 48}" y2="290" stroke="{c['line']}"/>
<text x="48" y="326" class="m">TODAY'S SCENE</text>
<text x="48" y="352" class="s" font-size="26" fill="{EMBER}" style="fill:{EMBER}">{e(scene)}</text>

<text x="{STUB + 150}" y="58" class="m" text-anchor="middle">ADMIT ONE</text>
<text x="{STUB + 150}" y="160" class="s" font-size="84" text-anchor="middle" style="fill:{EMBER}">No. {doy}</text>
<text x="{STUB + 150}" y="196" class="m" text-anchor="middle">SEASON {today[-4:]}</text>
{barcode(today, STUB + 60, 232, 180, 64, c['fg'])}
<text x="{STUB + 150}" y="330" class="m" text-anchor="middle">MASONPORTFOLIO.VERCEL.APP</text>
</svg>
"""


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now(TZ)
    doy = now.timetuple().tm_yday
    total = 366 if now.year % 4 == 0 and (now.year % 100 or now.year % 400 == 0) else 365
    today = f"{now:%A}, {now.day} {now:%B %Y}"
    wx, golden = weather()
    take = moon(now)
    scene = SCENES[doy % len(SCENES)]
    f = fonts()
    for name, c in THEMES.items():
        (out / f"callsheet-{name}.svg").write_text(svg(c, f, today, doy, total, wx, golden, take, scene))
    print(today, "|", wx, "|", golden, "|", take, "|", scene)


main()
