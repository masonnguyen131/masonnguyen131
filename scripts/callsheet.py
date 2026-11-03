"""Daily call sheet: a GitHub-style card rebuilt every morning by GitHub Actions.

Melbourne weather and golden hour (Open-Meteo, no key), the day of the year,
tonight's moon, and a rotating line from how I work.
Standard library only. Usage: python3 scripts/callsheet.py <out_dir>
"""
import datetime as dt
import json
import sys
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
from theme import THEMES, circle, style  # noqa: E402

USER = "masonnguyen131"
TZ = ZoneInfo("Australia/Melbourne")
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


def svg(c, today, stamp, doy, total, wx, golden, moon_phase, scene):
    W, H, P = 1200, 330, 24
    e = escape
    d = c["dots"]
    cols = [("Weather", wx), ("Golden hour", golden), ("Tonight's moon", moon_phase)]
    stats = "".join(
        f'<text x="{P + i * 380}" y="112" font-size="12" class="mu">{k}</text>'
        f'<text x="{P + i * 380}" y="142" font-size="22" class="b">{e(v)}</text>' for i, (k, v) in enumerate(cols))
    bar_w = W - 2 * P
    u = len(scene) * 9.6  # rough width of the line at 20px, for the pen underline
    done = bar_w * doy / total
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<title>Call sheet for {e(today)}</title>
<style>{style(c)}</style>
<defs><clipPath id="box"><rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="6"/></clipPath></defs>
<g clip-path="url(#box)">
  <rect width="{W}" height="{H}" fill="{c['bg']}"/>
  <rect width="{W}" height="56" fill="{c['subtle']}"/>
</g>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="6" fill="none" stroke="{c['border']}"/>
<line x1="0" y1="56.5" x2="{W}" y2="56.5" stroke="{c['border']}"/>
<circle cx="{P + 6}" cy="28" r="5" fill="{c['pen']}"><animate attributeName="opacity" values="1;0.25;1" dur="2s" repeatCount="indefinite"/></circle>
<text x="{P + 20}" y="33" font-size="14"><tspan class="b">Call sheet</tspan><tspan class="mu">  ·  {e(today)}  ·  Melbourne, Australia</tspan></text>
<text x="{W - P}" y="33" font-size="12" class="mu mono" text-anchor="end">printed {stamp} by daily-reel.yml</text>
{stats}
<line x1="0" y1="172.5" x2="{W}" y2="172.5" stroke="{c['border']}"/>
<text x="{P}" y="206" font-size="12" class="mu">Today's line</text>
<text x="{P}" y="242" font-size="20">{e(scene)}</text>
<path d="M{P - 2} 254C{P + u * 0.3:.0f} 249 {P + u * 0.7:.0f} 247 {P + u:.0f} 250" fill="none" stroke="{c['pen']}" stroke-width="2" stroke-linecap="round"/>
<line x1="0" y1="272.5" x2="{W}" y2="272.5" stroke="{c['border']}"/>
<rect x="{P}" y="290" width="{bar_w}" height="8" rx="4" fill="{d[0]}"/>
<rect x="{P}" y="290" width="{done:.1f}" height="8" rx="4" fill="{c['pen']}"><animate attributeName="width" from="0" to="{done:.1f}" dur="1.6s" fill="freeze"/></rect>
<text x="{P}" y="320" font-size="12" class="mu">Day {doy} of {total}</text>
<text x="{W - P}" y="320" font-size="12" class="mu" text-anchor="end">{round(100 * doy / total)}% of {today[-4:]}</text>
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
    for name, c in THEMES.items():
        (out / f"callsheet-{name}.svg").write_text(svg(c, today, f"{now:%H:%M %Z}", doy, total, wx, golden, take, scene))
    print(today, "|", wx, "|", golden, "|", take, "|", scene)


main()
