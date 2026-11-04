"""Animated sticker for the README: the portfolio's line-drawn Mason on a transparent
background, waving, blinking and breathing, with the doodles around him alive too.
Writes assets/sticker-{light,dark}.svg. Usage: python3 scripts/sticker.py"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# ink: the line work; paper: fills that hide lines behind them (GitHub's page colour); blob: behind the head
COLOURS = {
    "light": dict(ink="#1f2328", paper="#ffffff", blob="#ffb3e6", pen="#4f2bff"),
    "dark": dict(ink="#e6edf3", paper="#0d1117", blob="#3f3192", pen="#a594ff"),
}


def loop(attr, values, dur, extra=""):
    return f'<animate attributeName="{attr}" values="{values}" dur="{dur}s" repeatCount="indefinite"{extra}/>'


def spin(values, dur, kind="rotate", extra=""):
    return f'<animateTransform attributeName="transform" type="{kind}" values="{values}" dur="{dur}s" repeatCount="indefinite"{extra}/>'


def sparkle(cx, cy, r, delay):
    d = (f"M{cx} {cy - r}C{cx + r * .2} {cy - r * .2} {cx + r * .2} {cy - r * .2} {cx + r} {cy}"
         f"C{cx + r * .2} {cy + r * .2} {cx + r * .2} {cy + r * .2} {cx} {cy + r}"
         f"C{cx - r * .2} {cy + r * .2} {cx - r * .2} {cy + r * .2} {cx - r} {cy}"
         f"C{cx - r * .2} {cy - r * .2} {cx - r * .2} {cy - r * .2} {cx} {cy - r}Z")
    begin = f' begin="{delay}s"'
    return (f'<path d="{d}">{spin(f"0 {cx} {cy};90 {cx} {cy}", 2.4, extra=begin)}'
            f'{loop("opacity", "1;0.25;1", 2.4, begin)}</path>')


def svg(c):
    ink, paper, blob, pen = c["ink"], c["paper"], c["blob"], c["pen"]
    eye_open, eye_shut = "M226 150L226 160", "M226 155L226 155.5"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 500" width="400" height="500">
<title>Doodle of Mason waving, with a cine camera, a robot agent and a rising chart</title>
<defs><clipPath id="card"><rect width="400" height="500"/></clipPath></defs>
<g clip-path="url(#card)" fill="none" stroke="{ink}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
  <path d="M206 96C276 92 318 140 314 206C310 270 262 312 196 308C130 304 86 262 90 196C94 136 140 100 214 102" fill="{blob}" stroke="none"/>
  <g>{spin("0 0;0 4;0 0", 3.6, "translate", ' calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"')}
  <g transform="translate(0 74)"><g>
      <path d="M176 246C138 249 108 263 96 300C88 330 86 380 84 444"/>
      <path d="M224 246C262 249 292 263 304 300C312 330 314 380 316 444"/>
      <path d="M185 221L185 238M215 221L215 238"/>
      <path d="M176 246C160 240 160 226 176 228C180 229 183 232 185 236M224 246C240 240 240 226 224 228C220 229 217 232 215 236"/>
      <path d="M185 236C188 256 212 256 215 236"/>
      <path d="M192 252C191 266 190 278 191 292M208 252C209 266 210 278 209 292"/><path d="M191 292L191 299M209 292L209 299" stroke-width="5"/>
      <path d="M146 444L156 394C178 386 222 386 244 394L254 444"/>
    </g><g>
      <path d="M135 138C130 188 160 222 200 222C242 222 271 188 267 136"/>
      <path d="M134 150C117 143 113 174 137 179M266 150C283 143 287 174 263 179"/>
      <path d="M132 141C125 109 131 86 147 71C153 77 160 80 169 78C172 65 180 55 194 49C197 59 204 67 214 69C221 58 233 50 248 49C246 60 249 69 257 76C264 73 271 73 277 76C280 99 277 122 269 142"/>
      <path d="M132 141C148 128 158 113 163 96C176 113 204 119 230 109C246 104 263 118 269 142"/>
      <path d="M178 80C182 88 188 94 196 98M226 78C234 84 240 92 242 102"/>
      <path d="M202 160C196 170 197 177 205 177"/>
      <path d="{eye_open}" stroke-width="4">{loop("d", f"{eye_open};{eye_open};{eye_shut};{eye_open}", 3.8, ' keyTimes="0;0.92;0.96;1"')}</path>
      <path d="M167 157C172 161 180 161 185 156"/>
      <path d="M164 137C170 132 180 132 186 136M216 136C222 132 232 132 238 137"/>
      <path d="M182 186C186 206 216 206 220 186C207 190 195 190 182 186Z"/><path d="M185 191C195 194 207 194 217 191"/>
    </g><g>
      <path d="M120 318C124 360 126 400 126 444"/>
      <path d="M262 258C284 248 300 232 307 213M300 282C320 270 334 252 340 226"/>
      <g>{spin("-4 323 220;12 323 220;-4 323 220", 0.9, extra=' calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"')}
        <path d="M307 213C313 196 316 178 318 156M340 226C348 206 352 182 352 158"/>
        <path d="M316 170C328 176 342 177 354 172"/>
        <path fill="{paper}" d="M318 155C316 143 308 135 304 125C301 117 308 112 314 118L321 127L320 95C320 87 330 87 330 95L330 119L331 87C331 78 342 78 342 87L341 119L343 92C344 84 353 85 352 93L350 121L353 104C355 97 363 99 361 106L357 140C356 148 354 153 352 158"/>
        <path d="M372 94C381 103 384 115 381 127M292 90C285 99 284 110 287 121">{loop("opacity", "1;0.2;1", 0.9)}</path>
      </g>
    </g></g></g>
  <g transform="translate(30 34) rotate(-8)">
    <path d="M14 40C14 34 18 32 24 32L82 32C88 32 92 34 92 40L92 70C92 76 88 78 82 78L24 78C18 78 14 76 14 70Z" fill="{paper}"/>
    <path d="M34 30a13 13 0 1 0 0.1 0M70 26a16 16 0 1 0 0.1 0" fill="{paper}"/>
    <path d="M92 46L114 36L114 74L92 64"/>
    <path d="M26 44L40 44"/>
    <path d="M78 46a4 4 0 1 0 0.1 0" fill="{pen}">{loop("fill-opacity", "1;1;0.15;0.15", 1.4, ' calcMode="discrete"')}</path>
  </g>
  <g transform="translate(296 40)">
    <path d="M4 4L4 76L84 76"/>
    <path d="M12 64L30 50L46 56L74 22M74 22L60 24M74 22L72 36" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0">{loop("stroke-dashoffset", "100;0;0;100", 4, ' keyTimes="0;0.35;0.9;1"')}</path>
  </g>
  <g>{spin("0 0;0 -6;0 0", 2.2, "translate", ' calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"')}
  <g transform="translate(38 392) rotate(-8)">
    <path d="M10 0C10 -10 16 -14 30 -14L50 -14C64 -14 70 -10 70 0L70 28C70 38 64 42 50 42L30 42C16 42 10 38 10 28Z" fill="{paper}"/>
    <path d="M40 -14L40 -26"/>
    <path d="M40 -32a5 5 0 1 0 0.1 0" fill="{pen}">{loop("fill-opacity", "1;0.2;1", 1.6)}</path>
    <path d="M26 14C29 9 34 9 37 14M44 14C47 9 52 9 55 14"/>
    <path d="M33 27C37 31 44 31 48 27"/>
  </g></g>
  {sparkle(366, 326, 10, 0)}
  {sparkle(56, 202, 6, 1.2)}
</g>
</svg>
"""


for name, c in COLOURS.items():
    p = ROOT / "assets" / f"sticker-{name}.svg"
    p.write_text(svg(c))
    print(p.name, round(p.stat().st_size / 1024, 1), "KB")
