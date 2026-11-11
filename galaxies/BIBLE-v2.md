# Les Galaxies — bible v2 : une bande, un trésor, un dernier été

État : **proposition à valider par le propriétaire.** Rien n'est écrit ni dessiné tant que cette bible n'est pas validée (bible d'abord, histoires ensuite, images en dernier).

Cette version remplace le contenu de `BIBLE.md` (feuilleton merveilleux, animaux habillés — non retenu) et en garde la fabrication : format précis, règles du monde, descriptions visuelles fixes, plan d'épisodes avec question en suspens, règles d'écriture. La commande, mot pour mot : « de vrais humains. une équipe qui résout des énigmes et a des aventures en mode Goonies ». On en prend l'**esprit** — la bande, les vannes, la carte, la course, le dernier été — et rien d'autre : aucun personnage, nom, lieu ni scène d'une œuvre existante.

---

## 1. La promesse

1. **Une bande.** Quatre gamins dépareillés — bientôt cinq — qu'on reconnaît à l'oreille dès leur première phrase, qui se chamaillent sans arrêt et ne se lâchent jamais. On voudrait avoir sa place au Wagon.
2. **Une chasse au trésor jouée à la loyale.** L'auditeur a toutes les pièces en main avant les héros. Chaque soir, on s'endort avec une énigme — pas avec une peur — et l'on se réveille en ayant trouvé.
3. **Un vrai endroit**, qu'on pourrait chercher sur une carte de France, avec son étang, son rocher, sa cheminée, et une vieille légende que tout le village raconte de travers.
4. **Un dernier été.** Dans vingt-quatre nuits, quelque chose s'éteint et un copain s'en va. Il faut réussir avant. C'est drôle tout du long, et à la fin ça serre un peu le cœur.
5. **Des adultes qui ne voient rien** — et qui ont pourtant, chacun, la moitié d'une réponse dans la poche. Ici, personne n'est méchant : il y a seulement des gens pressés, et des enfants qui courent plus vite.

---

## 2. Le format

| | Les Galaxies |
|---|---|
| Unité | une **saison** = une seule grande aventure |
| Épisodes | **8** |
| Durée d'un épisode | **≈ 10 minutes** |
| Longueur d'un épisode | **1 500 mots** (fourchette 1 400 – 1 600), hors « précédemment » |
| Longueur d'une saison | ≈ 12 000 mots, ≈ 85 minutes d'écoute |
| Images | **1 illustration par épisode** + **1 carte à observer** = 9 images (+ 1 couverture sans personnage, facultative) |

La durée est à vérifier sur un essai de voix (hypothèse : 145-150 mots par minute). Si la voix est plus lente, on descend à 1 400 mots plutôt que de dépasser dix minutes.

### Structure d'un épisode : six temps

Ce n'est pas une mécanique visible ; les temps peuvent se fondre, mais chaque épisode les contient tous.

1. **La réponse** (≈ 200 mots). L'énigme de la veille est résolue dans les deux premières minutes — par un détail que l'auditeur possédait déjà. On ne triche jamais.
2. **La course** (≈ 350 mots). On y va : à vélo, à pied, en douce. Un obstacle, un adulte à contourner, et l'adversaire qu'on aperçoit — devant ou derrière.
3. **Le moment de bande** (≈ 250 mots). Une scène à deux ou trois où l'on ne cherche rien : une vanne qui dérape, une partie de billes, un aveu qui ne sort pas. C'est là que vit le vrai sujet.
4. **La trouvaille** (≈ 300 mots). Une cachette, un objet, un texte gravé. L'énigme suivante est lue **deux fois** (voir § 6).
5. **Le revers** (≈ 250 mots). Ce qu'on croyait acquis se retourne : l'autre est passé avant, un secret tombe, la bande se fend.
6. **L'énigme de la nuit et la phrase du four** (≈ 150 mots). L'épisode s'arrête sur une question qu'on peut chercher dans son lit, puis sur une phrase rituelle, toujours la même, qui ralentit et borde : *« Ce soir-là, le Grand Four brûlait encore. Il lui restait vingt-quatre nuits. »* Le chiffre baisse d'épisode en épisode. C'est le compte à rebours — et c'est une berceuse.

**Règle de fin d'épisode : une porte qui s'ouvre, jamais une lame qui tombe.** L'enfant doit pouvoir s'endormir en *cherchant*, pas en *craignant*.

### Le « précédemment »

- Absent de l'épisode 1.
- **Trois phrases, 50 mots au plus**, au passé composé, qui redonnent les **prénoms** de ceux qui vont parler ; puis **l'énigme de la veille, redite mot pour mot** (elle ne compte pas dans les 50 mots). Celui qui revient après une semaine doit pouvoir jouer.
- Fichier audio séparé, passable d'un geste : celui qui enchaîne deux épisodes ne le subit pas.

### À l'écran

- **Ouverture** : l'illustration plein écran ; la voix dit le numéro et le titre.
- **Lecture** : texte en grand corps, clair sur bleu nuit, surlignage mot à mot conservé ; une « page » = un paragraphe de 45 à 70 mots.
- **Fin** : un carton « À suivre » où **l'énigme de la nuit est écrite en toutes lettres** (c'est la page qui l'affiche, pas l'image : le générateur ne sait pas écrire), et un bouton vers la carte.
- **La carte** se rouvre après chaque épisode ; un oiseau s'y allume à chaque clef trouvée.
- **Progression** : cinq billes de couleur en haut de l'écran — bleue, jaune, verte, violette, rouge. La rouge ne s'allume qu'à la toute fin.

### Fichier source (compatible avec l'outillage existant)

Un fichier par saison (`galaxies/feles1.txt`), descriptions dans `galaxies/personnages.json`, même esprit que `histoires/*.txt` :

```
=== feles1_3
titre: Le moine qui ne priait pas
precedemment: Yasmine, Nuno et Lucie ont… (≤ 50 mots)
enigme: Va chez les verriers, là où ils se taisent…
nuits: 20
@ description unique de l'illustration, en anglais, avec {gaspard}, {nuno}, {etang}…
Une ligne = une page lue (45 à 70 mots).
(ligne vide = changement de temps)
```

### Les saisons suivantes

La bande est **une bande d'été** : à la fin de la saison 1, la vie la disperse. Chaque saison, elle se retrouve — chaque fois **chez l'un d'eux**, donc dans un lieu neuf, avec une légende neuve et un fil qui court d'une saison à l'autre (§ 4.8). Une saison se suffit : huit épisodes, une aventure bouclée. Qui n'a écouté que la première n'a rien manqué ; qui l'a aimée sait qu'il reste une page au carnet.

---

## 3. Trois propositions de bande et d'aventure

### A — « Les Fêlés : l'or d'Aubin » · un village verrier dans la forêt · *recommandée*

**Accroche.** À Valbraise, le four de la verrerie brûle sans interruption depuis cent soixante ans. On l'éteint le premier septembre. Il reste vingt-quatre nuits de feu, quatre gamins qu'on appelle les Fêlés, et, au fond d'une benne, un vieux moule en bois dans lequel personne n'a jamais soufflé.

**La bande.**
- *Yasmine*, onze ans : la cheffe, qui met tout aux voix et perd les votes qu'elle organise.
- *Nuno*, dix ans : commente sa propre vie comme un match de foot ; plaisante pour ne pas dire qu'il s'en va.
- *Lucie*, dix ans : voit tout, le dit une fois, tout bas, et personne n'écoute.
- *Gaspard*, dix ans : petit-fils de souffleur, costaud, prudent, un sac à dos « au cas où » — et le vertige.
- *Apolline*, dix ans : la fille de l'adversaire, qui parle comme un dictionnaire et n'a jamais eu de copains plus de quatre mois.

**Le lieu.** Un village de grès rose au creux des Vosges du Nord : une verrerie et sa grande cheminée, un étang, une chapelle aux vitraux, un château en ruine sur un rocher qui fait de l'écho, une forêt de hêtres. Le quartier général : un wagon de marchandises oublié sur une voie envahie d'herbes.

**La légende et le trésor.** Il y a cent cinquante ans, une comtesse paya maître Aubin cent pièces d'or pour cent verres d'un rouge « comme une braise qu'on regarde à travers ». Il en livra quatre-vingt-dix-neuf ; l'or disparut ; plus personne ne sut refaire ce rouge. Tout Valbraise a creusé pour trouver « l'or d'Aubin ». Or l'or n'a jamais été caché : **il est dans le verre** — c'est l'or fondu qui fait le rouge. Le trésor est une couleur perdue, le carnet de celle qui l'a vraiment inventée (Colombe, douze ans, qui n'avait pas le droit de souffler), et un verre qui n'existe pas encore : le centième.

**L'adversaire et sa raison.** Madame Delcourt, chargée par la Compagnie d'inventorier la verrerie avant fermeture : elle colle une gommette orange sur tout ce qui a de la valeur. Elle a grandi près d'une usine qu'on a laissée mourir dix ans ; elle croit aux fins nettes et aux belles choses mises à l'abri sous vitrine. En droit, elle a raison : tout appartient à la Compagnie.

**La raison intime.** Le père de Nuno, meilleur souffleur de la vallée, a trouvé du travail au Portugal : la famille part le premier septembre. Gaspard veut être verrier et il n'y aura plus de verrerie. C'est la dernière aventure à quatre — et la seule chance que le feu ne s'éteigne pas tout à fait.

**Le sujet profond, jamais énoncé.** Ce qui est précieux ne se garde pas, ça se passe de main en main : un feu, un tour de main, une bille, une amitié. Et l'or est souvent déjà là, sous nos yeux, dans ce qu'on ne regarde plus.

### B — « Le Trésor coupé en deux » · une île bretonne, la grande marée · grand air et comédie de rivalité

**Accroche.** Sur l'île de Trévarn, la plus grande marée de l'année découvrira pendant une heure, fin août, la Chaussée des Deux-Frères. Les enfants de l'île ont une moitié de carte. Les vacanciers d'en face ont l'autre. Aucune des deux bandes n'a l'intention de partager.

**La bande** (« les Bottes », enfants de l'île).
- *Maël*, onze ans : fils de la patronne du bateau-navette ; lit la mer mieux que ses propres colères.
- *Awa*, dix ans : fille du médecin, arrivée il y a deux ans ; commence toutes ses phrases par « En fait… ».
- *Enora*, dix ans : fille des crêpiers ; menteuse de génie, fournisseuse officielle d'alibis.
- *Tino*, neuf ans : petit frère de Maël ; n'a peur de rien, sauf des crabes, et répète tout ce qu'il ne fallait pas répéter.

**Le lieu.** Une île sans voitures, aujourd'hui : un port, une cale, un phare, une école à classe unique, des rochers qui ont tous un nom et un caractère. À dix ans personne n'a de téléphone, et le réseau s'arrête au bout de la jetée.

**La légende et le trésor.** Un capitaine corsaire revenu riche avait deux fils fâchés à mort — l'un resté pêcheur sur l'île, l'autre parti négociant sur le continent. Il coupa sa carte en deux : « Vous trouverez ensemble, ou pas du tout. » Ils ne trouvèrent jamais. L'or, lui, a servi depuis longtemps : c'est la jetée du port, sur laquelle tout le monde marche. Dans le coffre : la figure de proue de son navire, *la Rieuse*, emblème perdu de l'île, et deux longues-vues jumelles, une pour chaque fils.

**L'adversaire et sa raison.** *Victoire*, onze ans, cheffe des « Tongs », la bande des estivants : elle descend du fils qui est parti, et on lui répète depuis toujours que l'île a volé leur part. Elle est aussi têtue, aussi drôle et aussi seule que Maël.

**La raison intime.** Maël entre en sixième en pension sur le continent ; sans lui, l'école passe sous le nombre d'élèves qui la maintient ouverte. C'est la famille de Victoire, si elle s'installe, qui peut la sauver.

**Le sujet profond.** Ceux qui partent et ceux qui restent ; on n'est pas obligé d'hériter d'une fâcherie.

**Réserves.** C'est la proposition la plus attendue (mer, île, corsaire) ; la marée est une horloge magnifique mais elle frôle le danger physique, qu'il faudrait désamorcer à chaque épisode ; l'imagerie (port, bateaux, passes) est voisine de celle de la première bible, que le propriétaire n'a pas retenue.

### C — « La Treizième Heure » · un vieux quartier de Lyon, ses traboules · malice et mécanique

**Accroche.** Dans une cour des pentes de la Croix-Rousse, une horloge arrêtée depuis toujours sonne un soir treize coups. Derrière le cadran, quelqu'un avait tout prévu : il ne manquait que des enfants assez curieux pour compter.

**La bande** (les enfants d'une même cour, aujourd'hui).
- *Rose*, onze ans : petite-fille de la dernière tisseuse ; garde la clef de tout, n'ouvre son cœur à personne.
- *Bilal*, dix ans : démonte tout, remonte rarement ; parle en pièces détachées.
- *Sacha*, dix ans : ne se déplace qu'en trottinette, connaît chaque passage ; incapable de se taire.
- *Minh*, neuf ans : retient les mélodies, les codes et les numéros ; n'aime pas le noir, et le dit.

**Le lieu.** Les traboules, ces couloirs qui traversent les immeubles d'une rue à l'autre ; des cours à galeries, des escaliers sans fin, un atelier avec le dernier métier à tisser, le funiculaire qu'on appelle « la ficelle ».

**La légende et le trésor.** Un canut horloger, il y a deux siècles, aurait caché son chef-d'œuvre le jour où l'on saisit son atelier. Ce n'est pas de l'or : c'est un jeu de cartons perforés — un code fait de trous — qui, monté sur le vieux métier, tisse le portrait de tous les habitants de la cour ; et la preuve que l'invention est née ici, ce qui fait de l'immeuble un lieu qu'on n'a plus le droit de vider.

**L'adversaire et sa raison.** Monsieur Vial, horloger et collectionneur : il a passé trente ans à réunir les pièces dispersées de l'inventeur. Il les aime plus que personne — et les veut chez lui, à l'abri des enfants.

**La raison intime.** L'immeuble est vendu ; l'atelier de la grand-mère de Rose sera vidé le trente septembre et la bande relogée aux quatre coins de la ville.

**Le sujet profond.** Ce qu'on fabrique ensemble nous tient ensemble.

**Réserves.** La ville, la nuit, les toits : l'aventure pousse vers des endroits où l'on ne veut pas envoyer des enfants de dix ans, même en imagination ; les énigmes mécaniques (rouages, cartons perforés) sont plus belles à voir qu'à entendre.

### Recommandation : A, « Les Fêlés »

1. **Elle est à nous.** Une île au trésor ou un passage secret en ville, on en a lu vingt. Un trésor de verrier, non. Et le retournement — l'or n'est pas caché, il est *dans* le rouge — est vrai (on teinte le verre en rouge rubis avec de l'or), surprenant, et **trouvable par l'auditeur**, à qui l'on a dit trois épisodes plus tôt que le jaune se fait avec de l'argent.
2. **Le compte à rebours est dans le décor.** Un four de verrerie ne s'éteint jamais ; quand on l'éteint, c'est fini. « Il lui restait douze nuits » : pas besoin de méchant pour avoir de la hâte.
3. **La bande est la solution.** Les verriers travaillent en équipe de cinq, qu'on appelle *une place*. La chasse a été conçue il y a cent cinquante ans pour n'être réussie qu'à cinq. Les Fêlés sont quatre. La cinquième est dans le camp d'en face.
4. **Elle va bien au dessin.** Le verre, le feu, le grès rose, la forêt : des matières que le générateur rend bien. Et cinq enfants, cinq couleurs — jaune, rouge, vert, bleu, violet — qu'on ne peut pas confondre.
5. **Elle est sûre.** Ni mer, ni marée, ni mine, ni toits : un étang où l'on a de la boue aux genoux, un rocher avec une rampe, un souterrain où l'on tient debout.
6. **Elle est loin de la première bible** (pas de port, pas de bateaux, pas de lampe dans la nuit), et elle appelle naturellement une saison 2.

Son risque, à dire franchement : elle sent moins les embruns et les pirates que B. Si c'est la mer que le propriétaire voit quand il dit « Goonies », B se développe avec la même méthode.

---

## 4. Bible complète — « Les Fêlés : l'or d'Aubin »

### 4.1 Quand, où, et les règles du jeu

**Quand : un été du milieu des années 1990** (le texte ne donne jamais l'année). Choix tranché, pour quatre raisons.

1. **Pas de téléphone, pas d'internet** : une énigme se résout avec la tête et les copains, pas avec un moteur de recherche ; pour se parler il faut se retrouver ; quand on a disparu derrière la verrerie, aucun parent ne peut vous rappeler.
2. **La narratrice y gagne un visage.** Une seule voix de femme lit tout : autant qu'elle soit *quelqu'un*. C'est l'un des enfants, devenue adulte, qui raconte l'été de ses dix ans — on ne l'apprend qu'à la dernière page (§ 4.8). La contrainte devient le plus beau secret de la saison, et « l'histoire du soir » devient celle qu'une mère raconte de sa propre enfance.
3. **C'est l'époque juste** : celle où les verreries de village ont fermé, et où les enfants d'un village partaient le matin pour ne rentrer qu'au coup de sifflet du soir.
4. **Cela ne coûte rien à l'image** : des vélos, des shorts, des cabanes. La seule différence visible, c'est qu'il n'y a pas d'écran.

Marqueurs d'époque, discrets : les francs, la cabine téléphonique de la Fontaine, deux talkies-walkies, un appareil photo à développement instantané. Jamais de clin d'œil aux parents.

*Variante si le propriétaire préfère aujourd'hui* : l'histoire tient presque telle quelle — à dix ans, en CM2, on n'a pas encore de téléphone, et la forêt n'a pas de réseau. On y perd la narratrice révélée.

**Où : Valbraise**, village inventé des Vosges du Nord, aux confins de la Lorraine et de l'Alsace — pays réel de grès rose, de forêts, d'étangs, de châteaux perchés sur des rochers et de verreries. Tout tient dans un cercle de vingt minutes à vélo.

**Les règles** (elles ne changent jamais ; toute solution doit en sortir).

1. **Le Grand Four ne s'éteint jamais** — jusqu'à l'aube du premier septembre. Chaque épisode se clôt sur le nombre de nuits qui lui restent : 24, 22, 20, 16, 12, 8, 3, puis plus aucune.
2. **Le Grand Sifflet** de la verrerie sonne à six heures, à midi, à dix-huit heures. Au sifflet du soir, les enfants de Valbraise rentrent dîner : c'est la loi, et c'est la limite de chaque expédition. Une seule exception par été : **la nuit au Wagon**, autorisée une fois — elle servira à l'épisode 6.
3. **Les gommettes.** Tout ce que madame Delcourt inventorie reçoit une gommette orange et un numéro de lot : cela appartient à la Compagnie. La loi de la bande, votée par Yasmine : **« On ne prend rien qui porte une gommette. »** Les Fêlés ne volent pas. (Le moule sort d'une benne, où on l'avait jeté pour être brûlé.)
4. **Le vote.** Toute décision se vote. À quatre, on tombe sans cesse à deux contre deux : l'égalité se tranche **aux billes**. À cinq, il n'y a plus d'égalité possible — on le découvrira.
5. **Les talkies-walkies** portent « jusqu'à la Fontaine, pas plus » : en pratique, on s'entend mieux en criant.
6. **Le feu est aux grands.** Les enfants ne touchent jamais au verre chaud sans un souffleur derrière eux. Gaspard en rêve ; il attendra l'épisode 8.
7. **Aucun adulte ne résout une énigme.** Les adultes donnent des pièces sans le savoir, parce qu'ils parlent de leur métier ou qu'ils radotent.
8. **La chasse est faite pour cinq.** Celle qui l'a construite l'a voulu ainsi (§ 4.5).

**Le vocabulaire du verre** — douze mots, pas un de plus, introduits un par un, chacun dans une phrase qui l'éclaire : *le four, la canne* (le long tube où l'on souffle), *cueillir* (prendre du verre au bout de la canne), *la paraison* (la bulle de verre encore molle), *le moule, l'ouvreau* (la petite porte du four), *la sole* (son plancher de pierre), *une place* (l'équipe de cinq verriers), *le gamin* (le plus jeune de la place, celui qui court), *un calot* (une grosse bille), *la halle, le moine* (la bonde de pierre d'un étang).

### 4.2 Le lieu et ses dix endroits

Vue d'ensemble, pour toute image d'extérieur large : `a small old village of pink sandstone houses with red tiled roofs in a narrow wooded valley, dominated by a long red brick glassworks with one very tall brick chimney giving off a thin line of white smoke, dense green beech and pine forest on the slopes all around, summer light`

| Lieu | Ce qui s'y joue | Description fixe (anglais) |
|---|---|---|
| **Le Wagon** | le quartier général ; on y vote, on y joue aux billes, on y dort une nuit par été | `an old rust-red wooden freight wagon standing on a disused railway siding overgrown with tall grass and wild flowers, behind a long red brick factory wall, its sliding door half open, a patched striped curtain in the doorway, a storm lantern hanging inside, bicycles lying in the grass` |
| **La Grande Halle** | le Grand Four, les souffleurs, la dernière nuit | `the inside of a vast old glassworks hall with a high dark timber roof and tall dusty windows, in the centre a big round brick furnace with several small arched openings glowing bright orange, long steel blowpipes on racks, wooden benches and iron tools` |
| **Le Magasin aux moules** | le grenier de la verrerie, royaume de l'inventaire | `a long dim attic storeroom under a sloping timber roof, wooden shelves from floor to ceiling crowded with hundreds of old wooden and iron moulds of all sizes, dust floating in shafts of light from small skylights, round bright orange stickers on many objects` |
| **La Fontaine** | la place du village : l'épicerie, la cabine, le banc de Pépé | `a small village square with a round pink sandstone fountain, an old lime tree with a green wooden bench under it, and a little corner grocery shop with a red and white striped awning and crates of fruit outside` |
| **La rue des Souffleurs** | les maisons d'ouvriers ; une boule de verre à chaque fenêtre, une seule est rouge | `a straight street of identical small red brick workers' terraced houses with tiny front gardens and low wooden fences, one glass ball hanging in every front window` |
| **L'étang Neuf** | le moine, la première clef, la boue | `a quiet forest pond with dark green water, reeds and water lilies, closed at one end by a grassy earth dam; in the water close to the dam stands a square stone sluice tower as tall as a child, topped with a flat stone slab` |
| **La chapelle des Verriers** | le vitrail, la tache rouge de six heures | `the inside of a tiny pink sandstone forest chapel with bare walls and a few wooden benches, one tall narrow stained-glass window made of small diamond-shaped panes of blue, green, yellow and violet glass with one single deep red pane, coloured patches of light lying on the grey flagstone floor` |
| **La Roche Bavarde** | le château en ruine, l'écho, le vertige de Gaspard | `a huge outcrop of red-pink sandstone rising high above the treetops, with the ruins of a small medieval castle on top: a broken round tower, worn steps carved into the rock with an iron handrail, a doorway cut in the stone, and a shallow square basin carved in the rock, full of rainwater` |
| **La Galerie** | le passage sous la verrerie ; le lot 213 | `a low vaulted tunnel of old red bricks running under a factory, dry sandy floor, just high enough for a child to stand upright, small arched niches in the walls, lit only by a hand torch` |
| **La Bosse** | la butte où l'on fait de la luge depuis toujours ; dessous, le premier four | `a round mound as tall as a man in a clearing of a beech forest, covered with thick green moss and ferns; under the moss, the ruin of a very old round glass furnace of stone and blackened brick shaped like a beehive, with five small arched openings spaced evenly around it` |

### 4.3 La bande

On les appelle **les Fêlés**. Le mot vient du contremaître, un jour de carreau cassé ; Pépé leur en a donné le vrai sens : un verre fêlé sonne faux, mais il tient. Leur devise, trouvée par Nuno, qui ne sait pas qu'elle servira : **« Fêlés, pas cassés. »**

Règle de narration : la narratrice n'emploie qu'**un seul nom par personnage** — le prénom. Les surnoms n'existent que dans la bouche de Nuno.

#### Yasmine Belkacem — onze ans, la cheffe

- **Caractère** : organisée jusqu'au ridicule, juste, mauvaise perdante, loyale comme un mur.
- **Talent** : la logique. Elle range les indices, lit les plans, repère ce qui cloche dans un raisonnement.
- **Faille** : l'imprévu la panique, alors elle commande. Elle entre au collège en septembre, seule de la bande, par le car de sept heures : c'est elle qui a le plus peur de la rentrée, et elle préférerait avaler son carnet que de l'avouer.
- **Façon de parler** : en listes numérotées — « Un : on se tait. Deux : on vote. » — et elle clôt par « Vote. » ou « Adopté. ». Elle perd régulièrement les votes qu'elle organise.
- **Lien** : amie de Lucie depuis la maternelle ; se dispute avec Nuno comme on respire ; admire en secret madame Delcourt, qui fait des listes encore mieux qu'elle.
- **Famille** : sa mère tient l'épicerie de la Fontaine, son père taille le cristal à la verrerie depuis vingt ans. Deux grands frères au lycée ; les Belkacem resteront à Valbraise quoi qu'il arrive — c'est bien ce qui l'inquiète.
- **Visuel** : `one eleven-year-old girl, the tallest of the group, thin with long legs, light brown skin, dark brown eyes, black hair in one very long thick braid reaching her waist, wearing a bright yellow hooded windbreaker over grey shorts, a small notebook hanging from a string around her neck`

#### Nuno Ferreira — dix ans, le commentateur

- **Caractère** : drôle, vif, vantard, généreux en cachette. Il donne un surnom à tout le monde et un calembour à chaque malheur.
- **Talent** : il court, il grimpe, il se faufile — et ses jeux de mots idiots tombent parfois, sans qu'il le veuille, sur la réponse.
- **Faille** : il est incapable de dire une chose sérieuse. Il sait depuis juin qu'il part ; il ne l'a dit à personne.
- **Façon de parler** : il **commente l'action comme un match**, en parlant de lui à la troisième personne : « Et c'est Ferreira qui s'élance… le public retient son souffle… » Quand quelque chose le touche, le commentaire s'arrête au milieu.
- **Lien** : meilleur ami de Gaspard, qu'il charrie du matin au soir ; adversaire préféré de Yasmine.
- **Famille** : son père, Zé, est le meilleur souffleur de la vallée ; sa mère peint les filets d'or sur les verres. La famille repart au Portugal, dans une ville de verriers où vit la grand-mère, le premier septembre.
- **Visuel** : `one ten-year-old boy, the shortest of the group, small and wiry, olive tan skin, brown eyes, a big mop of very curly dark brown hair, a gap between his front teeth, wearing a plain bright red sleeveless football shirt over a white T-shirt, a black walkie-talkie clipped to his belt`

#### Lucie Marchal — dix ans, celle qui voit

- **Caractère** : calme, attentive, têtue en silence. Elle compte les marches, les fenêtres, les boules de verre.
- **Talent** : l'observation. Rien ne lui échappe : une brique sous la mousse, des cartons dans un couloir, une boule rouge parmi les vertes.
- **Faille** : elle ne dit les choses qu'une fois, tout bas, et quand on ne l'écoute pas elle laisse les autres se tromper. Il lui faudra apprendre à répéter plus fort.
- **Façon de parler** : très peu. Elle commence par **« Attendez. »**, puis une phrase courte et exacte. Dix minutes plus tard : « Je l'ai dit. »
- **Lien** : l'ombre de Yasmine depuis toujours ; la seule à qui Nuno ne donne pas de surnom, sans qu'on sache pourquoi.
- **Famille** : son père est garde forestier, né à Valbraise ; sa mère, infirmière, venue de Guadeloupe, sillonne la vallée en voiture. Fille unique, elle habite la maison forestière, à la lisière.
- **Visuel** : `one ten-year-old girl of medium height, slim, dark brown skin, large dark brown eyes, black curly hair tied in two big round afro puffs, wearing bright green denim dungarees over a white T-shirt, old black binoculars hanging around her neck`
- **Ce qu'on ne sait pas encore** : c'est elle qui raconte (§ 4.8). Indices loyaux : la narratrice n'entre que dans ses pensées à elle, jamais dans celles des autres.

#### Gaspard Thiriet — dix ans, le costaud prudent

- **Caractère** : lent, sûr, râleur, tendre. Il prévoit le pire et il a tout ce qu'il faut pour y faire face.
- **Talent** : il connaît le verre et la forêt, il est fort, et son sac contient toujours l'objet qu'il faut — une ficelle, un pied-de-biche, une lampe, un sandwich.
- **Faille** : le vertige, et l'obéissance. Il veut être souffleur comme son grand-père ; depuis l'annonce, il n'ose plus le dire.
- **Façon de parler** : posée, avec trois refrains — « Mon pépé dit que… », « Au cas où. », et, après chaque prédiction de catastrophe, « Je dis ça, je dis rien. »
- **Lien** : meilleur ami de Nuno ; il a perdu contre lui, le premier jour, son calot rouge porte-bonheur, et il fait semblant de s'en moquer.
- **Famille** : son grand-père, Pépé, a soufflé cinquante ans. Son père a refusé le four et conduit un camion — les deux hommes ne s'en parlent pas. Sa mère sert à la cantine de la verrerie.
- **Visuel** : `one ten-year-old boy, big, broad and sturdy, almost as tall as the tall girl and twice as wide, pale freckled skin, blue eyes, straight straw-blond hair cut in a bowl shape, wearing a bright blue adult work jacket far too big for him with the sleeves rolled up, a huge khaki backpack on his back`

#### Apolline Delcourt — dix ans, la cinquième

Elle n'est pas de la bande au début : elle la regarde depuis l'autre côté.

- **Caractère** : brillante, raide, seule. Elle ment un peu pour se rendre intéressante (un cheval, un oncle explorateur), puis s'en veut.
- **Talent** : elle a tout lu et retient les textes par cœur ; elle sait ce qu'il y a dans le registre de sa mère.
- **Faille** : sept écoles en quatre ans. Elle ne sait pas comment on entre dans une bande, alors elle essaie d'acheter sa place avec des renseignements.
- **Façon de parler** : comme un livre — « En l'occurrence… », « Techniquement… », des phrases entières avec leurs subordonnées. Plus tard, elle essaie l'argot de Nuno et le rate à chaque fois.
- **Lien** : bat Nuno aux billes dès la première partie, ce qu'il ne lui pardonne pas ; Yasmine la trouve formidable et suspecte.
- **Famille** : sa mère, madame Delcourt, qu'elle suit d'usine en usine ; un père à Paris, qui téléphone le dimanche à la cabine.
- **Visuel** : `one ten-year-old girl, small and neat, a little shorter than the girl in green, very pale skin, grey eyes behind round glasses with thin gold frames, straight ginger red hair cut in a chin-length bob with a fringe, wearing a bright violet short-sleeved dress with a white collar, a small brown leather satchel worn across her body`

**Contrôle des silhouettes.**

| | Taille et carrure | Cheveux | Couleur | Accessoire |
|---|---|---|---|---|
| Yasmine | la plus grande, mince | très longue tresse noire | **jaune** | carnet au cou |
| Nuno | le plus petit, nerveux | tignasse bouclée brune | **rouge** | talkie-walkie |
| Lucie | moyenne, fine | deux gros chignons afro | **vert** | jumelles |
| Gaspard | grand et large | blond paille, coupe au bol | **bleu** | énorme sac à dos |
| Apolline | petite, menue | carré roux à frange | **violet** | lunettes rondes, sacoche |

Cinq enfants, cinq couleurs — les cinq couleurs des clefs de verre. Nuno le remarque à l'épisode 7 : « On est assortis. C'est louche. »

### 4.4 Les autres personnages

**Madame Delcourt** — l'adversaire. Quarante-cinq ans, chargée d'inventaire pour la Compagnie.
- *Caractère* : exacte, courtoise, infatigable. Elle ne hausse jamais la voix et n'a jamais tort sur un point de droit.
- *Sa raison* : son père taillait le verre dans une usine du Nord qu'on a laissée agoniser dix ans ; il a gardé dix ans les clefs d'un atelier vide. Elle s'est juré que les fins seraient nettes, et que les belles choses iraient sous vitrine, à l'abri, plutôt que de pourrir dans un grenier. Elle veut le rouge pour qu'il soit sauvé — rangé.
- *Faille* : elle range ce qui vit encore.
- *Ce qu'elle a et que la bande n'a pas* : le Grand Livre de la verrerie, les plans des bâtiments, une voiture. *Ce qui lui manque* : le moule, donc les lieux — et quatre copains.
- *Façon de parler* : des numéros de lot et « C'est noté. » ; elle dit « jeunes gens ».
- *Visuel* : `one tall slender woman of about forty-five with very straight posture, pale skin, grey eyes, silver-grey hair in a sharp chin-length bob, wearing a charcoal grey trouser suit with a bright orange silk scarf, holding a clipboard and a sheet of round bright orange stickers`

**Zé Ferreira** — le père de Nuno, souffleur. Allié malgré lui.
- *Caractère* : calme, précis, peu causant ; depuis l'annonce il fait ses cartons le soir et ne regarde plus le four en face.
- *Rôle* : il répond à toutes les questions techniques sans jamais se demander pourquoi on les lui pose. C'est lui qui dit, sans le savoir, les deux phrases dont tout dépend (le moule à l'envers ; le jaune et l'argent).
- *Façon de parler* : courte, avec le verre pour mesure de tout — « Doucement. Le verre n'aime pas les pressés. »
- *Visuel* : `one stocky man of about forty with strong forearms, olive tan skin, brown eyes, short curly black hair and a thick black moustache, wearing a white sleeveless undershirt and a long brown leather apron, a dark green bandana around his neck, holding a long steel blowpipe`

**Pépé** (Aimé Thiriet) — le grand-père de Gaspard. L'ancien qui sait à moitié.
- *Caractère* : malicieux, sourd quand ça l'arrange, assis du matin au soir sur le banc de la Fontaine, face à la cheminée.
- *Ce qu'il sait* : que le moule à l'oiseau est « le moule de personne » et qu'on n'y touche pas ; que le premier four était dans la forêt ; que la cheminée s'appelle « la grande dame » ; la comptine. *Ce qu'il tait* : il a cherché l'or lui-même, à vingt ans, et on a ri de lui.
- *Façon de parler* : des proverbes de verrier, un juron unique — « Nom d'une canne ! » —, et « Hein ? » dès qu'une question le dérange.
- *Visuel* : `one very old thin man of about eighty-five, slightly stooped, pale wrinkled skin, bushy white eyebrows and a big white walrus moustache, wearing a dark flat cap and a mustard yellow knitted cardigan, leaning on a wooden walking stick`

**Mademoiselle Garance** — quatre-vingt-onze ans, ancienne graveuse. L'ancienne qui sait tout.
- *Caractère* : menue, gaie, cérémonieuse ; tout le village la croit un peu perdue parce qu'elle parle à ses géraniums.
- *Ce qu'elle sait* : la vérité sur Colombe, dont elle est l'arrière-petite-nièce. Elle porte au cou une larme de verre rouge ; la boule de sa fenêtre est la seule boule rouge de la rue. **Personne ne lui a jamais rien demandé.**
- *Façon de parler* : douce, à l'ancienne ; appelle les enfants « mes agneaux » ; finit par « Mais on ne me demande rien, à moi. »
- *Visuel* : `one tiny very old woman of about ninety, frail and smiling, pale skin, thick round glasses, white hair in a high round bun, wearing a long navy blue dress with a white lace collar and a coral pink knitted shawl, a small red glass teardrop pendant on a cord around her neck`

**Madame Belkacem** — la mère de Yasmine, épicière. Alliée malgré elle.
- *Caractère* : rieuse, débordée, au courant de tout ce qui se passe à Valbraise — sauf de ce que fait sa fille.
- *Rôle* : sa farine, son sel, son arrière-boutique et le miroir rond de sa boutique servent à l'épisode 2 ; chaque service se paie en corvées de cageots.
- *Façon de parler* : elle mélange les prix et les nouvelles — « Trois francs cinquante, et tu diras à ta mère que le car de jeudi est supprimé. »
- *Visuel* : `one round cheerful woman of about forty, light brown skin, dark eyes, black wavy hair in a low bun, wearing a long white grocer's coat over a turquoise blouse, a pencil behind her ear`

**Aubin et Colombe** — ceux de la légende (§ 4.5). Jamais dessinés.

### 4.5 La légende, la carte et les objets

**La légende, telle que Valbraise la raconte.** Il y a cent cinquante ans, une comtesse venue de loin commanda à maître Aubin cent verres d'un rouge que personne n'avait jamais vu, « rouge comme une braise qu'on regarde à travers », et les paya d'avance : cent pièces d'or. Aubin livra quatre-vingt-dix-neuf verres. La comtesse ne réclama rien. L'or, on ne le revit jamais. Quand on le pressait, Aubin répondait : « L'or ? Je l'ai rendu, jusqu'au dernier grain. » Personne ne le crut. Après lui, plus un verrier ne sut refaire ce rouge. Depuis, on a retourné des caves, sondé l'étang, soulevé des dalles. Et les petites filles sautent à la corde sur une comptine dont personne n'écoute plus les paroles :

> Colombe, Colombe, où est ton or ?
> — Ni sous la pierre, ni dans le coffre-fort.
> Colombe, Colombe, qui l'a mangé ?
> — C'est le feu, le feu, qui l'a tout changé.
> Colombe, Colombe, où le voit-on ?
> — Regarde au travers, pas dans le fond.

**Ce qui s'est vraiment passé** (ce que la bande découvre). Aubin n'a rien volé : pour faire du rouge, il faut de l'or, fondu dans le verre. Il l'a « rendu » dans chaque verre livré. Et le rouge n'était pas de lui. C'est sa filleule, **Colombe**, douze ans, qui trouva la dose et le tour de main, la nuit, au vieux four de la forêt — une fille au four, cela ne se pouvait pas, alors Aubin signa. Colombe n'était pas un oiseau. Devenue graveuse — cela, on le permettait aux femmes —, elle cacha avant de mourir son carnet et l'or de la centième pièce, et bâtit une piste qu'on ne peut suivre qu'**à cinq**, comme une place de verriers, parce que « le rouge ne se fait pas seul ». Pour les enfants du village, elle fit des calots rouges, qui passent de poche en poche depuis cent cinquante ans.

**Le Grand Livre** (ce que possède madame Delcourt). Le registre de la verrerie porte, à la mort d'Aubin, cette note du directeur d'alors : *« Aubin mort ce jour. N'a rien dit de l'or. Sa filleule dit seulement : le secret est au moule à l'oiseau. Le moine a la première, la lumière la deuxième, l'écho la troisième, la grande dame la quatrième ; et la cinquième, les enfants l'ont. On n'y a rien compris. »* Madame Delcourt a donc la liste des gardiens sans les lieux ; la bande a les lieux sans la liste. C'est ce qui rend la course loyale — et ce qui permettra à l'adversaire de sauter une étape.

**La carte à observer : l'empreinte.** Le moule à l'oiseau, ouvert, montre un paysage sculpté en creux qui ne ressemble à rien : tout y est à l'envers. Pressé dans de la pâte à sel, il donne Valbraise en relief, avec cinq petits oiseaux.

- **Fabrication** : la carte doit être exacte (les énigmes en dépendent) ; elle ne sort **pas** du générateur. Dessin fait main ou vectoriel, dans le style du recueil ; fond possible : `a rectangular slab of pale salt dough seen from above, showing a miniature valley modelled in relief: a pond with a dam, a rocky outcrop with a tiny ruined castle, a tiny chapel, a long building with one tall chimney, forest all around, and five tiny bird shapes pressed into the dough, soft side light, no text, no letters`.
- **Deux états** : avant l'épisode 2, la carte s'affiche **en miroir** (le paysage de nulle part), avec un bouton « à l'envers » qui la retourne — l'enfant peut trouver la solution du premier soir avec son doigt. Ensuite, un oiseau s'allume par clef trouvée.
- **Ce qu'un enfant attentif peut y trouver avant les héros** : un petit carré dans l'eau, au bout de la digue (le moine) ; la fenêtre de la chapelle dessinée plus grande que nature ; un bassin carré au sommet du rocher ; un oiseau au pied de la cheminée ; et le cinquième oiseau au milieu de la forêt, là où il n'y a rien — exactement au croisement des deux lignes qui relient les quatre autres.

**Les objets** (description fixe, réutilisée mot pour mot).

| Objet | Rôle | Description fixe (anglais) |
|---|---|---|
| **Le moule à l'oiseau** | la carte ; « le moule de personne » : on n'y a jamais soufflé — jusqu'à la dernière nuit | `an old two-part mould of dark pear wood as big as a school satchel, with two iron hinges and an iron clasp, a small bird carved on its lid` |
| **Les clefs de verre** | quatre cachées, une donnée | `a solid glass rod as long as a hand, twisted like barley sugar, ending in a flat round seal stamped with a small bird` — en `blue`, `yellow`, `green` ou `violet glass` |
| **Le calot rouge** | porte-bonheur de Gaspard, gagné par Nuno ; la cinquième clef | `a big marble of deep ruby-red glass, as large as a walnut, glowing like an ember when light passes through it` |
| **Les plaques gravées** | portent les énigmes ; **jamais montrées de face** (texte) | `a small plate of thick clear glass held in a child's hand` |
| **Les gommettes** | la marque de l'adversaire ; la dernière sera décollée | `round bright orange stickers` |
| **Les boules de verre** | une à chaque fenêtre de la rue des Souffleurs ; une seule rouge | `a glass ball as big as an orange hanging on a string in a window` |
| **La fiole** | l'or de la centième pièce, préparé par Colombe | `a tiny sealed glass vial full of dark purple powder` |
| **Le carnet de Colombe** | le trésor | `a small thick notebook bound in worn brown leather, tied with a faded red ribbon` |

**Motifs qui reviennent** (posés tôt, payés tard).

- **Le calot rouge** : perdu aux billes à l'épisode 1, clef de tout à l'épisode 8.
- **Le moule de personne** : ouvert à l'épisode 1, soufflé enfin à l'épisode 8.
- **« Attendez. » / « Je l'ai dit. »** : le refrain de Lucie ; à la fin, on comprend pourquoi c'est elle qui raconte.
- **Deux contre deux** : l'égalité des votes ; à cinq, elle disparaît.
- **Les gommettes orange** : elles gagnent du terrain d'épisode en épisode ; la dernière se décolle.
- **La comptine**, entendue dès la première scène comme un bruit de fond.
- **La Bosse** : on y fait de la luge au premier épisode ; on y creuse au septième.
- **Le commentaire de Nuno** : il s'interrompt quand le cœur y est ; il ira jusqu'au bout une seule fois.
- **« Fêlés, pas cassés. »**
- **La phrase du four**, et son chiffre qui descend.

### 4.6 La chaîne des énigmes

**Les règles du jeu loyal.**

1. Tout ce qu'il faut pour trouver a été **entendu avant** — souvent un épisode plus tôt, dans une scène drôle dont on se souvient.
2. Chaque énigme est **dite deux fois** dans l'épisode (un enfant la lit, un autre la fait relire), puis redite dans le « précédemment » et affichée sur le carton de fin.
3. Les héros se trompent **une fois**, de façon amusante ; jamais trois.
4. Aucune énigme ne dépend d'une image générée ; la carte, dessinée à la main, **confirme** la réponse sans jamais être nécessaire.
5. Neuf énigmes (huit d'étape et une grande, qui court sur toute la saison), jamais deux fois la même nature : logique, mot à double sens, devinette, jeu de sons, charade, ordre, observation, objet, déduction.
6. Aucun hasard ne sauve personne ; aucun adulte ne donne la réponse.

#### Énigme 1 — La carte de nulle part (posée à l'épisode 1, résolue à l'épisode 2) · logique

- **Énoncé entendu** : « Un étang à droite d'un rocher, une chapelle au pied d'une cheminée, une forêt là où devrait couler la rivière. Cet endroit n'existe nulle part. Et pourtant, quelqu'un avait passé des semaines à le sculpter dans le bois. »
- **Indices donnés avant** : le matin même, Zé montre à Gaspard le moule d'une carafe dont l'anse est du mauvais côté — « Un moule, c'est le verre à l'envers. Le creux fait la bosse, la gauche fait la droite. » En regardant le paysage, Nuno, la tête en bas : « On dirait Valbraise vue par quelqu'un qui marche sur les mains. » Et les griffures du couvercle sont « des lettres qui se tiennent à l'envers, comme celles de la vitrine quand on les lit de l'intérieur de l'épicerie ».
- **Solution** : un moule ne montre pas la chose, il montre son envers. Il faut en prendre l'empreinte — dans de la pâte à sel : c'est Valbraise, avec cinq oiseaux. Les lettres du couvercle se lisent dans le miroir rond de l'épicerie.
- **Pourquoi on trouve** : la règle a été donnée telle quelle quelques minutes plus tôt, la vanne de Nuno dit presque la réponse, et l'auditeur a une nuit pour faire le lien.

#### Énigme 2 — Le moine (épisode 2 → 3) · mot à double sens, lieu

- **Énoncé entendu** (gravé à l'envers dans le couvercle) :
  > Commence par le moine qui n'a jamais prié.
  > Il a les pieds dans la vase et le front au soleil.
  > Il ne boit pas une goutte de tout ce qu'il retient.
  > Sous son chapeau de pierre, je t'ai laissé la bleue.
- **Indices donnés avant** : à l'épisode 1, Pépé ronchonne sur son banc — « Le moine fuit. L'étang Neuf a baissé d'une main, et plus personne pour lui remettre une planche. » Nuno : « Il y a un moine dans l'étang ? » Gaspard : « C'est la bonde, andouille. La boîte en pierre au bout de la digue. »
- **Solution** : le moine de l'étang Neuf. Sous la dalle qui le coiffe : la clef bleue et la première plaque.
- **Pourquoi on trouve** : le mot a été expliqué, avec une vanne accrochée dessus. Et Gaspard, le seul à le connaître, est absent quand on lit l'énigme : la bande court à la chapelle, où vécut jadis un ermite — l'auditeur, lui, a de l'avance sur les héros et le droit de s'impatienter.

#### Énigme 3 — Celle qui entre sans ouvrir (épisode 3 → 4) · devinette

- **Énoncé entendu** :
  > Va chez les verriers, là où ils se taisent.
  > Cherche celle qui entre sans pousser la porte,
  > qui traverse le verre sans le casser,
  > qui change de robe à chaque carreau
  > et se couche par terre sans se salir.
  > Quand le four appelle au soir, pose la main où sa robe est rouge.
- **Indices donnés avant** : à l'épisode 2, dans la chapelle des Verriers, « des confettis de couleur traînaient sur les dalles », et Nuno les a traversés à cloche-pied en évitant le rouge. Le Grand Sifflet « appelle » à dix-huit heures depuis le premier épisode.
- **Solution** : la lumière du soleil. À six heures du soir, le seul carreau rouge du vitrail pose sa tache sur une dalle ; dessous, la clef jaune.
- **Pourquoi on trouve** : c'est une devinette en entonnoir — chaque vers ferme une fausse piste (le vent ne change pas de robe, un fantôme ne se couche pas par terre). Et l'auditeur a déjà vu ce sol.
- **Dans l'histoire** : Lucie donne la réponse tout de suite ; il faut qu'elle la dise trois fois. C'est la première fois que la bande l'écoute.

#### Énigme 4 — Le dernier mot (épisode 4 → 5) · jeu de sons

- **Énoncé entendu** :
  > Monte chez celui qui n'a pas de bouche et qui a toujours le dernier mot.
  > Il ne sait rien, il n'invente rien, il ne ment jamais.
  > Demande-lui bien fort : « Que garde le château ? »
  > Ce qu'il te rendra, c'est là que dort la verte.
- **Indices donnés avant** : le rocher s'appelle la Roche Bavarde depuis l'épisode 1, où l'on apprend que « tous les enfants de Valbraise y sont montés au moins une fois lui crier un gros mot, pour le plaisir de l'entendre revenir ».
- **Solution** : l'écho. On crie « Que garde le château ? » et la Roche rend : « …château… teau… eau. » La clef verte est dans le bassin d'eau de pluie taillé au sommet.
- **Pourquoi on trouve** : deux marches, chacune à hauteur d'enfant — qui a toujours le dernier mot sans avoir de bouche ? puis : que reste-t-il de « château » quand on n'en garde que la fin ? Il suffit de le dire tout haut dans son lit.

#### Énigme 5 — La grande dame (épisode 5 → 6) · charade

- **Énoncé entendu** :
  > Mon premier va d'un village à l'autre.
  > Mon second est au milieu du visage.
  > Mon tout est la plus haute dame de Valbraise :
  > elle fume du matin au soir et ne tousse jamais.
  > À ses pieds, la brique à l'oiseau. Derrière elle, la violette.
- **Indices donnés avant** : Pépé appelle la cheminée « la grande dame » depuis son banc ; le Grand Livre, récité par Apolline, dit « la grande dame la quatrième ».
- **Solution** : chemin + nez = la cheminée. À son pied, une brique marquée d'un oiseau ouvre la Galerie.
- **Pourquoi on trouve** : la charade est le jeu de mots des cours de récréation, et les deux derniers vers confirment. L'auditeur trouve — et comprend du même coup pourquoi la voiture grise est déjà garée là.

#### Énigme 6 — L'ordre des cinq portes (épisode 6 → 8) · logique d'ordre

- **Énoncé entendu** (plaque de la Galerie, récitée par Apolline) :
  > Là où le premier feu s'est éteint, il y a cinq portes, et il faut cinq mains.
  > La bleue ouvre la marche ; la rouge la ferme.
  > La verte suit la bleue.
  > La jaune ne touche jamais la rouge.
  > Tournez toutes ensemble, ou ne tournez pas.
- **Indices donnés avant** : les cinq couleurs sont connues ; Pépé a raconté que le premier four était dans la forêt, « rond comme une ruche » ; Zé a expliqué qu'une place, c'est cinq verriers qui font le même geste au même moment.
- **Solution** : bleue, verte, jaune, violette, rouge — et cinq personnes en même temps.
- **Pourquoi on trouve** : trois indices, chacun donne une place sûre (la première, la dernière, la deuxième) ; il ne reste que deux couleurs pour deux portes, et la dernière phrase tranche. On y arrive de tête, en comptant sur ses doigts.

#### Énigme 7 — Le premier feu (épisodes 6 → 7) · observation et mémoire

- **Énoncé entendu** : « Là où le premier feu s'est éteint. » Sur la carte, le cinquième oiseau est posé au milieu des arbres, là où il n'y a rien.
- **Indices donnés avant** : à l'épisode 1, sur la Bosse — « Attendez. Il y a des briques, sous la mousse. — C'est ça, et moi je suis le pape », répond Nuno. À l'épisode 3, Pépé : « Avant la verrerie, il y avait la hutte, dans le bois. Les verriers suivaient les arbres. »
- **Solution** : la Bosse est le vieux four, enseveli sous cent cinquante ans de mousse. Ils y font de la luge depuis toujours.
- **Pourquoi on trouve** : c'est l'énigme des auditeurs qui écoutent Lucie. Elle l'a dit dès le premier jour.

#### Énigme 8 — La cinquième clef (épisode 7 → 8) · devinette d'objet

- **Énoncé entendu** (gravé sur la pierre du vieux four) :
  > La rouge, je ne l'ai pas cachée : je l'ai donnée.
  > Elle est ronde, elle n'ouvre aucune serrure.
  > On la gagne, on la perd, on ne l'achète pas.
  > Les grands l'ont oubliée ; les enfants savent toujours où elle est.
- **Indices donnés avant** : le calot rouge de l'épisode 1 — « un rouge d'avant, on n'en fait plus ; Pépé le tenait de son pépé » ; le Grand Livre : « la cinquième, les enfants l'ont » ; à l'épisode 6, Nuno « rôda un moment autour du sac de Gaspard, pour une raison qu'il ne donna pas ».
- **Solution** : une bille — le calot rouge. La cinquième porte du four a un creux rond à sa taille.
- **Pourquoi on trouve** : « on la gagne, on la perd » ne laisse guère de doute à qui a joué aux billes ; et l'objet est sous les yeux de l'auditeur depuis la toute première scène.

#### La grande énigme — Où est l'or ? (du premier au dernier épisode) · déduction

- **Les pièces, toutes entendues** : la comptine (« c'est le feu qui l'a tout changé », « regarde au travers ») ; « Je l'ai rendu jusqu'au dernier grain » ; la comtesse qui ne réclame rien ; le rouge que personne n'a su refaire ; et la leçon de Zé, à l'épisode 4 : « Le bleu, c'est du cobalt. Le violet, du manganèse. Le vert, du fer. Le jaune — tiens-toi bien — c'est de l'argent. Du vrai. — Et le rouge ? — Le rouge d'Aubin ? Si je le savais, je ne ferais pas mes cartons. »
- **Solution** : l'or n'a jamais été caché. Il est fondu dans le verre : c'est lui qui fait le rouge.
- **Pourquoi on trouve** : si le jaune se fait avec de l'argent… L'auditeur qui fait le pas tout seul, un soir, entre deux épisodes, s'en souviendra longtemps.

### 4.7 Le plan des huit épisodes

Dans les descriptions d'images, `{nom}` renvoie aux descriptions fixes ci-dessus. Aucune image ne compte plus de trois personnages ; chaque scène écrite, pas plus de quatre voix (la bande se sépare souvent : c'est aussi ce qui la fait vivre).

#### Épisode 1 — Le moule de personne · *24 nuits*

Au Wagon, finale de billes : Nuno, qui commente son propre triomphe, gagne à Gaspard son calot rouge porte-bonheur. Derrière le mur, des petites sautent à la corde en chantant *Colombe*. À midi, le Grand Sifflet sonne trop longtemps : on annonce aux ouvriers que le four sera éteint le premier septembre. Une voiture grise arrive ; madame Delcourt en descend avec sa fille et des planches de gommettes orange — elle en colle partout, y compris sur le banc de la Fontaine, à un doigt de Pépé. Zé montre à Gaspard un moule de carafe : le verre à l'envers. Le soir, les vieux moules en bois « sans valeur » partent à la benne pour être brûlés. Gaspard ne le supporte pas ; on vote ; deux contre deux ; on joue ça aux billes. Ils en sauvent sept. L'un est scellé à la cire, un oiseau gravé sur le couvercle. Pépé pâlit : « Celui-là, c'est le moule de personne. On n'y a jamais soufflé. » Dedans : un paysage qui n'existe pas.

- **L'énigme** : la carte de nulle part.
- **Le moment de bande** : le vote à égalité tranché aux billes, sous le commentaire sportif de Nuno ; Lucie signale des briques sous la mousse de la Bosse, et se fait rembarrer.
- **En suspens** : quel est ce pays à l'envers — et pourquoi, à la fenêtre du Magasin aux moules, la dame aux gommettes reste-t-elle plantée devant une étagère vide ?
- **Illustration** : `Dusk inside {wagon}, warm light from a storm lantern: {gaspard} kneels and holds {moule} wide open on a wooden crate, serious and proud; {lucie} leans over it, peering closely, puzzled; {nuno} lies on his back on a bench with his head hanging down, looking at the mould upside down and grinning; exactly three children`

#### Épisode 2 — Le pays à l'envers · *22 nuits*

Nuno fait le poirier pour amuser la galerie — et Lucie, qui l'avait dit, est enfin comprise : il faut une empreinte. Dans l'arrière-boutique de l'épicerie, on pétrit de la pâte à sel (Nuno la goûte ; il le regrette). Le moule s'y imprime : c'est Valbraise, avec cinq oiseaux. Les griffures du couvercle, lues dans le miroir rond de la boutique, donnent la première énigme : un moine qui n'a jamais prié. Gaspard est parti pour la journée accompagner Pépé chez le docteur de la ville. Sans lui, les trois autres filent à la chapelle des Verriers, où vécut autrefois un ermite. Quelqu'un y est déjà : madame Delcourt, qui mesure les murs, et sa fille Apolline, qui prend des notes. Duel très poli. Elle sait que le moule existe ; elle le réclame : il appartient à la Compagnie. Yasmine, qui respecte les règlements, vacille. On repart les mains vides, entre les confettis de couleur que le vitrail jette sur les dalles.

- **L'énigme** : le moine.
- **Le moment de bande** : la pâte à sel, et madame Belkacem qui facture la farine en corvées de cageots sans demander à quoi elle a servi.
- **En suspens** : quel moine n'a jamais prié ? Et que dit ce gros livre que madame Delcourt serre sous son bras ?
- **Illustration** : `Afternoon in the cluttered back room of a small grocery shop, sacks of flour and shelves of tins: {yasmine} carefully lifts {moule} off a thick slab of pale salt dough, concentrated; {nuno}, his face and hair white with flour, sticks out his tongue in disgust; {lucie} points at the dough, eyes wide with recognition; exactly three children`

#### Épisode 3 — Le moine qui ne priait pas · *20 nuits*

Gaspard rentre, écoute, hausse les épaules : « Le moine ? C'est la bonde de l'étang. Je l'ai dit l'autre jour. » Consternation générale. À l'étang Neuf, l'eau est basse ; le moine dépasse, coiffé de sa dalle. Gaspard sort de son sac un pied-de-biche — au cas où. Nuno, qui voulait passer le premier, s'enfonce dans la vase jusqu'aux genoux et y laisse une sandale. Sous le chapeau de pierre : une clef de verre bleue et une plaque gravée. Sur la digue, Apolline les a suivis ; elle propose un marché, se fait baptiser « Mademoiselle Dictionnaire », puis bat Nuno aux billes en trois coups. Au retour, Pépé raconte le premier four, celui de la forêt. Et Lucie, dans ses jumelles, voit ce qu'elle ne cherchait pas : des cartons empilés dans le couloir des Ferreira. Elle ne dit rien.

- **L'énigme** : celle qui entre sans ouvrir.
- **Le moment de bande** : l'inventaire du sac de Gaspard, objet par objet, pendant que Nuno attend qu'on le désembourbe.
- **En suspens** : qui entre sans pousser la porte ? Et pourquoi ces cartons, chez Nuno ?
- **Illustration** : `Late morning on the grassy dam of {etang}: {gaspard} levers up the flat stone slab of the sluice tower with a short iron bar, cheeks red with effort; {nuno}, stuck up to his knees in dark mud, holds a twisted blue glass rod above his head, laughing in triumph; on the dam {yasmine} writes in her notebook with one eyebrow raised; exactly three children`

#### Épisode 4 — Celle qui entre sans ouvrir · *16 nuits*

« La lumière », dit Lucie. Personne n'entend. Elle le redit. Puis une troisième fois, plus fort qu'elle n'a jamais parlé — et la bande se tait. En attendant six heures, on regarde Zé souffler ; il fait des billes avec les restes et explique d'où viennent les couleurs. Lucie pose la question des cartons. Nuno avoue : le Portugal, le premier septembre. « Tu comptais nous le dire quand ? Par carte postale ? » Dispute, puis serment : trouver l'or avant que le four meure. À la chapelle, le ciel est couvert ; à six heures moins deux, le soleil passe sous les nuages ; la tache rouge se pose sur une dalle. Dessous : la clef jaune, et une plaque. Madame Delcourt arrive dix minutes trop tard. Elle ne se fâche pas ; elle leur dit pourquoi elle fait ce métier. Yasmine lui annonce la loi des gommettes ; madame Delcourt : « C'est noté. » Le soir, on frappe au Wagon. Apolline : « Vous avez les plaques. J'ai lu le Grand Livre. On court chacun avec une seule jambe. »

- **L'énigme** : le dernier mot.
- **Le moment de bande** : l'aveu de Nuno, et son commentaire qui s'arrête au milieu d'une phrase.
- **En suspens** : qui n'a pas de bouche et a toujours le dernier mot ? Et faut-il ouvrir la porte à la fille de l'adversaire ?
- **Illustration** : `Early evening inside {chapelle}, low golden sun through the stained-glass window: {lucie} kneels on the flagstones with her hand flat on a single patch of red light, calm and sure; {yasmine} stands beside her, astonished, holding her notebook against her chest; {nuno} keeps watch at the half-open door, looking back over his shoulder; exactly three children`

#### Épisode 5 — Le dernier mot de la Roche · *12 nuits*

Vote sur Apolline : deux contre deux. Aux billes, donc — contre Nuno, qu'elle bat une seconde fois. Elle entre « à l'essai ». L'énigme, tout Valbraise la connaît sans le savoir : c'est la Roche Bavarde. On monte. Gaspard s'arrête à mi-escalier, cramponné à la rampe ; Lucie lui fait compter les marches à voix haute, et il arrive en haut les yeux fermés. On crie. La Roche rend la fin des mots : Nuno en profite (« Nuno est le plus beau ! » — « …beau… beau… »). « Que garde le château ? » — « …eau. » Dans le bassin d'eau de pluie, sous un bouchon de pierre : la clef verte, et une charade. Apolline récite le Grand Livre : le moine, la lumière, l'écho, **la grande dame**, les enfants — et ceci : Aubin ne savait pas écrire. Qui donc a gravé les plaques ? Gaspard fronce le nez : la grande dame, c'est le nom que Pépé donne à la cheminée. Lucie lève ses jumelles. Au pied de la cheminée, une voiture grise.

- **L'énigme** : la charade.
- **Le moment de bande** : le concours de cris face à l'écho ; Gaspard qui hurle « J'ai le vertige ! » et à qui la Roche répond tranquillement « …tige ».
- **En suspens** : mon premier va d'un village à l'autre… et comment madame Delcourt peut-elle être déjà là-bas ?
- **Illustration** : `Bright windy afternoon on top of {roche}, treetops far below: {nuno} stands with his hands cupped around his mouth, shouting joyfully toward the valley; {apolline} covers her ears, half annoyed, half laughing; {gaspard} sits clinging to the iron handrail with both arms, his eyes squeezed shut; exactly three children`

#### Épisode 6 — Lot 213 · *8 nuits*

Chemin, nez : cheminée. Trop tard pour aujourd'hui — le sifflet du soir a sonné. Reste la nuit au Wagon, permise une fois par été. À la lampe, ils trouvent la brique à l'oiseau et se glissent dans la Galerie, sous la vieille halle. Au bout, une niche. Vide. Sur la brique, une gommette orange : *lot 213*. Tout casse d'un coup : Nuno accuse Apolline d'avoir tout raconté à sa mère ; Yasmine lance à Nuno que lui, de toute façon, il s'en va. Chacun rentre de son côté. Gaspard, resté seul avec Lucie : « Fêlés, pas cassés. Enfin j'espère. Je dis ça, je dis rien. » À l'aube, Apolline revient avec une photographie encore tiède : la quatrième plaque, posée sur le bureau de sa mère. Elle n'a rien pris — elle a photographié. Et madame Delcourt n'avait besoin d'aucune espionne : elle a les plans des souterrains depuis le premier jour. On lit la plaque. Nuno ne s'excuse pas ; il rôde un moment autour du sac de Gaspard.

- **L'énigme** : l'ordre des cinq portes — et « là où le premier feu s'est éteint ».
- **Le moment de bande** : la dispute. C'est la seule fois de la saison où personne ne plaisante pendant une page entière.
- **En suspens** : où le premier feu s'est-il éteint ? Il faut cinq mains — ils sont quatre, ou cinq, ou plus rien du tout ?
- **Illustration** : `Night inside {galerie}: {yasmine} shines a hand torch into a small empty arched niche where one round bright orange sticker is stuck on the brick, her face stunned; behind her {gaspard} crouches under the low vault, dismayed; {lucie} touches the sticker with one fingertip, thoughtful; exactly three children`

#### Épisode 7 — Le premier feu · *3 nuits*

Lucie ne dit pas « Attendez ». Elle dit : « Écoutez-moi. » Les briques sous la mousse ; le cinquième oiseau au milieu des arbres : le premier four, c'est la Bosse. Mais avant d'y courir, elle veut une réponse — qui a gravé les plaques ? Dans la rue des Souffleurs, toutes les boules de verre sont vertes ou bleues, sauf une. Mademoiselle Garance les reçoit au milieu de ses géraniums : « Colombe ? Ce n'était pas un oiseau, mes agneaux. C'était une petite fille. Mais on ne me demande rien, à moi. » Elle raconte. À la Bosse, on arrache la mousse à pleines mains : un four rond, cinq petites portes, et quatre vers gravés sur la pierre du seuil. Madame Delcourt sort du sous-bois, sans se presser, une boîte étiquetée à la main : la clef violette. Trois clefs d'un côté, une de l'autre ; la rouge, personne. Elle propose le musée, la vitrine, l'abri. Gaspard : « Sous une vitrine, on ne souffle pas. » Elle : « Dans trois nuits, ici non plus. »

- **L'énigme** : la cinquième clef.
- **Le moment de bande** : Nuno découvre qu'ils sont « assortis » aux clefs ; Apolline tente « c'est trop de la balle » et se fait corriger par quatre voix à la fois.
- **En suspens** : qui cédera ? Et où est la rouge, celle qu'on n'a pas cachée, mais donnée ?
- **Illustration** : `Late afternoon in front of the last house of {rue}, red geraniums on the windowsill and one red glass ball glowing in the window: {garance} sits on a small wooden chair holding her red glass pendant up to the light, smiling mischievously; {lucie} sits on the doorstep looking up at her, lips parted; {gaspard} stands gripping the straps of his backpack, mouth open; exactly three people: one old woman and two children`

#### Épisode 8 — Une place à cinq · *la dernière nuit*

Deux jours passent. La voiture des Ferreira est chargée. Dernier après-midi, à la Bosse : une bille ! Le calot ! « Nuno, sors-le. — Je l'ai plus. » Tollé. Lucie : « Attendez. Le sac. » Il est au fond du sac de Gaspard, sans un mot d'explication, depuis la nuit de la dispute. Cinq portes, cinq mains : ils sont quatre. Madame Delcourt regarde sa boîte, décolle la gommette, et pose la clef violette dans la main de sa fille : « Lot 213 : rayé. » Gaspard, Lucie, Yasmine, Apolline, Nuno — bleue, verte, jaune, violette, rouge. On tourne ensemble. La pierre du fond pivote. Pas d'or : un carnet, une fiole de poudre pourpre, et une première page qui commence ainsi : « Vous êtes cinq, sinon vous ne lisez pas ceci. » L'or était dans le rouge ; la fiole est celui de la centième pièce ; le centième verre reste à faire. Il faut une nuit entière : c'est justement ce qui reste. Dans la Grande Halle, Zé prend la canne, Pépé commande de sa chaise, les enfants font les gamins — et l'on souffle enfin dans le moule de personne. À l'aube, on laisse mourir le Grand Four. Le sifflet ne sonne pas.

- **L'énigme** : la cinquième clef, puis la grande : où était l'or.
- **Le moment de bande** : le premier vote à cinq — pour savoir qui tournera la rouge. Cinq voix pour Nuno. Yasmine, stupéfaite : « Adopté. Du premier coup. »
- **En suspens** : voir § 4.8.
- **Illustration** : `Deep night inside {halle}, the furnace openings glowing orange: {gaspard}, cheeks puffed out, blows for the first time into a long steel blowpipe with a small glowing ruby-red glass bubble at its end; {ze} stands right behind him steadying the pipe with both hands, proud and moved; {pepe} sits on a wooden stool leaning on his stick, his eyes shining; exactly three people: one boy, one man and one old man`

### 4.8 La fin

**Ce qu'ils trouvent vraiment.** Pas un coffre. Un carnet, une pincée d'or, et une phrase : le rouge ne se fait pas seul. Le trésor, c'était une couleur — et il fallait être cinq pour l'atteindre comme il faut être cinq pour la faire. Cette nuit-là, du moule de personne sort ce pour quoi il avait été sculpté : Valbraise en verre rouge, grande comme un cartable, qu'on regarde à travers. Avec ce qui reste au fond du creuset, Zé fait quatre calots.

**Ce que devient le feu.** Le Grand Four s'éteint à l'aube, comme prévu : la verrerie ferme, et l'histoire ne triche pas là-dessus. Mais avant, les cinq ont porté une pelle de braises jusqu'au petit four de la vieille halle. Madame Delcourt téléphone longuement à la Compagnie depuis la cabine de la Fontaine ; on ne saura jamais ce qu'elle a dit. La vieille halle et son four restent au village ; six verriers aussi. Sur le carnet, elle ne colle rien : « Lot non inventorié. Cela arrive. »

**Ce que chacun y gagne.**
- *Gaspard* : son premier souffle dans une canne, et un endroit où apprendre le métier. Son père est venu regarder, du fond de la halle, sans rien dire.
- *Yasmine* : elle a perdu tous ses votes et gagné une bande. Elle prend le car du collège avec un calot rouge dans la poche et, pour la première fois, sans liste.
- *Lucie* : une voix. On l'écoute, désormais, dès la première fois.
- *Nuno* : il n'a rien su dire. Il a rendu le calot — c'était sa phrase.
- *Apolline* : elle repart, comme toujours ; pour la première fois, quelqu'un lui écrira.
- *Madame Delcourt* : une chose qu'elle n'a pas rangée.
- *Pépé* : il a vu son petit-fils souffler. *Mademoiselle Garance* : on lui a enfin posé la question, et le nom de Colombe est peint sur la porte de la vieille halle.

**La dernière page.** Le matin du premier septembre, la voiture des Ferreira fait le tour de la Fontaine. Nuno, à la vitre arrière, commente son propre départ — « Et c'est Ferreira qui quitte le terrain… le public est debout… » — et cette fois il va jusqu'au bout de la phrase. Au tournant, il lève le vieux calot dans le soleil : un éclat rouge, puis plus rien. Personne ne dit « Fêlés, pas cassés ». Tout le monde le pense.

Alors la narratrice, qui n'avait jamais dit « je », le dit : elle sait tout cela parce qu'elle y était. La salopette verte, c'était la sienne. *« À l'époque, je parlais peu. Je me rattrape. »* Puis, une dernière fois, la phrase du four — retournée : cette nuit-là, pour la première fois depuis cent soixante ans, le Grand Four ne brûlait plus ; dans la vieille halle, il y avait une lueur ; on cessa de compter les nuits.

**Ce qui reste ouvert pour une saison 2.**
- La dernière page du carnet n'est pas une recette. C'est un dessin : un oiseau, et un endroit que personne à Valbraise ne reconnaît. Dessous : « Le bleu, je l'ai appris ailleurs. »
- En octobre, une carte postale du Portugal : sur le mur de la vieille verrerie de sa nouvelle ville, Nuno a trouvé, gravé dans la pierre, un petit oiseau. L'été suivant, les Fêlés prennent le train. **Saison 2 : « Le Bleu de Colombe »**, chez Nuno ; puis, chaque été, chez l'un d'eux.
- Deux questions que personne n'a posées : où sont passés les quatre-vingt-dix-neuf verres ? Et qui était la comtesse, qui savait, elle, qu'on lui avait rendu son or ?

---

## 5. Le style graphique

Ligne de style (remplace celle du recueil pour cette collection) :

> `Illustrated children's adventure novel plate, flat gouache illustration on lightly textured paper, clean thin dark outlines, soft muted colours with warm brick reds, forest greens and one glowing ember-orange light, realistic human children about ten years old with natural proportions and simple expressive faces, summer clothes, detailed cosy setting, wide cinematic composition, soft vignette edges. No text, no letters, no numbers, no logos, no signature, no watermark, no speech bubbles. `

Suffixe :

> ` Each character drawn only once, exactly as described, no other people in the background.`

- **Ce qui reste cousin des Étoiles** : les aplats, les contours fins et sombres, la douceur des couleurs.
- **Ce qui grandit avec l'auditeur** : des enfants humains aux proportions vraies (ni poupons ni héros de dessin animé), des décors fouillés où l'on a envie de chercher, un cadrage large de roman d'aventures illustré, un grain de papier.
- **Deux signatures** : une **lueur de braise** dans chaque image (four, lanterne, vitrail, soleil bas, verre rouge) ; et **les cinq couleurs** — chaque enfant se reconnaît à la sienne avant même qu'on voie son visage.
- **Format** : paysage, même rapport que les images existantes.
- **Avant d'écrire une ligne** : générer les cinq fiches d'enfants et trois images d'essai à trois personnages. C'est la première fois que la maison dessine des humains ; si deux enfants se confondent, on corrige la bible, pas les images.

---

## 6. Les règles d'écriture (8-10 ans)

### Le temps du récit : passé simple et imparfait, à la troisième personne

Tranché, pour une lecture à voix haute par une seule voix.

1. **Il sépare le récit des répliques.** Tout ce qui est au passé simple, c'est la narratrice ; tout ce qui est au présent ou au passé composé, c'est un enfant qui parle. Avec une voix unique, sans changement de timbre, c'est la grammaire qui dit à l'oreille qui tient la parole.
2. **Il fait courir.** « Ils enfourchèrent les vélos, coupèrent par le pré, dérapèrent devant la chapelle » : trois gestes, trois coups nets. Le présent met tout sur le même plan ; dix minutes de présent, c'est long.
3. **Il fait rire par contraste.** Une narratrice qui parle bien, des gamins qui parlent comme des gamins : la vanne claque mieux dans un récit tenu.
4. **Il dit que tout s'est bien fini.** Ce qui est raconté au passé a eu lieu ; quelqu'un en est revenu pour le dire. À l'heure du coucher, c'est rassurant — et c'est ce qui prépare la dernière page.

Garde-fous : troisième personne uniquement (le « je » n'apparaît que dans les soixante derniers mots de la saison, au présent) ; pas de subjonctif imparfait ; on évite les formes qui font sourire malgré elles. Le « précédemment » est au passé composé.

### La langue

- **Soutenue dans le récit, vivante dans les répliques.** Le mot juste plutôt que le mot rare ; deux à quatre mots nouveaux par épisode (*digue, vase, ouvreau, se raviser, vaciller…*), toujours éclairés par la phrase, jamais expliqués après coup.
- **Douze mots de verrier**, pas plus (§ 4.1).
- **Des phrases de longueurs inégales** : douze à quatorze mots en moyenne, des phrases de trois mots, de rares périodes ; jamais deux longues de suite.
- **Écrire pour l'oreille.** Pas de parenthèses, pas d'italique porteur de sens. Nombres en toutes lettres ; « madame », « mademoiselle » en toutes lettres. Chasser les homophones piégeux : jamais « le verre vert » ni « vers le verre » (les clefs sont au féminin pour cela : *la bleue, la verte*) ; la place du village s'appelle toujours *la Fontaine*, pour que *une place* ne désigne que l'équipe de verriers.
- **L'argot d'enfant, à petites doses, et sans date** : « andouille », « la honte », « c'est louche ». Rien qui sente la mode d'une année ; aucun gros mot — on sait seulement que la Roche en a entendu.
- **Le sensible avant l'abstrait.** On ne dit pas que Nuno est triste : son commentaire s'arrête au milieu.

### Les dialogues et les vannes

- **On sait qui parle avant la fin de la première proposition** : le prénom avant la réplique, un geste juste avant, ou la signature verbale — les listes de Yasmine, le commentaire de Nuno, l'« Attendez » de Lucie, le pépé de Gaspard, les « en l'occurrence » d'Apolline. Si l'on peut retirer l'incise sans perdre l'auditeur, la réplique est bonne.
- **Trois voix par scène, quatre au plus**, jamais plus de trois répliques sans réattribuer. La bande se sépare, quelqu'un est puni, Lucie se tait : on écrit pour le trio.
- **Verbes de parole variés et rares** : pas plus d'un « dit » par page ; on préfère le geste à l'incise.
- **La vanne obéit à trois lois.** Elle vient du caractère, jamais d'un bon mot plaqué. Elle vise ce que l'autre *fait*, jamais ce qu'il *est* — ni son corps, ni sa famille, ni d'où il vient. Et celui qui la reçoit en renvoie une dans les trois répliques. Ce sont des copains : on se charrie parce qu'on s'aime.
- **Au moins quatre sourires par épisode**, dont un dans la dernière minute — sauf à l'épisode 6, où le silence fait partie de l'histoire.
- Un tiers du texte en dialogue, deux tiers en récit : c'est un roman qu'on écoute, pas une pièce.

### Les énigmes

- Lues deux fois, sur le rythme d'un texte gravé ; la seconde fois plus lentement, parce qu'un enfant demande de relire.
- Après la lecture, une respiration : une scène, une vanne, une fausse piste. Jamais la solution dans le souffle qui suit.
- La solution passe par un détail *déjà entendu*, qu'on rappelle d'un mot, sans le réexpliquer.
- Celui ou celle qui trouve n'est pas toujours le même : chaque enfant a son énigme, et c'est Lucie qui en trouve le plus — sans qu'on la remarque.

### Le suspense sans la peur

- On remplace la peur par **la hâte, le secret, la gêne, la brouille**. Les dangers sont : arriver second, être surpris, se fâcher, voir partir un copain. Jamais le corps.
- **L'adversaire est poli.** Madame Delcourt ne menace pas, ne poursuit pas, n'élève pas la voix ; elle est redoutable parce qu'elle est organisée et qu'elle a souvent raison.
- **Les lieux inquiétants sont désamorcés par le rire** : dans la Galerie on tient debout, il fait sec, et Nuno commente la progression comme une finale.
- **La nuit est aimable** : c'est l'heure où le four rougeoie.
- **Chaque fin d'épisode est une énigme, pas une menace.**

### Ce qui est interdit

- Violence, arme, blessure, mort, maladie grave, créature ou lieu effrayant ; un adulte qui menace un enfant.
- Personnes réelles, marques, personnages ou scènes d'œuvres existantes.
- Voler, mentir pour nuire, se moquer d'un physique ou d'une origine ; toucher au verre chaud sans adulte.
- « La morale de l'histoire » sous toutes ses formes : « elle comprit que… », « depuis ce jour… ». Ni *transmission*, ni *partage*, ni *amitié* ne sont écrits comme des leçons.
- Un méchant. Des adultes idiots. Des enfants qui ont raison sur tout.
- L'adulte qui sauve la mise ; le hasard qui donne la solution ; l'indice qu'on n'avait pas entendu.
- Le schéma « trois essais ratés puis la réussite ».
- « Soudain » plus d'une fois par épisode ; « il dit, il dit, il dit » ; l'adresse à l'auditeur (« et toi, as-tu trouvé ? »).
- Plus de quatre voix dans une scène ; plus de trois personnages dans une image.

### Échantillon de ton (80 mots, non définitif)

> — Égalité, annonça Yasmine. Deux voix pour, deux voix contre.
> Elle referma son carnet d'un coup sec. Dans la bande, on savait ce que cela voulait dire.
> — Et c'est Ferreira qui s'avance sur le terrain ! claironna Nuno en sortant ses billes. Le public retient son souffle…
> — Le public aimerait surtout que tu te taises, grogna Gaspard.
> Lucie, elle, regardait la benne. Sous les planches dépassait un coin de bois sombre, où quelqu'un avait gravé un oiseau. Elle faillit le dire.

---

## 7. Trois questions ouvertes

1. **La forêt et le verre, ou la mer ?** La proposition recommandée est la plus originale, mais elle n'a ni bateau ni embruns. Si « Goonies », pour vous, c'est d'abord la mer, je développe B (l'île, la grande marée, les deux moitiés de carte) avec la même méthode — et je garde pour elle l'idée de la bande à qui il manque quelqu'un.

2. **Les années 1990, et la narratrice qui se dévoile ?** L'histoire se passe quand on n'avait pas de téléphone, et l'on découvre à la dernière page que la voix qui raconte est celle de Lucie devenue grande. On peut tout ramener à aujourd'hui (des CM2 sans portable, une forêt sans réseau) : l'auditeur s'y reconnaît peut-être plus vite, mais on perd ce dévoilement, qui est ce que la fin a de plus tendre.

3. **Jusqu'où la fin a-t-elle le droit de serrer le cœur ?** Dans cette version, le feu est sauvé mais l'usine ferme, et Nuno part quand même. C'est la fin la plus juste, et celle qui ouvre la saison 2. L'autre fin — les Ferreira restent, la verrerie repart — est plus joyeuse et moins vraie. À vous de dire.
