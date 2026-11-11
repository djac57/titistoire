# Titistoire — Mon Petit Conteur

De belles histoires à écouter et à regarder, pour les 3-6 ans (dans l'esprit de *Lunii*), dans le navigateur.

**En ligne :** https://djac57.github.io/titistoire/

## Ce qu'on y trouve

- **40 histoires écrites une par une** : 4 héros × 10 univers. Chaque histoire a son vrai sujet (dire non, la colère, dire au revoir, le petit frère, savoir perdre…), jamais énoncé : pas de « la morale de l'histoire ».
- **4 héros qui ont du caractère** : Filou le renard (malin, un peu vantard), Nestor l'ourson (doux, peureux, gourmand), Rosie la lapine (rapide, veut gagner), Plume la chouette (rêveuse, mille questions).
- **Des personnages qui reviennent** d'une histoire à l'autre dans chaque univers : Griffard le chat pirate, Grondar le tyrannosaure, Braise la dragonne, Bip le robot, Gloup, Margot la pie, Ondine la baleine…
- **Trois façons de choisir** : par héros puis par lieu, par sujet (« une histoire pour parler de… »), ou au hasard.
- **Des histoires de saison** (Noël, Halloween, ski, plage) qui passent en tête de l'accueil, avec un habillage du site assorti, quand c'est la période. Pour prévisualiser : `?saison=noel` (ou `halloween`, `ski`, `mer`, `aucune`).
- **Un livre illustré** : 8 illustrations par histoire, une voix de conteuse pré-enregistrée, et le mot lu qui se surligne.
- **« J'invente la mienne »** (réservé, mot de passe) : on décrit un héros, un lieu, un sujet, et une histoire est écrite à la demande.

## Écrire ou retoucher une histoire

Tout est dans `histoires/` — des fichiers texte, un par héros, plus `saisons.txt` :

```
=== filou_pirates
titre: Filou et la carte à l'envers
sujet: Dire « je ne sais pas »        (affiché dans « Choisir un sujet »)
famille: oser                          (oser | coeur | autres | grandir)

@ {filou} standing proudly at the bow of {coquille}, sunny blue sea     <- un tableau = une illustration (en anglais)
Sur la mer toute bleue file La Coquille…                                 <- une ligne = une page lue
Filou est un renard qui sait tout faire. Du moins… c'est ce qu'il dit.
```

Une histoire = 8 tableaux de 3 pages. `{nom}` renvoie aux descriptions de `histoires/personnages.json` (pour garder les mêmes personnages d'une image à l'autre).

Après une retouche :

```
python3 tools/build_stories.py     # vérifie tout et régénère stories.js
```

Les images et les voix des tableaux modifiés sont refaites automatiquement au passage suivant.

## Images et voix

| | Outil | Moteur | Rythme gratuit |
|---|---|---|---|
| Illustrations | `tools/gen_images.py` → `assets/scenes/` | FLUX (Cloudflare Workers AI) | ≈ 100 images par jour |
| Voix | `tools/gen_voix.py` → `assets/voix/` | Gemini TTS + alignement mot à mot (faster-whisper) | ≈ 10 histoires par jour |

Deux actions GitHub (`gen-images.yml`, `gen-voix.yml`) tournent chaque jour, reprennent là où elles s'étaient arrêtées, publient ce qui est prêt, et s'arrêtent d'elles-mêmes quand tout est fait. Tant qu'une histoire n'a pas ses images ou sa voix, l'appli se replie proprement (illustration d'ambiance, lecture en direct).

- Changer de voix : écouter `essais-voix/`, puis `python3 tools/gen_voix.py --voix Nom` (ou le champ *voix* de l'action).
- Refaire une image ratée : action « Générer les illustrations », champ *refaire* (ex. `filou_pirates_3`).

## Le worker (`worker/ai-worker.js`)

Petit service Cloudflare, déployé automatiquement à chaque modification : il écrit les histoires du mode « J'invente la mienne », lit les pages en direct quand une voix n'est pas encore enregistrée, et dessine à la demande. Les clés sont des secrets GitHub / Cloudflare, jamais dans le code.
