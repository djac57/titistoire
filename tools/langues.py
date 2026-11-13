#!/usr/bin/env python3
"""Histoires traduites : langues/<langue>/*.txt -> langues/<langue>/histoires.js (chargé par index.html).

    === <id de l'histoire française>
    titre: ...
    une ligne = une page ; une ligne vide = tableau suivant (même découpage que l'histoire française : vérifié ici)

    python3 tools/langues.py            vérifie et écrit les fichiers de toutes les langues
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import titi

ROOT = titi.ROOT


def load(langue):
    """-> {id: {"t": titre, "sc": [[pages] par tableau]}}"""
    out = {}; cur = None
    for f in sorted((ROOT / "langues" / langue).glob("*.txt")):
        for raw in f.read_text(encoding="utf-8").split("\n"):
            l = raw.strip()
            if l.startswith("#"): continue
            if l.startswith("==="): cur = out.setdefault(l.strip("= ").strip(), {"t": "", "sc": [[]]}); continue
            if cur is None: continue
            if l.startswith("titre:") and not any(cur["sc"]): cur["t"] = l[6:].strip(); continue
            if not l:
                if cur["sc"][-1]: cur["sc"].append([])
                continue
            cur["sc"][-1].append(l)
    for s in out.values(): s["sc"] = [t for t in s["sc"] if t]
    return out


if __name__ == "__main__":
    fr = {s["id"]: [len(sc["pages"]) for sc in s["scenes"]] for s in titi.load()}; pb = 0
    for d in sorted(p for p in (ROOT / "langues").iterdir() if p.is_dir()):
        T = load(d.name)
        for sid, s in T.items():
            forme = [len(t) for t in s["sc"]]
            if sid not in fr: print(f"⚠️  {d.name}/{sid} : histoire inconnue"); pb += 1
            elif forme != fr[sid]: print(f"⚠️  {d.name}/{sid} : découpage {forme} au lieu de {fr[sid]}"); pb += 1
            if not s["t"]: print(f"⚠️  {d.name}/{sid} : titre manquant"); pb += 1
        if pb: continue
        (d / "histoires.js").write_text("/* Généré par tools/langues.py — ne pas modifier à la main. */\nwindow.TITI_LANGUES=window.TITI_LANGUES||{};window.TITI_LANGUES[" + json.dumps(d.name) + "]="
                                        + json.dumps(T, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
        print(f"✅ {d.name} : {len(T)} histoire(s), {sum(len(p.split()) for s in T.values() for t in s['sc'] for p in t)} mots")
    sys.exit(1 if pb else 0)
