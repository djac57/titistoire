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
# LE TEXTE PUBLIÉ SUIT LA VOIX, histoire par histoire. Tant que la voix par défaut n'a pas enregistré le nouveau texte d'une histoire,
# on garde l'ancien texte publié (celui que lit l'enregistrement existant) : sinon l'histoire perdrait sa voix d'un coup.
import re, zlib
def _sig(pages): x = "\n".join(pages); return f"{len(x)}:{zlib.crc32(x.encode('utf-8'))}"
_anc = {}
try:
    _t = (titi.ROOT / "stories.js").read_text(encoding="utf-8"); _anc = json.loads(_t[_t.index("window.TITI_STORIES=") + 20:].rstrip().rstrip(";"))
except Exception: pass
_voix0 = (titi.ROOT / "assets" / "voix" / "voix.txt").read_text().split()[0]
gardes = []
for sid in list(data):
    fv = titi.ROOT / "assets" / "voix" / _voix0 / f"{sid}.json"
    if not fv.exists() or sid not in _anc: continue
    sigs = {k: m.get("sig") for k, m in json.loads(fv.read_text(encoding="utf-8")).get("sc", {}).items() if m}
    lu = lambda sc: sum(1 for k, pages in enumerate(sc, 1) if sigs.get(str(k)) == _sig(pages))
    if lu(data[sid]["sc"]) < len(data[sid]["sc"]) and lu(_anc[sid]["sc"]) > lu(data[sid]["sc"]):
        for c in ("t", "sc", "im"): data[sid][c] = _anc[sid].get(c, data[sid][c])
        gardes.append(sid)
if gardes: print(f"⏳ {len(gardes)} histoire(s) gardent leur ancien texte en attendant leur nouvelle voix")
petits = {s["id"]: [sc["pages"][0] for sc in s["scenes"]] for s in titi.load_petits()}      # "p" : version Lucioles (1-3 ans), une ligne par tableau
for sid, lignes in petits.items():
    if sid in data: data[sid]["p"] = lignes
out = titi.ROOT / "stories.js"
out.write_text("/* Généré par tools/build_stories.py depuis histoires/*.txt — ne pas modifier à la main. */\n"
               "window.TITI_STORIES=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
pages = sum(len(sc["pages"]) for s in stories for sc in s["scenes"])
chars = sum(len(p) for s in stories for sc in s["scenes"] for p in sc["pages"])
print(f"✅ {len(stories)} histoires, {sum(len(s['scenes']) for s in stories)} tableaux, {pages} pages, {chars} caractères, {sum(1 for d in data.values() if "p" in d)} versions Lucioles -> {out.name}")
