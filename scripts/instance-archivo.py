"""Pin the Archivo variable font to the one style the site uses.

The headings, menu and buttons all use Archivo semi-expanded (wdth 115) at
weight 650. Shipping the full variable font (wdth 62-125, wght 100-900) cost
~90 kB per subset, and the hero h1 waits on it for Largest Contentful Paint.

Run from the repo root:  pixi run python scripts/instance-archivo.py
Source files are the Fontsource variable woff2s (OFL-1.1), downloaded fresh.
"""
import io
import urllib.request
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

BASE = "https://cdn.jsdelivr.net/npm/@fontsource-variable/archivo/files/"
OUT = Path(__file__).resolve().parents[1] / "static/fonts"
AXES = {"wdth": 115, "wght": 650}

for subset in ("latin", "latin-ext"):
    name = f"archivo-{subset}-wdth-normal.woff2"
    data = urllib.request.urlopen(BASE + name).read()
    font = TTFont(io.BytesIO(data))
    static = instantiateVariableFont(font, AXES)
    static.flavor = "woff2"
    static.save(OUT / name)
    print(f"{name}: {len(data)} -> {(OUT / name).stat().st_size} bytes")
