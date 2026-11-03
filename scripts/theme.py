"""Shared look for every profile SVG: transparent backgrounds that sit on GitHub's own
white or dark, system type, and the portfolio's violet pen as the one accent."""

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"

THEMES = {
    "light": dict(fg="#1f2328", muted="#59636e", line="#d1d9e0", pen="#4f2bff"),
    "dark": dict(fg="#e6edf3", muted="#9198a1", line="#3d444d", pen="#a594ff"),
}


def style(c):
    return (f"text{{font-family:{FONT};fill:{c['fg']}}}"
            f".mu{{fill:{c['muted']}}}.pen{{fill:{c['pen']}}}.mono{{font-family:{MONO}}}.b{{font-weight:600}}")
