#!/usr/bin/env python3
"""Écrit les trois pages légales (mentions-legales.html, confidentialite.html, cgu.html) avec la mise en page des pages d'histoire.
Tant que le site est gratuit, l'éditeur (un particulier) ne publie pas son identité, comme la loi le permet. À L'OUVERTURE DES ACHATS il faudra :
nom ou dénomination, adresse, SIRET, nom du prestataire d'e-mail, du prestataire de paiement et du médiateur.
PROJET à faire relire par un juriste avant l'ouverture des achats.

    python3 tools/textes_legaux.py
"""
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pages

ROOT = pages.ROOT; AC = "<strong>[À COMPLÉTER]</strong>"; MAJ = "12 novembre 2026"; MEL = '<a href="mailto:contact@titistoire.fr">contact@titistoire.fr</a>'


def doc(nom, titre, desc, corps):
    h = pages.page(nom, titre + " | Titistoire", desc, f'<p class="fil"><a href="./">Titistoire</a></p><h1>{titre}</h1><p><em>Dernière mise à jour : {MAJ}.</em></p><div class="texte">{corps}</div>')
    (ROOT / nom).write_text(h.replace('href="../', 'href="./'), encoding="utf-8")


doc("mentions-legales.html", "Mentions légales", "Mentions légales du site Titistoire.", f"""
<h2>Éditeur du site</h2>
<p>Titistoire est un projet personnel. Le site est conçu, écrit et tenu par un particulier, seul, sur son temps libre, avec l'aide d'outils d'intelligence artificielle. Il n'y a ni société, ni équipe, ni service client.</p>
<p>Le site est édité à titre non professionnel. Comme le permet l'article 6, III, 2 de la loi n° 2004-575 du 21 juin 2004 pour la confiance dans l'économie numérique, l'éditeur a choisi de ne pas publier son identité ; elle est connue de l'hébergeur ci-dessous, qui la communiquerait à l'autorité judiciaire si elle le demandait.</p>
<h2>Hébergement</h2>
<p>Le site et ses services sont hébergés par Cloudflare, Inc., 101 Townsend Street, San Francisco, CA 94107, États-Unis — <a href="https://www.cloudflare.com">www.cloudflare.com</a>.<br>Le nom de domaine est enregistré auprès d'OVH SAS, 2 rue Kellermann, 59100 Roubaix, France.</p>
<h2>Comment le site est fait</h2>
<p>Les histoires du catalogue sont écrites avec l'aide d'une intelligence artificielle, puis relues et corrigées par l'éditeur. Les illustrations et les voix sont produites par des outils d'intelligence artificielle, puis choisies et vérifiées une à une. Les histoires créées à la demande, elles, sont entièrement produites par des programmes et contrôlées automatiquement : personne ne les relit avant vous.</p>
<h2>Propriété intellectuelle</h2>
<p>Les textes des histoires, les personnages, les illustrations, les enregistrements et le site lui-même sont mis à disposition pour une écoute et une lecture privées, en famille ou en classe. Toute reproduction ou rediffusion publique, totale ou partielle, demande une autorisation écrite.</p>
<h2>Vos données</h2>
<p>Tout ce qui concerne vos données se fait vous-même, tout de suite, depuis l'écran « Mon compte » : en obtenir une copie, ou tout supprimer. Voir la <a href="confidentialite.html">politique de confidentialité</a>.</p>
<h2>Contact</h2>
<p>Le site est gratuit et n'a pas de service client ni d'adresse de contact. Pour vos données personnelles, utilisez les boutons de votre compte : c'est immédiat. Un contenu illicite peut être signalé à l'hébergeur, Cloudflare, par son formulaire : <a href="https://abuse.cloudflare.com">abuse.cloudflare.com</a>.</p>""")

doc("confidentialite.html", "Politique de confidentialité", "Quelles données Titistoire traite, pourquoi, et quels sont vos droits.", f"""
<p>Titistoire est fait pour des enfants. Nous avons donc choisi de collecter le moins de données possible : <strong>aucune publicité, aucun traceur publicitaire, aucun outil tiers de mesure d'audience, aucune donnée sur l'enfant.</strong></p>
<h2>Responsable du traitement</h2>
<p>L'éditeur du site, un particulier (voir les <a href="mentions-legales.html">mentions légales</a>).</p>
<h2>Sans compte : ce qui reste sur votre appareil</h2>
<p>Pour écouter les histoires, aucun compte n'est nécessaire. Vos réglages (âge choisi, voix, thème clair ou sombre, histoires déjà écoutées) sont enregistrés uniquement dans votre navigateur, sur votre appareil. Ils ne nous sont pas transmis. Vous les effacez en vidant les données du site dans votre navigateur.</p>
<h2>Avec un compte (réservé aux adultes)</h2>
<p>Le compte est créé par un parent ou un adulte responsable, jamais par l'enfant. Nous traitons alors :</p>
<ul><li>votre adresse e-mail, pour vous connecter (envoi d'un code) et vous écrire au sujet du service ;</li>
<li>vos réglages et la liste des histoires écoutées, pour les retrouver sur vos appareils ;</li>
<li>les histoires que vous choisissez de garder (leur texte et leurs images), pour vous les conserver ; ce que vous avez saisi pour les créer n'est pas conservé ;</li>
<li>en cas d'achat : l'historique de vos crédits. Le paiement est traité par notre prestataire de paiement ; nous ne voyons ni ne conservons votre numéro de carte.</li></ul>
<p>Base légale : l'exécution du service que vous demandez (article 6.1.b du RGPD) et, pour la sécurité du service, notre intérêt légitime (article 6.1.f).</p>
<h2>Création d'histoires : ce qui est transmis</h2>
<p>Ce que vous saisissez pour créer une histoire (héros, lieu, sujet) est envoyé à des services d'intelligence artificielle pour écrire le texte, dessiner les images et produire la voix, puis contrôlé automatiquement. <strong>N'y indiquez ni nom de famille, ni adresse, ni aucune information personnelle sur un enfant.</strong> Un prénom suffit.</p>
<h2>Destinataires et sous-traitants</h2>
<ul><li>Cloudflare, Inc. : hébergement, base de données des comptes, envoi des e-mails de connexion, génération d'images et contrôle de contenu ;</li>
<li>Google (modèles Gemini) : écriture des histoires et voix ; en secours, OpenRouter (écriture) et ElevenLabs (voix). Ils ne reçoivent que le texte de la demande ou de l'histoire, jamais votre adresse e-mail ;</li>
<li>Ko-fi et son prestataire de paiement, uniquement si vous ouvrez le cadre de don : ils peuvent alors déposer leurs propres cookies ;</li>
<li>un prestataire de paiement, lorsque les achats seront ouverts. Son nom sera indiqué ici à ce moment-là.</li></ul>
<p>Certains de ces prestataires sont établis aux États-Unis. Les transferts sont encadrés par les clauses contractuelles types de la Commission européenne ou par le cadre de protection des données UE–États-Unis.</p>
<h2>Durées de conservation</h2>
<ul><li>Compte, réglages et histoires gardées : tant que le compte existe. Si vous le supprimez, tout est effacé immédiatement et vos autres appareils sont déconnectés. Seule reste une empreinte chiffrée de votre adresse, illisible, avec le nombre de créations qu'il vous restait, pour ne pas en offrir de nouvelles à chaque recréation de compte.</li>
<li>Compte inactif : effacé automatiquement après 24 mois sans visite ; les images de ses histoires sont effacées par un nettoyage hebdomadaire.</li>
<li>Code de connexion : 15 minutes. Session ouverte sur un appareil : 180 jours au plus.</li>
<li>Nous ne tenons aucun journal de vos visites ni de ce que vous écoutez. Le compte retient seulement la date de votre dernière visite (pour la règle des 24 mois). Pour freiner les abus, une empreinte de votre adresse IP est conservée une heure, un jour au plus.</li>
<li>En cas d'achat : les pièces comptables sont conservées par le prestataire de paiement pendant la durée légale.</li></ul>
<h2>Vos droits : tout se fait depuis votre compte, sans nous écrire</h2>
<p>Vous disposez des droits d'accès, de rectification, d'effacement, de portabilité, de limitation et d'opposition prévus par le RGPD. Pour qu'ils soient effectifs tout de suite, sans attendre une réponse de notre part, ils s'exercent par des boutons, dans l'écran « Mon compte » :</p>
<ul><li><strong>« Télécharger mes données »</strong> : vous recevez immédiatement un fichier contenant tout ce que nous détenons sur vous (adresse e-mail, dates, réglages, crédits, texte des histoires gardées et adresses de leurs images). C'est votre droit d'accès et de portabilité.</li>
<li><strong>« Supprimer mon compte et mes histoires »</strong> : tout est effacé immédiatement et définitivement (compte, réglages, histoires, images). C'est votre droit à l'effacement et d'opposition.</li>
<li><strong>Rectification</strong> : vos réglages se modifient dans l'appli. Pour changer d'adresse e-mail, supprimez le compte et recréez-en un.</li>
<li><strong>« Se déconnecter »</strong> : ferme la session sur l'appareil.</li></ul>
<p>Sans compte, nous ne détenons aucune donnée vous concernant : il n'y a rien à demander ni à effacer.</p>
<p>Si vous estimez que vos droits ne sont pas respectés, vous pouvez saisir la CNIL (<a href="https://www.cnil.fr">www.cnil.fr</a>).</p>
<h2>Cookies</h2>
<p>Le site n'utilise aucun cookie publicitaire ni de mesure d'audience. Seul un identifiant de session strictement nécessaire est utilisé lorsque vous êtes connecté à votre compte ; il ne demande pas de consentement.</p>""")

doc("cgu.html", "Conditions d'utilisation", "Conditions générales d'utilisation et de vente de Titistoire.", f"""
<h2>1. Le service</h2>
<p><strong>Titistoire est un projet personnel</strong>, conçu et tenu par un particulier, seul, avec l'aide d'outils d'intelligence artificielle. Il est proposé tel quel, de bonne foi, sans service client. En l'utilisant, vous acceptez les présentes conditions.</p>
<p>Titistoire propose des histoires illustrées et lues à voix haute pour les enfants de 1 à 10 ans. Le catalogue est accessible gratuitement, sans inscription. La création d'histoires sur mesure est réservée aux titulaires d'un compte.</p>
<h2>2. Qui peut l'utiliser</h2>
<p>Le compte est ouvert par une personne majeure. Les enfants utilisent Titistoire sous la responsabilité et la surveillance d'un adulte. Le service ne remplace ni la présence d'un adulte ni un avis médical, éducatif ou psychologique.</p>
<h2>3. Histoires créées à la demande</h2>
<p>Les histoires créées sont écrites, illustrées et lues par des programmes d'intelligence artificielle, sans relecture humaine. Chaque texte et chaque image passent par plusieurs contrôles automatiques avant d'être affichés ; en cas de doute, rien n'est montré. Aucun contrôle automatique n'étant infaillible, <strong>lisez ou écoutez une histoire créée avant de la proposer à un enfant</strong> : cette vérification relève de l'adulte titulaire du compte.</p>
<p><strong>Ce que vous obtenez, et ce qui n'est pas promis.</strong> Une création vous donne une histoire nouvelle, en plusieurs tableaux, avec ses illustrations et sa lecture à voix haute. C'est un résultat produit par un programme : il varie d'une fois à l'autre et peut comporter des imperfections (un personnage dont l'aspect change d'une image à l'autre, un détail incohérent, une intrigue simple, une voix inégale, une demande suivie de loin). La qualité littéraire, l'intérêt de l'histoire et sa conformité exacte à votre demande ne sont pas garantis. <strong>Qu'une histoire ne plaise pas ne donne droit ni à un remboursement ni à une nouvelle création.</strong></p>
<p><strong>Ce qui est garanti.</strong> Une création n'est décomptée que lorsque l'histoire a été écrite, contrôlée et vous a été remise. Si la création échoue pour une raison technique, ou si la demande est refusée par le contrôle, rien n'est décompté : c'est automatique, vous n'avez rien à demander.</p>
<p>Vous vous engagez à ne pas chercher à obtenir des contenus violents, haineux, sexuels, illicites ou portant sur des personnes réelles, ni à contourner les contrôles. Une demande peut être refusée sans justification ; un compte qui abuse du service peut être fermé.</p>
<p>Les histoires que vous créez sont pour votre usage privé et familial. Vous pouvez en garder jusqu'à 20 sur votre compte.</p>
<h2>4. Crédits et paiement</h2>
<p><em>Cette section s'appliquera à l'ouverture des achats ; d'ici là, les créations sont offertes, en nombre limité.</em> La création d'histoires consomme des crédits : un crédit, une création remise. Les crédits s'achètent par lots, au prix affiché toutes taxes comprises au moment de l'achat ; ils ne sont ni échangeables contre de l'argent ni cessibles. La vente est réalisée et encaissée par un prestataire de paiement, qui émet la facture et auprès duquel se font les demandes de remboursement.</p>
<p><strong>Droit de rétractation.</strong> Vous disposez de 14 jours pour vous rétracter d'un achat de crédits non utilisés. En créant une histoire, vous demandez l'exécution immédiate d'un contenu numérique et reconnaissez perdre votre droit de rétractation pour les crédits ainsi consommés (article L221-28 du Code de la consommation).</p>
<h2>5. Disponibilité</h2>
<p>Le service est fourni « en l'état ». Il dépend de prestataires techniques et d'une seule personne : il peut être lent, indisponible, modifié, suspendu ou arrêté, sans préavis. Les histoires gardées sur un compte peuvent alors ne plus être accessibles : n'y conservez rien d'irremplaçable. En cas d'arrêt définitif, les crédits achetés et non utilisés sont remboursés par le prestataire de paiement.</p>
<h2>6. Propriété intellectuelle</h2>
<p>Le catalogue (textes, personnages, images, voix) appartient à l'éditeur. Il est réservé à un usage privé, familial ou en classe ; il ne peut être ni revendu, ni rediffusé publiquement, ni utilisé pour entraîner un modèle d'intelligence artificielle.</p>
<h2>7. Responsabilité</h2>
<p>Le catalogue gratuit est proposé sans aucune garantie. Pour les créations payantes, la responsabilité de l'éditeur est limitée, dans toute la mesure permise par la loi, aux dommages directs et prévisibles, et au montant que vous avez payé au cours des douze derniers mois. L'éditeur n'est pas responsable de l'usage fait des histoires, ni des pannes de ses prestataires techniques.</p>
<p>Ces limites ne retirent rien aux droits que la loi accorde obligatoirement aux consommateurs, notamment la garantie légale de conformité des contenus numériques.</p>
<h2>8. Données personnelles</h2>
<p>Voir la <a href="confidentialite.html">politique de confidentialité</a>.</p>
<h2>9. Droit applicable, litiges</h2>
<p>Les présentes conditions sont soumises au droit français. Pour un achat, adressez-vous d'abord au prestataire de paiement qui vous a facturé. Vous pouvez recourir gratuitement à un médiateur de la consommation, dont les coordonnées seront indiquées ici à l'ouverture des achats.</p>""")
# « Qui sommes-nous ? » : le mot du papa qui fabrique le site, avec l'invitation à le soutenir (pas de date de mise à jour ici).
_h = pages.page("a-propos.html", "Qui sommes-nous ? | Titistoire", "Titistoire, c'est un papa qui voulait autre chose que la télé pour ses enfants : des histoires à écouter et à regarder, gratuites et sans publicité.",
  """<p class="fil"><a href="./">Titistoire</a></p><h1>Qui sommes-nous ?</h1><div class="texte">
<p>Titistoire, c'est un papa qui voulait autre chose que la télé pour ses enfants.</p>
<p>J'ai fabriqué un site d'histoires à écouter et à regarder : la voix raconte, les images tournent comme dans un album, et le texte s'allume mot à mot pour que l'enfant suive et apprenne à lire sans s'en rendre compte. Il y en a pour tous les âges, de 1 à 10 ans : des imagiers pour les tout-petits, des histoires du soir, des aventures, un feuilleton à énigmes.</p>
<p>Tout est gratuit, sans publicité, sans traceur. Je le fais seul, sur mon temps libre.</p>
<p>Mais ça coûte de l'argent : chaque image, chaque voix, chaque histoire créée à la demande est facturée par les services qui les produisent, et l'hébergement aussi. Si Titistoire plaît à vos enfants et que vous le pouvez, un petit don m'aide à le garder gratuit pour tout le monde et à écrire la suite.</p>
<p><a class="btn" id="don" href="https://ko-fi.com/titistoire" target="_blank" rel="noopener">Soutenir Titistoire</a></p>
<p>Merci, et bonne histoire !</p>
<p><a class="btn" href="./" style="background:#ffcb4d;color:#2d2570">▶ Écouter une histoire</a></p></div>
<div id="donVue" hidden style="position:fixed;inset:0;z-index:60;background:rgba(10,8,30,.82);overflow:auto;padding:14px">
<div style="max-width:440px;margin:0 auto;background:#f9f9f9;border-radius:18px;overflow:hidden">
<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 10px 0 16px;color:#2d2570;font-family:Fredoka,system-ui,sans-serif;font-weight:600"><span>Soutenir Titistoire</span><button id="donFermer" aria-label="Fermer" style="border:none;background:none;font-size:1.6rem;line-height:1;cursor:pointer;color:#2d2570;padding:6px 10px">×</button></div>
<iframe id="donCadre" title="Faire un don à Titistoire" style="border:none;width:100%;height:570px;display:block;background:#f9f9f9"></iframe>
<p style="margin:0;padding:6px 12px 12px;text-align:center;font-size:.8rem"><a href="https://ko-fi.com/titistoire" target="_blank" rel="noopener" style="color:#2d2570">Si rien ne s'affiche, ouvrir la page de don</a></p></div></div>
<script>(function(){var v=document.getElementById('donVue'),c=document.getElementById('donCadre');
document.getElementById('don').addEventListener('click',function(e){e.preventDefault();if(!c.src)c.src='https://ko-fi.com/titistoire/?hidefeed=true&widget=true&embed=true';v.hidden=false;});
document.getElementById('donFermer').addEventListener('click',function(){v.hidden=true;});
v.addEventListener('click',function(e){if(e.target===v)v.hidden=true;});})();</script>""")
(ROOT / "a-propos.html").write_text(_h.replace('href="../', 'href="./'), encoding="utf-8")
print("✅ mentions-legales.html, confidentialite.html, cgu.html")
