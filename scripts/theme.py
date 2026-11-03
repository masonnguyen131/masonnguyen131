"""Shared look for every profile SVG, matched to the portfolio: warm paper and ink, with a
ballpoint-violet pen as the accent. The contribution-reel palette runs from paper to violet
(the same dots the snake eats)."""

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"

# dots: contribution levels 0..4, identical to the snake's color_dots in daily-reel.yml
THEMES = {
    "light": dict(bg="#eceae6", subtle="#e3e1dc", fg="#161514", muted="#6b6862", border="#d3d0ca", pen="#4f2bff",
                  dots=["#E3E1DC", "#D9D0FF", "#B3A4FF", "#7F66FF", "#4F2BFF"]),
    "dark": dict(bg="#131211", subtle="#1c1b19", fg="#eceae6", muted="#8f8b84", border="#2e2c29", pen="#a594ff",
                 dots=["#1C1B19", "#2A2347", "#3F3192", "#5E45E0", "#8F7BFF"]),
}


def style(c):
    return (f"text{{font-family:{FONT};fill:{c['fg']}}}"
            f".mu{{fill:{c['muted']}}}.mono{{font-family:{MONO}}}.b{{font-weight:600}}")


def circle(x, y, w, h, colour):
    """The portfolio's hand-drawn pen circle, fitted around a box."""
    return (f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="0 0 200 100" preserveAspectRatio="none" overflow="visible">'
            f'<path d="M118 8C60 2 10 22 8 52C6 84 60 96 112 92C164 88 194 70 192 44C190 18 150 6 96 10C70 12 52 18 40 26" '
            f'fill="none" stroke="{colour}" stroke-width="1.8" stroke-linecap="round" vector-effect="non-scaling-stroke"/></svg>')
