#!/usr/bin/env python3
# Génère les illustrations "ligne claire années 50-60" pour titistoire.
# Clé lue dans ~/.gemini_key (ou env GEMINI_API_KEY) -> jamais commitée.
# Usage :  python3 tools/gen_images.py test     (1 image de test)
#          python3 tools/gen_images.py all      (les 16 : héros x univers)
import os, sys, json, base64, time, urllib.request, pathlib

key = os.environ.get("GEMINI_API_KEY")
kf = os.path.expanduser("~/.gemini_key")
if not key and os.path.exists(kf):
    key = open(kf).read().strip()
if not key:
    print("❌ Pas de clé. Mets ta clé Gemini dans ~/.gemini_key  (ou export GEMINI_API_KEY=...).")
    sys.exit(1)

MODEL = "imagen-3.0-generate-002"   # modifiable si besoin (ex: imagen-3.0-fast-generate-001)

HEROS = {
    "filou":  "a cute little mischievous red fox cub with a friendly smile",
    "nestor": "a cute soft brown teddy bear cub, gentle and brave",
    "rosie":  "a cute little white bunny rabbit with big soft eyes",
    "plume":  "a cute little beige owl, curious and sweet",
}
UNIV = {
    "pirates":    "on a friendly pirate ship sailing on the sea near a treasure island",
    "dino":       "in a prehistoric jungle with friendly dinosaurs and a volcano",
    "chevaliers": "in a medieval kingdom with a castle, colorful flags and brave knights",
    "espace":     "in outer space with planets, stars, a little rocket and the moon",
    "foret":      "in an enchanted forest with tall trees and flowers",
    "ocean":      "at the bottom of the sea with corals and colorful fish",
}
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

def style(h, u):
    return ("Children's storybook illustration, vintage 1950s-1960s clean clear-line (ligne claire) style, "
            "thick clean outlines, flat soft pastel colors, gentle and whimsical, retro mid-century. "
            f"{HEROS[h]} in {UNIV[u]}. Centered character, friendly and cheerful, soft lighting. "
            "No text, no words, no letters, no watermark.")

def gen(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:predict?key={key}"
    body = {"instances":[{"prompt":prompt}],
            "parameters":{"sampleCount":1,"aspectRatio":"16:9"}}
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.load(r)
    preds = d.get("predictions", [])
    if not preds or "bytesBase64Encoded" not in preds[0]:
        raise RuntimeError("réponse sans image: " + json.dumps(d)[:400])
    return base64.b64decode(preds[0]["bytesBase64Encoded"])

pairs = [(h, u) for h in HEROS for u in UNIV]
mode = sys.argv[1] if len(sys.argv) > 1 else "test"
if mode == "test":
    pairs = [("filou", "foret")]
print(f"🎨 Génération ({mode}) : {len(pairs)} image(s) — modèle {MODEL}")
ok = 0
for i, (h, u) in enumerate(pairs, 1):
    f = OUT / f"{h}_{u}.png"
    try:
        png = gen(style(h, u)); f.write_bytes(png); ok += 1
        print(f"  [{i}/{len(pairs)}] ✅ {f.name} ({len(png)//1024} Ko)")
    except Exception as e:
        print(f"  [{i}/{len(pairs)}] ❌ {h}_{u}: {e}")
    time.sleep(1.2)
print(f"Fini : {ok}/{len(pairs)} générées dans {OUT}")
