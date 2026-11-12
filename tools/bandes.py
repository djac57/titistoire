#!/usr/bin/env python3
"""Écrit worker/bandes.js : ce que le worker doit savoir des bandes des recueils (Comètes, Galaxies) pour inventer
une histoire « avec la bande » — le style d'image et la description fixe de chaque enfant viennent de
<recueil>/personnages.json (une seule source), le monde et les caractères sont résumés ici d'après les bibles.

    python3 tools/bandes.py
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

BANDES = {
    "cometes": {
        "nom": "la bande de Virevent",
        "monde": "Virevent, une petite ville posée dans une boucle de la Flânette, une rivière très lente. On y va partout à pied. Époque douce et sans date : ni voitures, ni écrans, ni téléphones ; des vélos, une péniche, des lettres, des réverbères qu'on allume à la main, on paie en sous. Lieux : la place du Beffroi (dont l'horloge retarde de cinq minutes et dont la girouette est une comète dorée), l'école et sa cour au grand cerisier, le bazar, le Fournil (la boulangerie), la maison haute (onze enfants), le quai des Saules où est amarrée la péniche L'Hirondelle, l'écluse, le moulin du menuisier, la petite île au saule avec sa cabane, la butte aux Alouettes. Chaque histoire finit à la tombée du jour, quand on allume les réverbères.",
        "enfants": {
            "jeanne": ("Jeanne", "7 ans, la plus petite, tignasse rousse, salopette rouge. Veut qu'on l'écoute ; elle « arrondit » tout (trois devient trente), promet la lune, invente des mots (« archi-véridique », « juré-craché-mouillé »). Quand elle en rajoute, ses joues se gonflent. Sa phrase : « Vous n'allez pas me croire ! » Septième de onze enfants ; promène son petit frère Titou."),
            "gaspard": ("Gaspard", "8 ans, trapu, lunettes rondes, gilet turquoise, un crayon très court sur l'oreille. Veut que ce soit juste : il compte tout dans un carnet, mauvais perdant, ne sait pas dire pardon sans ajouter « mais », mais tient toujours parole. Parle en « Premièrement… deuxièmement… ». Sa phrase : « J'ai compté. » Vit une semaine à l'écluse chez sa mère, une semaine au moulin chez son père."),
            "suzie": ("Suzie", "7 ans, ronde, cheveux blonds en nuage, robe violette. Veut que tout le monde s'entende : elle dit oui à tout, range son avis au fond d'elle ; le jour où elle dit non, il en vaut mille. Parle doucement, par questions. Sa phrase : « Oui, oui… enfin, je crois. » Tortille une boucle de cheveux quand elle hésite. Fille des boulangers."),
            "marin": ("Marin", "8 ans, immense et mince, cheveux noirs, ciré jaune. Le nouveau, fils de mariniers, vit sur la péniche L'Hirondelle ; il a connu dix-sept écoles et voudrait un endroit où rester, sans l'avouer. Peu de mots, tous exacts, vocabulaire du bateau, humour pince-sans-rire. Sa phrase : « Ça m'est égal. » (presque toujours fausse). Se tient sur une jambe quand il n'est pas à l'aise."),
        },
    },
    "galaxies": {
        "nom": "les Bottes et les Tongs",
        "monde": "Lodenn, une petite île inventée au large de la Bretagne, à vingt-cinq minutes de navette de Port-Neuf, sur « la Grande Terre ». Pas une voiture ; des téléphones qui ne captent presque nulle part. L'île a la forme d'un poisson : le phare au nez, la chapelle sur la butte, le bourg, le port, la cale et le Môle de granit rose au ventre, la lande et la pierre levée (la Sentinelle) au dos, la plage des Dames et ses cabines rayées, l'école de voile, la crêperie « À la Rieuse » sur le quai, une vieille coque de bateau retournée qui sert de cabane. La marée monte et descend deux fois par jour et commande tout. Deux bandes : les Bottes (enfants de l'île) et les Tongs (enfants de l'été), longtemps rivales, désormais alliées. IMPORTANT : cette histoire est une aventure À PART, pendant le même été ; elle ne parle NI du trésor du capitaine, NI de la carte coupée en deux, et ne révèle rien du feuilleton.",
        "enfants": {
            "mael": ("Maël", "11 ans, chef des Bottes, grand, blond, ciré jaune, toujours un bout de corde. Taiseux, fier, juste ; il lit la mer mieux que les gens et ne sait ni demander ni s'excuser. Parle en bulletin météo marine (« Avis de grand frais sur les Tongs. », « Affirmatif. », « Calme plat. »)."),
            "enora": ("Enora", "10 ans, des Bottes, deux longues tresses rousses, pull vert. Rieuse, rapide, menteuse de génie : elle invente pour faire plus beau, si bien qu'on ne la croit plus quand elle dit vrai. Commence par « La vérité vraie, c'est que… ». Ses parents tiennent la crêperie."),
            "tino": ("Tino", "9 ans, des Bottes, le plus petit, salopette de ciré orange trop grande. Intrépide, exact, bavard ; il compte tout (pas, marches, rochers), répète mot pour mot ce qu'il entend, a peur des crabes. « C'est pas moi qui le dis, c'est Job. »"),
            "victoire": ("Victoire", "11 ans, cheffe des Tongs, queue-de-cheval noire, polo fuchsia. Brillante, raide, drôle malgré elle ; elle négocie tout (« Je propose un marché. », « Clause un… », « Objection. », « Marché conclu. ») et lit les vieilles écritures."),
            "awa": ("Awa", "10 ans, des Tongs, chignon de tresses, gilet de voile bleu, un sifflet au cou. Sportive, précise, loyale ; la meilleure barreuse de l'école de voile, elle sait les nœuds et la boussole et corrige tout le monde. Commence par « En fait… », et ce qui suit est exact."),
            "oscar": ("Oscar", "10 ans, des Tongs, rond, lunettes rouges, poncho violet, harmonica. Doux, drôle, douillet, enfant de la ville que tout ce qui est mouillé inquiète ; une oreille absolue : il fait la musique de sa propre vie (« Tadam ! ») et entend ce qui sonne faux."),
        },
    },
}

out = {}
for rec, b in BANDES.items():
    c = json.loads((ROOT / rec / "personnages.json").read_text(encoding="utf-8"))
    out[rec] = {"nom": b["nom"], "style": c["style"], "monde": b["monde"],
                "enfants": {k: {"nom": n, "qui": q, "desc": c["personnages"][k]} for k, (n, q) in b["enfants"].items()}}
    for k in b["enfants"]: assert (ROOT / rec / "refs" / f"{k}.jpg").exists(), f"fiche manquante : {rec}/{k}"
f = ROOT / "worker" / "bandes.js"
f.write_text("/* Généré par tools/bandes.py depuis <recueil>/personnages.json — ne pas modifier à la main. */\nexport const BANDES = "
             + json.dumps(out, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
print("✅", f.relative_to(ROOT), {k: list(v["enfants"]) for k, v in out.items()})
