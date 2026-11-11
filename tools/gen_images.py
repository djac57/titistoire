#!/usr/bin/env python3
"""Illustrations des histoires : une image par tableau, décrite dans histoires/*.txt (lignes « @ »).

    assets/scenes/<heros>_<univers>_<n>.jpg      n = 1..8

Source (TITI_IMG_SRC) :
  • cf      : API Cloudflare Workers AI directe (CF_ACCOUNT_ID + CF_API_TOKEN) — utilisée en CI
  • worker  : le worker /img (même modèle flux-1-schnell, même quota de 10 000 neurons/jour)

    python3 tools/gen_images.py                 # toutes les images manquantes (reprend où il s'est arrêté)
    python3 tools/gen_images.py --only filou_pirates
    python3 tools/gen_images.py --limit 8
    python3 tools/gen_images.py --refaire filou_pirates_3     # regénère une image qui ne plaît pas

Les histoires sont illustrées une par une, en entier : d'abord les 24 histoires de base,
puis les histoires de saison en commençant par la saison qui arrive.
"""
import argparse, base64, datetime, json, os, pathlib, sys, time, urllib.error, urllib.parse, urllib.request, zlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import titi

WORKER = os.environ.get("TITI_WORKER", "https://titistoire-ai.djac-gene.workers.dev").rstrip("/")
CF_ACCOUNT = os.environ.get("CF_ACCOUNT_ID", "").strip()
CF_TOKEN = os.environ.get("CF_API_TOKEN", "").strip()
SRC = os.environ.get("TITI_IMG_SRC", "").strip() or ("cf" if (CF_ACCOUNT and CF_TOKEN) else "worker")
OUT = titi.ROOT / "assets" / "scenes"
SAISONS = {"noel": (12, 1), "ski": (2, 1), "mer": (7, 1), "halloween": (10, 15)}   # début approximatif


class Quota(Exception):
    pass


def gen_cf(prompt):
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT}/ai/run/@cf/black-forest-labs/flux-1-schnell"
    req = urllib.request.Request(url, data=json.dumps({"prompt": prompt, "steps": 8}).encode(),
                                 headers={"Authorization": "Bearer " + CF_TOKEN, "Content-Type": "application/json"})
    try:
        d = json.load(urllib.request.urlopen(req, timeout=180))
    except urllib.error.HTTPError as e:
        msg = e.read().decode("utf-8", "replace")[:300]
        if e.code == 429 or "neurons" in msg:
            raise Quota(msg)
        raise RuntimeError(f"HTTP {e.code} {msg}")
    im = (d.get("result") or {}).get("image")
    if not im:
        raise RuntimeError("pas d'image : " + json.dumps(d)[:200])
    return base64.b64decode(im)


def gen_worker(prompt):
    req = urllib.request.Request(WORKER + "/img?" + urllib.parse.urlencode({"p": prompt, "steps": 8, "frais": int(time.time())}),
                                 headers={"User-Agent": "titistoire-gen/2.0"})
    try:
        data = urllib.request.urlopen(req, timeout=180).read()
    except urllib.error.HTTPError as e:
        msg = e.read().decode("utf-8", "replace")[:300]
        if "neurons" in msg or e.code == 429:
            raise Quota(msg)
        raise RuntimeError(f"HTTP {e.code} {msg}")
    return data


def alleger(data, cote=832, qualite=82):
    """Réduit l'image (1024 px, ~400 Ko) à 832 px en JPEG ~100 Ko : bien plus léger sur téléphone."""
    try:
        import io
        from PIL import Image
    except ImportError:
        return data
    im = Image.open(io.BytesIO(data)).convert("RGB")
    if max(im.size) > cote:
        im = im.resize((cote, cote * im.size[1] // im.size[0]), Image.LANCZOS)
    out = io.BytesIO(); im.save(out, "JPEG", quality=qualite, optimize=True, progressive=True)
    return out.getvalue()


def est_image(data):
    return len(data) > 8000 and (data[:3] == b"\xff\xd8\xff" or data[:8] == b"\x89PNG\r\n\x1a\n")


def ordre(stories):
    """Histoires de base d'abord (un univers après l'autre), puis les saisons, la plus proche en premier."""
    auj = datetime.date.today()
    def delai(u):
        m, j = SAISONS[u]
        d = datetime.date(auj.year, m, j)
        if d < auj:
            d = datetime.date(auj.year + 1, m, j)
        return (d - auj).days
    base = [s for s in stories if s["univ"] not in SAISONS]
    sais = sorted((s for s in stories if s["univ"] in SAISONS), key=lambda s: (delai(s["univ"]), s["id"]))
    return base + sais


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--refaire", default="", help="ids d'images à regénérer, séparés par des virgules (ex. filou_pirates_3)")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    refaire = {x.strip() for x in a.refaire.split(",") if x.strip()}
    jobs = []
    c = titi.cast()
    if not a.only:                                      # 10 décors sans personnage (repli du mode libre et des vignettes)
        for u, d in c["decors"].items():
            f = titi.ROOT / "assets" / f"decor_{u}.jpg"
            if f"decor_{u}" in refaire or not (f.exists() and f.stat().st_size > 8000):
                jobs.append((f, c["style"] + "A wide landscape with no characters: " + d + ". No animals, no people, no text, no letters, no watermark.", None, None))
    # empreinte de la description de chaque image : une description retouchée -> image refaite
    fsig = OUT / "_descriptions.json"
    sigs = json.loads(fsig.read_text()) if fsig.exists() else {}
    for s in ordre(titi.load()):
        if a.only and not s["id"].startswith(a.only):
            continue
        for i, sc in enumerate(s["scenes"], 1):
            nom = f"{s['id']}_{i}"
            f = OUT / f"{nom}.jpg"
            sig = zlib.crc32(sc["desc"].encode("utf-8"))
            if nom in refaire or not (f.exists() and f.stat().st_size > 8000) or sigs.get(nom, sig) != sig:
                jobs.append((f, sc["prompt"], nom, sig))
    total = len(list(titi.load())) * 8
    print(f"🎨 Source : {SRC} — {len(jobs)} image(s) à faire", flush=True)
    ok = rate = 0
    for f, prompt, nom, sig in jobs:
        if a.limit and ok >= a.limit:
            break
        try:
            data = None
            for essai in range(3):
                try:
                    data = gen_cf(prompt) if SRC == "cf" else gen_worker(prompt)
                    if est_image(data):
                        break
                    data = None
                except Quota:
                    raise
                except Exception as e:
                    print(f"    …essai {essai + 1} {f.name} : {str(e)[:140]}", flush=True); time.sleep(4 * (essai + 1))
            if data is None:
                rate += 1; print(f"  ❌ {f.name}", flush=True)
                if rate >= 6:
                    print("⛔ Trop d'échecs d'affilée, arrêt."); break
                continue
        except Quota as q:
            print(f"⛔ Quota Cloudflare du jour atteint (reprise demain) : {str(q)[:160]}", flush=True); break
        data = alleger(data); f.write_bytes(data); ok += 1; rate = 0
        if nom:
            sigs[nom] = sig; fsig.write_text(json.dumps(sigs, separators=(",", ":"), sort_keys=True))
        print(f"  ✅ {f.name} ({len(data) // 1024} Ko)", flush=True)
        time.sleep(0.4)
    print(f"Images : {ok} générées — {len(list(OUT.glob('*.jpg')))} / {total} prêtes.")
    # code de sortie 0 même si le quota a coupé : ce n'est pas une erreur, la suite se fait le lendemain


if __name__ == "__main__":
    main()
