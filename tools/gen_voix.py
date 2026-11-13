#!/usr/bin/env python3
"""Voix pré-enregistrées des histoires (une piste par tableau) + minutage mot à mot pour le karaoké.

Moteur : Gemini TTS (gratuit dans les quotas de la clé). Le minutage vient d'un alignement
par reconnaissance vocale (faster-whisper), qui sert aussi de contrôle qualité : si la voix
n'a pas lu le bon texte, l'enregistrement est refusé.

Le palier gratuit n'autorise que 10 requêtes par jour et par modèle. Une histoire ENTIÈRE est
donc lue en une seule requête (≈ 5 min d'audio), puis découpée en 8 pistes dans les silences
entre les tableaux : ≈ 10 histoires par jour avec le meilleur modèle, timbre constant.

    python3 tools/gen_voix.py                     # toutes les pistes manquantes (reprend où il s'est arrêté)
    python3 tools/gen_voix.py --only filou_       # seulement les histoires dont l'id commence par…
    python3 tools/gen_voix.py --limit 40          # au plus 40 pistes (quota du jour)
    python3 tools/gen_voix.py --essai Sulafat,Gacrux,Algieba   # même tableau lu par plusieurs voix -> essais-voix/
    python3 tools/gen_voix.py --voix Gacrux --refaire          # tout regénérer avec une autre voix

Clé : variable GEMINI_API_KEY, sinon ~/.config/gemini_key. Dépendance : pip install faster-whisper
Encodage : ffmpeg si présent, sinon afconvert (macOS).
"""
import argparse, base64, difflib, io, json, os, pathlib, re, shutil, subprocess, sys, tempfile, time, unicodedata, urllib.error, urllib.request, wave
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import titi

BASE = titi.ROOT / "assets" / "voix"
OUT = BASE            # dossier de la voix en cours : assets/voix/<Voix>/ (réglé dans main)
MODELES = [m.strip() for m in os.environ.get("TITI_TTS_MODELES", "gemini-3.8-flash-tts,gemini-3.1-flash-tts-preview").split(",") if m.strip()]
# gemini-2.5-flash-preview-tts n'est pas utilisé ici : son quota (10/jour) est laissé aux histoires inventées,
# et sa voix ralentit sur les longues lectures.
VOIX_DEFAUT = "Sulafat"
# Format « profil + notes + TRANSCRIPT » : seul le texte sous TRANSCRIPT est lu.
# (Une consigne en phrase libre est LUE À VOIX HAUTE par gemini-3.x-tts ; systemInstruction est refusé.)
CONSIGNE = ("# AUDIO PROFILE: La conteuse\n"
            "Une conteuse française chaleureuse, qui lit un album à un enfant de quatre ans.\n\n"
            "### DIRECTOR'S NOTES\n"
            "Style : voix douce, souriante et vivante ; elle joue légèrement les dialogues et les bruits.\n"
            "Rythme : posé, sans lenteur, avec de petites pauses entre les phrases.\n"
            "Langue : français de France.\n\n"
            "#### TRANSCRIPT\n")
QUALITE_MIN = 0.86      # part du texte retrouvée dans la reconnaissance vocale
# Histoires traduites (--langue) : consigne dans la langue, et reconnaissance vocale réglée sur elle.
LANGUE = "fr"
CONSIGNES = {"ar": ("# AUDIO PROFILE: الحكواتية\n"
                    "حكواتية مغربية حنينة، كتقرا قصة لطفل عندو ربع سنين.\n\n"
                    "### DIRECTOR'S NOTES\n"
                    "Style : صوت دافي ومبتسم وحيّ؛ كتمثّل شوية الحوار والأصوات.\n"
                    "Rythme : بالمهل، مع وقفات صغار بين الجمل.\n"
                    "Langue : الدارجة المغربية ديال كل نهار، بنطق مغربي، ماشي العربية الفصحى.\n\n"
                    "#### TRANSCRIPT\n")}
LENT = lambda: 4.5 if LANGUE == "ar" else 7      # débit le plus lent admis, en caractères par seconde (l'arabe n'écrit pas ses voyelles : moins de lettres pour la même durée)
# L'arabe s'écrit de plusieurs façons pour un même son : on ramène tout à une forme simple avant de comparer le texte à ce qui est entendu.
ARABE = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ى": "ي", "ئ": "ي", "ؤ": "و", "ة": "ه", "گ": "ك", "ڭ": "ك", "ڤ": "ف", "پ": "ب", "ـ": ""})


def cle():
    k = os.environ.get("GEMINI_API_KEY", "").strip()
    if not k:
        p = pathlib.Path.home() / ".config" / "gemini_key"
        if p.is_file():
            k = p.read_text().strip().split("=")[-1].strip().strip('"')
    if not k:
        sys.exit("Clé Gemini absente (GEMINI_API_KEY ou ~/.config/gemini_key)")
    return k


class Quota(Exception):
    pass


class QuotaJour(Quota):
    """Plafond QUOTIDIEN atteint (même en niveau payant : 100 requêtes par jour et par modèle) : inutile d'insister avant demain."""


def tts(texte, voix, modele, key):
    """-> PCM 16 bits mono, fréquence.
    Niveau payant (TITI_PAYANT=1) : la limite de débit est basse ; plusieurs enregistrements lancés en parallèle
    se partagent donc UN verrou et espacent leurs appels (TITI_TTS_ESPACE secondes), l'alignement se faisant hors verrou."""
    if os.environ.get("TITI_PAYANT") != "1":
        return _tts(texte, voix, modele, key)
    if os.environ.get("TITI_TTS_ESPACE") == "0":          # débit suffisant : appels en parallèle, simple patience sur un 429
        for essai in range(6):
            try: return _tts(texte, voix, modele, key)
            except QuotaJour: raise
            except Quota: time.sleep(30)
        raise Quota("limite de débit persistante")
    import fcntl
    esp = float(os.environ.get("TITI_TTS_ESPACE", "25")); verrou = pathlib.Path(tempfile.gettempdir()) / "titistoire_tts.lock"
    with open(verrou, "a+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            for essai in range(12):
                f.seek(0); dernier = float(f.read().strip() or 0)
                attente = dernier + esp - time.time()
                if attente > 0: time.sleep(attente)
                try:
                    return _tts(texte, voix, modele, key)
                except Quota:
                    time.sleep(40)
                finally:
                    f.seek(0); f.truncate(); f.write(str(time.time())); f.flush()
            raise Quota("limite de débit persistante")
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def _budget():
    """Réserve pour le site : au plus TITI_TTS_BUDGET appels par « jour de quota » (remis à zéro à 08:00 UTC). Sans cela, les enregistrements
    du catalogue consomment tout le quota de la voix et les histoires inventées n'en ont plus de la journée."""
    maxi = int(os.environ.get("TITI_TTS_BUDGET", "0") or 0)
    if not maxi: return
    import datetime
    jour = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=8)).strftime("%Y%m%d")
    f = pathlib.Path.home() / ".cache" / f"titistoire_tts_{jour}.txt"; f.parent.mkdir(exist_ok=True)
    n = int(f.read_text().strip() or 0) if f.exists() else 0
    if n >= maxi: raise QuotaJour(f"PerDay : réserve du site ({maxi} appels par jour pour le catalogue, {n} faits)")
    f.write_text(str(n + 1))


def _tts(texte, voix, modele, key):
    _budget()
    body = {"contents": [{"parts": [{"text": CONSIGNES.get(LANGUE, CONSIGNE) + texte}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voix}}}}}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{modele}:generateContent?key={key}",
        data=json.dumps(body).encode(), headers={"content-type": "application/json"})
    try:
        d = json.load(urllib.request.urlopen(req, timeout=180))
    except urllib.error.HTTPError as e:
        msg = e.read().decode("utf-8", "replace")
        if e.code == 429:
            raise (QuotaJour if "PerDay" in msg else Quota)(re.sub(r"\s+", " ", msg)[:400])
        raise RuntimeError(f"HTTP {e.code} {msg[:200]}")
    try:
        part = d["candidates"][0]["content"]["parts"][0]["inlineData"]
    except Exception:
        raise RuntimeError("réponse sans audio : " + json.dumps(d)[:200])
    raw = base64.b64decode(part["data"])
    if raw[:4] == b"RIFF":
        w = wave.open(io.BytesIO(raw))
        if w.getnchannels() != 1 or w.getsampwidth() != 2:
            raise RuntimeError("format WAV inattendu")
        return w.readframes(w.getnframes()), w.getframerate()
    m = re.search(r"rate=(\d+)", part.get("mimeType", ""))
    return raw, int(m.group(1)) if m else 24000


def ecrire_wav(pcm, rate, path):
    w = wave.open(str(path), "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(pcm); w.close()


def encoder(wav, m4a):
    if shutil.which("ffmpeg"):
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-ac", "1", "-c:a", "aac", "-b:a", "56k", "-movflags", "+faststart", str(m4a)]
    elif shutil.which("afconvert"):
        cmd = ["afconvert", "-f", "m4af", "-d", "aac", "-b", "56000", str(wav), str(m4a)]
    else:
        sys.exit("Ni ffmpeg ni afconvert pour encoder l'audio")
    subprocess.run(cmd, check=True)


# ---------- alignement ----------
_modele_asr = None
def asr():
    global _modele_asr
    if _modele_asr is None:
        from faster_whisper import WhisperModel
        _modele_asr = WhisperModel(os.environ.get("TITI_ASR", "small"), device="cpu", compute_type="int8")
    return _modele_asr


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(ch for ch in s if ch.isalnum() and not unicodedata.combining(ch))
    return s.translate(ARABE) if LANGUE == "ar" else s


def aligner(pcm, rate, pages):
    """-> (minutage par page : liste des débuts de chaque mot, qualité 0..1, durée)"""
    import numpy as np
    x = np.frombuffer(pcm, dtype="<i2").astype("float32") / 32768.0
    if rate != 16000:                                 # whisper attend du 16 kHz
        n = int(len(x) * 16000 / rate)
        x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype("float32")
    segs, info = asr().transcribe(x, language=LANGUE, word_timestamps=True, beam_size=5,
                                  initial_prompt=" ".join(pages)[:400], condition_on_previous_text=False)
    hc, ht = [], []                                   # caractères reconnus + instant de chacun
    for sg in segs:
        for w in (sg.words or []):
            n = norm(w.word)
            for i, ch in enumerate(n):
                hc.append(ch); ht.append(w.start + (w.end - w.start) * i / max(1, len(n)))
    tokens = [(pi, tok) for pi, p in enumerate(pages) for tok in p.split()]
    tc, tw = [], []                                   # caractères attendus + index du mot
    for wi, (_, tok) in enumerate(tokens):
        for ch in norm(tok):
            tc.append(ch); tw.append(wi)
    sm = difflib.SequenceMatcher(None, "".join(tc), "".join(hc), autojunk=False)
    debut = [None] * len(tokens); ok = 0
    for a, b, size in sm.get_matching_blocks():
        for k in range(size):
            ok += 1
            wi = tw[a + k]
            if debut[wi] is None:
                debut[wi] = ht[b + k]
    qual = ok / max(1, len(tc))
    duree = len(pcm) / 2 / rate
    # mots sans repère (ponctuation seule, mot mal reconnu) : interpolation entre voisins
    connus = [(i, t) for i, t in enumerate(debut) if t is not None]
    if not connus:
        return None, 0.0, len(pcm) / 2 / rate
    for i in range(len(debut)):
        if debut[i] is None:
            av = [(j, t) for j, t in connus if j < i]; ap = [(j, t) for j, t in connus if j > i]
            if av and ap:
                (j0, t0), (j1, t1) = av[-1], ap[0]
                debut[i] = t0 + (t1 - t0) * (i - j0) / (j1 - j0)
            elif ap:
                # Mots du TOUT DÉBUT non reconnus : on remonte depuis le premier mot reconnu, au débit moyen de la lecture.
                # (Les coller au premier mot reconnu faisait couper le début de l'histoire au découpage.)
                j0, t0 = ap[0]; jn, tn = connus[-1]
                car = lambda a_, b_: sum(len(norm(tokens[k][1])) + 1 for k in range(a_, b_))
                cps = car(j0, jn) / (tn - t0) if tn - t0 > 2 and jn > j0 else 14.0
                debut[i] = max(0.0, t0 - car(i, j0) / max(8.0, min(22.0, cps)))
            else:
                debut[i] = av[-1][1] + 0.05
    for i in range(1, len(debut)):                    # jamais de retour en arrière
        debut[i] = max(debut[i], debut[i - 1])
    par_page = [[] for _ in pages]
    for (pi, _), t in zip(tokens, debut):
        par_page[pi].append(round(t, 2))
    return par_page, qual, duree


def produire(pages, voix, key, m4a, modele):
    """Génère + aligne + encode une piste avec CE modèle. -> dict de minutage, ou lève Quota."""
    texte = "\n\n".join(pages)
    dernier = None
    for essai in range(3):
        try:
            pcm, rate = tts(texte, voix, modele, key)
        except Quota:
            raise
        except Exception as e:
            dernier = str(e)[:160]; print(f"      …{modele} : {dernier}", flush=True); time.sleep(4)
            continue
        w, qual, duree = aligner(pcm, rate, pages)
        n_car = len(texte)
        # refus : texte mal lu, débit aberrant, ou voix qui ne démarre pas sur le texte (consigne lue, long blanc)
        if w is None or qual < QUALITE_MIN or not (n_car / 26 < duree < n_car / LENT()) or w[0][0] > 2.0 or duree - w[-1][-1] > 6.0:
            print(f"      …piste refusée (qualité {qual:.2f}, durée {duree:.1f}s, début {w[0][0] if w else '?'}s), nouvel essai", flush=True)
            dernier = f"qualité {qual:.2f}"
            continue
        with tempfile.TemporaryDirectory() as td:
            wav = pathlib.Path(td) / "a.wav"
            ecrire_wav(pcm, rate, wav)
            m4a.parent.mkdir(parents=True, exist_ok=True)
            encoder(wav, m4a)
        return {"d": round(duree, 2), "w": w, "q": round(qual, 3), "m": modele}
    raise RuntimeError(dernier or "échec")


def attaque(pcm, rate):
    """Instant où la voix commence : premier passage d'au moins 0,1 s nettement au-dessus du bruit de fond."""
    import numpy as np
    x = np.frombuffer(pcm, dtype="<i2").astype("float32")
    pas = int(rate * 0.02); n = len(x) // pas
    if n < 10: return 0.0
    rms = np.sqrt((x[: n * pas].reshape(n, pas) ** 2).mean(axis=1) + 1e-9)
    seuil = max(np.median(rms) * 0.08, rms.max() * 0.012); fort = rms > seuil
    for i in range(n - 5):
        if fort[i:i + 5].all(): return i * 0.02
    return 0.0


def coupes(pcm, rate, bornes):
    """Pour chaque frontière (fin du dernier mot connu, début du mot suivant), l'instant le plus calme."""
    import numpy as np
    x = np.frombuffer(pcm, dtype="<i2").astype("float32")
    pas = int(rate * 0.02)
    n = len(x) // pas
    rms = np.sqrt((x[: n * pas].reshape(n, pas) ** 2).mean(axis=1) + 1e-9)
    out = []
    for t0, t1 in bornes:
        a, b = int((t0 + 0.25) / 0.02), int(t1 / 0.02)
        if b - a < 3:
            out.append(max(t0, t1 - 0.3)); continue
        seg = rms[a:b]
        seuil = max(seg.min() * 2.5, np.median(rms) * 0.08)
        best, start, cur = (0, a), None, 0
        for i, v in enumerate(seg):
            if v <= seuil:
                if start is None: start = i
                cur = i - start + 1
                if cur > best[0]: best = (cur, a + start)
            else:
                start = None
        ln, st = best
        if ln == 0:
            out.append(max(t0, t1 - 0.3))
        else:                                           # on coupe aux 2/3 du silence : la piste suivante garde un court souffle
            out.append(min(t1 - 0.12, (st + ln * 0.66) * 0.02))
    return out


def produire_histoire(s, voix, key, modele, decal=0):
    """Lit toute l'histoire en UNE requête, aligne, découpe en 8 pistes. -> {n°: minutage} ou lève Quota."""
    pages = [p for sc in s["scenes"] for p in sc["pages"]]
    texte = "\n\n\n".join("\n\n".join(sc["pages"]) for sc in s["scenes"])
    n_car = len(texte)
    pcm, rate = tts(texte, voix, modele, key)
    w, qual, duree = aligner(pcm, rate, pages)
    # Refus seulement si le texte est mal lu, le débit aberrant, ou si la voix lit autre chose avant le texte (> 8 s).
    # Un simple blanc au début ou à la fin n'est pas un défaut : on le coupe.
    if w is None or qual < QUALITE_MIN or not (n_car / 26 < duree < n_car / LENT()) or w[0][0] > 8.0:
        raise RuntimeError(f"enregistrement refusé (qualité {qual:.2f}, durée {duree:.0f}s pour {n_car} car., début {w[0][0] if w else '?'} s)")
    # Début de la piste : là où la voix commence VRAIMENT (énergie du signal), pas au premier mot reconnu —
    # la reconnaissance vocale rate parfois les premiers mots, et l'histoire commençait alors au milieu d'une phrase.
    debut = max(0.0, min(w[0][0] - 0.3, attaque(pcm, rate) - 0.5))
    if debut > 0.2:
        pcm = pcm[int(debut * rate) * 2:]; w = [[round(t - debut, 2) for t in pg] for pg in w]; duree -= debut
    fin = min(duree, w[-1][-1] + 2.5)
    if duree - fin > 0.5:
        pcm = pcm[:int(fin * rate) * 2]; duree = fin
    # regroupe le minutage par tableau
    par_sc, k = [], 0
    for sc in s["scenes"]:
        par_sc.append(w[k:k + len(sc["pages"])]); k += len(sc["pages"])
    bornes = [(par_sc[i][-1][-1], par_sc[i + 1][0][0]) for i in range(len(par_sc) - 1)]
    cuts = [0.0] + coupes(pcm, rate, bornes) + [duree]
    res = {}
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        for i, sc in enumerate(s["scenes"], 1):
            a, b = cuts[i - 1], cuts[i]
            ia, ib = int(a * rate) * 2, int(b * rate) * 2
            wav = pathlib.Path(td) / f"{i}.wav"
            ecrire_wav(pcm[ia:ib], rate, wav)
            encoder(wav, OUT / f"{s['id']}_{i + decal}.m4a")       # decal : numéro du premier tableau du morceau (histoires longues lues en plusieurs requêtes)
            # minutage recalé sur les silences du signal (début de piste, mots charnières entre deux pages) : tools/recaler_voix.py
            import numpy as np, recaler_voix
            wp, _ = recaler_voix.recaler(np.frombuffer(pcm[ia:ib], dtype="<i2").astype("float32"), rate, [[round(max(0.0, t - a), 2) for t in pg] for pg in par_sc[i - 1]], sc["pages"])
            res[str(i + decal)] = {"d": round(b - a, 2), "w": wp, "sig": signature(sc["pages"])}
    return res, qual, duree


def signature(pages):
    return str(len("\n".join(pages))) + ":" + str(hash_txt(pages))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voix", default="")
    ap.add_argument("--only", default="")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--essai", default="")
    ap.add_argument("--refaire", action="store_true")
    ap.add_argument("--petits", action="store_true", help="versions Lucioles (1-3 ans) : histoires/petits/, pistes dans assets/voix/<Voix>/petits/")
    ap.add_argument("--recueil", default="", help="recueil des grands (cometes, galaxies) : <recueil>/histoires/, pistes dans assets/voix/<Voix>/<recueil>/")
    ap.add_argument("--langue", default="", help="histoires traduites (langues/<langue>/) : pistes dans assets/voix/<Voix>/<langue>/")
    a = ap.parse_args()
    # assets/voix/voix.txt : les voix proposées dans l'appli, une par ligne. La 1re est celle par défaut ;
    # elle est enregistrée pour TOUTES les histoires avant qu'on passe à la suivante.
    fv = BASE / "voix.txt"
    liste = [l.strip() for l in (fv.read_text().split("\n") if fv.exists() else []) if l.strip()] or [VOIX_DEFAUT]
    if a.voix:
        liste = [a.voix]
    key = cle()
    if a.recueil:
        import recueil as _rec
        stories = _rec.load(a.recueil)
    else:
        stories = titi.load_petits() if a.petits else titi.load()
    if a.langue:                                        # mêmes histoires, texte de la langue ; seules les histoires traduites sont enregistrées
        global LANGUE, QUALITE_MIN
        import langues as _lg
        T = _lg.load(a.langue); LANGUE = a.langue; QUALITE_MIN = float(os.environ.get("TITI_QUALITE_MIN", "0.6"))
        stories = [dict(s, titre=T[s["id"]]["t"], scenes=[dict(sc, pages=T[s["id"]]["sc"][k]) for k, sc in enumerate(s["scenes"])]) for s in stories if s["id"] in T]
    dispo = list(MODELES)                               # modèles dont le quota du jour n'est pas épuisé

    if a.essai:                                         # banc d'essai de voix
        dst = titi.ROOT / "essais-voix"; dst.mkdir(exist_ok=True)
        s = next(x for x in stories if x["id"] == (a.only or "filou_pirates"))
        pages = s["scenes"][0]["pages"]
        for v in [x.strip() for x in a.essai.split(",") if x.strip()]:
            f = dst / f"{v}.m4a"
            if f.exists():
                continue
            while dispo:
                try:
                    r = produire(pages, v, key, f, dispo[0])
                    print(f"  ✅ {v} ({r['d']} s, qualité {r['q']}, {r['m']})", flush=True); break
                except Quota as q:
                    print(f"  quota épuisé sur {dispo[0]} : {str(q)[:200]}"); dispo.pop(0)
                except Exception as e:
                    print(f"  ❌ {v} : {e}"); break
        return

    # Une histoire garde le MÊME modèle du début à la fin (timbre constant).
    global OUT
    fait = saute = 0
    for voix, s in [(v, s) for v in liste for s in stories]:
        a.voix = voix
        OUT = BASE / voix / a.langue if a.langue else BASE / voix / a.recueil if a.recueil else (BASE / voix / "petits" if a.petits else BASE / voix)
        if a.only and not s["id"].startswith(a.only):
            continue
        if not dispo:
            break
        fj = OUT / f"{s['id']}.json"
        meta = json.loads(fj.read_text()) if fj.exists() else {}
        if a.refaire or meta.get("voix") != a.voix:
            meta = {"voix": a.voix, "sc": {}}
        manque = [i for i, sc in enumerate(s["scenes"], 1)
                  if not (meta["sc"].get(str(i), {}).get("sig") == signature(sc["pages"]) and (OUT / f"{s['id']}_{i}.m4a").exists())]
        nsc = len(s["scenes"]); saute += nsc - len(manque)
        if not manque:
            continue
        if a.limit and fait >= a.limit:
            print(f"Limite de {a.limit} pistes atteinte."); break

        def sauver():
            OUT.mkdir(parents=True, exist_ok=True)
            fj.write_text(json.dumps(meta, ensure_ascii=False, separators=(",", ":")))

        if len(manque) * 2 > nsc:                       # l'essentiel est à (re)faire : histoire entière, en une requête — ou en quelques morceaux si elle est longue
            payant = os.environ.get("TITI_PAYANT") == "1"      # niveau payant : un 429 est une limite de débit, on patiente
            morceaux, cur_, car = [], [], 0                   # morceaux de tableaux consécutifs d'au plus ~4 500 caractères (ce que le modèle lit bien d'une traite)
            for k, sc in enumerate(s["scenes"]):
                c = sum(len(p) for p in sc["pages"])
                if cur_ and car + c > 4500: morceaux.append(cur_); cur_, car = [], 0
                cur_.append(k); car += c
            if cur_: morceaux.append(cur_)
            tout, ok = {}, True
            for mor in morceaux:
                sous = {"id": s["id"], "scenes": [s["scenes"][k] for k in mor]}; fait_mor = False
                for essai in range(8 if payant else 2):
                    if not dispo:
                        break
                    modele = dispo[0]
                    try:
                        res, qual, duree = produire_histoire(sous, a.voix, key, modele, decal=mor[0])
                    except QuotaJour:
                        print(f"⛔ Plafond quotidien atteint sur {modele} : la suite demain", flush=True); dispo.pop(0); continue
                    except Quota as q:
                        if payant:
                            print(f"  …limite de débit, pause 45 s ({str(q)[:80]})", flush=True); time.sleep(45); continue
                        print(f"⛔ Quota du jour atteint sur {modele}", flush=True); dispo.pop(0); continue
                    except Exception as e:
                        print(f"  ❌ {s['id']} ({modele}) : {str(e)[:200]}", flush=True); time.sleep(5); continue
                    tout.update(res); fait_mor = True; fait += len(mor)
                    print(f"  ✅ {s['id']} — tableaux {mor[0] + 1} à {mor[-1] + 1} ({duree:.0f} s, qualité {qual:.3f}, {modele})", flush=True)
                    break
                time.sleep(float(os.environ.get("TITI_TTS_PAUSE", "8")))
                if not fait_mor: ok = False; break
            if tout:                                         # ce qui est enregistré est gardé, même si l'histoire n'est pas finie (reprise au passage suivant)
                meta.update({"m": modele}); meta["sc"] = {**{k: v for k, v in meta.get("sc", {}).items() if v.get("sig") == signature(s["scenes"][int(k) - 1]["pages"])}, **tout}; sauver()
            continue

        modele = meta.get("m") or dispo[0]               # histoire commencée : on complète tableau par tableau, même modèle
        if modele not in dispo:
            continue
        meta["m"] = modele
        for i in manque:
            sc = s["scenes"][i - 1]
            try:
                r = produire(sc["pages"], a.voix, key, OUT / f"{s['id']}_{i}.m4a", modele)
            except Quota:
                print(f"⛔ Quota du jour atteint sur {modele}", flush=True); dispo.remove(modele); break
            except Exception as e:
                print(f"  ❌ {s['id']} tableau {i} : {e}", flush=True); continue
            r.pop("m", None); r.pop("q", None); r["sig"] = signature(sc["pages"])
            meta["sc"][str(i)] = r; sauver(); fait += 1
            print(f"  ✅ {s['id']} {i}/{nsc} ({r['d']} s)", flush=True)
            time.sleep(float(os.environ.get("TITI_TTS_PAUSE", "8")))
    bilan(stories, fait, saute)


def hash_txt(pages):
    import zlib
    return zlib.crc32("\n".join(pages).encode("utf-8"))


def bilan(stories, fait, saute):
    total = sum(len(s["scenes"]) for s in stories)
    print(f"Voix : {fait} pistes générées cette fois.")
    for d in sorted(x for x in BASE.iterdir() if x.is_dir()) if BASE.exists() else []:
        print(f"  {d.name} : {len(list(d.glob('*.m4a')))} / {total} pistes")


if __name__ == "__main__":
    main()
