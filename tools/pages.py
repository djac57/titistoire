#!/usr/bin/env python3
"""Référencement : une vraie page par histoire (texte lisible par les moteurs), le plan du site, robots.txt,
l'icône de l'app et l'image de partage.

    python3 tools/pages.py        écrit h/*.html, sitemap.xml, robots.txt, manifest.webmanifest, icone-*.png, partage.jpg

L'appli charge les textes par script : sans ces pages, un moteur de recherche ne voit qu'une page vide.
Chaque page renvoie vers l'appli, qui ouvre directement l'histoire (?h=filou_pirates, ?h=cometes/c01).
"""
import datetime, html, json, pathlib, sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import titi, recueil

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://titistoire.fr"
HEROS = {"filou": "Filou le renard", "nestor": "Nestor l'ourson", "rosie": "Rosie la lapine", "plume": "Plume la chouette"}
RECUEILS = {"cometes": ("Les Comètes", "6-8 ans", "Une année à Virevent", "6-8"), "galaxies": ("Les Galaxies", "8-10 ans", "Le Trésor coupé en deux", "8-10"),
            "imagiers": ("Les Lucioles", "1-3 ans", "Les imagiers", "1-3")}
e = html.escape

CSS = """body{margin:0;font-family:Nunito,system-ui,sans-serif;background:#2d2570;color:#fff;line-height:1.65}
main{max-width:760px;margin:0 auto;padding:24px 18px 60px}a{color:#ffcb4d}
h1{font-family:Fredoka,system-ui,sans-serif;color:#ffcb4d;font-size:clamp(1.7rem,6vw,2.4rem);line-height:1.2;margin:14px 0 6px}
h2{font-family:Fredoka,system-ui,sans-serif;font-size:1.2rem;margin:30px 0 8px;color:#ffcb4d}
.sur{opacity:.85;font-weight:700}.fil{font-size:.9rem;opacity:.85}
img{width:100%;height:auto;max-width:520px;border-radius:22px;display:block;margin:18px auto}
.btn{display:inline-block;background:#2fc08f;color:#fff;font-family:Fredoka,system-ui,sans-serif;font-weight:600;font-size:1.15rem;padding:13px 26px;border-radius:999px;text-decoration:none;margin:10px 0 6px}
.texte p{margin:0 0 .9em;font-size:1.08rem}.texte .t{margin-top:1.6em}
footer{margin-top:40px;font-size:.9rem;opacity:.85}"""


def page(chemin, titre, desc, corps, image="", ld=None):
    url = f"{SITE}/{chemin}".removesuffix(".html")          # l'hébergeur sert les pages sans « .html » (et y redirige)
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titre)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:site_name" content="Titistoire"><meta property="og:locale" content="fr_FR">
<meta property="og:title" content="{e(titre)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/{image or 'partage.jpg'}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../icone-192.png"><meta name="theme-color" content="#2d2570">
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Nunito:wght@500;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
{'<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>' if ld else ''}
</head><body><main>
{corps}
<footer><a href="../">Toutes les histoires de Titistoire</a> · <a href="../mentions-legales.html">Mentions légales</a> · <a href="../confidentialite.html">Confidentialité</a> · <a href="../cgu.html">Conditions d'utilisation</a></footer>
</main></body></html>
"""


def resume(pages, n=155):
    t = " ".join(pages)
    if len(t) <= n: return t
    c = t[:n]; return c[:c.rfind(" ")].rstrip(",;:") + "…"


def histoire(chemin, lien, titre, groupe, age, tranche, intro, image, tableaux, suite=""):
    pages = [p for tb in tableaux for p in tb]
    desc = f"{intro} {resume(pages, 120)}"
    texte = "".join(f'<p class="{"t" if k == 0 and i else ""}">{e(p)}</p>' for i, tb in enumerate(tableaux) for k, p in enumerate(tb))
    corps = f"""<p class="fil"><a href="../">Titistoire</a> › {e(groupe)} ({age})</p>
<h1>{e(titre)}</h1>
<p class="sur">{e(intro)}</p>
<img src="../{image}" alt="{e(titre)} — illustration" width="960" height="960">
<p><a class="btn" href="../?h={lien}">▶ Écouter et regarder l'histoire</a><br>Gratuit, sans inscription : la voix lit, le texte suit mot à mot, les images tournent comme dans un album.</p>
<h2>Le texte de l'histoire</h2>
<div class="texte">{texte}</div>
<p><a class="btn" href="../?h={lien}">▶ L'écouter dans Titistoire</a></p>{suite}"""
    ld = {"@context": "https://schema.org", "@type": "ShortStory", "name": titre, "inLanguage": "fr", "isAccessibleForFree": True, "url": f"{SITE}/{chemin}".removesuffix(".html"),
          "image": f"{SITE}/{image}", "description": desc, "typicalAgeRange": tranche, "audience": {"@type": "PeopleAudience", "suggestedMinAge": int(tranche.split("-")[0]), "suggestedMaxAge": int(tranche.split("-")[1])},
          "publisher": {"@type": "Organization", "name": "Titistoire", "url": SITE}}
    return page(chemin, f"{titre} — histoire à écouter pour les {age} | Titistoire", desc, corps, image, ld)


def police(taille, graisse=b"Bold"):
    f = ImageFont.truetype(str(ROOT / "tools" / "Fredoka.ttf"), taille); f.set_variation_by_name(graisse); return f


def icone(cote):
    im = Image.new("RGB", (cote, cote), (45, 37, 112)); d = ImageDraw.Draw(im); c = cote / 64        # le livre ouvert du favicon, sur fond nuit
    for s in (-1, 1):
        d.polygon([(32 * c, 21 * c), (32 * c + s * 17 * c, 17 * c), (32 * c + s * 17 * c, 44 * c), (32 * c, 47 * c)], fill=(255, 203, 77))
    d.line([(32 * c, 20 * c), (32 * c, 48 * c)], fill=(45, 37, 112), width=max(2, int(2.4 * c)))
    return im


def partage():
    im = Image.new("RGB", (1200, 630), (45, 37, 112)); d = ImageDraw.Draw(im)
    for k, h in enumerate(("filou", "nestor", "rosie", "plume")):
        f = ROOT / "assets" / f"{h}_foret.png"
        if f.exists():
            v = Image.open(f).convert("RGB").resize((250, 250), Image.LANCZOS); m = Image.new("L", (250, 250), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, 249, 249], 40, fill=255)
            im.paste(v, (70 + k * 270, 330), m)
    d.text((600, 120), "Titistoire", font=police(150), fill=(255, 203, 77), anchor="mm")
    d.text((600, 245), "De belles histoires à écouter et à regarder, de 1 à 10 ans", font=police(40, b"Medium"), fill=(255, 255, 255), anchor="mm")
    return im


if __name__ == "__main__":
    H = ROOT / "h"; H.mkdir(exist_ok=True); urls = [("", "1.0")]; titres = []
    for s in titi.load():
        tb = [sc["pages"] for sc in s["scenes"]]; nom = f"{s['id']}.html"
        (H / nom).write_text(histoire(f"h/{nom}", s["id"], s["titre"], "Les Étoiles", "3-6 ans", "3-6",
                                      f"Une histoire de {HEROS.get(s['hero'], s['hero'])} pour parler de : {s['sujet'][0].lower() + s['sujet'][1:]}.", f"assets/scenes/{s['id']}_1.jpg", tb), encoding="utf-8")
        urls.append((f"h/{nom}", "0.8")); titres.append((f"h/{nom}", f"{s['titre']} (Étoiles, 3-6 ans)"))
    for rec, (groupe, age, serie, tranche) in RECUEILS.items():
        st = recueil.load(rec)
        for k, s in enumerate(st):
            nom = f"{rec}-{s['id']}.html"; tb = [sc["pages"] for sc in s["scenes"]]
            intro = {"cometes": f"{serie}, l'histoire du mois de {s['sous'].lower()} : Jeanne, Gaspard, Suzie et Marin.", "galaxies": f"{serie}, épisode {k + 1} sur {len(st)} : un feuilleton à énigmes sur l'île de Lodenn.",
                     "imagiers": f"Un imagier pour les tout-petits : {s['sous'].lower()}."}[rec]
            suite = ""
            if rec == "galaxies" and k + 1 < len(st): suite = f'<p>Épisode suivant : <a href="{rec}-{st[k + 1]["id"]}.html">{e(st[k + 1]["titre"])}</a></p>'
            (H / nom).write_text(histoire(f"h/{nom}", f"{rec}/{s['id']}", s["titre"], groupe, age, tranche, intro, f"{rec}/scenes/{s['id']}_1.jpg", tb, suite), encoding="utf-8")
            urls.append((f"h/{nom}", "0.8")); titres.append((f"h/{nom}", f"{s['titre']} ({groupe}, {age})"))
    # la liste de toutes les histoires : le point d'entrée des moteurs vers chaque page
    liste = "".join(f'<li><a href="{u[2:]}">{e(n)}</a></li>' for u, n in titres)
    (H / "index.html").write_text(page("h/", "Toutes les histoires de Titistoire — à écouter de 1 à 10 ans", "La liste de toutes les histoires de Titistoire : les Étoiles (3-6 ans), les Comètes (6-8 ans), les Galaxies (8-10 ans) et les imagiers des Lucioles (1-3 ans).",
        f'<p class="fil"><a href="../">Titistoire</a></p><h1>Toutes les histoires</h1><p>Des histoires illustrées, lues à voix haute, gratuites et sans publicité.</p><ul class="texte">{liste}</ul>'), encoding="utf-8")
    urls.append(("h/", "0.6"))
    for p in ("mentions-legales.html", "confidentialite.html", "cgu.html"):
        if (ROOT / p).exists(): urls.append((p, "0.2"))
    jour = datetime.date.today().isoformat()
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                      + "".join(f"<url><loc>{SITE}/{u.removesuffix('.html')}</loc><lastmod>{jour}</lastmod><priority>{p}</priority></url>\n" for u, p in urls) + "</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /histoires/\nDisallow: /tools/\nDisallow: /worker/\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    for c in (192, 512): icone(c).save(ROOT / f"icone-{c}.png")
    partage().save(ROOT / "partage.jpg", quality=88)
    (ROOT / "manifest.webmanifest").write_text(json.dumps({"name": "Titistoire — histoires à écouter", "short_name": "Titistoire", "lang": "fr", "start_url": "./", "scope": "./", "display": "standalone",
        "background_color": "#2d2570", "theme_color": "#2d2570", "description": "De belles histoires à écouter et à regarder, pour les enfants de 1 à 10 ans.",
        "icons": [{"src": "icone-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"}, {"src": "icone-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"✅ {len(urls)} adresses dans sitemap.xml, {len(list(H.glob('*.html')))} pages d'histoire")
