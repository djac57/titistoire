#!/usr/bin/env python3
"""Essai d'images pour un NOUVEAU recueil, avant d'écrire les histoires : fiches de personnages puis quelques scènes d'après ces fiches.

    python3 tools/pilote_images.py cometes/pilote.json

Le fichier JSON donne : "style", "sortie" (dossier), "personnages" {id: description anglaise}, "scenes" {nom: texte avec des {id}},
et éventuellement "modele_fiches" / "modele_scenes". Nécessite CF_ACCOUNT_ID et CF_API_TOKEN.
"""
import json, pathlib, re, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import gen_images2 as g

def essais(modele, champs, fichiers, n=5):
    err = None
    for k in range(n):
        try: return g.appel(modele, champs, fichiers)
        except Exception as e:
            err = e; print(f"   …essai {k + 1} : {str(e)[:110]}", flush=True); time.sleep(3)
    raise err

def main():
    spec = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    racine = pathlib.Path(__file__).resolve().parent.parent
    out = racine / spec["sortie"]; (out / "fiches").mkdir(parents=True, exist_ok=True)
    style = spec["style"]; P = spec["personnages"]
    mf = spec.get("modele_fiches", "@cf/black-forest-labs/flux-2-dev"); ms = spec.get("modele_scenes", "@cf/black-forest-labs/flux-2-klein-9b")
    fiches = {}
    for pid, desc in P.items():
        f = out / "fiches" / f"{pid}.jpg"
        if not f.exists():
            p = style + "Character reference sheet of one single character: " + desc + ". Full body, standing, facing slightly left, friendly expression, centred on a plain white background, nothing else in the picture."
            try: f.write_bytes(g.jpeg(essais(mf, {"prompt": p, "width": "1024", "height": "1024"}, {}), 512)); print("📇", f.name, flush=True)
            except Exception as e: print("❌ fiche", pid, str(e)[:200], flush=True); continue
        fiches[pid] = f.read_bytes()
    for nom, texte in spec["scenes"].items():
        dest = out / f"{nom}.jpg"
        if dest.exists(): continue
        jetons = [j for j in dict.fromkeys(re.findall(r"\{([a-z_]+)\}", texte)) if j in fiches][:4]
        fichiers = {}
        for k, j in enumerate(jetons):
            fichiers[f"input_image_{k}"] = fiches[j]
            texte = texte.replace("{" + j + "}", f"{re.sub(r'^one ', '', P[j])} (exactly the character shown in image {k + 1}, with the same clothes and accessories)", 1).replace("{" + j + "}", "the same character")
        p = style + texte + ". Full detailed background scene filling the whole picture, never a plain white background. Draw only the characters described here, each one exactly once, as separate individuals that do not blend into each other; do not add any extra person, animal or creature. Keep every referenced character identical to its reference image: same face, same hair, same colours, same clothes."
        try: dest.write_bytes(g.jpeg(essais(ms, {"prompt": p, "width": "1024", "height": "1024"}, fichiers), 832)); print("✅", dest.name, f"({len(jetons)} référence(s))", flush=True)
        except Exception as e: print("❌", nom, str(e)[:200], flush=True)

if __name__ == "__main__":
    main()
