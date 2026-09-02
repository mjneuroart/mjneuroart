#!/usr/bin/env python3
"""
outline_title.py — convertit les textes typographiés de la bannière en tracés SVG.

POURQUOI. Un SVG affiché par GitHub dans <img> peut incorporer une police en base64,
mais dans Chromium ce bloc <style> gèle la timeline SMIL : la bannière restait figée
à t=0 (mesuré le 02/09/2026, dans la page comme dans <img>). Des tracés n'ont besoin
d'aucune police, s'animent partout, et rendent pareil sur toutes les machines — y
compris le japonais, qu'une machine sans police CJK afficherait en cases.

Polices (toutes sous SIL Open Font License, licences dans assets/fonts/) :
  - Big Shoulders Display Black : le titre, comme les titres du site du studio.
  - Noto Sans JP Bold (sous-ensemble de 9 glyphes) : la légende katakana et le filigrane.

Lancé UNE fois, ou quand un texte, une taille ou un interlettrage change. Le résultat,
assets/glyphs.json, est lu par build_banner.py : l'action quotidienne n'a donc besoin
ni de fontTools ni des polices.

Usage : python3 tools/outline_title.py   (depuis la racine du dépôt)
Dépendances : pip install fonttools brotli
"""
from __future__ import annotations

import json
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

RACINE = Path(__file__).resolve().parent.parent
FONTS = RACINE / "assets" / "fonts"
OUT = RACINE / "assets" / "glyphs.json"

# nom, police, texte, taille en px, interlettrage en px
ITEMS = [
    ("title", "bigshoulders-900.woff2", "MJNEUROART", 128, 4),
    ("caption", "notosansjp-700-subset.woff2", "ニューロアート", 15, 5),
    ("mark", "notosansjp-700-subset.woff2", "電脳", 190, 14),
]


def outline(font_file: Path, text: str, size: float, spacing: float) -> tuple[float, str]:
    font = TTFont(str(font_file))
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    k = size / font["head"].unitsPerEm
    x = 0.0
    parts = []
    for ch in text:
        glyph = glyphs[cmap[ord(ch)]]
        pen = SVGPathPen(glyphs, ntos=lambda v: f"{v:.1f}")
        glyph.draw(TransformPen(pen, (k, 0, 0, -k, x, 0)))   # y de la police vers le haut → y SVG vers le bas
        parts.append(pen.getCommands())
        x += glyph.width * k + spacing
    return x - spacing, " ".join(parts)


def main() -> int:
    out = {}
    for name, font_file, text, size, spacing in ITEMS:
        width, d = outline(FONTS / font_file, text, size, spacing)
        out[name] = {"text": text, "font": font_file, "size": size, "width": round(width, 1), "d": d}
        print(f"{name:8s} {text!r:18s} {len(text)} glyphes, {width:.0f}px de large, {len(d)} car. de tracé")
    OUT.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print(f"{OUT.name} écrit, {OUT.stat().st_size} o")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
