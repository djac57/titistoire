#!/usr/bin/env python3
"""Relecture des voix enregistrées : chaque piste est réécoutée par reconnaissance vocale et comparée au texte.
Signale les mots non reconnus (mal prononcés, sautés), les débits anormaux et les blancs. macOS (afconvert) ou ffmpeg.

    python3 tools/relire_voix.py [Voix]        # défaut : toutes les voix présentes
"""
import sys, json, pathlib, subprocess, tempfile, wave, difflib, unicodedata, shutil
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import titi
import numpy as np
from faster_whisper import WhisperModel

BASE = titi.ROOT / "assets" / "voix"
norm = lambda s: "".join(c for c in unicodedata.normalize("NFD", s.lower()) if c.isalnum() and not unicodedata.combining(c))

def pcm16k(m4a):
    with tempfile.TemporaryDirectory() as td:
        w = pathlib.Path(td) / "a.wav"
        if shutil.which("ffmpeg"): subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(m4a), "-ac", "1", "-ar", "16000", str(w)], check=True)
        else: subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16@16000", "-c", "1", str(m4a), str(w)], check=True)
        x = wave.open(str(w)); return np.frombuffer(x.readframes(x.getnframes()), dtype="<i2").astype("float32") / 32768

def main():
    voix = sys.argv[1:] or sorted(d.name for d in BASE.iterdir() if d.is_dir())
    asr = WhisperModel("small", device="cpu", compute_type="int8")
    stories = {s["id"]: s for s in titi.load()}
    rapport = {}
    for v in voix:
        for fj in sorted((BASE / v).glob("*.json")):
            sid = fj.stem; meta = json.loads(fj.read_text()); pb = []
            for i, sc in enumerate(stories[sid]["scenes"], 1):
                f = BASE / v / f"{sid}_{i}.m4a"
                if not f.exists() or str(i) not in meta["sc"]: pb.append(f"tableau {i} : piste absente"); continue
                x = pcm16k(f); dur = len(x) / 16000
                segs, _ = asr.transcribe(x, language="fr", beam_size=5, condition_on_previous_text=False)
                entendu = " ".join(s.text for s in segs)
                attendu = " ".join(sc["pages"]); ta = [t for t in attendu.split() if norm(t)]; he = [t for t in entendu.split() if norm(t)]
                sm = difflib.SequenceMatcher(None, [norm(t) for t in ta], [norm(t) for t in he], autojunk=False)
                manque = []
                for tag, a0, a1, b0, b1 in sm.get_opcodes():
                    if tag in ("replace", "delete"):
                        at, en = " ".join(ta[a0:a1]), " ".join(he[b0:b1])
                        # on ne garde que les vrais écarts : mot sauté, ou son très différent (les homophones
                        # et les noms propres mal orthographiés par la reconnaissance ne sont pas des défauts)
                        if not en or difflib.SequenceMatcher(None, norm(at), norm(en)).ratio() < 0.55: manque.append(f"« {at} » entendu « {en or '∅'} »")
                cps = len(attendu) / dur
                amp = np.abs(x); pas = 320; rms = np.sqrt((x[: len(x) // pas * pas].reshape(-1, pas) ** 2).mean(axis=1)); calme = rms < max(1e-4, np.percentile(rms, 90) * 0.05)
                blanc, cur = 0, 0
                for c in calme:
                    cur = cur + 1 if c else 0; blanc = max(blanc, cur)
                if manque: pb.append(f"tableau {i} : " + " ; ".join(manque[:6]))
                if not 8 <= cps <= 19: pb.append(f"tableau {i} : débit inhabituel ({cps:.1f} car./s)")
                if blanc * 0.02 > 3.5: pb.append(f"tableau {i} : blanc de {blanc * 0.02:.1f} s")
                if meta["sc"][str(i)]["w"][0][0] > 1.5: pb.append(f"tableau {i} : la voix démarre à {meta['sc'][str(i)]['w'][0][0]} s")
            rapport[f"{v}/{sid}"] = pb
            print(f"{v}/{sid} ({meta.get('m')}) : " + ("rien à signaler" if not pb else f"{len(pb)} point(s)"), flush=True)
            for p in pb: print("    " + p, flush=True)
    return rapport

if __name__ == "__main__":
    main()
