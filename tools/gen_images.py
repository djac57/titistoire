#!/usr/bin/env python3
# Illustrations "ligne claire 50-60" pour titistoire.
#
# Deux jeux d'images :
#   • ambiances  : assets/<hero>_<univ>.png                 (page 1 / couverture de chaque histoire)
#   • scenes     : assets/scenes/<hero>_<univ>_<moral>_pN.png (une par page de l'histoire, N=2..7)
#
# Source d'image (par ordre, selon l'env) :
#   • worker (DÉFAUT)   : appelle le worker Cloudflare /img (flux-1-schnell, gratuit, même DA).
#                         Nécessite le binding "AI" actif sur le worker. URL via TITI_WORKER.
#   • cf                : API Cloudflare directe si CF_ACCOUNT_ID + CF_API_TOKEN.
#   • poll              : Pollinations/turbo (secours, qualité médiocre).
# Forcer avec TITI_IMG_SRC=worker|cf|poll.
#
# Usage :
#   python3 tools/gen_images.py ambiances            # 24 ambiances (héros x univers)
#   python3 tools/gen_images.py scenes test          # 1 histoire complète (6 scènes) pour validation
#   python3 tools/gen_images.py scenes               # TOUTES les scènes manquantes (576)
#   python3 tools/gen_images.py all                  # ambiances + toutes les scènes
# Reprend toujours là où il s'est arrêté (saute les fichiers déjà bons).
import os, sys, json, time, base64, zlib, urllib.parse, urllib.request, pathlib

WORKER = os.environ.get("TITI_WORKER", "https://titistoire-ai.djac-gene.workers.dev").rstrip("/")
CF_ACCOUNT = os.environ.get("CF_ACCOUNT_ID", "").strip()
CF_TOKEN   = os.environ.get("CF_API_TOKEN", "").strip()
SRC = os.environ.get("TITI_IMG_SRC", "").strip() or ("cf" if (CF_ACCOUNT and CF_TOKEN) else "worker")

HEROS = {
    "filou":  "a cute little mischievous red fox cub with orange fur, a white belly and a friendly smile",
    "nestor": "a cute soft brown teddy bear cub, round and gentle",
    "rosie":  "a cute little white bunny rabbit with long ears and big soft eyes",
    "plume":  "a cute little beige owl with round eyes, curious and sweet",
}
# graine fixe par héros -> l'apparence reste cohérente de page en page
HERO_SEED = {"filou": 1111, "nestor": 2222, "rosie": 3333, "plume": 4444}

UNIV = {
    "pirates":    "on a friendly wooden pirate ship sailing on a calm blue sea near a treasure island",
    "dino":       "in a sunny prehistoric jungle with friendly gentle dinosaurs and a distant volcano",
    "chevaliers": "in a cheerful medieval kingdom with a castle, towers and colourful flags",
    "espace":     "in outer space among planets, bright stars, a little rocket and the moon",
    "foret":      "in an enchanted forest with tall trees, soft grass and flowers",
    "ocean":      "deep under the sea among colourful corals and friendly fish",
}

# Scènes = une description d'ACTION par page (pages 2..7 de l'histoire, index 1..6).
# L'ordre suit exactement les trames de buildStory() dans index.html.
MORALS = {
    "partage": [
        "finding a big wicker basket overflowing with delicious food and fruit",
        "hugging the full basket happily, looking a little greedy, wanting it all for itself",
        "noticing a few small hungry friends nearby with empty tummies",
        "pausing to think kindly, then opening the big basket wide",
        "sharing the food, giving a treat to each friend, everyone eating and laughing",
        "all the friends happy together around the empty basket, joyful and grateful",
    ],
    "courage": [
        "ears perked up, hearing a tiny faraway cry for help, looking around worried",
        "discovering a tiny little friend stuck and trembling with fear",
        "with a pounding heart, looking nervous but determined, taking a deep breath",
        "bravely stepping forward one small step at a time to help",
        "gently rescuing and freeing the little friend, who says thank you",
        "standing proud and brave, the rescued little friend smiling happily beside it",
    ],
    "amitie": [
        "sitting alone, looking a little lonely and wistful",
        "meeting a small someone who is crying softly",
        "reaching out a friendly paw, inviting the other to come and play",
        "the two of them playing together, inventing games and laughing with joy",
        "two new friends side by side watching a gentle warm sunset",
        "two best friends hugging warmly, a glowing little heart between them",
    ],
    "verite": [
        "accidentally knocking over and breaking a pretty little vase, looking surprised",
        "hiding behind something, looking guilty and worried",
        "looking thoughtful and torn, a small worry tickling its heart",
        "bravely confessing to a kind grown-up friend and saying sorry",
        "being hugged warmly and forgiven, looking relieved",
        "smiling with a light, happy heart, everything is okay now",
    ],
}

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
SCN = OUT / "scenes"
OUT.mkdir(exist_ok=True); SCN.mkdir(exist_ok=True)

STYLE = ("Flat 2D vector illustration in the Belgian 'ligne claire' comic style of Tintin and Herge: "
         "bold uniform black outlines, flat pastel colours, NO gradients, NO shading, NO texture, NO photorealism. "
         "Charming clean vintage 1950s-1960s children's picture-book background, simple geometric shapes. ")
TAIL = " Friendly animal character, expressive, no humans, no text, no letters, no watermark."

def prompt_ambiance(h, u):
    return STYLE + f"A cute {HEROS[h]} {UNIV[u]}." + TAIL

def prompt_scene(h, u, m, idx):
    return STYLE + f"A cute {HEROS[h]} {MORALS[m][idx]}, {UNIV[u]}." + TAIL

# ---------- sources ----------
def gen_worker(prompt, seed):
    q = urllib.parse.urlencode({"p": prompt, "seed": seed, "steps": 8})
    req = urllib.request.Request(WORKER + "/img?" + q, headers={"User-Agent": "titistoire-gen/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = r.read()
    if data[:10].lstrip()[:9] == b"Erreur AI" or (len(data) < 3000 and b"indisponible" in data):
        raise RuntimeError("worker: " + data[:160].decode("utf-8", "replace"))
    return data

def gen_cf(prompt, seed):
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT}/ai/run/@cf/black-forest-labs/flux-1-schnell"
    body = json.dumps({"prompt": prompt, "steps": 8}).encode()  # flux-1-schnell n'accepte pas de seed
    req = urllib.request.Request(url, data=body, headers={"Authorization": "Bearer " + CF_TOKEN, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.load(r)
    im = (d.get("result") or {}).get("image")
    if not im:
        raise RuntimeError("CF: pas d'image (" + json.dumps(d)[:200] + ")")
    return base64.b64decode(im)

def gen_poll(prompt, seed):
    url = ("https://image.pollinations.ai/prompt/" + urllib.parse.quote(prompt)
           + f"?width=1024&height=576&nologo=true&model=turbo&seed={seed}&referrer=titistoire")
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "titistoire/1.0"}), timeout=240) as r:
        return r.read()

def gen(prompt, seed):
    if SRC == "cf":   return gen_cf(prompt, seed)
    if SRC == "poll": return gen_poll(prompt, seed)
    return gen_worker(prompt, seed)

def good(f): return f.exists() and f.stat().st_size > 5000

def make(f, prompt, seed):
    if good(f): return "skip"
    for attempt in range(1, 4):
        try:
            data = gen(prompt, seed + attempt)
            if len(data) < 3000: raise RuntimeError(f"trop petit/{len(data)}o")
            f.write_bytes(data)
            return "ok"
        except Exception as e:
            print(f"    …essai {attempt} {f.name}: {str(e)[:140]}")
            time.sleep(3 * attempt)
    return "fail"

# ---------- plans ----------
def plan_ambiances():
    return [(OUT / f"{h}_{u}.png", prompt_ambiance(h, u), HERO_SEED[h]) for h in HEROS for u in UNIV]

def plan_scenes():
    jobs = []
    for h in HEROS:
        for u in UNIV:
            for m in MORALS:
                for idx in range(6):            # pages 2..7
                    f = SCN / f"{h}_{u}_{m}_p{idx+2}.png"
                    jobs.append((f, prompt_scene(h, u, m, idx), HERO_SEED[h]))
    return jobs

def run(jobs, label):
    print(f"🎨 Source : {SRC} ({WORKER if SRC=='worker' else ''}) — {label} : {len(jobs)} cible(s)")
    ok = sk = fa = 0
    for i, (f, p, seed) in enumerate(jobs, 1):
        r = make(f, p, seed)
        if r == "ok":   ok += 1; print(f"  [{i}/{len(jobs)}] ✅ {f.name} ({f.stat().st_size//1024} Ko)")
        elif r == "skip": sk += 1
        else: fa += 1;    print(f"  [{i}/{len(jobs)}] ❌ {f.name} (échec)")
        if r == "ok": time.sleep(0.5)
    print(f"Fini {label} : {ok} générées, {sk} déjà là, {fa} échecs.")
    return fa

mode = sys.argv[1] if len(sys.argv) > 1 else "scenes"
sub  = sys.argv[2] if len(sys.argv) > 2 else ""
fails = 0
if mode in ("ambiances", "all"):
    fails += run(plan_ambiances(), "ambiances")
if mode in ("scenes", "all"):
    jobs = plan_scenes()
    if sub == "test":
        jobs = [j for j in jobs if j[0].name.startswith("filou_foret_partage_")]
    fails += run(jobs, "scenes" + (" (test)" if sub == "test" else ""))
if mode not in ("ambiances", "scenes", "all"):
    print("Usage: gen_images.py ambiances | scenes [test] | all")
sys.exit(1 if fails else 0)
