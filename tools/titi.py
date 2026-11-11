#!/usr/bin/env python3
"""Lecture des histoires de Titistoire (source unique : histoires/*.txt + personnages.json).

Format d'un fichier d'histoires :
    === <heros>_<univers>        ouvre une histoire
    titre: ...  theme: ...  sujet: ...  famille: oser|coeur|autres|grandir
    @ <description de l'illustration, en anglais>   ouvre un tableau (= 1 piste audio) ; image de sa 1re page
    > <description, en anglais>  image propre à la page qui SUIT (pages 2 et 3 du tableau) ; facultatif
    <texte>                      chaque ligne = 1 page lue à voix haute
    # ...                        commentaire

Dans les lignes « @ », {nom} est remplacé par la description du personnage
(pour un héros : avec le costume de l'univers ; {nom-} = sans costume).
"""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "histoires"
FAMILLES = ("oser", "coeur", "autres", "grandir")


def cast():
    return json.loads((SRC / "personnages.json").read_text(encoding="utf-8"))


def expand(prompt, univ, c):
    def rep(m):
        name = m.group(1)
        bare = name.endswith("-")
        name = name.rstrip("-")
        if name in c["heros"]:
            d = c["heros"][name]
            cos = "" if bare else c["costumes"].get(univ, "")
            return d + (", " + cos if cos else "")
        if name in c["seconds"]:
            return c["seconds"][name]
        raise KeyError(f"personnage inconnu : {{{name}}}")
    return re.sub(r"\{([a-z_]+-?)\}", rep, prompt)


def load():
    """-> liste d'histoires {id, hero, univ, titre, theme, sujet, famille, scenes:[{prompt, pages:[...]}]}"""
    c = cast()
    stories, cur = [], None
    for f in sorted(SRC.glob("*.txt")):
        for n, raw in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            where = f"{f.name}:{n}"
            if line.startswith("==="):
                sid = line.strip("= ").strip()
                hero, _, univ = sid.partition("_")
                if hero not in c["heros"] or univ not in c["costumes"]:
                    raise ValueError(f"{where} : identifiant inconnu « {sid} »")
                cur = {"id": sid, "hero": hero, "univ": univ, "titre": "", "theme": "", "sujet": "", "famille": "", "scenes": []}
                stories.append(cur)
            elif cur is None:
                raise ValueError(f"{where} : texte avant la première histoire")
            elif line.startswith("@"):
                try:
                    p = expand(line[1:].strip(), cur["univ"], c)
                except KeyError as e:
                    raise ValueError(f"{where} : {e.args[0]}")
                cur["scenes"].append({"prompt": c["style"] + p + "." + c["fin"], "desc": p, "pages": [], "imgs": [], "_att": None})
            elif line.startswith(">"):
                if not cur["scenes"]:
                    raise ValueError(f"{where} : « > » avant le premier tableau")
                try:
                    cur["scenes"][-1]["_att"] = expand(line[1:].strip(), cur["univ"], c)
                except KeyError as e:
                    raise ValueError(f"{where} : {e.args[0]}")
            elif not cur["scenes"] and re.match(r"^(titre|theme|sujet|famille):", line):
                k, _, v = line.partition(":")
                cur[k] = v.strip()
            else:
                if not cur["scenes"]:
                    raise ValueError(f"{where} : page avant le premier tableau « @ »")
                sc = cur["scenes"][-1]
                sc["pages"].append(line)
                d = sc["_att"]; sc["_att"] = None            # image propre à cette page (None = celle du tableau)
                sc["imgs"].append({"prompt": c["style"] + d + "." + c["fin"], "desc": d} if d else None)
    ids = [s["id"] for s in stories]
    if len(ids) != len(set(ids)):
        raise ValueError("identifiant d'histoire en double")
    return stories


def check(stories):
    """Renvoie la liste des anomalies (vide = tout va bien)."""
    pb = []
    for s in stories:
        if not s["titre"] or not s["sujet"]:
            pb.append(f"{s['id']} : titre ou sujet manquant")
        if s["famille"] not in FAMILLES:
            pb.append(f"{s['id']} : famille « {s['famille']} » inconnue")
        if len(s["scenes"]) != 8:
            pb.append(f"{s['id']} : {len(s['scenes'])} tableaux (8 attendus)")
        for i, sc in enumerate(s["scenes"], 1):
            if not 2 <= len(sc["pages"]) <= 4:
                pb.append(f"{s['id']} tableau {i} : {len(sc['pages'])} pages")
            for p in sc["pages"]:
                if len(p) > 330:
                    pb.append(f"{s['id']} tableau {i} : page trop longue ({len(p)} car.)")
                if re.search(r"\bla morale\b|cette histoire (montre|apprend)", p, re.I):
                    pb.append(f"{s['id']} tableau {i} : morale énoncée")
            if len(sc["prompt"]) > 1450:
                pb.append(f"{s['id']} tableau {i} : description d'image trop longue")
    return pb
