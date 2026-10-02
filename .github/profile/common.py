"""Shared pieces for the profile SVG generators: themes, outline text, documents.

Text is drawn from Geist outlines (fonts/glyphs.json) with real advances and
kerning rather than a web font, so every image renders identically in any
browser and inside GitHub's image sandbox, which blocks font loading.
"""

from __future__ import annotations

import json
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
_FONT = json.loads((HERE / "fonts" / "glyphs.json").read_text(encoding="utf-8"))
UPM = _FONT["upm"]
CAP = .71  # Geist cap height in em: baseline = centre + CAP * size / 2

EASE_OUT = "cubic-bezier(.16,1,.3,1)"
EASE_IN_OUT = "cubic-bezier(.65,0,.35,1)"

# GitHub Primer neutrals, so the images sit natively on github.com in either theme.
THEMES = {
    "dark": {
        "canvas": "#0d1117", "subtle": "#151b23", "raised": "#1b222c",
        "border": "#30363d", "hair": "#21262d",
        "fg": "#e6edf3", "muted": "#8d96a0", "faint": "#6e7681",
        "accent": "#4493f8", "accentSoft": "#4493f8", "success": "#3fb950", "danger": "#f85149",
        "headTop": "#ffffff", "headBottom": "#a4acb7", "grid": "#ffffff", "gridAlpha": .05,
        "shadow": .0,
        "levels": ["#1b222c", "#2e3742", "#4c5664", "#808b99", "#d6dde5"],
    },
    "light": {
        "canvas": "#ffffff", "subtle": "#f6f8fa", "raised": "#ffffff",
        "border": "#d1d9e0", "hair": "#e4e9ee",
        "fg": "#1f2328", "muted": "#59636e", "faint": "#818b98",
        "accent": "#0969da", "accentSoft": "#0969da", "success": "#1a7f37", "danger": "#d1242f",
        "headTop": "#1f2328", "headBottom": "#4b5563", "grid": "#1f2328", "gridAlpha": .055,
        "shadow": .06,
        "levels": ["#eff2f5", "#d1d9e0", "#9ea8b3", "#5f6b78", "#1f2328"],
    },
}

REDUCED_MOTION = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def f(v: float) -> str:
    """Compact number for SVG attributes."""
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def pct(t: float, total: float) -> str:
    return f"{t / total * 100:.3f}".rstrip("0").rstrip(".") + "%"


def onoff(name: str, total: float, on: float, off: float, ramp: float = .3, prop: str = "opacity") -> str:
    """Keyframes that fade a property in at `on` and back out at `off` (seconds into the loop)."""
    return (f"@keyframes {name}{{0%,{pct(on, total)}{{{prop}:0}}{pct(on + ramp, total)},{pct(off, total)}{{{prop}:1}}"
            f"{pct(off + ramp, total)},100%{{{prop}:0}}}}")


def attrs(**kw) -> str:
    """Python kwargs -> SVG attributes (trailing _ dropped, _ -> -)."""
    out = []
    for k, v in kw.items():
        if v is None:
            continue
        name = k.rstrip("_").replace("_", "-")
        out.append(f' {name}="{f(v) if isinstance(v, float) else v}"')
    return "".join(out)


def _layout(s: str, weight: int, family: str, tracking: float):
    """Glyph origins in font units, applying kerning and tracking (in em)."""
    face = _FONT["families"][family][str(weight)]
    glyphs, kern = face["glyphs"], face["kern"]
    x, prev, placed = 0.0, None, []
    for ch in s.replace(" ", " "):
        if ch not in glyphs:
            raise KeyError(f"no glyph for {ch!r} in {s!r}")
        if prev is not None:
            x += kern.get(prev + ch, 0) + tracking * UPM
        if ch != " ":
            placed.append((ch, x))
        x += glyphs[ch][0]
        prev = ch
    return placed, x


def measure(s: str, size: float, weight: int = 400, family: str = "sans", tracking: float = 0.0) -> float:
    return _layout(s, weight, family, tracking)[1] * size / UPM


class Doc:
    """An SVG document that collects glyph definitions as text is laid out."""

    def __init__(self, width: int, height: int, title: str, desc: str = ""):
        self.width, self.height = width, height
        self.title, self.desc = title, desc
        self.css: list[str] = []
        self.defs: list[str] = []
        self.body: list[str] = []
        self._glyphs: dict[str, str] = {}

    def text(self, s: str, x: float, y: float, size: float, weight: int = 400, family: str = "sans",
             anchor: str = "start", tracking: float = 0.0, **kw) -> str:
        """Outline text with its baseline at y. Returns markup; callers place it."""
        placed, width = _layout(s, weight, family, tracking)
        k = size / UPM
        if anchor == "middle":
            x -= width * k / 2
        elif anchor == "end":
            x -= width * k
        table = _FONT["families"][family][str(weight)]["glyphs"]
        uses = []
        for ch, gx in placed:
            gid = f"{family[0]}{weight}-{ord(ch):x}"
            self._glyphs.setdefault(gid, table[ch][1])
            uses.append(f'<use href="#{gid}" x="{f(gx)}"/>')
        return (f'<g transform="translate({f(x)} {f(y)}) scale({k:g} {-k:g})"{attrs(**kw)}>'
                f'{"".join(uses)}</g>')

    def render(self) -> str:
        glyphs = "".join(f'<path id="{gid}" d="{d}"/>' for gid, d in sorted(self._glyphs.items()))
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" '
            f'viewBox="0 0 {self.width} {self.height}" role="img" aria-labelledby="title desc">'
            f'<title id="title">{escape(self.title)}</title><desc id="desc">{escape(self.desc)}</desc>'
            f'<style>{"".join(self.css)}{REDUCED_MOTION}</style>'
            f'<defs>{glyphs}{"".join(self.defs)}</defs>{"".join(self.body)}</svg>\n'
        )

    def save(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.render(), encoding="utf-8")
        return path


def rrect(x: float, y: float, w: float, h: float, r: float, **kw) -> str:
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(r)}"{attrs(**kw)}/>'
