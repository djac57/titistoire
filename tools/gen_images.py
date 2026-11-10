#!/usr/bin/env python3
# Illustrations "ligne claire 50-60" pour titistoire.
# Source préférée : Cloudflare Workers AI (flux-1-schnell) si CF_ACCOUNT_ID + CF_API_TOKEN.
# Sinon Hugging Face (~/.hf_token ou HF_TOKEN) ; sinon Pollinations/turbo (médiocre).
# Usage : python3 tools/gen_images.py test | missing | all
import os, sys, json, time, base64, urllib.parse, urllib.request, pathlib

CF_ACCOUNT = os.environ.get("CF_ACCOUNT_ID", "").strip()
CF_TOKEN   = os.environ.get("CF_API_TOKEN", "").strip()
USE_CF = bool(CF_ACCOUNT and CF_TOKEN)

HF_TOKEN = os.environ.get("HF_TOKEN", "").strip()
_hf = os.path.expanduser("~/.hf_token")
if not HF_TOKEN and os.path.exists(_hf):
    HF_TOKEN = open(_hf).read().strip()
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
            f"The main character is {HEROS[h]} {UNIV[u]}. No humans, no text, no letters, no watermark. "
            "Centered friendly animal character, soft warm lighting.")

def gen_cf(prompt):
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT}/ai/run/@cf/black-forest-labs/flux-1-schnell"
    body = json.dumps({"prompt": prompt, "steps": 8}).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": "Bearer " + CF_TOKEN, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.load(r)
    img = (d.get("result") or {}).get("image")
    if not img:
        raise RuntimeError("CF: pas d'image (" + json.dumps(d)[:200] + ")")
    return base64.b64decode(img)

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
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "titistoire/1.0"}), timeout=240) as r:
        return r.read()

def gen(prompt, seed):
    if USE_CF: return gen_cf(prompt)
    if USE_HF: return gen_hf(prompt)
    return gen_poll(prompt, seed)

def good(f): return f.exists() and f.stat().st_size > 5000

pairs = [(h, u) for h in HEROS for u in UNIV]
mode = sys.argv[1] if len(sys.argv) > 1 else "test"
missing = [(h, u) for (h, u) in pairs if not good(OUT / f"{h}_{u}.png")]
todo = [("filou", "dino")] if mode == "test" else (missing if mode == "missing" else pairs)

src = "Cloudflare Workers AI (flux-1-schnell)" if USE_CF else ("Hugging Face FLUX" if USE_HF else "Pollinations/turbo")
print(f"🎨 Source : {src} — {mode} : {len(todo)} image(s)")
ok = 0
for i, (h, u) in enumerate(todo, 1):
    f = OUT / f"{h}_{u}.png"
    for attempt in range(1, 4):
        try:
            data = gen(style(h, u), 1000 + hash((h, u)) % 9000 + attempt)
            if len(data) < 3000: raise RuntimeError(f"trop petit/{len(data)}o")
            f.write_bytes(data); ok += 1
            print(f"  [{i}/{len(todo)}] ✅ {f.name} ({len(data)//1024} Ko)")
            break
        except Exception as e:
            print(f"  [{i}/{len(todo)}] …essai {attempt} {h}_{u}: {e}")
            time.sleep(3 * attempt)
    time.sleep(0.5)
tot = sum(1 for p in pairs if good(OUT / f"{p[0]}_{p[1]}.png"))
print(f"Fini : {ok} générées. Présentes : {tot}/24")
