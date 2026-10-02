"""Extract Geist / Geist Mono outlines, advances and kerning into glyphs.json.

Run once (needs fontTools + brotli). The profile SVGs draw text as outlines
instead of embedding a web font, so they render identically in every browser
and inside GitHub's image sandbox, which blocks font loading. The data is a
Modified Version of Geist, distributed under the SIL OFL 1.1 (see OFL.txt).

    python build_glyphs.py <geist-latin.woff2> <geist-mono-latin.woff2>

Both variable fonts ship with Next.js (next/dist/next-devtools/server/font/).
"""

import json
import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

CHARS = [chr(c) for c in range(0x20, 0x7F)] + list("·•–—…×−©°")
FAMILIES = {"sans": (400, 500, 600, 700), "mono": (400, 500, 600)}


def kerning(font: TTFont, names: dict[str, str]) -> dict[str, int]:
    """Pair kerning (first glyph XAdvance) from the GPOS 'kern' feature."""
    gpos = font["GPOS"].table
    indices = sorted({i for rec in gpos.FeatureList.FeatureRecord if rec.FeatureTag == "kern"
                      for i in rec.Feature.LookupListIndex})
    matched: dict[tuple[str, str], int] = {}
    for index in indices:
        lookup = gpos.LookupList.Lookup[index]
        for sub in lookup.SubTable:
            if lookup.LookupType == 9:
                sub = sub.ExtSubTable
            if getattr(sub, "LookupType", 2) != 2 or not hasattr(sub, "Coverage"):
                continue
            for i, first in enumerate(sub.Coverage.glyphs):
                if first not in names:
                    continue
                if sub.Format == 1:
                    for rec in sub.PairSet[i].PairValueRecord:
                        if rec.SecondGlyph in names:
                            pair = (names[first], names[rec.SecondGlyph])
                            matched.setdefault(pair, getattr(rec.Value1, "XAdvance", 0) or 0)
                else:
                    row = sub.Class1Record[sub.ClassDef1.classDefs.get(first, 0)].Class2Record
                    for second, ch in names.items():
                        rec = row[sub.ClassDef2.classDefs.get(second, 0)]
                        matched.setdefault((names[first], ch), getattr(rec.Value1, "XAdvance", 0) or 0)
    return {a + b: v for (a, b), v in sorted(matched.items()) if v}


def extract(path: Path, weight: int) -> dict:
    font = instantiateVariableFont(TTFont(path), {"wght": weight})
    cmap, glyphs = font.getBestCmap(), font.getGlyphSet()
    names = {cmap[ord(ch)]: ch for ch in CHARS if ord(ch) in cmap}
    table = {}
    for name, ch in names.items():
        pen = SVGPathPen(glyphs, ntos=lambda v: f"{v:g}")
        glyphs[name].draw(pen)
        table[ch] = [font["hmtx"][name][0], pen.getCommands()]
    return {"glyphs": table, "kern": kerning(font, names)}


def main() -> None:
    sources = dict(zip(FAMILIES, map(Path, sys.argv[1:3])))
    out = {"upm": 1000, "families": {}}
    for family, weights in FAMILIES.items():
        out["families"][family] = {str(w): extract(sources[family], w) for w in weights}
    path = Path(__file__).with_name("glyphs.json")
    path.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(path, path.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
