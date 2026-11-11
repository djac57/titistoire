#!/usr/bin/env python3
"""Illustrations avec FLUX.2 et IMAGES DE RÉFÉRENCE (cohérence des personnages).

1. Une « fiche » par personnage : assets/refs/<jeton>[_<univers>].jpg (le personnage seul, sur fond blanc).
2. Chaque scène est dessinée en fournissant au modèle les fiches des personnages qu'elle contient (4 au plus).

    python3 tools/gen_images2.py --only plume_espace [--sortie assets/scenes2] [--modele @cf/black-forest-labs/flux-2-klein-4b]

Nécessite CF_ACCOUNT_ID + CF_API_TOKEN (API Cloudflare Workers AI) : tourne dans l'action GitHub.
"""
import argparse, base64, io, json, os, pathlib, re, sys, time, urllib.error, urllib.request, uuid
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import titi
from PIL import Image

ACC, TOK = os.environ.get("CF_ACCOUNT_ID", "").strip(), os.environ.get("CF_API_TOKEN", "").strip()
REFS = titi.ROOT / "assets" / "refs"


def appel(modele, champs, fichiers):
    """POST multipart -> octets de l'image"""
    b = uuid.uuid4().hex; corps = io.BytesIO()
    for k, v in champs.items():
        corps.write(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    for k, data in fichiers.items():
        corps.write(f'--{b}\r\nContent-Disposition: form-data; name="{k}"; filename="{k}.jpg"\r\nContent-Type: image/jpeg\r\n\r\n'.encode()); corps.write(data); corps.write(b"\r\n")
    corps.write(f"--{b}--\r\n".encode())
    req = urllib.request.Request(f"https://api.cloudflare.com/client/v4/accounts/{ACC}/ai/run/{modele}", data=corps.getvalue(),
                                 headers={"Authorization": "Bearer " + TOK, "Content-Type": f"multipart/form-data; boundary={b}"})
    try:
        r = urllib.request.urlopen(req, timeout=240); raw = r.read(); ct = r.headers.get("content-type", "")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} {e.read().decode('utf-8', 'replace')[:400]}")
    if "json" in ct:
        d = json.loads(raw); im = (d.get("result") or {}).get("image")
        if not im: raise RuntimeError("pas d'image : " + json.dumps(d)[:300])
        return base64.b64decode(im)
    return raw


def jpeg(data, cote, q=84):
    im = Image.open(io.BytesIO(data)).convert("RGB")
    if max(im.size) > cote: im = im.resize((cote, cote * im.size[1] // im.size[0]), Image.LANCZOS)
    o = io.BytesIO(); im.save(o, "JPEG", quality=q, optimize=True, progressive=True); return o.getvalue()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=""); ap.add_argument("--sortie", default="assets/scenes2")
    ap.add_argument("--tout", action="store_true", help="redessiner même les images déjà présentes")
    ap.add_argument("--refaire", default="", help="fichier listant les images à redessiner (une par ligne, ex. filou_pirates_3b), ou liste séparée par des virgules")
    ap.add_argument("--fiches", action="store_true", help="ne dessiner que les fiches de personnages de toutes les histoires")
    ap.add_argument("--modele", default="@cf/black-forest-labs/flux-2-klein-4b"); ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    if not (ACC and TOK): sys.exit("CF_ACCOUNT_ID + CF_API_TOKEN requis")
    c = titi.cast(); out = titi.ROOT / a.sortie; out.mkdir(parents=True, exist_ok=True); REFS.mkdir(parents=True, exist_ok=True)
    style = c["style"]; t0 = time.time(); n = 0

    def fiche(jeton, univ):
        """jeton tel qu'écrit dans le texte (ex. 'plume', 'plume-', 'zig') -> (octets de la fiche, nom court)"""
        nu = jeton.rstrip("-"); heros = nu in c["heros"]
        cos = c["costumes"].get(univ, "") if heros and not jeton.endswith("-") else ""
        desc = (c["heros"][nu] if heros else c["seconds"][nu]) + (", " + cos if cos else "")
        f = REFS / (nu + ("_" + univ if cos else "") + ".jpg")
        if not f.exists():
            p = style + "Character reference sheet of one single character: " + desc + ". Full body, standing, facing slightly left, friendly expression, centred on a plain white background, nothing else in the picture."
            f.write_bytes(jpeg(appel(a.modele, {"prompt": p, "width": "1024", "height": "1024"}, {}), 512))
            print(f"  📇 fiche {f.name}", flush=True)
        court = desc.split(",")[0].replace("the only fox in the picture", "").strip()
        return f.read_bytes(), court

    cible = set()
    if a.refaire:
        f = pathlib.Path(a.refaire)
        cible = {x.strip() for x in (f.read_text().replace(",", "\n").split("\n") if f.exists() else a.refaire.split(",")) if x.strip()}
    for s in titi.load():
        if not a.fiches and a.only and not any(s["id"].startswith(x.strip()) for x in a.only.split(",") if x.strip()): continue
        # on relit le fichier source pour retrouver les jetons de chaque ligne d'image (titi.load les a déjà développés)
        brut = {}; sid = None; sc = pg = 0
        for f in sorted(titi.SRC.glob("*.txt")):
            for line in f.read_text(encoding="utf-8").split("\n"):
                l = line.strip()
                if l.startswith("==="): sid = l.strip("= ").strip(); sc = pg = 0
                elif l.startswith("@"): sc += 1; pg = 0; brut[f"{sid}_{sc}"] = l[1:].strip()
                elif l.startswith(">"): brut[f"{sid}_{sc}" + "abcdef"[pg]] = l[1:].strip()
                elif l and not l.startswith("#") and sc and not re.match(r"^(titre|theme|sujet|famille):", l): pg += 1
        for nom, ligne in brut.items():
            if not nom.startswith(s["id"] + "_"): continue
            dest = out / f"{nom}.jpg"
            if a.fiches:
                for m in re.finditer(r"\{([a-z_]+-?)\}", ligne):
                    if m.group(1).rstrip("-") in {**c["heros"], **c["seconds"]}: fiche(m.group(1), s["univ"])
                continue
            if cible and nom not in cible: continue
            if dest.exists() and not a.tout and not cible: continue
            if a.limit and n >= a.limit: break
            jetons = []
            for m in re.finditer(r"\{([a-z_]+-?)\}", ligne):
                if m.group(1) not in jetons and m.group(1).rstrip("-") in {**c["heros"], **c["seconds"]}: jetons.append(m.group(1))
            jetons = jetons[:4]; fichiers = {}; texte = ligne
            for k, j in enumerate(jetons):
                data, court = fiche(j, s["univ"]); fichiers[f"input_image_{k}"] = data
                texte = texte.replace("{" + j + "}", f"{court} (exactly the character shown in image {k + 1})")
            texte = titi.expand(texte, s["univ"], c)        # jetons restants (au-delà de 4) : description en clair
            p = style + texte + ". Full detailed background scene filling the whole picture, never a plain white background. Draw only the characters described here, each one exactly once, as separate individuals that do not blend into each other; do not add any extra animal, creature or person." + c["fin"] + (" Keep every referenced character identical to its reference image: same species, same colours, same shape." if jetons else "")
            try:
                data = None
                for essai in range(3):                      # le filtre du modèle bloque parfois une image au hasard : on retente
                    try: data = appel(a.modele, {"prompt": p, "width": "1024", "height": "1024"}, fichiers); break
                    except Exception as e:
                        if "flagged" not in str(e) or essai == 2: raise
                dest.write_bytes(jpeg(data, 832)); n += 1
                print(f"  ✅ {dest.name} ({len(jetons)} référence(s))", flush=True)
            except Exception as e:
                print(f"  ❌ {nom} : {str(e)[:300]}", flush=True)
                if "HTTP 4" in str(e) and n == 0: sys.exit(1)       # erreur de format dès la 1re image : inutile d'insister
    print(f"{n} image(s) en {time.time() - t0:.0f} s avec {a.modele}")


if __name__ == "__main__":
    main()
