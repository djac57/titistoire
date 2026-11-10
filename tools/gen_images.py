#!/usr/bin/env python3
# Génère les illustrations "ligne claire années 50-60" pour titistoire.
# GRATUIT, SANS CLÉ : via Pollinations.ai (modèle FLUX).
# Usage :  python3 tools/gen_images.py test   (1 image)
#          python3 tools/gen_images.py all    (24 : 4 héros x 6 univers)
import sys, time, urllib.parse, urllib.request, pathlib

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
            f"{HEROS[h]} {UNIV[u]}. Centered character, friendly and cheerful, soft warm lighting. "
            "No text, no words, no letters, no watermark.")

def gen(prompt, seed):
    url = ("https://image.pollinations.ai/prompt/" + urllib.parse.quote(prompt)
           + f"?width=1024&height=576&nologo=true&model=flux&seed={seed}")
    req = urllib.request.Request(url, headers={"User-Agent": "titistoire-gen/1.0"})
    with urllib.request.urlopen(req, timeout=240) as r:
        return r.read()

pairs = [(h, u) for h in HEROS for u in UNIV]
mode = sys.argv[1] if len(sys.argv) > 1 else "test"
if mode == "test":
    pairs = [("filou", "foret")]
print(f"🎨 Pollinations ({mode}) : {len(pairs)} image(s)")
ok = 0
for i, (h, u) in enumerate(pairs, 1):
    f = OUT / f"{h}_{u}.png"
    try:
        data = gen(style(h, u), 1000 + i * 7)
        if len(data) < 2000:
            raise RuntimeError(f"réponse trop petite ({len(data)} o)")
        f.write_bytes(data); ok += 1
        print(f"  [{i}/{len(pairs)}] ✅ {f.name} ({len(data)//1024} Ko)")
    except Exception as e:
        print(f"  [{i}/{len(pairs)}] ❌ {h}_{u}: {e}")
    time.sleep(1.0)
print(f"Fini : {ok}/{len(pairs)} dans {OUT}")
