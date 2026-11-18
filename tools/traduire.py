#!/usr/bin/env python3
"""Traduit les histoires (Étoiles) dans une langue avec Gemini, au format de langues/<langue>/*.txt.

    python3 tools/traduire.py ar [--only id1,id2] [--limit N]

- Une histoire par requête, découpage imposé (même nombre de pages par tableau), vérifié avant écriture.
- Les prénoms sont fixés dans langues/<langue>/noms.json (complété au fil de l'eau par les nouveaux noms).
- Les histoires déjà traduites sont sautées. Clé : ~/.config/gemini_key_titistoire.
"""
import json, pathlib, sys, time, urllib.request, urllib.error
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import titi, langues

ROOT = titi.ROOT
KEY = (pathlib.Path.home() / ".config/gemini_key_titistoire").read_text().strip()
MODELES = ["gemini-3.8-flash", "gemini-flash-latest"]
CONSIGNE_NOMS = {
    "ar": 'Pour tout autre personnage nommé, choisis un prénom ou un surnom arabe court, facile pour un petit enfant, et indique-le dans "nouveaux_noms" (nom français -> nom traduit).',
    # anglais : les héros gardent leur prénom (Filou, Nestor, Rosie, Plume) ; seuls les noms qui veulent dire quelque chose sont adaptés, et toujours de la même façon
    "en": 'Les héros gardent leur prénom français tel quel (Filou, Nestor, Rosie, Plume), comme tout prénom qui se dit bien en anglais. Un nom qui veut dire quelque chose (surnom, nom de bateau, « Mamie… », « Monsieur… ») reçoit un équivalent anglais court et amusant. Indique dans "nouveaux_noms" CHAQUE nom de personnage ou de lieu inventé rencontré (nom français -> nom utilisé en anglais, identique s\'il ne change pas), pour qu\'il reste le même d\'une histoire à l\'autre.',
}
CONSIGNE_PLUS = {
    "en": "Ponctuation ANGLAISE des dialogues : guillemets “ ” (jamais « »), et l'incise HORS des guillemets (“That was just a test,” stammers Filou. “Hard to starboard!”), pas à la française.\n",
}
NOM_LANGUE = {"ar": "arabe standard moderne (fusha), SANS voyelles écrites (pas de harakat)", "en": "anglais britannique"}


def guillemets(p, langue):
    """En anglais, les dialogues s'écrivent entre “ ” et non entre « »."""
    if langue != "en":
        return p
    import re
    return re.sub(r"\s*»", "”", re.sub(r"«\s*", "“", p))


def appel(prompt, schema):
    corps = {"contents": [{"role": "user", "parts": [{"text": prompt}]}],
             "generationConfig": {"temperature": 0.4, "responseMimeType": "application/json", "responseSchema": schema}}
    for m in MODELES:
        for essai in range(4):
            req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}",
                                         data=json.dumps(corps).encode(), headers={"Content-Type": "application/json"})
            try:
                r = json.load(urllib.request.urlopen(req, timeout=300))
                return json.loads(r["candidates"][0]["content"]["parts"][0]["text"])
            except urllib.error.HTTPError as e:
                msg = e.read().decode()[:300]
                print(f"   {m} HTTP {e.code} : {msg[:160]}", flush=True)
                if e.code == 429 and "PerDay" in msg:
                    break
                time.sleep(20 * (essai + 1))
            except Exception as e:  # réponse vide, JSON cassé, délai
                print(f"   {m} erreur : {e}", flush=True)
                time.sleep(10)
    return None


def main():
    langue = sys.argv[1]
    only = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--only=")), "")
    limit = int(next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--limit=")), "0"))
    d = ROOT / "langues" / langue
    d.mkdir(parents=True, exist_ok=True)
    noms_f = d / "noms.json"
    noms = json.loads(noms_f.read_text(encoding="utf-8")) if noms_f.exists() else {}
    deja = langues.load(langue)
    faites = 0
    for s in titi.load():
        if s["id"] in deja or (only and s["id"] not in only.split(",")):
            continue
        if limit and faites >= limit:
            break
        forme = [len(sc["pages"]) for sc in s["scenes"]]
        src = {"titre": s["titre"], "tableaux": [sc["pages"] for sc in s["scenes"]]}
        prompt = f"""Tu traduis une histoire pour enfants de 3 à 6 ans, du français vers l'{NOM_LANGUE[langue]}.
Elle sera LUE À VOIX HAUTE par une voix de synthèse : phrases naturelles, simples, rythmées, chaleureuses ; garde les onomatopées, les répétitions, l'humour et les dialogues entre « ».
Adapte avec naturel (pas de mot à mot), mais garde EXACTEMENT le même découpage : même nombre de tableaux, et dans chaque tableau le même nombre de pages, chaque page traduite à la même place ({forme}).
Prénoms : utilise OBLIGATOIREMENT ces équivalents déjà fixés : {json.dumps(noms, ensure_ascii=False)}.
{CONSIGNE_NOMS.get(langue, CONSIGNE_NOMS["ar"])}
{CONSIGNE_PLUS.get(langue, "")}Pas de références religieuses ajoutées ; les fêtes (Noël, Halloween) restent telles quelles, nommées simplement.

HISTOIRE (JSON) :
{json.dumps(src, ensure_ascii=False)}"""
        schema = {"type": "OBJECT", "properties": {
            "titre": {"type": "STRING"},
            "tableaux": {"type": "ARRAY", "items": {"type": "ARRAY", "items": {"type": "STRING"}}},
            "nouveaux_noms": {"type": "ARRAY", "items": {"type": "OBJECT", "properties": {"fr": {"type": "STRING"}, "trad": {"type": "STRING"}}, "required": ["fr", "trad"]}}},
            "required": ["titre", "tableaux"]}
        t0 = time.time()
        r = None
        for _ in range(3):
            r = appel(prompt, schema)
            if r and [len(t) for t in r["tableaux"]] == forme and all(p.strip() for t in r["tableaux"] for p in t):
                break
            print(f"   découpage incorrect pour {s['id']}, nouvel essai", flush=True)
            r = None
        if not r:
            print(f"❌ {s['id']} : échec", flush=True)
            continue
        for n in r.get("nouveaux_noms") or []:
            noms.setdefault(n["fr"], n["trad"])
        noms_f.write_text(json.dumps(noms, ensure_ascii=False, indent=1), encoding="utf-8")
        fichier = d / f"{s['hero']}.txt"
        bloc = [f"\n=== {s['id']}", f"titre: {r['titre'].strip()}", ""]
        for t in r["tableaux"]:
            bloc += [guillemets(p.replace("\n", " ").strip(), langue) for p in t] + [""]
        if not fichier.exists():
            fichier.write_text(f"# Histoires de {s['hero']} — {NOM_LANGUE[langue]}. Traduction automatique (Gemini) à faire relire.\n", encoding="utf-8")
        with fichier.open("a", encoding="utf-8") as f:
            f.write("\n".join(bloc) + "\n")
        faites += 1
        print(f"✅ {s['id']} ({round(time.time() - t0)} s)", flush=True)
    print(f"FIN : {faites} histoire(s) traduite(s)")


if __name__ == "__main__":
    main()
