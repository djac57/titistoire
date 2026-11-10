#!/usr/bin/env python3
# Illustrations "ligne claire 50-60" pour titistoire.
# Qualité (FLUX) via Hugging Face si token dans ~/.hf_token (GRATUIT, sans CB).
# Sinon repli keyless Pollinations/turbo (qualité médiocre).
# Usage : python3 tools/gen_images.py test | missing | all
import os, sys, json, time, urllib.parse, urllib.request, pathlib

HF_TOKEN = os.environ.get("HF_TOKEN", "").strip()   # secret en CI
hf = os.path.expanduser("~/.hf_token")
if not HF_TOKEN and os.path.exists(hf):
    HF_TOKEN = open(hf).read().strip()
USE_HF = bool(HF_TOKEN)

HEROS = {
    "filou":  "a cute little mischievous red fox cub with a friendly smile",
    "nestor": "a cute soft brown teddy bear cub, gentle",
    "rosie":  "a cute little white bunny rabbit with big soft eyes",
    "plume":  "a cute little beige owl, curious and sweet",
}
UNIV = {
    "pirates":    "on a friendly pirate ship sailing on the sea near a treasure island",
    "dino":       "in a prehistoric jungle with friendly dinosaurs and a volcano",
    "chevaliers": "in a medieval kingdom with a castle and colorful flags",
    "espace":     "in outer space with planets, stars, a little rocket and the moon",
    "foret":      "in an enchanted forest with tall trees and flowers",
    "ocean":      "at the bottom of the sea with corals and colorful fish",
}
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

def style(h, u):
    return ("Children's storybook illustration, vintage 1950s-1960s clean clear-line (ligne claire) style, "
            "thick clean outlines, flat soft pastel colours, gentle and whimsical, retro mid-century picture book. "
            f"The main character is {HEROS[h]} {UNIV[u]}. No humans. Centered animal character, friendly and cheerful, "
            "soft warm lighting. No text, no words, no letters, no watermark.")

def gen_hf(prompt):
    url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
    body = json.dumps({"inputs": prompt, "parameters": {"width": 1024, "height": 576}}).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": "Bearer " + HF_TOKEN, "Content-Type": "application/json", "Accept": "image/png"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()

def gen_poll(prompt, seed):
    url = ("https://image.pollinations.ai/prompt/" + urllib.parse.quote(prompt)
           + f"?width=1024&height=576&nologo=true&model=turbo&seed={seed}&referrer=titistoire")
    req = urllib.request.Request(url, headers={"User-Agent": "titistoire/1.0"})
    with urllib.request.urlopen(req, timeout=240) as r:
        return r.read()

def gen(prompt, seed):
    return gen_hf(prompt) if USE_HF else gen_poll(prompt, seed)

def good(f):
    return f.exists() and f.stat().st_size > 5000

pairs = [(h, u) for h in HEROS for u in UNIV]
mode = sys.argv[1] if len(sys.argv) > 1 else "test"
missing = [(h, u) for (h, u) in pairs if not good(OUT / f"{h}_{u}.png")]
if mode == "test":
    todo = [("filou", "dino")]
elif mode == "missing":
    todo = missing
else:  # all -> régénère tout (écrase), pour une qualité homogène
    todo = pairs

print(f"🎨 Source : {'Hugging Face FLUX.1-schnell (qualité)' if USE_HF else 'Pollinations/turbo (repli médiocre)'} — {mode} : {len(todo)} image(s)")
ok = 0
for i, (h, u) in enumerate(todo, 1):
    f = OUT / f"{h}_{u}.png"
    for attempt in range(1, 5):
        try:
            data = gen(style(h, u), 1000 + hash((h, u)) % 9000 + attempt)
            if len(data) < 5000:
                raise RuntimeError(f"trop petit/{len(data)}o (HF charge le modèle ?)")
            f.write_bytes(data); ok += 1
            print(f"  [{i}/{len(todo)}] ✅ {f.name} ({len(data)//1024} Ko)")
            break
        except Exception as e:
            print(f"  [{i}/{len(todo)}] …essai {attempt} {h}_{u}: {e}")
            time.sleep(6 * attempt)
    time.sleep(2)
tot = sum(1 for p in pairs if good(OUT / f"{p[0]}_{p[1]}.png"))
print(f"Fini : {ok} générées. Présentes : {tot}/24")
