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
<p>Le site titistoire.fr est édité à titre non professionnel par un particulier. Comme le permet l'article 6, III, 2 de la loi n° 2004-575 du 21 juin 2004 pour la confiance dans l'économie numérique, l'éditeur a choisi de ne pas publier son identité ; elle est connue de l'hébergeur ci-dessous, qui la communiquerait à l'autorité judiciaire si elle le demandait.<br>Contact : {MEL}.</p>
<h2>Hébergement</h2>
<p>Le site et ses services sont hébergés par Cloudflare, Inc., 101 Townsend Street, San Francisco, CA 94107, États-Unis — <a href="https://www.cloudflare.com">www.cloudflare.com</a>.<br>Le nom de domaine est enregistré auprès d'OVH SAS, 2 rue Kellermann, 59100 Roubaix, France.</p>
<h2>Propriété intellectuelle</h2>
<p>Les textes des histoires, les personnages, les illustrations, les enregistrements et le site lui-même sont protégés. Ils sont mis à disposition pour une écoute et une lecture privées, en famille ou en classe. Toute reproduction ou rediffusion publique, totale ou partielle, demande une autorisation écrite.</p>
<p>Les illustrations et les voix sont produites à l'aide d'outils d'intelligence artificielle, puis choisies, relues et corrigées par l'éditeur.</p>
<h2>Signaler un problème</h2>
<p>Pour signaler un contenu inapproprié, une erreur ou une atteinte à vos droits : {MEL}. Nous répondons dans les meilleurs délais.</p>""")

doc("confidentialite.html", "Politique de confidentialité", "Quelles données Titistoire traite, pourquoi, et quels sont vos droits.", f"""
<p>Titistoire est fait pour des enfants. Nous avons donc choisi de collecter le moins de données possible : <strong>aucune publicité, aucun traceur publicitaire, aucun outil tiers de mesure d'audience, aucune donnée sur l'enfant.</strong></p>
<h2>Responsable du traitement</h2>
<p>L'éditeur du site (voir les <a href="mentions-legales.html">mentions légales</a>). Contact : {MEL}.</p>
<h2>Sans compte : ce qui reste sur votre appareil</h2>
<p>Pour écouter les histoires, aucun compte n'est nécessaire. Vos réglages (âge choisi, voix, thème clair ou sombre, histoires déjà écoutées) sont enregistrés uniquement dans votre navigateur, sur votre appareil. Ils ne nous sont pas transmis. Vous les effacez en vidant les données du site dans votre navigateur.</p>
<h2>Avec un compte (réservé aux adultes)</h2>
<p>Le compte est créé par un parent ou un adulte responsable, jamais par l'enfant. Nous traitons alors :</p>
<ul><li>votre adresse e-mail, pour vous connecter (envoi d'un code) et vous écrire au sujet du service ;</li>
<li>vos réglages et la liste des histoires écoutées, pour les retrouver sur vos appareils ;</li>
<li>les histoires que vous avez créées (ce que vous avez saisi, le texte, les images et la voix produits), pour vous les conserver ;</li>
<li>en cas d'achat : l'historique de vos crédits. Le paiement est traité par notre prestataire de paiement ; nous ne voyons ni ne conservons votre numéro de carte.</li></ul>
<p>Base légale : l'exécution du service que vous demandez (article 6.1.b du RGPD) et, pour la sécurité du service, notre intérêt légitime (article 6.1.f).</p>
<h2>Création d'histoires : ce qui est transmis</h2>
<p>Ce que vous saisissez pour créer une histoire (héros, lieu, sujet) est envoyé à des services d'intelligence artificielle pour écrire le texte, dessiner les images et produire la voix, puis contrôlé automatiquement. <strong>N'y indiquez ni nom de famille, ni adresse, ni aucune information personnelle sur un enfant.</strong> Un prénom suffit.</p>
<h2>Destinataires et sous-traitants</h2>
<ul><li>Cloudflare, Inc. (hébergement, base de données, génération d'images et contrôle de contenu) ;</li>
<li>Google (modèles Gemini : écriture des histoires et voix) ;</li>
<li>un prestataire d'envoi d'e-mails, pour les codes de connexion, lorsque les comptes seront ouverts ;</li>
<li>un prestataire de paiement, lorsque les achats seront ouverts. Leur nom sera indiqué ici à ce moment-là.</li></ul>
<p>Certains de ces prestataires sont établis aux États-Unis. Les transferts sont encadrés par les clauses contractuelles types de la Commission européenne ou par le cadre de protection des données UE–États-Unis.</p>
<h2>Durées de conservation</h2>
<ul><li>Compte et contenus : tant que le compte existe ; supprimés dans les 30 jours après sa suppression.</li>
<li>Compte inactif : supprimé après 24 mois sans connexion, après un e-mail d'avertissement.</li>
<li>Journaux techniques de sécurité : 12 mois au plus.</li>
<li>Pièces comptables liées aux achats : 10 ans (obligation légale).</li></ul>
<h2>Vos droits</h2>
<p>Vous pouvez accéder à vos données, les corriger, les faire effacer, en demander une copie, limiter ou refuser leur traitement, en écrivant à {MEL}. Vous pouvez supprimer votre compte à tout moment. Vous pouvez aussi saisir la CNIL (<a href="https://www.cnil.fr">www.cnil.fr</a>).</p>
<h2>Cookies</h2>
<p>Le site n'utilise aucun cookie publicitaire ni de mesure d'audience. Seul un identifiant de session strictement nécessaire est utilisé lorsque vous êtes connecté à votre compte ; il ne demande pas de consentement.</p>""")

doc("cgu.html", "Conditions d'utilisation", "Conditions générales d'utilisation et de vente de Titistoire.", f"""
<h2>1. Le service</h2>
<p>Titistoire propose des histoires illustrées et lues à voix haute pour les enfants de 1 à 10 ans. Le catalogue est accessible gratuitement, sans inscription. La création d'histoires sur mesure est réservée aux titulaires d'un compte.</p>
<h2>2. Qui peut l'utiliser</h2>
<p>Le compte est ouvert par une personne majeure. Les enfants utilisent Titistoire sous la responsabilité et la surveillance d'un adulte. Le service ne remplace ni la présence d'un adulte ni un avis médical, éducatif ou psychologique.</p>
<h2>3. Histoires créées à la demande</h2>
<p>Les histoires créées sont écrites, illustrées et lues par des outils d'intelligence artificielle. Chaque texte et chaque image passent par plusieurs contrôles automatiques avant d'être affichés ; en cas de doute, rien n'est montré. Aucun contrôle automatique n'étant infaillible, <strong>nous vous demandons de lire ou d'écouter une histoire créée avant de la proposer à un enfant</strong>, et de nous signaler tout contenu inadapté à {MEL}.</p>
<p>Vous vous engagez à ne pas chercher à obtenir des contenus violents, haineux, sexuels, illicites ou portant sur des personnes réelles, ni à contourner les contrôles. Une demande peut être refusée sans justification ; un compte qui abuse du service peut être suspendu.</p>
<p>Les histoires que vous créez sont pour votre usage privé et familial. Un résultat peut être imparfait (personnage qui change d'aspect, détail incohérent) : écrivez-nous, nous recréditons volontiers une création ratée.</p>
<h2>4. Crédits et paiement</h2>
<p><em>Cette section s'appliquera à l'ouverture des achats.</em> La création d'histoires consomme des crédits. Les crédits s'achètent par lots, au prix affiché toutes taxes comprises au moment de l'achat ; ils ne sont ni échangeables contre de l'argent ni cessibles. Le paiement est encaissé par notre prestataire, qui émet la facture.</p>
<p><strong>Droit de rétractation.</strong> Vous disposez de 14 jours pour vous rétracter d'un achat de crédits non utilisés. En créant une histoire, vous demandez l'exécution immédiate d'un contenu numérique et reconnaissez perdre votre droit de rétractation pour les crédits ainsi consommés (article L221-28 du Code de la consommation).</p>
<h2>5. Disponibilité</h2>
<p>Nous faisons de notre mieux pour que le service fonctionne, sans pouvoir garantir qu'il soit disponible en permanence : il dépend de prestataires techniques. Nous pouvons le faire évoluer, le suspendre pour maintenance ou l'arrêter ; dans ce dernier cas, les crédits achetés et non utilisés sont remboursés.</p>
<h2>6. Propriété intellectuelle</h2>
<p>Le catalogue (textes, personnages, images, voix) appartient à l'éditeur. Il est réservé à un usage privé, familial ou en classe ; il ne peut être ni revendu, ni rediffusé publiquement, ni utilisé pour entraîner un modèle d'intelligence artificielle.</p>
<h2>7. Responsabilité</h2>
<p>Notre responsabilité est limitée aux dommages directs et prévisibles liés à l'usage du service et, pour un service payant, au montant payé au cours des douze derniers mois. Rien ici ne limite les droits que la loi accorde aux consommateurs.</p>
<h2>8. Données personnelles</h2>
<p>Voir la <a href="confidentialite.html">politique de confidentialité</a>.</p>
<h2>9. Droit applicable, litiges</h2>
<p>Les présentes conditions sont soumises au droit français. En cas de litige, écrivez-nous d'abord : {MEL}. Vous pouvez ensuite recourir gratuitement à un médiateur de la consommation, dont les coordonnées seront indiquées ici à l'ouverture des achats.</p>""")
print("✅ mentions-legales.html, confidentialite.html, cgu.html")
