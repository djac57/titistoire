#!/usr/bin/env python3
"""Recale le minutage des pistes de voix sur le SIGNAL (les silences), là où la reconnaissance vocale est imprécise :

  - le début de chaque piste : le premier mot s'allume quand la voix commence vraiment ;
  - les mots « charnières » entre deux pages : la page tourne dans le silence qui sépare les deux pages, le dernier mot
    d'une page ne déborde pas sur la suivante, et le premier mot de la suivante s'allume à la reprise de la voix.

Ne réenregistre rien : relit les pistes .m4a existantes et corrige les fichiers .json (le texte et sa signature ne changent pas).

    python3 tools/recaler_voix.py [Voix …] [--essai]      # défaut : toutes les voix ; --essai : compte sans écrire
"""
import json, pathlib, shutil, subprocess, sys, tempfile, unicodedata, wave

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = ROOT / "assets" / "voix"
PAS = 0.01                                             # trames de 10 ms
mot = lambda t: any(c.isalnum() for c in unicodedata.normalize("NFD", t))


def silences(x, rate):
    """-> (liste des silences [début, fin] d'au moins 0,18 s, instant où la voix commence)"""
    import numpy as np
    pas = int(rate * PAS); n = len(x) // pas
    if n < 20: return [], 0.0
    rms = np.sqrt((x[: n * pas].reshape(n, pas).astype("float64") ** 2).mean(axis=1) + 1e-12)
    voix = rms > max(np.median(rms) * 0.1, rms.max() * 0.015)
    out, i = [], 0
    while i < n:
        if not voix[i]:
            j = i
            while j < n and not voix[j]: j += 1
            if (j - i) * PAS >= 0.18 or i == 0: out.append((i * PAS, j * PAS))
            i = j
        else: i += 1
    debut = 0.0
    for i in range(n - 5):
        if voix[i:i + 5].all(): debut = i * PAS; break
    return out, debut


def poser(pg, mots, t):
    """Le premier vrai mot de la page commence à t ; la ponctuation qui le précède («) juste avant ; rien ensuite n'est plus tôt."""
    k = next((i for i, m in enumerate(mots) if mot(m)), 0) if len(mots) == len(pg) else 0
    for i in range(k): pg[i] = round(max(0.0, t - 0.06), 2)
    pg[k] = round(t, 2)
    for i in range(k + 1, len(pg)): pg[i] = max(pg[i], pg[k])


def recaler(x, rate, w, pages):
    """x : échantillons de la piste ; w : débuts des mots, page par page ; pages : leurs textes. -> (w corrigé, nb de retouches)"""
    w = [list(pg) for pg in w]; mots = [p.split() for p in pages]; n = 0
    if not w or not all(w): return w, 0
    sil, debut = silences(x, rate)
    # 1. début de la piste
    suivant = w[0][1] if len(w[0]) > 1 else w[0][0] + 1
    if abs(w[0][0] - debut) > 0.1 and debut < max(suivant, w[0][0]) + 0.6:
        poser(w[0], mots[0], debut); n += 1
    # 2. charnières entre pages
    for k in range(len(w) - 1):
        a, b = w[k][-1], w[k + 1][0]
        if len(mots[k + 1]) == len(w[k + 1]):                 # b : le premier VRAI mot de la page suivante
            b = next((t for t, m in zip(w[k + 1], mots[k + 1]) if mot(m)), b)
        if len(mots[k]) == len(w[k]):                         # a : le dernier VRAI mot de la page (« ! » et « » » sont souvent datés dans le silence)
            a = next((t for t, m in zip(reversed(w[k]), reversed(mots[k])) if mot(m)), a)
        apres = min([t for t in w[k + 1] if t > b + 0.01] + [w[k + 2][0] if k + 2 < len(w) else 1e9])      # le mot (ou la page) qui suit : la reprise ne peut pas être au-delà
        cand = [(abs(f - b), d, f) for d, f in sil if d > a and f > a + 0.1 and d < b + 0.45 and f < apres - 0.05]      # le silence qui finit le plus près du mot
        if not cand: continue
        _, d, f = min(cand)
        if abs(f - b) > 0.06 or w[k + 1][0] < d or (w[k + 1][0] < b - 0.01 and abs(w[k + 1][0] - (f - 0.06)) > 0.05):
            poser(w[k + 1], mots[k + 1], f); n += 1
        plafond = round(max(w[k][0], d - 0.12), 2)            # la fin de la page reste avant le silence
        for i in range(len(w[k])):
            if w[k][i] > plafond: w[k][i] = plafond; n += 1
    prec = 0.0                                                 # garde-fou : jamais de retour en arrière, d'une page à l'autre non plus
    for pg in w:
        for i in range(len(pg)): pg[i] = prec = max(pg[i], prec)
    return [[round(t, 2) for t in pg] for pg in w], n


def lire(m4a, rate=16000):
    import numpy as np
    with tempfile.TemporaryDirectory() as td:
        f = pathlib.Path(td) / "a.wav"
        if shutil.which("ffmpeg"): subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(m4a), "-ac", "1", "-ar", str(rate), str(f)], check=True)
        else: subprocess.run(["afconvert", "-f", "WAVE", "-d", f"LEI16@{rate}", "-c", "1", str(m4a), str(f)], check=True)
        v = wave.open(str(f)); return np.frombuffer(v.readframes(v.getnframes()), dtype="<i2").astype("float32"), rate


def textes():
    """{(sous-dossier, id): [pages de chaque tableau]} pour tout ce qui a une voix"""
    sys.path.insert(0, str(ROOT / "tools")); import titi, recueil
    T = {("", s["id"]): [sc["pages"] for sc in s["scenes"]] for s in titi.load()}
    T.update({("petits", s["id"]): [sc["pages"] for sc in s["scenes"]] for s in titi.load_petits()})
    for rec in ("imagiers", "cometes", "galaxies"):
        T.update({(rec, s["id"]): [sc["pages"] for sc in s["scenes"]] for s in recueil.construire(rec)[0]})
    return T


if __name__ == "__main__":
    essai = "--essai" in sys.argv; voix = [a for a in sys.argv[1:] if not a.startswith("--")] or sorted(d.name for d in BASE.iterdir() if d.is_dir())
    T = textes(); tot = pistes = 0
    for v in voix:
        for fj in sorted((BASE / v).rglob("*.json")):
            sous = "" if fj.parent == BASE / v else fj.parent.name; pg = T.get((sous, fj.stem))
            if not pg: continue
            meta = json.loads(fj.read_text()); chg = 0
            for s, m in meta.get("sc", {}).items():
                f = fj.parent / f"{fj.stem}_{s}.m4a"; i = int(s) - 1
                if not m or not f.exists() or i >= len(pg) or len(pg[i]) != len(m["w"]): continue
                x, rate = lire(f); m["w"], n = recaler(x, rate, m["w"], pg[i]); chg += n; pistes += 1
            tot += chg
            if chg and not essai: fj.write_text(json.dumps(meta, ensure_ascii=False, separators=(",", ":")))
            print(f"{v}/{sous + '/' if sous else ''}{fj.stem} : {chg} retouche(s)", flush=True)
    print(tot, "retouche(s) sur", pistes, "piste(s)", "(essai : rien d'écrit)" if essai else "")
