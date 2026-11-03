"""Shared look for every profile SVG: GitHub's Primer colours and system fonts,
with the contribution-reel palette (the same dots the snake eats) as the accent."""

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"
EMBER = "#FF5B1F"

# dots: contribution levels 0..4, identical to the snake's color_dots in daily-reel.yml
THEMES = {
    "light": dict(bg="#ffffff", subtle="#f6f8fa", fg="#1f2328", muted="#59636e", border="#d1d9e0",
                  dots=["#E6E0D4", "#EBC3AA", "#F3A07A", "#FA7A47", "#FF5B1F"]),
    "dark": dict(bg="#0d1117", subtle="#151b23", fg="#f0f6fc", muted="#9198a1", border="#3d444d",
                 dots=["#1A1A1C", "#3B241B", "#6E3016", "#B54217", "#FF5B1F"]),
}


def style(c):
    return (f"text{{font-family:{FONT};fill:{c['fg']}}}"
            f".mu{{fill:{c['muted']}}}.mono{{font-family:{MONO}}}.b{{font-weight:600}}")
