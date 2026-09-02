#!/usr/bin/env python3
"""
build_banner.py — génère banner.svg (sombre) et banner-light.svg (clair) du profil GitHub.

L'image de Mike (assets/face.jpg, sa création Midjourney) est incorporée en base64 :
un SVG affiché par GitHub dans une balise <img> ne peut charger aucun fichier externe,
donc l'image doit vivre DANS le SVG. Les animations SMIL, elles, passent.

Le titre, la légende katakana et le filigrane sont des TRACÉS (assets/glyphs.json,
produits une fois par tools/outline_title.py) : une police incorporée en <style> gèle
la timeline SMIL de Chromium, des tracés non. Ce script n'a donc aucune dépendance.

Lancé chaque jour par .github/workflows/uplink.yml : la ligne « uplink » du HUD porte
le compteur de jours depuis l'ouverture du compte GitHub (17/11/2023, donnée réelle de
l'API) et la date du jour. Rien d'autre ne change d'un jour à l'autre.

Usage : python3 tools/build_banner.py   (depuis la racine du dépôt)
"""
from __future__ import annotations

import base64
import datetime as dt
import json
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
FACE = RACINE / "assets" / "face.jpg"
GLYPHS = RACINE / "assets" / "glyphs.json"
EPOCH = dt.date(2023, 11, 17)  # création du compte mjneuroart sur GitHub (API get_me)

# Palette tirée de l'image : noir, indigo, violet, or, corail, éclats blancs.
DARK = dict(
    bg="#050508", ink="#f4f2ff", muted="#8d8aa8", readout="#c9c4e6",
    indigo="#4c5ee0", violet="#7b5fd6", gold="#e8a94e", coral="#e0564b", spark="#f4f2ff",
    stripe="#0a0a12",
)
LIGHT = dict(
    bg="#f7f6fb", ink="#0b0b12", muted="#5a5878", readout="#3b3a58",
    indigo="#3546c8", violet="#6a4ec4", gold="#c98a2c", coral="#c8453b", spark="#0b0b12",
    stripe="#f7f6fb",
)

MONO = "'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1200" height="420" viewBox="0 0 1200 420" role="img" aria-label="mjneuroart. MJ, neuro, art. Paris. Generative since 2022.">
  <defs>
    <linearGradient id="feather" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset="0.34" stop-color="#fff" stop-opacity="1"/>
      <stop offset="1" stop-color="#fff" stop-opacity="1"/>
    </linearGradient>
    <mask id="mface"><rect x="505" y="0" width="695" height="420" fill="url(#feather)"/></mask>
    <linearGradient id="streakA" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{indigo}" stop-opacity="0"/><stop offset="0.5" stop-color="{indigo}" stop-opacity="0.9"/><stop offset="1" stop-color="{violet}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="streakB" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{gold}" stop-opacity="0"/><stop offset="0.5" stop-color="{gold}" stop-opacity="0.9"/><stop offset="1" stop-color="{coral}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="streakC" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{spark}" stop-opacity="0"/><stop offset="0.5" stop-color="{spark}" stop-opacity="0.7"/><stop offset="1" stop-color="{spark}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="bar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{spark}" stop-opacity="0"/><stop offset="0.5" stop-color="{spark}" stop-opacity="0.08"/><stop offset="1" stop-color="{spark}" stop-opacity="0"/>
    </linearGradient>
    <pattern id="scan" width="3" height="3" patternUnits="userSpaceOnUse"><rect width="3" height="1.5" fill="#000" fill-opacity="0.10"/></pattern>
    <pattern id="hz" width="16" height="8" patternUnits="userSpaceOnUse" patternTransform="skewX(-45)"><rect width="8" height="8" fill="{gold}"/></pattern>
    <filter id="glow" x="-10%" y="-40%" width="120%" height="180%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
    <!-- typography as outlines: Big Shoulders Display Black (title), Noto Sans JP Bold (caption, mark). SIL OFL. -->
    <path id="ttl" d="{title_d}"/>
    <path id="cap" d="{caption_d}"/>
    <path id="mark" d="{mark_d}"/>
    <clipPath id="s1"><rect x="0" y="0" width="1200" height="128"/></clipPath>
    <clipPath id="s2"><rect x="0" y="128" width="1200" height="18"/></clipPath>
    <clipPath id="s3"><rect x="0" y="146" width="1200" height="18"/></clipPath>
    <clipPath id="s4"><rect x="0" y="164" width="1200" height="18"/></clipPath>
    <clipPath id="s5"><rect x="0" y="182" width="1200" height="78"/></clipPath>
    <clipPath id="hzclip"><rect x="58" y="386" width="360" height="7"/></clipPath>
  </defs>

  <rect width="1200" height="420" fill="{bg}"/>

  <!-- the art: face band, feathered into the background on its left edge -->
  <image x="505" y="0" width="695" height="420" preserveAspectRatio="xMidYMid slice" mask="url(#mface)" xlink:href="data:image/jpeg;base64,{face}"/>

  <!-- kanji watermark, cyberbrain, behind everything on the left -->
  <use xlink:href="#mark" x="250" y="388" fill="{indigo}" fill-opacity="0.07"/>

  <!-- data streaks, echo of the holographic bands in the art -->
  <g>
    <rect x="-300" y="96" width="420" height="3" fill="url(#streakA)"><animate attributeName="x" values="-300;760" dur="9s" repeatCount="indefinite"/></rect>
    <rect x="-200" y="142" width="260" height="2" fill="url(#streakB)"><animate attributeName="x" values="-200;760" dur="6.5s" repeatCount="indefinite"/></rect>
    <rect x="-400" y="168" width="520" height="5" fill="url(#streakA)" opacity="0.55"><animate attributeName="x" values="-400;760" dur="12s" repeatCount="indefinite"/></rect>
    <rect x="-160" y="214" width="200" height="1.5" fill="url(#streakC)"><animate attributeName="x" values="-160;760" dur="5s" repeatCount="indefinite"/></rect>
    <rect x="-320" y="262" width="380" height="3" fill="url(#streakB)" opacity="0.8"><animate attributeName="x" values="-320;760" dur="10.5s" repeatCount="indefinite"/></rect>
    <rect x="-240" y="286" width="300" height="2" fill="url(#streakA)"><animate attributeName="x" values="-240;760" dur="7.8s" repeatCount="indefinite"/></rect>
    <rect x="-360" y="330" width="440" height="4" fill="url(#streakB)" opacity="0.5"><animate attributeName="x" values="-360;760" dur="13.5s" repeatCount="indefinite"/></rect>
    <rect x="-180" y="386" width="220" height="1.5" fill="url(#streakC)"><animate attributeName="x" values="-180;760" dur="6s" repeatCount="indefinite"/></rect>
  </g>

  <!-- frame line with travelling dashes, corner brackets, top ruler -->
  <rect x="14" y="14" width="1172" height="392" fill="none" stroke="{gold}" stroke-opacity="0.32" stroke-width="1" stroke-dasharray="160 48">
    <animate attributeName="stroke-dashoffset" from="0" to="-208" dur="7s" repeatCount="indefinite"/>
  </rect>
  <g fill="none" stroke="{indigo}" stroke-width="2">
    <path d="M22 44V22H44"/><path d="M1178 44V22H1156"/><path d="M22 376V398H44"/><path d="M1178 376V398H1156"/>
    <animate attributeName="stroke-opacity" values="1;0.35;1;1;1" dur="3s" repeatCount="indefinite"/>
  </g>
  <g stroke="{muted}" stroke-opacity="0.55" stroke-width="1">{ruler}</g>

  <!-- edge labels, rotated like a print margin -->
  <g font-family="{mono}" font-size="10" letter-spacing="4" fill="{muted}">
    <text transform="translate(37 330) rotate(-90)">NEURAL LINK // EST. 2022 // PARIS</text>
    <text transform="translate(1170 90) rotate(90)">MJ // NEURO // ART</text>
  </g>
  <g font-family="{mono}" font-size="11" letter-spacing="3.5" fill="{muted}">
    <text x="58" y="36">MJ // NEURO // ART</text>
    <text x="58" y="54">EST. 2022 · PARIS</text>
  </g>

  <!-- katakana caption, outlined -->
  <use xlink:href="#cap" x="60" y="82" fill="{muted}"/>
  <text x="{caption_end}" y="82" font-family="{mono}" font-size="11" letter-spacing="4" fill="{muted}">// NEURO ART</text>

  <!-- title: Big Shoulders Black outlines, sliced glitch bands, indigo and gold splits -->
  <g>
    <use xlink:href="#ttl" x="51" y="200" fill="{indigo}" fill-opacity="0.9">
      <animate attributeName="x" calcMode="discrete" values="51;51;43;51;57;51;51;46;51;51" dur="2.6s" repeatCount="indefinite"/>
      <animate attributeName="fill-opacity" calcMode="discrete" values="0.9;0.35;0.9;0.9;0.2;0.9;0.6;0.9;0.9;0.3" dur="2.6s" repeatCount="indefinite"/>
    </use>
    <use xlink:href="#ttl" x="65" y="200" fill="{gold}" fill-opacity="0.85">
      <animate attributeName="x" calcMode="discrete" values="65;65;73;65;59;65;65;70;65;65" dur="2.6s" repeatCount="indefinite"/>
      <animate attributeName="fill-opacity" calcMode="discrete" values="0.85;0.85;0.3;0.85;0.85;0.2;0.85;0.5;0.85;0.85" dur="2.6s" repeatCount="indefinite"/>
    </use>
    <g clip-path="url(#s1)"><use xlink:href="#ttl" x="58" y="200" fill="{ink}"/>
      <animateTransform attributeName="transform" type="translate" calcMode="discrete" values="0 0;0 0;0 0;-10 0;0 0;0 0;0 0;7 0;0 0" dur="3.1s" repeatCount="indefinite"/></g>
    <g clip-path="url(#s2)"><use xlink:href="#ttl" x="58" y="200" fill="{ink}"/>
      <animateTransform attributeName="transform" type="translate" calcMode="discrete" values="0 0;16 0;0 0;0 0;-12 0;0 0;0 0;0 0;6 0;0 0" dur="2.3s" repeatCount="indefinite"/></g>
    <g clip-path="url(#s3)"><use xlink:href="#ttl" x="58" y="200" fill="{ink}"/>
      <animateTransform attributeName="transform" type="translate" calcMode="discrete" values="0 0;0 0;-22 0;0 0;0 0;0 0;10 0;0 0;0 0;-5 0" dur="2.9s" repeatCount="indefinite"/></g>
    <g clip-path="url(#s4)"><use xlink:href="#ttl" x="58" y="200" fill="{ink}"/>
      <animateTransform attributeName="transform" type="translate" calcMode="discrete" values="0 0;0 0;0 0;14 0;0 0;-8 0;0 0;0 0;0 0;0 0" dur="2.1s" repeatCount="indefinite"/></g>
    <g clip-path="url(#s5)"><use xlink:href="#ttl" x="58" y="200" fill="{ink}"/>
      <animateTransform attributeName="transform" type="translate" calcMode="discrete" values="0 0;0 0;0 0;0 0;-7 0;0 0;0 0;12 0;0 0;0 0" dur="3.5s" repeatCount="indefinite"/></g>
    <!-- corruption flashes: one band turns gold, another indigo, for a frame -->
    <g clip-path="url(#s3)"><use xlink:href="#ttl" x="58" y="200" fill="{gold}">
      <animate attributeName="opacity" calcMode="discrete" values="0;0;0;1;0;0;0;0;1;0;0;0" dur="3.7s" repeatCount="indefinite"/></use></g>
    <g clip-path="url(#s5)"><use xlink:href="#ttl" x="58" y="200" fill="{indigo}">
      <animate attributeName="opacity" calcMode="discrete" values="0;0;0;0;0;0;1;0;0;0;0;0;0" dur="4.3s" repeatCount="indefinite"/></use></g>
  </g>
  <rect x="58" y="212" width="0" height="3" fill="{gold}" filter="url(#glow)">
    <animate attributeName="width" values="0;{title_w};{title_w};0" keyTimes="0;0.4;0.8;1" dur="5s" repeatCount="indefinite"/>
  </rect>

  <!-- tagline, with a redaction sweep that strikes a word and lets it go -->
  <text x="58" y="246" font-family="{mono}" font-weight="700" font-size="15" letter-spacing="5" fill="{gold}">NEURAL TOOLS · ARTIST EYE · AGENTS</text>
  <rect x="58" y="240" width="0" height="2" fill="{coral}">
    <animate attributeName="width" calcMode="discrete" values="0;0;0;0;226;226;0;0;0;0" dur="8s" repeatCount="indefinite"/>
  </rect>

  <!-- iris lock on the eye -->
  <g fill="none" stroke="{gold}" stroke-width="1.5">
    <path d="M917 122V112H927"/><path d="M961 122V112H951"/><path d="M917 146V156H927"/><path d="M961 146V156H951"/>
    <animate attributeName="stroke-opacity" values="1;0.3;1" dur="1.8s" repeatCount="indefinite"/>
  </g>
  <circle cx="939" cy="134" r="22" fill="none" stroke="{indigo}" stroke-opacity="0.8" stroke-width="1" stroke-dasharray="3 6">
    <animateTransform attributeName="transform" type="rotate" from="0 939 134" to="360 939 134" dur="16s" repeatCount="indefinite"/>
  </circle>
  <text x="970" y="116" font-family="{mono}" font-size="10" letter-spacing="3" fill="{gold}">IRIS · SYNC</text>

  <!-- boot readout -->
  <g font-family="{mono}" font-size="13" letter-spacing="1.5" fill="{readout}">
    <text x="58" y="304">&gt; neural.link ........... OK<animate attributeName="opacity" values="0;0;1;1;1;1;0" keyTimes="0;0.05;0.1;0.9;0.95;0.98;1" dur="9s" repeatCount="indefinite"/></text>
    <text x="58" y="324">&gt; agents.spawn .......... READY<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.2;0.25;0.95;1" dur="9s" repeatCount="indefinite"/></text>
    <text x="58" y="344">&gt; uplink ................ DAY {days} · {today}<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.35;0.4;0.95;1" dur="9s" repeatCount="indefinite"/></text>
    <text x="58" y="364">&gt; status ................ ONLINE · PARIS<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.5;0.55;0.95;1" dur="9s" repeatCount="indefinite"/></text>
    <rect x="58" y="370" width="8" height="12" fill="{gold}"><animate attributeName="opacity" values="1;0;1" dur="0.9s" repeatCount="indefinite"/></rect>
  </g>

  <!-- hazard stripes, moving -->
  <g clip-path="url(#hzclip)"><rect x="26" y="386" width="440" height="7" fill="url(#hz)">
    <animateTransform attributeName="transform" type="translate" from="0 0" to="16 0" dur="0.8s" repeatCount="indefinite"/></rect></g>
  <text x="430" y="392" font-family="{mono}" font-size="9" letter-spacing="3" fill="{gold}">SYS·OK</text>

  <!-- barcode block and handle -->
  <g fill="{spark}" fill-opacity="0.8">{barcode}</g>
  <text x="1142" y="392" text-anchor="end" font-family="{mono}" font-size="12" letter-spacing="3" fill="{muted}">@mjneuroart</text>

  <!-- scan bar, grain, faint scanlines -->
  <rect x="0" y="-60" width="1200" height="60" fill="url(#bar)"><animate attributeName="y" values="-60;420" dur="6s" repeatCount="indefinite"/></rect>
  <rect width="1200" height="420" filter="url(#grain)" opacity="0.05"/>
  <rect width="1200" height="420" fill="url(#scan)"/>
</svg>
"""


def ruler() -> str:
    """Tick marks along the top edge, a tall one every 100 px."""
    out = []
    for x in range(60, 1141, 20):
        h = 8 if x % 100 == 0 else 4
        out.append(f'<line x1="{x}" y1="14" x2="{x}" y2="{14 + h}"/>')
    return "".join(out)


def barcode() -> str:
    """A deterministic barcode-like block at the bottom right (seeded, so the daily build is stable)."""
    widths = [3, 1, 2, 1, 1, 3, 2, 1, 1, 2, 3, 1, 2, 2, 1, 3, 1, 1, 2, 1, 3, 2, 1, 1, 2, 1, 3, 1, 2, 1]
    x, out = 1000, []
    for i, w in enumerate(widths):
        out.append(f'<rect x="{x}" y="352" width="{w}" height="18"/>')
        x += w + (2 if i % 3 else 3)
    return "".join(out)


def render(palette: dict, face_b64: str, glyphs: dict, days: int, today: str) -> str:
    out = TEMPLATE
    values = {
        **palette,
        "face": face_b64,
        "mono": MONO,
        "title_d": glyphs["title"]["d"], "title_w": str(glyphs["title"]["width"]),
        "caption_d": glyphs["caption"]["d"], "caption_end": str(round(60 + glyphs["caption"]["width"] + 14)),
        "mark_d": glyphs["mark"]["d"],
        "ruler": ruler(), "barcode": barcode(),
        "days": str(days), "today": today,
    }
    for k, v in values.items():
        out = out.replace("{" + k + "}", v)
    return out


def main() -> int:
    face_b64 = base64.b64encode(FACE.read_bytes()).decode("ascii")
    glyphs = json.loads(GLYPHS.read_text(encoding="utf-8"))
    today = dt.date.today()
    days = (today - EPOCH).days
    stamp = today.strftime("%Y-%m-%d")
    (RACINE / "banner.svg").write_text(render(DARK, face_b64, glyphs, days, stamp), encoding="utf-8")
    (RACINE / "banner-light.svg").write_text(render(LIGHT, face_b64, glyphs, days, stamp), encoding="utf-8")
    print(f"banner.svg + banner-light.svg écrits — day {days}, {stamp}, image {FACE.stat().st_size} o, titre {glyphs['title']['width']:.0f}px")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
