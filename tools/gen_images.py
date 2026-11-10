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

# Scènes = une description d'ACTION par page (pages 2..11 de l'histoire, index 1..10).
# L'ordre suit EXACTEMENT les trames de buildStory() dans index.html (11 pages : 1 intro + 9 + morale).
MORALS = {
    "partage": [
        "walking cheerfully along a path, humming happily in the morning sun",
        "discovering a big wicker basket overflowing with fruit, cakes and good food",
        "eyes sparkling with delight at all the food, wanting it all",
        "hugging the full basket tightly, not wanting to give any away",
        "noticing a few little friends nearby with empty tummies, looking hungry",
        "pausing thoughtfully, a kind idea appearing, a little glowing heart",
        "taking a big breath and opening the basket wide with a smile",
        "giving a piece of fruit to each friend, everyone eating and laughing together",
        "sitting happily among grateful little friends, content and warm",
        "all the friends together around the empty basket, joyful warm group hug",
    ],
    "courage": [
        "exploring joyfully and curiously, happy and carefree",
        "ears perked up, hearing a tiny faraway cry for help, surprised",
        "following the sound carefully, searching around with concern",
        "finding a tiny little friend stuck and trembling with fear",
        "looking worried with a pounding heart, but caring",
        "taking a deep brave breath, with a determined little face",
        "stepping forward carefully, reaching out a paw to help",
        "gently freeing and rescuing the little trapped friend",
        "the rescued little friend hugging and thanking, both smiling",
        "standing proud and brave together, happy, little sparkles of courage",
    ],
    "amitie": [
        "sitting alone, looking a little lonely and wistful",
        "wandering and daydreaming, wishing for a friend to play with",
        "meeting a small someone who is crying softly",
        "approaching gently and kindly asking what is wrong",
        "reaching out a paw with a big smile, inviting the other to play",
        "starting to play together, first shy happy smiles",
        "inventing lots of fun games together, laughing with joy",
        "sharing a little snack, resting side by side, happy",
        "two friends watching a warm golden sunset together",
        "two best friends hugging warmly, a glowing little heart between them",
    ],
    "verite": [
        "playing happily and having lots of fun",
        "accidentally knocking over and breaking a pretty little vase",
        "staring surprised at the broken pieces on the ground",
        "looking guilty and worried, wanting to hide",
        "hiding behind something, a worry tickling its heart",
        "sitting thoughtful and torn, unable to stop thinking about it",
        "bravely walking over to tell a kind grown-up friend the truth",
        "confessing honestly and saying sorry, sincere and brave",
        "being hugged warmly and forgiven, looking relieved and light",
        "smiling with a light happy heart under a bright sky, all is well",
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
                for idx in range(10):           # pages 2..11
                    f = SCN / f"{h}_{u}_{m}_p{idx+2}.png"
                    jobs.append((f, prompt_scene(h, u, m, idx), HERO_SEED[h]))
    return jobs

MAX_CONSEC_FAIL = int(os.environ.get("TITI_MAX_FAIL", "12"))  # arrêt si quota/API en rade

def run(jobs, label):
    print(f"🎨 Source : {SRC} ({WORKER if SRC=='worker' else ''}) — {label} : {len(jobs)} cible(s)", flush=True)
    ok = sk = fa = consec = 0
    for i, (f, p, seed) in enumerate(jobs, 1):
        r = make(f, p, seed)
        if r == "ok":   ok += 1; consec = 0; print(f"  [{i}/{len(jobs)}] ✅ {f.name} ({f.stat().st_size//1024} Ko)", flush=True)
        elif r == "skip": sk += 1
        else:
            fa += 1; consec += 1; print(f"  [{i}/{len(jobs)}] ❌ {f.name} (échec)", flush=True)
            if consec >= MAX_CONSEC_FAIL:
                print(f"⛔ {consec} échecs d'affilée — quota/API probablement épuisé, arrêt (reprise plus tard).", flush=True)
                break
        if r == "ok": time.sleep(0.5)
    print(f"Fini {label} : {ok} générées, {sk} déjà là, {fa} échecs.", flush=True)
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
    else:
        lim = int(os.environ.get("TITI_LIMIT", "0"))
        if lim > 0:  # ne garder qu'un lot de N manquantes (pour committer par paquets)
            jobs = [j for j in jobs if not good(j[0])][:lim]
    fails += run(jobs, "scenes" + (" (test)" if sub == "test" else ""))
if mode not in ("ambiances", "scenes", "all"):
    print("Usage: gen_images.py ambiances | scenes [test] | all")
sys.exit(1 if fails else 0)
