#!/usr/bin/env python3
"""Imagiers des Lucioles (couleurs, nombres, formes, alphabet) : imagiers/histoires/*.txt, au format des recueils.

Le générateur d'images ne sait ni écrire ni compter. Il ne dessine donc que des objets seuls (imagiers/brut/) ;
ce script pose ensuite, à coup sûr, la lettre, la pastille de couleur ou la forme, et compose les pages des nombres
en répétant l'objet le bon nombre de fois (imagiers/scenes/).

    python3 tools/imagiers.py --brut [--refaire a,b]   dessine les objets manquants (CF_ACCOUNT_ID, CF_API_TOKEN)
    python3 tools/imagiers.py                          compose imagiers/scenes/ et écrit imagiers/recueil.js
Les pages avec un héros ({rosie}…) se dessinent d'après sa fiche :  python3 tools/recueil.py imagiers --images --sortie imagiers/brut
"""
import argparse, io, math, pathlib, sys, time
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import recueil

ROOT = recueil.ROOT; REC = "imagiers"; BRUT = ROOT / REC / "brut"; OUT = ROOT / REC / "scenes"; C = 960
ENCRE = (45, 42, 90); OR = (255, 190, 50)
COULEURS = [None, (229, 57, 53), (41, 121, 255), (255, 214, 0), (67, 160, 71), (251, 140, 0), (255, 128, 171), (142, 68, 173), (121, 85, 72), (33, 33, 33), (255, 255, 255)]
FORMES = [None, "rond", "carre", "triangle", "rectangle", "ovale", "etoile", "coeur", "losange"]
RANGS = {1: [1], 2: [2], 3: [3], 4: [2, 2], 5: [3, 2], 6: [3, 3], 7: [4, 3], 8: [4, 4], 9: [3, 3, 3], 10: [5, 5]}


def police(taille, graisse=b"SemiBold"):
    f = ImageFont.truetype(str(ROOT / "tools" / "Fredoka.ttf"), taille); f.set_variation_by_name(graisse); return f


def pastille(im, cote=230, marge=26):
    """carré blanc arrondi, en haut à gauche -> (dessin, x, y, cote)"""
    d = ImageDraw.Draw(im); d.rounded_rectangle([marge, marge, marge + cote, marge + cote], 48, fill=(255, 255, 255), outline=ENCRE, width=6)
    return d, marge, marge, cote


def forme(d, nom, x, y, c, plein, bord=8):
    a, b = x + c * 0.16, y + c * 0.16; e, f = x + c * 0.84, y + c * 0.84; mx, my = (a + e) / 2, (b + f) / 2
    if nom == "rond": d.ellipse([a, b, e, f], fill=plein, outline=ENCRE, width=bord)
    elif nom == "carre": d.rectangle([a, b, e, f], fill=plein, outline=ENCRE, width=bord)
    elif nom == "rectangle": d.rectangle([a - c * 0.04, b + c * 0.14, e + c * 0.04, f - c * 0.14], fill=plein, outline=ENCRE, width=bord)
    elif nom == "ovale": d.ellipse([a + c * 0.1, b - c * 0.03, e - c * 0.1, f + c * 0.03], fill=plein, outline=ENCRE, width=bord)
    else:
        if nom == "triangle": pts = [(mx, b), (e, f), (a, f)]
        elif nom == "losange": pts = [(mx, b - c * 0.03), (e - c * 0.08, my), (mx, f + c * 0.03), (a + c * 0.08, my)]
        elif nom == "etoile":
            r = (e - a) / 2 * 1.08; pts = [(mx + (r if k % 2 == 0 else r * 0.45) * math.sin(k * math.pi / 5), my + c * 0.03 - (r if k % 2 == 0 else r * 0.45) * math.cos(k * math.pi / 5)) for k in range(10)]
        else:                                               # cœur
            r = (e - a) / 2; pts = []
            for k in range(60):
                t = 2 * math.pi * k / 60; pts.append((mx + r * 16 * math.sin(t) ** 3 / 16, my - r * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) / 16))
        d.polygon(pts, fill=plein); d.line(pts + [pts[0]], fill=ENCRE, width=bord, joint="curve")


def composer(s, i, sc):
    src = BRUT / f"{s['id']}_{i}.jpg"
    if not src.exists(): return None
    im = Image.open(src).convert("RGB").resize((C, C), Image.LANCZOS); n = i - 1            # tableau 1 : la couverture, avec le héros
    if s["id"] == "alphabet" and 1 <= n <= 26:
        d, x, y, c = pastille(im, 250); L = chr(64 + n); f1 = police(170, b"Bold"); f2 = police(120)
        w1 = d.textlength(L, font=f1); w2 = d.textlength(L.lower(), font=f2)
        if w1 + w2 + 8 > c - 36:                             # lettres larges (M, W) : on réduit pour rester dans la pastille
            k = (c - 36) / (w1 + w2 + 8); f1 = police(int(170 * k), b"Bold"); f2 = police(int(120 * k)); w1 = d.textlength(L, font=f1); w2 = d.textlength(L.lower(), font=f2)
        x0 = x + (c - w1 - w2 - 8) / 2
        d.text((x0, y + c - 46), L, font=f1, fill=ENCRE, anchor="ls"); d.text((x0 + w1 + 8, y + c - 46), L.lower(), font=f2, fill=(230, 120, 30), anchor="ls")
    elif s["id"] == "couleurs" and 1 <= n < len(COULEURS):
        d, x, y, c = pastille(im, 200); d.ellipse([x + 26, y + 26, x + c - 26, y + c - 26], fill=COULEURS[n], outline=ENCRE, width=8)
    elif s["id"] == "formes" and 1 <= n < len(FORMES):
        d, x, y, c = pastille(im, 230); forme(d, FORMES[n], x, y, c, OR)
    elif s["id"] == "nombres" and 1 <= n <= 10:
        fond = Image.new("RGB", (C, C), (255, 244, 214)); d = ImageDraw.Draw(fond); haut = 250
        d.text((C / 2, haut / 2 + 14), str(n), font=police(250, b"Bold"), fill=(230, 120, 30), anchor="mm", stroke_width=8, stroke_fill=ENCRE)
        rangs = RANGS[n]; marge = 30; esp = 18; hz = C - haut - marge
        cote = int(min((C - 2 * marge - esp * (max(rangs) - 1)) / max(rangs), (hz - esp * (len(rangs) - 1)) / len(rangs), 420))
        y = haut + (hz - (cote * len(rangs) + esp * (len(rangs) - 1))) / 2
        obj = im.resize((cote, cote), Image.LANCZOS); masque = Image.new("L", (cote, cote), 0); ImageDraw.Draw(masque).rounded_rectangle([0, 0, cote - 1, cote - 1], int(cote * 0.16), fill=255)
        for k in rangs:
            x = (C - (cote * k + esp * (k - 1))) / 2
            for _ in range(k):
                fond.paste(obj, (int(x), int(y)), masque); d.rounded_rectangle([int(x), int(y), int(x) + cote - 1, int(y) + cote - 1], int(cote * 0.16), outline=ENCRE, width=4); x += cote + esp
            y += cote + esp
        im = fond
    return im


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--brut", action="store_true"); ap.add_argument("--refaire", default=""); ap.add_argument("--modele", default="@cf/black-forest-labs/flux-2-klein-9b")
    a = ap.parse_args(); stories, cast = recueil.construire(REC); BRUT.mkdir(exist_ok=True); OUT.mkdir(exist_ok=True)
    if a.brut:
        import gen_images2 as g
        cible = {x.strip() for x in a.refaire.split(",") if x.strip()}
        for s in stories:
            for i, sc in enumerate(s["scenes"], 1):
                nom = f"{s['id']}_{i}"; dest = BRUT / f"{nom}.jpg"
                if "{" in sc["desc"] or (cible and nom not in cible) or (dest.exists() and not cible): continue
                err = None
                for k in range(8):
                    try: dest.write_bytes(g.jpeg(g.appel(a.modele, {"prompt": cast["style"] + sc["desc"] + ".", "width": "1024", "height": "1024"}, {}), 960)); print("✅", nom, flush=True); err = None; break
                    except Exception as e: err = e; time.sleep(2 + k)
                if err: print("❌", nom, str(err)[:160], flush=True)
    n = 0
    for s in stories:
        for i, sc in enumerate(s["scenes"], 1):
            im = composer(s, i, sc)
            if im is None: print("… manque", f"{s['id']}_{i}"); continue
            im.save(OUT / f"{s['id']}_{i}.jpg", quality=86); n += 1
    print(n, "page(s) composée(s)")
