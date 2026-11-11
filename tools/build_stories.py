#!/usr/bin/env python3
"""histoires/*.txt  ->  stories.js (chargé par index.html). À relancer après toute retouche d'un texte.

    python3 tools/build_stories.py
"""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import titi

stories = titi.load()
pb = titi.check(stories)
for p in pb:
    print("⚠️ ", p)
if pb:
    sys.exit(1)

data = {s["id"]: {"t": s["titre"], "s": s["sujet"], "f": s["famille"], "sc": [sc["pages"] for sc in s["scenes"]]} for s in stories}
out = titi.ROOT / "stories.js"
out.write_text("/* Généré par tools/build_stories.py depuis histoires/*.txt — ne pas modifier à la main. */\n"
               "window.TITI_STORIES=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
pages = sum(len(sc["pages"]) for s in stories for sc in s["scenes"])
chars = sum(len(p) for s in stories for sc in s["scenes"] for p in sc["pages"])
print(f"✅ {len(stories)} histoires, {sum(len(s['scenes']) for s in stories)} tableaux, {pages} pages, {chars} caractères -> {out.name}")
