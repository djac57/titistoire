# Titistoire — Mon Petit Conteur

De belles histoires à écouter et à regarder, dans le navigateur, pour les enfants de 1 à 10 ans (dans l'esprit de *Lunii* et des albums jeunesse).

**En ligne :** https://titistoire.fr

## Quatre groupes d'âge

| Groupe | Âge | Ce que c'est | Source |
|---|---|---|---|
| **Les Lucioles** | 1-3 ans | Les 40 histoires des Étoiles en version courte : 8 pages d'une ou deux phrases, sur les mêmes images | `histoires/petits/` |
| *Imagiers des Lucioles* | 1-3 ans | Couleurs, nombres, formes, alphabet : le générateur ne dessine que des objets seuls, `tools/imagiers.py` pose lettres, chiffres et formes et répète l'objet le bon nombre de fois | `imagiers/` |
| **Les Étoiles** | 3-6 ans | 40 histoires : 4 héros (Filou, Nestor, Rosie, Plume) × 10 univers, 8 tableaux de 3 pages, une image par page | `histoires/` |
| **Les Comètes** | 6-8 ans | *Une année à Virevent* : 12 histoires, une par mois, avec une bande de quatre enfants (Jeanne, Gaspard, Suzie, Marin). 12 tableaux, une image par tableau, récit au passé simple | `cometes/` |
| **Les Galaxies** | 8-10 ans | *Le Trésor coupé en deux* : un feuilleton à énigmes en 8 épisodes sur l'île de Lodenn, deux bandes rivales, une carte de corsaire à consulter. Une image par épisode | `galaxies/` |

Le groupe se choisit en haut de l'accueil et reste mémorisé. Les histoires de saison des Étoiles (Noël, Halloween, ski, plage) n'apparaissent que pendant leur période (`?saison=noel|halloween|ski|mer|aucune` pour prévisualiser). Deux habillages : nuit étoilée et jour.

**« Je crée mon histoire »** (compte parent, 3 créations offertes) : on choisit l'âge, puis son propre héros ou — chez les Comètes et les Galaxies — la bande du recueil ; l'histoire est écrite, contrôlée, illustrée (8 images) et lue à la demande.

## La méthode (apprise à nos dépens)

On construit un recueil **dans cet ordre** : la bible (personnages, lieux, objets, synopsis) → les fiches dessinées de chaque personnage → les histoires → les images → la relecture.

- Chaque personnage a une **description visuelle fixe** et une **fiche** (image de référence). Les scènes sont dessinées d'après les fiches, et le texte de la demande rappelle toute la description (costume et accessoires compris).
- **Trois personnages au plus par image**, placés, avec le compte exact en fin de description. Au-delà : doublons, fusions, costumes qui passent de l'un à l'autre.
- On décrit **ce qu'on doit voir**, jamais ce qu'on ne veut pas (« pas de… » fait apparaître la chose). Pas de sujet « tout petit au loin » (il se dédouble). Pas de texte dans l'image, pas de nombre d'objets à compter.
- Une tenue différente de la fiche (maillot de bain, cheveux mouillés) demande **sa propre fiche**.
- Toute nouvelle image est dessinée **dans un dossier à part**, comparée à l'ancienne par des relecteurs, et on garde la meilleure.
- La morale n'est jamais énoncée. Les textes sont relus d'affilée pour la continuité.

## Écrire ou retoucher

### Étoiles et Lucioles

```
=== filou_pirates
titre: Filou et la carte à l'envers
sujet: Dire « je ne sais pas »            (affiché dans « Choisir un sujet »)
famille: oser                              (oser | coeur | autres | grandir)

@ {filou} standing proudly at the bow…    <- image de la 1re page du tableau (en anglais)
Sur la mer toute bleue file La Coquille…   <- une ligne = une page lue
> {filou} on the deck, chest puffed out…   <- image de la page suivante
Filou est un renard qui sait tout faire…
```

`{nom}` renvoie à `histoires/personnages.json` (`{filou}` avec le costume de l'univers, `{filou-}` sans). La version Lucioles d'une histoire est dans `histoires/petits/` : 8 lignes, une par tableau, lue sur la première image du tableau.

```
python3 tools/build_stories.py     # vérifie tout et régénère stories.js
```

### Comètes et Galaxies

Un dossier par recueil : `BIBLE.md`, `personnages.json` (style, personnages, lieux, objets), `histoires/*.txt`, `refs/` (fiches), `scenes/` (images). Format des histoires en tête de `tools/recueil.py`.

```
python3 tools/recueil.py cometes              # vérifie et écrit cometes/recueil.js
python3 tools/recueil.py cometes --fiches     # dessine les fiches manquantes
python3 tools/recueil.py cometes --images     # dessine les scènes manquantes
```

La carte des Galaxies (`galaxies/carte_1.svg` … `carte_3.svg`) est dessinée à la main par `tools/carte_galaxies.py` : le générateur d'images ne sait ni écrire ni respecter une géographie, et les énigmes dépendent d'alignements exacts.

## Images et voix

| | Outil | Moteur |
|---|---|---|
| Fiches de personnages | `tools/gen_images2.py --fiches`, `tools/recueil.py --fiches` | FLUX.2 dev (Cloudflare Workers AI) |
| Scènes | `tools/gen_images2.py`, `tools/recueil.py --images` | FLUX.2 klein, d'après les fiches ; les récalcitrantes en FLUX.2 dev |
| Voix | `tools/gen_voix.py` (`--petits`, `--recueil cometes`) | Gemini TTS, puis calage mot à mot par reconnaissance vocale |

Trois voix : Sulafat (par défaut), Vindemiatrix, Algieba, dans `assets/voix/<Voix>/` (sous-dossiers `petits/`, `cometes/`, `galaxies/`). Une histoire courte est lue en une seule demande puis découpée par tableau ; une histoire longue en quelques morceaux. Chaque enregistrement porte la signature du texte lu : l'appli ne le joue que s'il correspond au texte affiché.

Limites à connaître : le meilleur modèle de voix est plafonné à 100 demandes par jour ; le modèle d'image renvoie souvent des erreurs passagères, d'où les boucles de relance.

Les actions GitHub (`gen-voix.yml`, `gen-images2.yml`, `deploy.yml`) font la même chose dans le nuage ; l'action des voix régénère `stories.js` dans le même envoi que les enregistrements, pour que le texte publié suive toujours la voix.

## Le site en production

| Quoi | Où | Déploiement |
|---|---|---|
| Le site (pages, images, voix) et l'API des comptes | projet Cloudflare `titistoire`, `wrangler.site.toml`, `site/site.js` | automatique à chaque envoi (Workers Builds : `npx wrangler deploy -c wrangler.site.toml`) |
| Le worker d'IA (histoires à la demande) | `titistoire-ai`, `wrangler.toml`, `worker/` | action GitHub `deploy-worker.yml` |

`.assetsignore` liste ce qui n'est pas publié (sources, outils, code). Le site est fait de fichiers statiques ; `site/site.js` ne voit passer que `/assets/voix/*` (lecture partielle, exigée par Safari) et `/api/*`.

**Comptes** (réservés aux parents) : connexion par code à 6 chiffres reçu par e-mail (Cloudflare Email Service), sans mot de passe ni cookie. Base KV `titistoire-comptes` (comptes, sessions, crédits, histoires gardées, plafonds de dépense), stockage R2 `titistoire-medias` (images des 20 histoires gardées par compte). Export et suppression des données par boutons. Le worker d'IA lit et débite les crédits dans la même base ; il plafonne les créations à 10 par jour et 100 par mois, tous comptes confondus (`LIBRE_MAX_JOUR`, `LIBRE_MAX_MOIS`).

**Référencement et pages** : `python3 tools/pages.py` écrit une page par histoire (`h/`), le plan du site, l'icône et la fiche de l'appli installable ; `python3 tools/textes_legaux.py` écrit les mentions légales, la confidentialité, les conditions et « Qui sommes-nous ? ». À relancer après toute retouche de texte.

**Voix** : le texte publié suit la voix, histoire par histoire (`build_stories.py` garde l'ancien texte tant que la voix par défaut n'a pas enregistré le nouveau). Le meilleur modèle est plafonné à 100 demandes par jour.

## « Je crée mon histoire » et le worker d'IA (`worker/`)

Ouvert aux comptes qui ont des crédits (et au mot de passe de l'éditeur), en Cloudflare payant à la demande, avec des plafonds par jour et par mois. Le worker :

1. **contrôle la demande** (liste de mots, Llama Guard, puis un juge « convient à un enfant de cet âge ? ») ;
2. **fait écrire l'histoire** en 8 tableaux, dans une langue adaptée à l'âge choisi, et écarte les textes pauvres ; puis **contrôle le texte et les descriptions d'images** ;
3. **signe** ce qu'il a validé : les routes d'image et de voix refusent tout ce qui n'est pas signé ;
4. **dessine une fiche** pour le héros et pour son ami, puis **chaque page d'après ces fiches** ; chaque image est regardée par un modèle de vision avant d'être envoyée ;
5. **fait lire** l'histoire tableau par tableau (on écoute dès que le premier est prêt) et cale le texte mot à mot.

Tout est fermé par défaut : au moindre doute ou à la moindre panne d'un contrôle, rien n'est affiché. Aucun filtre automatique n'étant infaillible, les conditions demandent au parent de lire une histoire créée avant de la proposer à un enfant.

Tests hors ligne : `node tools/test_controle.mjs`, `node tools/test_voix.mjs <dossier>`.

Les clés sont des secrets GitHub / Cloudflare ou des fichiers privés hors du dépôt, jamais dans le code.
