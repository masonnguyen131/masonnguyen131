"""Avatar that flips between my photo and my sticker, like a card turning over.
Writes assets/avatar.svg from assets/photo.jpg and assets/sticker.svg. Usage: python3 scripts/avatar.py"""
import base64
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
photo = base64.b64encode((ROOT / "assets/photo.jpg").read_bytes()).decode()
sticker = (ROOT / "assets/sticker.svg").read_text()
sticker = re.sub(r"<title>.*?</title>", "", sticker).replace('<svg xmlns="http://www.w3.org/2000/svg"', '<svg x="0" y="0"', 1)

T = 8  # photo 0 to 3.6s, turn, sticker 4 to 7.6s, turn back
SQUASH = 'values="1 1;1 1;0.02 1;1 1;1 1;0.02 1;1 1" keyTimes="0;0.45;0.475;0.5;0.95;0.975;1"'
SHOW_PHOTO = 'values="1;0;1" keyTimes="0;0.475;0.975"'
SHOW_STICKER = 'values="0;1;0" keyTimes="0;0.475;0.975"'

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="400" height="400" viewBox="0 0 400 400">
<title>Mason Nguyen, photo and sticker</title>
<defs>
  <clipPath id="ph"><circle cx="200" cy="200" r="166"/></clipPath>
  <filter id="sh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#151413" flood-opacity="0.28"/></filter>
</defs>
<g transform="translate(200 200)"><g>
  <animateTransform attributeName="transform" type="scale" {SQUASH} dur="{T}s" repeatCount="indefinite"/>
  <g transform="translate(-200 -200)">
    <g opacity="1"><animate attributeName="opacity" {SHOW_PHOTO} calcMode="discrete" dur="{T}s" repeatCount="indefinite"/>
      <g filter="url(#sh)"><circle cx="200" cy="200" r="182" fill="#fffdf8"/></g>
      <image href="data:image/jpeg;base64,{photo}" xlink:href="data:image/jpeg;base64,{photo}" x="20" y="20" width="360" height="360" clip-path="url(#ph)"/>
      <circle cx="200" cy="200" r="166" fill="none" stroke="#151413" stroke-width="6"/>
    </g>
    <g opacity="0"><animate attributeName="opacity" {SHOW_STICKER} calcMode="discrete" dur="{T}s" repeatCount="indefinite"/>
      {sticker}
    </g>
  </g>
</g></g>
</svg>
"""
out = ROOT / "assets/avatar.svg"
out.write_text(svg)
print(out.name, round(out.stat().st_size / 1024), "KB")
