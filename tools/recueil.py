#!/usr/bin/env python3
"""Recueils « grands » (Les Comètes 6-8 ans, Les Galaxies 8-10 ans) : un dossier par recueil, bâti dans l'ordre
bible -> personnages.json -> histoires -> images.

    <recueil>/personnages.json   {"style": "...", "personnages": {id: description anglaise}, "lieux": {id: ...}, "objets": {id: ...}}
    <recueil>/histoires/*.txt    une ou plusieurs histoires par fichier :

        === c01
        titre: Le vélo sur le toit
        sous: septembre                      (sous-titre : mois, numéro d'épisode…)
        sujet: Être jaloux du nouveau        (facultatif)
        @ description de l'image du tableau, en anglais, avec des {id}     (facultatif : sans « @ », le tableau garde l'image précédente)
        une ligne = une page lue
        (ligne vide ou nouveau « @ » ou « -- » = tableau suivant)

Dans une description, {id} d'un personnage est dessiné d'après sa fiche (image de référence) ; {id} d'un lieu ou d'un objet est
remplacé par sa description fixe.

    python3 tools/recueil.py cometes            vérifie et écrit cometes/recueil.js (chargé par index.html)
    python3 tools/recueil.py cometes --images   dessine les fiches manquantes puis les scènes manquantes (CF_ACCOUNT_ID, CF_API_TOKEN)
                                 [--refaire a,b | fichier] [--sortie dossier] [--modele m] [--modele-fiches m] [--fiches]
"""
import argparse, json, pathlib, re, sys, time, zlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def cast(rec):
    return json.loads((ROOT / rec / "personnages.json").read_text(encoding="utf-8"))


def load(rec):
    """-> liste d'histoires {id, titre, sous, sujet, scenes: [{desc (ou None), pages: [...]}]}"""
    out = []; cur = None; neuf = True
    for f in sorted((ROOT / rec / "histoires").glob("*.txt")):
        for n, raw in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
            line = raw.strip()
            if line.startswith("#"): continue
            if line.startswith("==="):
                cur = {"id": line.strip("= ").strip(), "titre": "", "sous": "", "sujet": "", "scenes": []}; out.append(cur); neuf = True; continue
            if cur is None:
                if line: raise ValueError(f"{f.name}:{n} : texte avant la première histoire")
                continue
            if not line or line == "--": neuf = True; continue
            m = re.match(r"^(titre|sous|sujet):\s*(.*)$", line)
            if m and not cur["scenes"]: cur[m.group(1)] = m.group(2).strip(); continue
            if line.startswith("@"):
                cur["scenes"].append({"desc": line[1:].strip(), "pages": []}); neuf = False; continue
            if neuf or not cur["scenes"]:
                cur["scenes"].append({"desc": None, "pages": []}); neuf = False
            cur["scenes"][-1]["pages"].append(line)
    for s in out: s["scenes"] = [sc for sc in s["scenes"] if sc["pages"]]
    return out


def check(rec, stories, c):
    pb = []; connus = {**c.get("personnages", {}), **c.get("lieux", {}), **c.get("objets", {})}
    ids = [s["id"] for s in stories]
    if len(ids) != len(set(ids)): pb.append("identifiant d'histoire en double")
    for s in stories:
        if not s["titre"]: pb.append(f"{s['id']} : titre manquant")
        if not s["scenes"]: pb.append(f"{s['id']} : aucune page")
        if s["scenes"] and not s["scenes"][0]["desc"]: pb.append(f"{s['id']} : le premier tableau n'a pas d'image")
        for i, sc in enumerate(s["scenes"], 1):
            for p in sc["pages"]:
                if len(p) > 420: pb.append(f"{s['id']} tableau {i} : page trop longue ({len(p)} car.)")
                if re.search(r"\bla morale\b|cette histoire (montre|apprend)", p, re.I): pb.append(f"{s['id']} tableau {i} : morale énoncée")
            if sc["desc"]:
                js = re.findall(r"\{([a-z0-9_]+)\}", sc["desc"])
                for j in js:
                    if j not in connus: pb.append(f"{s['id']} tableau {i} : {{{j}}} inconnu")
                if len([j for j in dict.fromkeys(js) if j in c.get("personnages", {})]) > 3: pb.append(f"{s['id']} tableau {i} : plus de trois personnages dans l'image")
    return pb


def nom_image(s, i):
    """numéro du tableau qui porte l'image affichée au tableau i (le dernier « @ » rencontré)"""
    k = i
    while k > 1 and not s["scenes"][k - 1]["desc"]: k -= 1
    return k


def construire(rec):
    c = cast(rec); stories = load(rec); pb = check(rec, stories, c)
    for p in pb: print("⚠️ ", p)
    if pb: sys.exit(1)
    data = {s["id"]: {"t": s["titre"], "u": s["sous"], "s": s["sujet"], "sc": [sc["pages"] for sc in s["scenes"]],
                      "im": [nom_image(s, i) for i in range(1, len(s["scenes"]) + 1)]} for s in stories}
    out = ROOT / rec / "recueil.js"
    out.write_text(f"/* Généré par tools/recueil.py depuis {rec}/histoires — ne pas modifier à la main. */\n"
                   f"window.TITI_RECUEILS=window.TITI_RECUEILS||{{}};window.TITI_RECUEILS[{json.dumps(rec)}]=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    mots = sum(len(p.split()) for s in stories for sc in s["scenes"] for p in sc["pages"])
    print(f"✅ {rec} : {len(stories)} histoires, {sum(len(s['scenes']) for s in stories)} tableaux, {sum(1 for s in stories for sc in s['scenes'] if sc['desc'])} images, {mots} mots -> {out.relative_to(ROOT)}")
    return stories, c


def images(rec, a):
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import gen_images2 as g
    stories, c = construire(rec); P = c.get("personnages", {}); fixes = {**c.get("lieux", {}), **c.get("objets", {})}; style = c["style"]
    refs = ROOT / rec / "refs"; refs.mkdir(exist_ok=True); out = ROOT / (a.sortie or f"{rec}/scenes"); out.mkdir(parents=True, exist_ok=True)

    def essais(modele, champs, fichiers, n=6):
        err = None
        for k in range(n):
            try: return g.appel(modele, champs, fichiers)
            except Exception as e:
                err = e; time.sleep(2 + k)
        raise err

    cible = set()
    if a.refaire:
        f = pathlib.Path(a.refaire); cible = {x.strip() for x in (f.read_text() if f.exists() else a.refaire).replace(",", "\n").split("\n") if x.strip()}
    utiles = {j for s in stories for sc in s["scenes"] if sc["desc"] for j in re.findall(r"\{([a-z0-9_]+)\}", sc["desc"]) if j in P} if not a.fiches else set(P)
    fiche = {}
    for pid in sorted(utiles):
        f = refs / f"{pid}.jpg"
        if not f.exists():
            p = c.get("style_fiches", style) + "Character reference sheet of one single character: " + P[pid] + ". Full body, standing, facing slightly left, friendly expression, centred on a plain white background, nothing else in the picture."
            try: f.write_bytes(g.jpeg(essais(a.modele_fiches, {"prompt": p, "width": "1024", "height": "1024"}, {}), 512)); print("📇", f.name, flush=True)
            except Exception as e: print("❌ fiche", pid, str(e)[:160], flush=True); continue
        fiche[pid] = f.read_bytes()
    if a.fiches: return
    n = 0
    for s in stories:
        for i, sc in enumerate(s["scenes"], 1):
            if not sc["desc"]: continue
            nom = f"{s['id']}_{i}"; dest = out / f"{nom}.jpg"
            if cible and nom not in cible: continue
            if dest.exists() and not cible: continue
            texte = sc["desc"]; fichiers = {}; k = 0
            for j in dict.fromkeys(re.findall(r"\{([a-z0-9_]+)\}", texte)):
                if j in fiche and k < 4:
                    fichiers[f"input_image_{k}"] = fiche[j]; k += 1
                    texte = texte.replace("{" + j + "}", f"{re.sub(r'^one ', '', P[j])} (exactly the character shown in image {k}, with the same face, hair, clothes and accessories)", 1).replace("{" + j + "}", "the same character")
                elif j in P: texte = texte.replace("{" + j + "}", P[j])
                else: texte = texte.replace("{" + j + "}", fixes.get(j, j))
            p = style + texte + (". " if not texte.rstrip().endswith(".") else " ") + "Full detailed background scene filling the whole picture, never a plain white background. Draw only the characters described here, each one exactly once, as separate individuals that do not blend into each other; do not add any extra person, animal or creature." + (" Keep every referenced character identical to its reference image." if fichiers else "")
            try: dest.write_bytes(g.jpeg(essais(a.modele, {"prompt": p, "width": "1024", "height": "1024"}, fichiers), 960)); n += 1; print("✅", dest.name, f"({len(fichiers)} référence(s))", flush=True)
            except Exception as e: print("❌", nom, str(e)[:200], flush=True)
    print(f"{n} image(s) dessinée(s) avec {a.modele}")


def signature(pages):
    t = "\n".join(pages); return str(len(t)) + ":" + str(zlib.crc32(t.encode("utf-8")))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("recueil"); ap.add_argument("--images", action="store_true"); ap.add_argument("--fiches", action="store_true")
    ap.add_argument("--refaire", default=""); ap.add_argument("--sortie", default=""); ap.add_argument("--modele", default="@cf/black-forest-labs/flux-2-klein-9b")
    ap.add_argument("--modele-fiches", dest="modele_fiches", default="@cf/black-forest-labs/flux-2-dev")
    a = ap.parse_args()
    if a.images or a.fiches: images(a.recueil, a)
    else: construire(a.recueil)
