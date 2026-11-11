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

# "im" : pour chaque tableau, les pages (à partir de la 2e) qui ont leur propre illustration, ex. "bc"
data = {s["id"]: {"t": s["titre"], "s": s["sujet"], "f": s["famille"], "sc": [sc["pages"] for sc in s["scenes"]],
                  "im": ["".join("abcdef"[k] for k, im in enumerate(sc["imgs"]) if k and im) for sc in s["scenes"]]} for s in stories}
petits = {s["id"]: [sc["pages"][0] for sc in s["scenes"]] for s in titi.load_petits()}      # "p" : version Lucioles (1-3 ans), une ligne par tableau
for sid, lignes in petits.items():
    if sid in data: data[sid]["p"] = lignes
out = titi.ROOT / "stories.js"
out.write_text("/* Généré par tools/build_stories.py depuis histoires/*.txt — ne pas modifier à la main. */\n"
               "window.TITI_STORIES=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
pages = sum(len(sc["pages"]) for s in stories for sc in s["scenes"])
chars = sum(len(p) for s in stories for sc in s["scenes"] for p in sc["pages"])
print(f"✅ {len(stories)} histoires, {sum(len(s['scenes']) for s in stories)} tableaux, {pages} pages, {chars} caractères, {sum(1 for d in data.values() if "p" in d)} versions Lucioles -> {out.name}")
