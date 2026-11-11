# Les Galaxies — bible de la collection (8-10 ans)

État : **proposition à valider par le propriétaire.** Rien n'est écrit ni dessiné tant que cette bible n'est pas validée (leçon n° 1 du premier recueil : bible d'abord, histoires ensuite, images en dernier).

---

## 1. La promesse

1. **Une suite.** Les Étoiles et les Comètes se referment chaque soir ; une Galaxie reste ouverte. On s'endort avec une question, et on a hâte d'être à demain.
2. **Un monde où l'on habite**, avec ses règles, sa carte, ses mots à lui — assez solide pour qu'on y pense dans la journée et qu'on devine la suite avant le héros.
3. **Un vrai mystère, joué à la loyale** : tous les indices sont donnés à l'auditeur ; la solution ne se contente pas d'être maligne, elle serre un peu le cœur.
4. **Une langue de roman.** Des phrases qui prennent leur temps, le passé simple, des mots qu'on apprend en passant sans qu'on nous les explique. On écoute, ou on lit seul, comme un grand.
5. **Des adultes qui ont eu neuf ans.** Ici les grandes personnes se trompent, regrettent, cachent des choses pour de bonnes raisons — et ce sont les enfants qui réparent.

---

## 2. Le format exact

| | Les Galaxies | Rappel : Les Étoiles |
|---|---|---|
| Unité | un **feuilleton** = une seule grande histoire | une histoire close |
| Épisodes | **8** | 1 |
| Durée d'un épisode | **≈ 10 min** | ≈ 5-6 min |
| Longueur d'un épisode | **1 400 mots** (fourchette stricte 1 300 – 1 500), « précédemment » compris | ≈ 780 mots |
| Longueur totale | ≈ 11 000 mots, ≈ 80 min d'écoute (l'audio d'environ 14 histoires des Étoiles) | — |
| Images | **1 frontispice par épisode** + 1 couverture + 1 carte = **10 images** | 24 par histoire |

La durée est à vérifier sur un essai de voix (hypothèse : 140-150 mots/minute pour une lecture contée). Si la voix est plus lente, on baisse la cible à 1 300 mots plutôt que de dépasser 10 minutes.

### Découpage d'un épisode : cinq mouvements

Chaque mouvement fait 250 à 300 mots. Ce n'est pas une mécanique visible : les mouvements peuvent être d'inégale longueur, se fondre, mais chaque épisode doit contenir ces cinq fonctions.

0. **Précédemment** (50 mots au plus, voir plus bas).
1. **La reprise.** On répond à la question laissée la veille dans les 150 premiers mots. On ne triche jamais : pas de « ce n'était qu'un rêve », pas de danger qui s'évapore.
2. **L'avancée.** Un lieu nouveau, ou un personnage nouveau, ou un indice nouveau. Un seul des trois à la fois.
3. **La respiration.** Une scène calme, souvent drôle, à deux personnages. C'est là que vit le sujet profond — dans ce qu'ils se disent en faisant autre chose.
4. **La bascule.** Un retournement : ce qu'on croyait savoir depuis deux épisodes change de sens.
5. **Le suspens et l'atterrissage.** Une image finale et une question ouverte ; puis une dernière phrase rituelle, toujours construite de la même façon (« Cette nuit-là… »), qui ralentit et borde l'enfant. La fin d'épisode est **une porte qui s'ouvre, jamais une lame qui tombe** : c'est une histoire du soir.

### Le « précédemment »

- Absent de l'épisode 1 (remplacé par un prologue de trois phrases qui pose la première énigme).
- **Trois phrases, 50 mots au plus**, au passé composé (c'est la voix de quelqu'un qui raconte ce qu'on a manqué, différente de la voix du récit) ; la troisième phrase est la question de la veille, reformulée.
- Il redonne les **noms** des personnages qui vont parler dans l'épisode : avec une seule voix de narratrice, c'est lui qui remet chaque nom dans l'oreille.
- Enregistré dans un **fichier audio séparé** et **passable** d'un geste : l'enfant qui enchaîne deux épisodes ne le subit pas, celui qui revient après une semaine le retrouve.

### Le texte à l'écran

À 8-10 ans on peut lire seul : le texte devient l'élément principal de l'écran, l'image l'accompagne.

- **Ouverture** : frontispice plein écran, numéro et titre de l'épisode dits par la voix (« Épisode trois. Tombée du Plafond. »).
- **Lecture** : mode « liseuse de nuit » — texte en grand corps, clair sur fond bleu nuit, une « page » = un paragraphe de 45 à 70 mots (environ 24 pages par épisode) ; le surlignage mot à mot est conservé (il aide les lecteurs fragiles à suivre) ; le frontispice reste en bandeau discret en haut.
- **Deux façons d'entrer** : « Écouter » (la voix tourne les pages) ou « Lire » (pas de voix, l'enfant tourne).
- **Fin** : un carton « À suivre » qui affiche la question en suspens, et un bouton vers la carte.
- **Progression** : huit étoiles en haut de l'écran ; une étoile s'allume par épisode terminé — à la fin, elles forment la constellation du feuilleton.

### Fichier source (compatible avec l'outillage existant)

Même esprit que `histoires/*.txt`, un fichier par feuilleton (`galaxies/etoile.txt`), descriptions dans `galaxies/personnages.json` :

```
=== etoile_3
titre: Tombée du Plafond
precedemment: Ancolie a découvert que… (≤ 50 mots)
suspens: Comment un vieux crapaud qui n'a jamais quitté son marais…
@ description unique du frontispice, en anglais, avec {ancolie}, {osier}…
Une ligne = une page lue (45 à 70 mots).
(ligne vide = changement de mouvement)
```

---

## 3. Trois concepts de feuilleton

### A — « L'Étoile qui ne tournait pas » · merveilleux et enquête · *recommandé*

**Accroche.** Un soir, l'étoile qui guide les bateaux sur la Mer de Nuages ne s'allume pas. Ancolie, dix ans, est la seule à avoir remarqué que cette étoile-là, depuis toujours, ne tournait pas avec les autres — et une étoile qui ne tourne pas n'est pas une étoile.

**Le duo.** *Ancolie*, jeune lynx des Cimes : elle voit tout ce qui est loin et rien de ce qui est près ; elle veut qu'on la croie. *Osier*, jeune salamandre du pays d'en bas, apprenti allumeur de lanternes : il rêve de voir ces « étoiles » dont lui parlait son vieux maître, mais il attend toujours qu'on lui donne la permission. Chacun est perdu dans le monde de l'autre.

**Le monde.** Deux pays séparés par une couche de nuages que personne ne traverse. En haut, un archipel de sommets où l'on navigue sur les nuages ; en bas, un pays d'eau et de pluie douce qui n'a jamais vu ni soleil, ni lune, ni étoiles — et qui s'est fabriqué une « Lune » avec une lanterne. Chacun est sûr que l'autre n'existe pas.

**L'enjeu.** Le convoi des bateaux — avec les parents d'Ancolie — rentre dans six nuits et ne peut franchir la Passe sans l'étoile.

**Le sujet profond, jamais énoncé.** La fidélité sans preuve (allumer une lampe pendant cinquante ans pour quelqu'un qui ne répond pas), et la vérité qui répare mieux qu'un beau mensonge. En sourdine : la différence — on ne peut pas habiter chez l'autre, on peut s'y inviter.

**Pourquoi on veut l'épisode suivant.** Chaque réponse ouvre un étage : l'étoile est une lampe ; sous la mer il y a un pays ; dans ce pays il y a une seconde lampe, éteinte la même nuit ; les deux gardiens se connaissaient ; et celle qui interdit tout depuis cinquante ans est celle qui fournissait l'huile.

### B — « Le Voleur de bruits » · enquête de quartier, réaliste et drôle

**Accroche.** À Port-Grelot, les bruits disparaissent un par un : le grincement de la boulangerie, la cloche de l'école, le « ding » du tramway. Chaque fois un seul bruit, chaque fois une seule journée.

**Le duo.** Deux enfants humains. *Noor*, dix ans, détective autoproclamée, carnet « Affaires en cours » rempli d'affaires jamais closes : elle conclut trop vite et accuse à tort. *Achille*, neuf ans, son voisin et meilleur ami, oreille absolue, fabricant de micros en boîtes de conserve : il ne sait pas dire les choses importantes.

**Le monde.** Un petit port, ses quais, son tram numéro trois, sa corne de brume de six heures. Rien de magique : tout est dans l'écoute. La carte du quartier se couvre de croix — et les croix dessinent peu à peu un trajet.

**L'enjeu.** Trouver le coupable avant que la voisine que Noor a accusée — Mme Sourdine, qui travaille de nuit et réclame du silence, donc la suspecte idéale — ne soit montrée du doigt par tout le quartier.

**Le sujet profond.** Le deuil doux d'une amitié. Le voleur, c'est Achille : il déménage à la fin du mois, n'a pas osé le dire, et enregistre un par un les bruits de sa ville pour l'emporter (pour capter un bruit proprement, il fait taire ses voisins une journée). Les croix dessinent son chemin, de sa porte à celle de Noor. Le dernier bruit qui lui manque est le sifflet à deux doigts de Noor quand elle l'appelle.

**Pourquoi on veut l'épisode suivant.** Un bruit vole, un suspect tombe ; et dès l'épisode 4 l'auditeur en sait plus que la détective — on attend, le cœur serré, le moment où elle comprendra.

**Réserves.** Héros humains (interdits aujourd'hui dans les images) ; et c'est le seul concept qui appellerait de vrais sons, donc un autre outillage.

### C — « Pour celui qui n'a jamais reçu de courrier » · science-fiction douce, voyage

**Accroche.** Au fond de sa sacoche, le jour de sa dernière tournée, un petit robot facteur trouve un colis vieux de quarante ans, adressé « à celui qui n'a jamais reçu de courrier ». Un facteur ne rentre pas avec une sacoche pleine : il part le livrer.

**Le héros.** *Pli*, robot facteur de la Poste des Petites Planètes, modèle périmé, promis au musée. Il connaît le Règlement par cœur (« Article 4 : un colis n'est jamais en retard, il est en chemin »). Son désir : finir sa tournée. Sa faille : il ne sait que servir, personne ne lui a jamais demandé ce qu'il voulait, lui. À ses côtés, *Miette*, neuf ans, passagère clandestine de la sacoche, qui ne respecte aucun article.

**Le monde.** Le Chapelet : quarante planètes grandes comme des villages, chacune avec sa seule règle bizarre (celle où c'est toujours dimanche, celle où l'on fait la queue pour s'asseoir sous l'unique arbre, celle de deux voisins fâchés…). On y voyage sur un tricycle à voile.

**L'enjeu.** Livrer avant que l'Inspectrice Oblitère, qui le suit formulaire en main, ne mette le colis au rebut — elle a une bonne raison : le Règlement protège le courrier de tous.

**Le sujet profond.** Grandir, c'est découvrir qu'on a le droit de vouloir quelque chose pour soi. Sur chaque planète, le candidat répond : « Si, j'ai reçu une lettre, une fois. C'est toi qui me l'as apportée » — et raconte ce qu'elle a changé. Le voyage devient le portrait d'une vie utile. Le seul qui n'a jamais reçu de courrier, c'est le facteur : le colis, envoyé par celle qui l'a construit, est pour lui.

**Pourquoi on veut l'épisode suivant.** Une planète par épisode, une règle absurde, une lettre ancienne ; et le plaisir de deviner avant le héros, puis d'attendre qu'il ose ouvrir.

### Recommandation : commencer par A

1. **C'est le plus feuilleton des trois.** Une seule énigme qui se creuse d'étage en étage ; B repose sur une révélation unique, C sur des étapes presque indépendantes (ce serait un excellent deuxième feuilleton, peu coûteux, avec un héros robot facile à dessiner).
2. **Il tient dans l'outillage actuel** : personnages animaux très différents les uns des autres, aucune image à plus de trois personnages, aucun humain.
3. **Il porte l'identité du site** — le ciel de nuit. Sa plus belle scène est un enfant qui voit les étoiles pour la première fois : difficile de mieux ouvrir une collection qui s'appelle Les Galaxies.
4. **Deux héros, une fille et un garçon, deux mondes** : chacun y trouve sa porte d'entrée.

---

## 4. Bible complète — « L'Étoile qui ne tournait pas »

### 4.1 Le monde

**Une seule chose, deux noms.** Entre les deux pays s'étend une couche de nuages épaisse d'une journée. Ceux d'en haut l'appellent **la Mer**. Ceux d'en bas l'appellent **le Plafond**. Ancolie et Osier se disputeront sur ce mot pendant huit épisodes ; à la dernière page, chacun emploiera celui de l'autre.

**Les règles** (elles ne changent jamais ; toute solution de l'intrigue doit en sortir) :

1. **La Mer porte ce qui est large et léger.** Les *brumiers* — barques à fond plat, tressées — y glissent à la voile. Ce qui est lourd et étroit s'y enfonce lentement, « comme une cuillère dans la crème ». On ne tombe pas : on descend.
2. **Dans le Blanc** (l'épaisseur du nuage), il n'y a ni haut ni bas, ni près ni loin. Personne ne le traverse par ses propres moyens ; les falaises des montagnes y sont lisses et ruisselantes.
3. **Deux passages seulement.** Pour descendre : **la Bonde**, un lent tourbillon dans la Mer, qui avale ce qui s'en approche (les passeurs la contournent, des bouées la signalent). Pour monter : **la Montante**, une colonne d'air tiède qui s'élève des Sources Chaudes, **seulement les nuits où il gèle là-haut**. Elle débouche près du Pic Sans-Nom ; en haut on l'appelle *l'Haleine* : un banc de brume tiède qui sent la menthe, sans que personne sache pourquoi.
4. **La Nuit Mince.** Très rarement — une fois dans une vie —, à la première gelée, la Mer s'amincit quelques heures jusqu'à n'être plus qu'un voile. D'en haut on devine des lueurs dessous ; d'en bas on aperçoit quelques points brillants dans le Plafond. Presque tout le monde dort.
5. **Les montagnes ont des pieds.** Les sommets d'en haut sont les cimes des *Piliers* d'en bas, dont les gens de Mille-Gouttes pensent qu'ils « tiennent le Plafond ». Le Pic Sans-Nom est exactement au-dessus du Grand Mât.
6. **En haut** : air sec, vent, soleil, ombres nettes, étoiles. On se repère à l'œil et aux astres. Le bois est rare ; les coques des brumiers sont tressées dans un bois souple « qui ne pousse sur aucune cime » et qu'on se transmet de mère en fille sans savoir d'où il vient.
7. **En bas** : pluie fine, lumière gris perle qui vient de partout à la fois — **personne n'a d'ombre** —, nuit noire sans astre. On se repère à l'oreille (le bruit de la pluie change selon les feuilles) et au nez. On s'éclaire aux lanternes de vers luisants.
8. **Chacun souffre un peu chez l'autre**, sans danger : Osier et les siens ont la peau qui tire au sec et au soleil (il leur faut de l'ombre et de l'eau) ; ceux d'en haut, en bas, s'enrhument, se perdent, ne voient pas à dix pas. C'est de l'inconfort et de l'urgence douce, jamais une menace de mort.
9. **Ce qui tombe, ce qui monte.** En bas, il « tombe du Plafond » de temps en temps une pomme de pin, une rame, un bouton : on les expose comme des trésors. En haut, l'Haleine dépose parfois un duvet de roseau, une libellule étourdie.
10. **Le calendrier.** On compte en *hivers*. L'histoire dure six nuits, à la fin de l'automne, entre la première gelée et la veille de la nouvelle lune.

**L'histoire ancienne** (ce que les enfants découvrent peu à peu). Il y a cinquante hivers, une jeune passeuse, Gentiane, fut avalée par la Bonde. En bas, un jeune allumeur de lanternes, Saule, la recueillit. Ils passèrent une saison à s'étonner l'un de l'autre. Il lui fabriqua une cloche de toile pour remonter par la Montante. Ils se promirent une lampe chacun, tous les soirs, « pour se dire bonsoir ». Mais le nuage était trop épais : aucun des deux ne vit jamais la lampe de l'autre. Ils allumèrent quand même. En haut, personne ne crut Gentiane ; sa meilleure amie, Joubarbe, fut celle qui dit le plus fort qu'elle avait rêvé. Gentiane partit vivre seule sur le Pic Sans-Nom. Sa lampe, vue de Port-Givre, devint « l'Étoile du Seuil » — Joubarbe, alors jeune commise du port, l'inscrivit elle-même sur les cartes. En bas, la lampe de Saule devint « la Lune » : il avait donné à son pays un mot et un astre qu'on lui avait racontés.

La nuit qui précède l'épisode 1 est une Nuit Mince. Pour la première fois, chacun voit la lampe de l'autre. Chacun part aussitôt le rejoindre — elle par la Bonde, lui par la Montante. **Ils se croisent.** Les deux lampes s'éteignent le même soir.

**Le vocabulaire inventé** (douze mots, pas un de plus, introduits un par un) : la Mer / le Plafond, le Blanc, un brumier, un passeur / une passeuse, la Bonde, la Montante / l'Haleine, la Nuit Mince, le Seuil, les Piliers, la Lune (de Mille-Gouttes), un Tombé-du-Ciel, la cloche. Pour les points cardinaux, on dit **le levant** et **le couchant**, jamais « l'est » (la voix de synthèse le confondrait avec le verbe).

### 4.2 Les lieux (description visuelle fixe, à réutiliser mot pour mot)

| Lieu | Ce que c'est | Description fixe (anglais) |
|---|---|---|
| **Port-Givre** | le village d'Ancolie, sur un sommet | `a small harbour village of grey stone houses with steep slate roofs and warm yellow windows, built on a rocky mountain peak that rises like an island out of a flat white sea of clouds, wooden jetties reaching out over the clouds, small wicker boats with cream sails moored on the cloud surface` |
| **L'Observatoire** | tour de Maître Mélèze, où loge Ancolie | `a round stone observatory tower with a green copper dome and a long brass telescope, a flat roof terrace with a wooden railing, at the highest point of a mountain-top village above a sea of clouds` |
| **La Passe des Dents** | porte d'entrée de Port-Givre | `two tall sharp dark rock spires standing close together like a gate, rising out of a flat white sea of clouds` |
| **Le Pic Sans-Nom** | l'îlot de Gentiane, la maison de la lampe | `a lone thin needle of dark rock rising from a flat white sea of clouds, with a tiny stone hut on top whose roof carries a small round glass lamp room, a wooden rain barrel beside the door` |
| **La Bonde** | le passage vers le bas | `a wide slow whirlpool in a flat white sea of clouds, the clouds spiralling gently downward like cream into a funnel, ringed by a few faded orange buoys` |
| **Mille-Gouttes** | le village d'Osier | `a village of round reed-thatched huts on wooden stilts above dark still canals, linked by rope bridges, among giant reeds and water mint, under a low pearl-grey ceiling of cloud, fine rain, soft even light with no shadows, small glass lanterns glowing pale green` |
| **Le Grand Mât** | la tour de la « Lune » | `a bare giant tree trunk as tall as a tower, wrapped in a spiral wooden staircase, with a round platform at the top holding a large globe lantern of golden glass, the top almost touching the low grey cloud ceiling` |
| **Le Cabinet des Tombés-du-Ciel** | le musée de Madame Tourbe | `the inside of a long wooden hut lined with shelves and glass cases where ordinary objects are displayed like treasures: pine cones on velvet cushions, a single old boot, a broken oar, a brass button under a glass dome, lit by pale green lanterns` |
| **Les Sources Chaudes** | pied du Pilier, départ de la Montante | `steaming turquoise hot pools among mossy stones at the foot of a colossal sheer wet rock wall that disappears into a low grey cloud ceiling, a column of white steam rising straight up into the clouds` |
| **La Citerne** | sous le port ; seule cachette humide d'en haut | `a cool vaulted stone cistern under a harbour, a still pool of dark water, wet stone steps, one hanging lantern casting golden light` |

### 4.3 Les personnages

**Parti pris : ce ne sont pas des humains.** Ce sont des animaux qui se tiennent debout et portent de vrais vêtements — un « roman animalier » dans la lignée du *Vent dans les saules*, pas des peluches à foulard. Trois raisons : le recueil existant interdit les humains dans ses images ; le générateur tient beaucoup mieux une espèce reconnaissable ; et le partage des espèces *dessine* le monde (bêtes de montagne en haut, bêtes d'eau en bas), sans jamais renvoyer à des différences entre humains. Toutes les espèces sont distinctes ; aucun oiseau (on demanderait pourquoi il ne traverse pas en volant). C'est la première question ouverte (§ 7).

Règle d'image rappelée : chaque description commence par « one », ne contient aucun prénom, et s'emploie mot pour mot.

#### Les deux héros

**Ancolie** — jeune lynx, dix ans, apprentie à l'Observatoire.
- *Caractère* : vive, têtue, drôle sans le vouloir ; s'emporte, puis regrette.
- *Désir* : devenir passeuse comme sa mère — et surtout qu'on la croie.
- *Faille* : des yeux de lynx pour ce qui est loin, aucun regard pour ce qui est tout près : elle ne voit pas ce que ressentent ceux qui lui parlent. Elle a raté trois fois l'« épreuve du cap » en fixant l'horizon et en heurtant la bouée.
- *Façon de parler* : phrases courtes, affirmations (« C'est impossible. Je l'ai vu. »), coupe la parole ; quand elle doute, elle se tait — et c'est rare.
- *Visuel* : `one young lynx girl about ten years old, standing upright, slim, with sandy grey fur with faint dark spots, white cheek ruffs, tall pointed ears ending in black tufts, a very short black-tipped tail and amber eyes, wearing a bright red hooded wool cape`

**Osier** — jeune salamandre, neuf ans, apprenti allumeur de lanternes à Mille-Gouttes.
- *Caractère* : posé, attentif, pince-sans-rire ; remarque tout ce qui est près.
- *Désir* : voir ce que son maître lui a raconté — « des points de lumière au-dessus du Plafond, autant que de gouttes ».
- *Faille* : il attend qu'on lui permette. Il n'a jamais dit tout haut qu'il croyait aux étoiles, de peur qu'on rie de lui comme on rit du vieux Saule. Il n'a pas osé monter seul au Grand Mât — et le message qui l'y attendait est resté trois jours sans lecteur.
- *Façon de parler* : lente, précise ; compare tout à l'eau (« tu parles comme une gouttière ») ; pose des questions là où Ancolie affirme (« C'est comment, une ombre ? »).
- *Visuel* : `one young fire salamander boy about nine years old, standing upright, a head shorter than the lynx girl, with smooth glossy black skin covered in bright yellow spots, a long tail, a round head with large dark eyes, wearing a wide cone-shaped woven reed hat tied with a bright turquoise ribbon`
- *Motif* : son dos noir semé de taches jaunes. Ancolie le lui dira à l'épisode 6 : il porte depuis toujours un ciel qu'il n'avait jamais vu.

#### Les anciens

**Gentiane** — très vieux bouquetin, gardienne de la lampe du Pic Sans-Nom.
- *Caractère* : sèche, brave, moqueuse ; cinquante hivers de solitude l'ont rendue économe de mots, pas de cœur.
- *Désir* : savoir enfin s'il a répondu.
- *Faille* : l'orgueil — elle a préféré s'exiler plutôt que de pardonner à Joubarbe, et n'a jamais redescendu au port.
- *Façon de parler* : trois mots où il en faudrait dix ; appelle tout le monde « petite » ou « petit », y compris Joubarbe.
- *Visuel* : `one very old female ibex, standing upright, tall and lean, twice as tall as the lynx girl, with a grey-brown coat turned silver around the muzzle, a short white beard and two long ridged horns curving backward, wearing a long deep blue wool shawl closed with a brass pin`

**Père Saule** — très vieux crapaud, allumeur de la Lune de Mille-Gouttes, maître d'Osier.
- *Caractère* : lent, tendre, rieur ; raconte les étoiles depuis cinquante hivers à qui veut bien l'écouter, sans se fâcher qu'on n'y croie pas.
- *Désir* : revoir celle qui lui a appris le mot « lune ».
- *Faille* : il n'a jamais rien exigé de personne — pas même d'Osier ; il est parti en laissant un mot tout en haut du Mât plutôt que de réveiller l'enfant.
- *Façon de parler* : des dictons de pluie (« goutte à goutte, on remplit le lac ») ; compte tout en gouttes ; rit avant la fin de ses propres phrases.
- *Visuel* : `one very old toad, standing upright, short and wide, half as tall as the old ibex, with bumpy olive-brown skin, a pale belly, a very wide mouth and large calm golden eyes, wearing a bright orange knitted waistcoat`

#### L'adversaire qui a une bonne raison

**Dame Joubarbe** — vieille marmotte, Maîtresse du Port de Port-Givre.
- *Caractère* : autoritaire, infatigable, sentinelle dans l'âme (elle siffle l'alerte) ; tout le village lui doit sa sécurité.
- *Désir* : que personne, plus jamais, ne disparaisse dans la Mer.
- *Sa raison* : il y a cinquante hivers, sa seule amie est revenue d'en bas « avec un autre nom plein la bouche ». Par jalousie et par peur, elle a dit que Gentiane avait rêvé. Elle l'a dit si fort qu'elle l'a perdue quand même. Depuis, **elle dépose en secret une jarre d'huile par mois au pied du Pic** — c'est tout ce qu'elle a su faire pour demander pardon sans le dire. Elle sait donc que l'étoile est une lampe, et tient au mensonge : si le village apprend que l'étoile était fausse, croira-t-il encore aux cartes, et à elle ?
- *Faille* : elle confond protéger et se taire.
- *Façon de parler* : des ordres brefs, clos par « Point. » ; ne pose jamais de question — jusqu'à l'épisode 7.
- *Visuel* : `one old stout marmot, standing upright, round and heavy, as tall as the lynx girl, with grey-brown fur, a grey muzzle, small round ears and short arms, wearing a dark plum purple harbour master coat with two rows of brass buttons and a silver whistle hanging on a cord around the neck`

#### Les alliés

**Génépi** — jeune lièvre des neiges, dix ans, meilleur élève passeur, rival puis ami.
- *Caractère* : vantard, rapide, généreux dès qu'on ne le regarde plus.
- *Désir* : être le premier ; au fond, être admiré d'Ancolie.
- *Faille* : ne reconnaît jamais une erreur — or c'est son nœud mal fait qui envoie Ancolie dans la Bonde.
- *Façon de parler* : commence par « Moi, je… » ; enjolive tout ; devient très bref quand il a peur.
- *Visuel* : `one young white mountain hare boy about ten years old, standing upright, tall and thin, with pure white fur, very long upright ears tipped with black and big feet, wearing a bright green knitted jumper slightly too large`

**Maître Mélèze** — vieil ours, Compteur d'étoiles de l'Observatoire, tuteur d'Ancolie pendant le convoi.
- *Caractère* : savant, doux, distrait ; il dort tout l'hiver et **n'a donc jamais vu les constellations d'hiver** : chaque printemps, il demande à Ancolie de les lui raconter.
- *Désir* : finir son compte des étoiles avant de s'endormir (il ne finit jamais).
- *Faille* : le sommeil le prend au milieu des phrases importantes — c'est ce qui laisse Ancolie seule, et libre.
- *Façon de parler* : des phrases savantes qui s'achèvent en bâillement.
- *Visuel* : `one huge old brown bear, standing upright, three times as tall as the lynx girl, with shaggy dark brown fur, a grey muzzle and small half-moon spectacles, wearing a long mustard yellow quilted dressing gown`

**Maître Aulne** — castor, charpentier des digues de Mille-Gouttes.
- *Caractère* : bougon, exact, incapable de refuser un beau problème.
- *Désir* : que ça tienne.
- *Faille* : ne croit que ce qui se mesure.
- *Façon de parler* : en chiffres et en estimations (« Dix-sept brasses. À vue de nez. Dix-huit s'il pleut. Il pleut. »).
- *Visuel* : `one sturdy adult beaver, standing upright, as tall as the lynx girl, with dark brown fur, a broad flat scaly tail and two orange front teeth, wearing a tan leather carpenter apron and a sky blue neckerchief`

**Madame Tourbe** — taupe, conservatrice du Cabinet des Tombés-du-Ciel.
- *Caractère* : passionnée, myope, cérémonieuse. Sa théorie, œuvre d'une vie : « le Plafond pond ».
- *Désir* : classer le monde entier.
- *Faille* : elle aime sa théorie plus que les faits — c'est le reflet doux de Joubarbe, en bas. Quand la vérité arrivera, elle se rendra avec panache : « Catégorie nouvelle. »
- *Façon de parler* : en catégories (« Tombé-du-Ciel de troisième classe, ligneux, écailleux : la pomme de pin »).
- *Visuel* : `one small plump mole, standing upright, shorter than the salamander boy, with velvety black fur, a pink pointed nose, large pink hands and thick round glasses, wearing a lilac smock with bulging pockets`

**Bruyère** — mère d'Ancolie, passeuse du convoi. Présente par l'absence (c'est elle qui a tricoté les moufles) et par sa voix à l'épisode 8. **Jamais dessinée** : même espèce que l'héroïne, donc risque de fusion dans l'image.

*Contrôle des silhouettes.* Lynx (oreilles à pinceaux, cape rouge) · salamandre (noir et jaune, chapeau conique) · bouquetin (grandes cornes, châle bleu) · crapaud (large, gilet orange) · marmotte (ronde, manteau prune) · lièvre (longues oreilles, pull vert) · ours (énorme, robe de chambre moutarde) · castor (queue plate, tablier) · taupe (noire, blouse lilas). Aucune paire proche ; chaque personnage a sa couleur vive.

### 4.4 Objets et motifs récurrents

| Objet | Rôle | Description fixe (anglais) |
|---|---|---|
| **La lampe de Gentiane** (« l'Étoile du Seuil ») | l'énigme | `a big brass lamp with a thick round glass lens and a small brass shutter` |
| **La Lune de Mille-Gouttes** | la lampe jumelle | `a large globe lantern of golden glass, as big as a barrel, held in a ring of dark wood` |
| **L'Écuelle** | le petit brumier d'Ancolie ; Génépi dit qu'elle navigue « dans une soupière » ; deviendra la nacelle de la cloche | `a small round shallow boat woven from pale wicker like a big basket, with one short mast, a patched cream triangular sail and a red tiller` |
| **La cloche** | le ballon qui remonte par la Montante | `a bell-shaped balloon sewn from patches of waxed green and cream cloth, open at the bottom, with ropes holding a round wicker basket` |
| **La moufle** | Ancolie n'en a qu'une : l'autre est tombée à la Mer il y a deux hivers ; elle garde l'orpheline dans sa poche | `a single dark blue knitted mitten with a small white star pattern on the back` |
| **La poire à brume** | Osier s'en asperge dès que sa peau tire ; source de gags, puis d'inquiétude en haut | `a small brass spray bottle with a round green rubber bulb` |
| **Le sifflet de Joubarbe** | alerte, autorité ; à la fin, une seule note longue et douce | `a small silver whistle on a cord` |
| **Les jarres d'huile** | l'indice qui retourne l'adversaire | `squat clay jars sealed with dark red wax` |
| **Les deux portraits au charbon** | Gentiane a dessiné Saule sur son mur ; Saule a dessiné Gentiane sur le sien | `a rough charcoal drawing of a toad on a stone wall` / `a rough charcoal drawing of an ibex with long horns on a wooden wall` |

**Motifs qui reviennent** (chacun posé tôt, payé tard) :

- **« Elle ne tourne pas. »** Première phrase d'Ancolie sur l'étoile ; dernière phrase du feuilleton, retournée.
- **L'odeur de menthe** de l'Haleine (épisode 1, simple curiosité) : c'est la menthe d'eau de Mille-Gouttes ; à l'épisode 8, le nez d'Osier remplace l'étoile éteinte.
- **L'osier.** Le bois des coques d'en haut « ne pousse sur aucune cime » ; le garçon d'en bas porte son nom et sait le tresser. Les deux pays ont été liés autrefois : ce fil reste ouvert pour une suite.
- **Compter.** Mélèze compte les étoiles, Aulne les brasses, Saule les gouttes, Gentiane les nuits (dix-huit mille traits sur son mur). Personne ne tombe juste.
- **L'ombre.** Osier n'en a jamais eu. Il rencontre la sienne à l'épisode 6.
- **Les mots de l'autre.** Mer / Plafond ; la « Lune » qui n'est pas la lune.
- **La phrase de fin.** Chaque épisode se clôt sur une phrase commençant par « Cette nuit-là » qui dit combien de lampes brillent : aucune (ép. 1 à 3), une, en bas (ép. 4 à 7), deux (ép. 8).

### 4.5 Le plan des épisodes

Chronologie : nuit 0 = la Nuit Mince (avant le récit) ; nuit 1 = épisode 1 ; nuit 3 = la Lune rallumée (ép. 4) ; nuit 5 = la remontée (ép. 6) ; nuit 6 = le convoi arrive, avec une nuit d'avance sur la nouvelle lune (ép. 7-8).

Dans les descriptions d'images, `{nom}` renvoie aux descriptions fixes ci-dessus (personnages, lieux, objets), comme dans `histoires/personnages.json`.

#### Épisode 1 — Une lueur sous la mer

Port-Givre, première gelée. Ancolie vient de rater pour la troisième fois l'épreuve du cap ; Génépi le fait savoir à tout le port. Elle a pourtant vu, la nuit dernière, depuis le toit de l'Observatoire, quelque chose que personne ne croit : la Mer devenue mince comme un voile, et dessous, une lueur. Ce soir, nouvelle affaire : l'Étoile du Seuil, celle qui guide les brumiers dans la Passe des Dents, ne paraît pas. Dame Joubarbe siffle le rassemblement : le ciel a ses humeurs, nul ne sort du port, point. Or le convoi — avec les parents d'Ancolie — rentre dans six nuits. Ancolie fouille les cartes de Maître Mélèze : sur celles qui ont plus de cinquante hivers, l'étoile n'existe pas. Et elle ose enfin dire ce que ses yeux savent depuis toujours : toutes les étoiles tournent dans la nuit ; celle-là, jamais. Mélèze, qui bâille depuis le début, commence une réponse capitale… et s'endort pour l'hiver. Ancolie braque la grande lunette vers le levant : sur le Pic Sans-Nom, là où devrait briller l'étoile, il y a une maison.

- **En suspens** : qui habite le Pic Sans-Nom — et qu'allumait-on là-bas, chaque soir, qu'on a pris pour une étoile ?
- **Phrase de fin** : aucune lampe.
- **Frontispice** : `Night on the roof terrace of {observatoire}, under a sky full of stars: {ancolie} leans over the railing looking through a brass spyglass toward a tiny dark rock needle far away on the horizon of the cloud sea, her ears pricked, intrigued; behind her {meleze} sleeps in a big armchair, smiling, a star chart sliding off his knees; one empty dark patch of sky low above the horizon`

#### Épisode 2 — Le Pic Sans-Nom

À l'aube, Ancolie détache l'Écuelle. Génépi la surprend, menace de tout dire, puis saute à bord « pour l'en empêcher ». Traversée au-delà des bouées ; ils longent la Bonde, qui tourne sans bruit. Sur le Pic : une cabane, une lampe énorme et froide, un fauteuil, dix-huit mille traits gravés au mur, des jarres d'huile scellées de cire rouge, et, dessiné au charbon, un être qu'ils n'ont jamais vu — « une pomme de terre avec des yeux », décrète Génépi. Sur la table, un mot : « Plus d'huile. Il a répondu. Je descends. » Qui, *il* ? Descendre où ? Pendant qu'ils se chamaillent, l'Écuelle, amarrée par un nœud dont Génépi était très fier, s'en va. Ancolie saute dedans pour la rattraper ; le courant la porte vers la Bonde. Le brumier se met à tourner, lentement, puis à s'enfoncer dans le blanc comme une cuillère dans la crème. Sur le rocher, Génépi reste seul — et dans le tonneau d'eau de pluie, derrière lui, quelque chose fait « hum ».

- **En suspens** : qu'y a-t-il sous la Mer ? (Et qui a fait « hum » ?)
- **Phrase de fin** : aucune lampe.
- **Frontispice** : `Late afternoon inside a small round glass lamp room on top of a stone hut, the white sea of clouds visible all around through the windows: {ancolie} lays one paw on {lampe}, cold and unlit, frowning, puzzled; behind her {genepi} points at a rough charcoal drawing of a toad on the stone wall and laughs; squat clay jars sealed with dark red wax on the floor`

#### Épisode 3 — Tombée du Plafond

La descente dans le Blanc : ni haut ni bas, et pour la première fois les yeux d'Ancolie ne servent à rien. Puis le nuage s'ouvre par en dessous : il pleut, tout est gris perle et vert, et l'Écuelle se pose dans des roseaux hauts comme des mâts. Un garçon noir et jaune, sous un chapeau pointu, la regarde sans s'étonner beaucoup : « Tu es tombée du Plafond. D'habitude, il ne tombe que des pommes de pin. » C'est Osier. Malentendus en cascade : il lui apprend que « la Lune s'est éteinte » ; elle répond que la lune ne s'éteint pas ; ils ne parlent pas de la même. À Mille-Gouttes, Madame Tourbe lui fait les honneurs du Cabinet des Tombés-du-Ciel — et là, sous cloche, étiquetée comme une merveille, Ancolie reconnaît sa propre moufle perdue. Osier cherche son maître, le Père Saule, disparu la nuit où le Plafond s'est aminci. Deux lampes, éteintes la même nuit. Dans l'atelier de Saule, au mur : le portrait au charbon d'un être cornu. « Un monstre de ses contes, dit Osier. Elle s'appelle Gentiane. » Ancolie reconnaît un bouquetin.

- **En suspens** : comment un vieux crapaud qui n'a jamais quitté son marais a-t-il pu dessiner quelqu'un d'en haut ?
- **Phrase de fin** : aucune lampe.
- **Frontispice** : `Daytime under a low pearl-grey cloud ceiling, fine rain, among giant reeds beside a dark canal: {ancolie} sits soaked and grumpy in {ecuelle}, which is stuck in the reeds, her cape dripping; on a plank walkway {osier} looks up at her calmly, holding a pole with a small glass lantern glowing pale green; soft even light, no shadows`

#### Épisode 4 — La Lune de Mille-Gouttes

Ancolie est malheureuse en bas : pas d'horizon, tout mouille, elle se perd à dix pas. Osier la guide à l'oreille — la pluie ne chante pas pareil sur le roseau et sur la menthe. Il lui demande comment sont les étoiles ; elle qui a réponse à tout ne trouve pas les mots. Il faut monter au Grand Mât ; Osier n'y est jamais allé seul, personne ne le lui a permis. Ancolie monte la première, il suit. Tout en haut : la grande lanterne froide, une longue-vue braquée sur le Plafond, des milliers de traits gravés — et un mot, qui attend depuis trois jours : « Elle a répondu. Je monte. Garde la Lune. » Osier comprend que son maître comptait sur lui, et qu'il n'était pas là. Alors, pour la première fois, sans permission, il allume la Lune. La lueur dorée lèche le dessous des nuages ; tout Mille-Gouttes lève la tête. Et du pied du Mât monte une voix rauque, furieuse, enrhumée : « Qui a rallumé ça ? Saule ? C'est toi ? »

- **En suspens** : si Gentiane est ici, en bas… où est le Père Saule ?
- **Phrase de fin** : une lampe — en bas.
- **Frontispice** : `Night at the top of {grandmat}, just under the dark cloud ceiling: {osier}, standing on tiptoe, lights {lune} for the first time, his face serious and glowing in the golden light; {ancolie} holds the ladder steady and looks up at the golden glow spreading on the underside of the clouds, amazed; far below, tiny pale green lanterns of a stilt village`

#### Épisode 5 — Ceux qui se sont croisés

Gentiane, trempée, a tourné trois jours dans les roseaux (« Tout se ressemble, ici. Et tout mouille. ») ; la Lune rallumée l'a enfin guidée. Près du poêle de l'atelier, elle raconte : la Bonde, il y a cinquante hivers ; un jeune crapaud qui riait avant la fin de ses phrases ; la cloche de toile ; la promesse des deux lampes ; puis le retour, et sa meilleure amie qui jure devant tout le port qu'elle a rêvé. Dix-huit mille soirs sans réponse — jusqu'à la Nuit Mince. Les enfants font le compte avant elle : cette nuit-là, Saule est monté pendant qu'elle descendait. Il l'attend là-haut, sur un rocher sec, au vent, devant une lampe froide. Gentiane en rit, puis n'en rit plus : un crapaud au soleil, il faut vite lui rendre sa pluie. Il faudra remonter par la Montante, à la prochaine gelée. Ancolie, pour dire quelque chose, parle des jarres. Gentiane hausse les épaules : elle n'a jamais su qui les déposait. Une par mois, au pied du rocher, depuis cinquante hivers. Ancolie revoit la cire rouge : c'est le sceau du port.

- **En suspens** : pourquoi celle qui l'a traitée de menteuse nourrit-elle sa lampe depuis cinquante hivers ?
- **Phrase de fin** : une lampe.
- **Frontispice** : `Evening inside a cosy wooden workshop on stilts, rain on the window, a small iron stove glowing: {gentiane}, wrapped in a blanket, sits by the stove telling a story, one hand raised, a half smile; {ancolie} and {osier} sit on the floor facing her, listening with wide eyes; on the wooden wall behind them, a rough charcoal drawing of an ibex with long horns; exactly three characters: one ibex, one lynx, one salamander`

#### Épisode 6 — La Montante

La cloche est partie avec Saule : il en faut une autre, et Maître Aulne ne construit pas pour aller « dans le Plafond, où il n'y a rien ». Ancolie sort la moufle de sa poche et la pose à côté de celle du Cabinet. Une paire. « Le Plafond ne pond pas par paires », admet Madame Tourbe, et, très droite : « Catégorie nouvelle. » Tout le village s'y met ; Osier retresse le fond de l'Écuelle, qui devient nacelle ; Aulne mesure, grogne, recommence. Avant de partir, Osier demande à ceux qui restent de garder la Lune allumée — « pour ceux d'en haut, s'ils existent », concède Aulne. La nuit gèle là-haut : la Montante se lève. Montée dans le Blanc, à trois. Puis la cloche crève la Mer, et Osier voit les étoiles. Il ne dit rien pendant très longtemps. Ensuite : « Le Père Saule a dit *autant que de gouttes*. Il a menti. Il y en a plus. » Ancolie lui apprend qu'il en porte autant sur le dos. À l'aube, le Pic Sans-Nom : la cabane est vide, des jarres neuves sont posées devant la porte, et le soleil qui se lève colle aux pieds d'Osier une chose noire qui le suit partout.

- **En suspens** : qui est venu au Pic, et où a-t-on emmené Saule et Génépi ? Et combien de temps Osier tiendra-t-il au soleil ?
- **Phrase de fin** : une lampe en bas — et, pour la première fois, toutes les étoiles.
- **Frontispice** : `Deep night above a flat white sea of clouds, an immense sky crowded with stars and the Milky Way: {cloche} has just risen out of the clouds; in its basket {osier} stands with his reed hat fallen onto his back, head tilted up, mouth open, seeing stars for the first time, starlight on his yellow spots; beside him {ancolie} watches him instead of the sky, smiling quietly` (Gentiane, assise au fond de la nacelle, n'est volontairement pas dans l'image.)

#### Épisode 7 — L'huile de cinquante hivers

L'Écuelle, redevenue brumier, file vers Port-Givre ; Osier voyage sous la cape mouillée d'Ancolie. Sur la jetée, au petit jour, une seule silhouette : Dame Joubarbe charge son propre brumier pour aller à la Bonde chercher l'enfant — elle qui l'interdit depuis cinquante hivers. C'est elle qui est venue au Pic : elle y a trouvé Génépi, et dans le tonneau, un vieux crapaud. Elle a caché Saule dans la Citerne, seul endroit humide du village, et fait jurer le silence à Génépi (qui tient l'histoire du siècle et n'a pas le droit de la raconter : il en est malade). Retrouvailles dans la Citerne : « Tu as vieilli. — Toi, tu as séché. » Puis Joubarbe et Gentiane, face à face. Joubarbe veut rallumer et se taire : une étoile ne s'explique pas, un mensonge de cinquante hivers, si. Ancolie s'emporte — elle ne veut pas d'un ami qu'il faut cacher sous une cape. Puis, pour la première fois, elle regarde ce qui est tout près : les pattes de la vieille marmotte tremblent. Elle ne la dénonce pas. Elle lui tend son sifflet tombé : « C'est à vous de le dire. » À cet instant, la vigie crie : des voiles derrière les Dents. Le convoi a une nuit d'avance, le soir tombe, la lampe est éteinte — à deux heures de mer.

- **En suspens** : comment allumer avant la nuit une lampe qui est à deux heures de brumier ? Et Joubarbe parlera-t-elle ?
- **Phrase de fin** : une lampe en bas ; en haut, pas encore.
- **Frontispice** : `Inside {citerne}, golden lantern light on dark water: {saule} sits in the shallow water at the edge of the pool, looking up with a wide tender smile; {gentiane} stands on the wet steps facing him, leaning on the wall, moved, trying to look stern; behind them at the top of the steps {joubarbe} stands apart holding a lantern, eyes lowered; exactly three characters: one toad, one ibex, one marmot`

#### Épisode 8 — Deux lampes

Aucun brumier du port n'est assez rapide. Sauf un : l'Écuelle, coque d'en haut, fond tressé d'en bas, avec pour voile la toile de la cloche. Ancolie à la barre, Génépi aux nœuds (« Celui-là tiendra. L'autre fois, c'était le mien. »), Osier à l'avant. La nuit est noire, et l'étoile qu'il faudrait pour trouver le Pic est justement celle qui manque. Ancolie ne voit rien — et accepte de ne rien voir. C'est Osier qui guide, au nez : « À gauche. Encore. Ça sent chez moi. » La menthe de l'Haleine les mène au rocher ; l'huile de Joubarbe est là ; Ancolie allume. Le convoi passe les Dents. Alors il gèle, la Mer s'amincit, et sous la lampe en apparaît une autre, floue et dorée : Mille-Gouttes a tenu parole. Sur la jetée, tout Port-Givre la voit ; Gentiane et Saule regardent enfin leurs deux lampes ensemble ; et Joubarbe dit, à voix haute, ce qu'elle sait depuis cinquante hivers. Le lendemain, il faut que chacun rentre chez soi : on ne peut pas habiter chez l'autre. Ancolie donne une moufle à Osier et garde la seconde. Ils conviennent d'un code de lampe — un éclat long : bonsoir. Épilogue au printemps : Mélèze s'éveille. « J'ai manqué quelque chose ? — L'hiver, comme d'habitude. Et une étoile. » Elle ne tournait pas : ce n'était pas une étoile, c'était quelqu'un. Ce soir-là, la lampe d'en bas fait trois éclats brefs, qui ne sont pas dans le code.

- **En suspens** (petite porte laissée ouverte, pas un manque) : que veut dire Osier ? — Aulne a trouvé, sous le lierre du Pilier, de très vieilles marches.
- **Phrase de fin** : deux lampes.
- **Frontispice** : `Night at the top of a lone rock needle above a thin misty sea of clouds, under a starry sky: {lampe} shines bright gold from the small glass lamp room; directly below it, through the thin clouds, a second soft golden glow shines up from underneath; in front of the hut {ancolie} and {osier} sit side by side on the rock, seen from behind, each wearing one dark blue mitten, looking at the two lights, peaceful`

### 4.6 La carte à observer : « la carte à deux étages »

Une seule carte, qu'on rouvre après chaque épisode et qui **change trois fois**.

- **État 1 (dès l'épisode 1)** — la carte des passeurs. L'Archipel des Cimes vu du dessus : Port-Givre, l'Observatoire, la Passe des Dents, le Pic Sans-Nom, la Bonde et ses bouées, la route du convoi ; dans la marge, un morceau de ciel avec ses constellations. Sous la Mer, un grand blanc, et la mention des cartographes : « Rien. »
- **État 2 (après l'épisode 3)** — la carte se déplie vers le bas : en coupe, sous la couche de nuages, apparaissent Mille-Gouttes, le Grand Mât, le Cabinet, les Sources Chaudes, les Piliers. Le mot « Rien » est barré d'une autre écriture.
- **État 3 (après l'épisode 8)** — les deux lampes sont allumées, reliées par un trait pointillé ; et tout en bas du Pilier, un minuscule escalier.

**Ce qu'un enfant attentif peut y trouver avant le héros** : l'Étoile du Seuil est dessinée d'une autre encre que les vraies étoiles et n'appartient à aucune constellation ; elle est posée exactement sur le Pic Sans-Nom ; dans l'état 2, le Grand Mât est à la verticale exacte du Pic ; la Montante débouche à côté du Pic ; un brin de menthe est dessiné près de l'Haleine.

**Fabrication.** La carte a besoin de noms de lieux : elle ne doit **pas** sortir du générateur d'images (qui ne sait pas écrire). Fond aquarellé généré sans texte, ou dessin vectoriel fait main ; les noms et les indices sont posés par-dessus dans la page. Description du fond : `an old hand-drawn nautical chart on cream paper seen from above, a few small rocky islands scattered on a flat white sea of clouds, fine ink lines and pale watercolour washes in blue and grey, a compass rose, a corner of night sky with small gold stars, no text, no letters`.

---

## 5. Le style graphique

Ligne de style (remplace celle du recueil pour cette collection) :

> `Illustrated children's novel frontispiece, hand-painted gouache look on textured paper, clean thin dark outlines, flat muted colours with deep night blues, soft greys and one warm golden light, simple shapes, detailed quiet landscape with small characters, wide composition, soft vignette edges. No text, no letters, no numbers, no signature, no watermark, no speech bubbles, no humans. `

Suffixe :

> ` Gentle animal characters standing upright in simple clothes, each one drawn only once.`

Ce qui reste cousin des Étoiles : aplats, contours fins et sombres, formes simples, douceur. Ce qui grandit avec le lecteur : une palette plus nocturne et plus sourde, des décors plus vastes où les personnages sont petits (c'est le monde qui est le héros de l'image), des proportions moins « bébé », un grain de papier. **Signature de la collection : une lumière dorée dans chaque frontispice** — lampe, lanterne, fenêtre ou étoile. Dans le dernier, il y en a deux.

Format : paysage, même rapport que les images existantes, pour que le bandeau de lecture se découpe dans le frontispice.

---

## 6. Les règles d'écriture (8-10 ans)

### Le temps du récit : passé simple et imparfait, à la troisième personne

Tranché, pour quatre raisons.

1. **C'est la marche d'après.** Les Étoiles sont au présent ; le passé simple est le temps des romans que ces enfants commencent à lire seuls, et celui qu'ils étudient en CM1-CM2. L'entendre bien employé, c'est l'apprivoiser.
2. **À l'oreille, il donne du relief.** L'imparfait installe (« la Mer était blanche et lisse »), le passé simple frappe (« l'étoile ne parut pas »). Avec une seule voix, sans musique ni bruitage, c'est la grammaire qui fait la mise en scène. Le présent aplatit tout sur un même plan — dix minutes de présent, c'est long.
3. **Il sert le suspens.** « Alors la barque se mit à tourner » : l'événement tombe, net.
4. **Il met de la distance.** Ce qui est raconté au passé a déjà eu lieu ; quelqu'un est revenu pour le dire. À l'heure du coucher, c'est rassurant.

Garde-fous : troisième personne seulement (jamais « nous partîmes ») ; pas de subjonctif imparfait ; on évite les formes qui font rire sans le vouloir. **Les dialogues sont au présent et au passé composé**, comme on parle. Le « précédemment » est au passé composé.

### La langue

- **Soutenue et limpide.** Le mot juste plutôt que le mot rare ; deux à quatre mots nouveaux par épisode (*amarre, fanal, vigie, tresser, se raviser…*), toujours éclairés par la phrase, jamais expliqués.
- **Des phrases de longueurs inégales.** Douze à quatorze mots en moyenne, quelques-unes de trois mots, de rares périodes de trente. Jamais deux longues de suite : la voix n'a pas de souffle à reprendre, l'auditeur si.
- **Écrire pour l'oreille.** Pas de parenthèses, pas d'italique porteur de sens, pas de majuscules pour crier : la voix ne les rend pas. Nombres en toutes lettres. Chasser les homographes piégeux (*l'est*, *les fils*, *le couvent*). Les noms propres doivent se prononcer sans hésiter.
- **Douze mots inventés**, pas plus (liste au § 4.1), introduits un par un, chacun dans une phrase qui le fait comprendre.
- **Le sensible avant l'abstrait.** On ne dit pas qu'Ancolie est triste : sa moufle unique tourne dans sa poche.

### Les dialogues (une seule voix les dit tous)

- **On sait toujours qui parle avant la fin de la première proposition** : nom avant la réplique, incise dès la première virgule, ou geste du personnage juste avant (« Osier ôta son chapeau. — Tu es tombée du Plafond. »).
- **Deux interlocuteurs par échange**, trois au plus ; jamais plus de trois répliques sans réattribuer.
- **Chacun se reconnaît à sa façon de parler** (les ordres et le « Point. » de Joubarbe, les chiffres d'Aulne, les questions d'Osier, les « petite » de Gentiane) : le tic fait l'attribution, le verbe de parole devient presque inutile.
- **Verbes de parole variés et rares** : pas plus d'un « dit » par page ; on préfère le geste à l'incise.
- Un quart à un tiers du texte en dialogue, pas davantage : c'est un récit, pas une pièce.

### L'humour

Il vient des **caractères** et des **malentendus entre les deux mondes** (la Lune qui s'éteint, la pomme de pin sur son coussin, l'ombre qui suit Osier), de la **précision comique** (les brasses d'Aulne) et de l'**euphémisme** (Gentiane). Au moins trois sourires par épisode, dont un dans le dernier tiers. Jamais de moquerie d'un personnage par la narratrice ; pas de clin d'œil aux parents.

### Le suspens sans la peur

- On remplace la peur par **l'étonnement, la hâte, le secret, la gêne**. Les enjeux sont le retard, la séparation, la vérité à dire — jamais le corps.
- **Ce qui inquiète est lent et doux** : on ne tombe pas, on descend ; on n'a pas mal, on a la peau qui tire.
- **L'obscurité est aimable** : la nuit est le lieu des lampes.
- **Chaque fin d'épisode est une question, pas une menace.** Test : l'enfant doit pouvoir s'endormir en *cherchant*, pas en *craignant*. La phrase rituelle « Cette nuit-là… » fait l'atterrissage.
- **Jeu loyal** : toute solution utilise quelque chose qu'on a déjà vu. Aucun hasard ne sauve personne.

### Ce qui est interdit

- Violence, blessure, mort, arme, maladie grave, créature effrayante ; personnes réelles, personnages sous licence, marques.
- « La morale de l'histoire », sous toutes ses formes : « elle comprit que… », « depuis ce jour… » suivi d'une leçon. Le sujet profond n'est jamais nommé — ni *fidélité*, ni *pardon*, ni *différence* n'apparaissent dans le texte.
- Un méchant. Il n'y a que des gens qui ont peur de perdre quelque chose.
- Des adultes idiots, et des enfants qui ont raison sur tout.
- Le schéma « trois essais ratés puis la solution » ; la fin « ce n'était qu'un rêve » ; le sauvetage par un adulte.
- « Soudain » plus d'une fois par épisode ; les adverbes en grappe ; « il dit, il dit, il dit ».
- Les scènes à plus de trois personnages parlants (et aucune scène illustrée à plus de trois).
- L'adresse au lecteur (« chers enfants », « tu te demandes sans doute… »).

### Échantillon de ton (une quarantaine de mots, pour juger la voix — non définitif)

> Toutes les étoiles tournaient. Ancolie le savait depuis toujours, comme on sait que l'eau mouille : au fil de la nuit, elles glissaient d'un bord du ciel à l'autre, sans se presser. Toutes, sauf une. Et ce soir-là, celle-là ne vint pas.

---

## 7. Trois questions ouvertes

1. **Animaux habillés, ou enfants humains ?** La bible propose un roman animalier (lynx, salamandre, bouquetin…) : il respecte la règle « pas d'humains » du recueil, tient dans le générateur d'images et dessine les deux pays par les espèces. Mais un lecteur de neuf ans s'identifie peut-être mieux à un enfant qu'à un lynx. Si vous préférez des humains, l'histoire tient telle quelle (une fille des Cimes, un garçon des marais) ; il faudra lever l'interdit, refaire les descriptions et prévoir un essai d'images avant d'écrire.

2. **Un épisode par soir, ou tout disponible d'un coup ?** Le feuilleton est écrit pour l'attente : ouvrir l'épisode suivant seulement le lendemain (ou après la fin du précédent) donne tout son poids au « à suivre », mais peut frustrer un enfant qui veut enchaîner — ou des parents en voiture. C'est un choix de produit, pas d'écriture.

3. **Une fin douce-amère, cela vous convient-il ?** Dans la version proposée, tout est réparé mais personne ne déménage : Ancolie et Osier rentrent chacun chez soi, avec une moufle chacun et une lampe pour se dire bonsoir. C'est la fin la plus juste, et elle laisse une porte pour une suite (les vieilles marches). L'autre possibilité — un passage ouvert, les deux pays réunis dès la dernière page — est plus joyeuse et moins vraie. À vous de dire jusqu'où une histoire du soir a le droit de serrer le cœur.
