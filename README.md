# 📖 Titistoire — Mon Petit Conteur

Petit **jeu à histoires pour les 3-6 ans** (inspiration *Lunii*), 100 % dans le navigateur.

**En ligne :** https://djac57.github.io/titistoire/

## Deux modes
- **🎴 Avec des images** : l'enfant choisit un **héros**, un **univers** et une **leçon** (morale) via de grosses icônes → une histoire illustrée se crée.
- **✏️ Mode libre** : on **décrit** le héros / le lieu / la leçon, et un LLM (**Gemini**) invente l'histoire.

## L'histoire
- Présentée comme un **livre** dont on **tourne les pages** lentement (illustration en haut, texte en bas).
- **Lue à voix haute** avec le **mot en cours surligné** (karaoké), via la synthèse vocale du navigateur.
- Astuce voix : installer une voix FR **« Premium / Améliorée »** (Réglages → Accessibilité → Contenu énoncé) pour un rendu doux et naturel.

## Mode libre — clé API
Le mode libre appelle l'API **Google Gemini** depuis le navigateur. La **clé est saisie dans l'appli** et reste en **localStorage** sur l'appareil — elle **n'est jamais commitée** dans ce dépôt. (Fonctionne mieux servi en HTTPS, ex. GitHub Pages, qu'en fichier local pour cause de CORS.)

## Perso / édition
Les listes (héros, univers, valeurs) sont en haut du `<script>` dans `index.html` — faciles à modifier/étendre.

*Projet perso de la famille — pas affilié aux marques citées.*
