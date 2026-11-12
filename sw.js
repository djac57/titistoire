/* Titistoire — service minimal, exigé par certains navigateurs pour proposer l'installation de l'appli.
   Il ne garde RIEN en mémoire : chaque page, image et voix vient toujours du réseau (pas de version périmée possible). */
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));
self.addEventListener('fetch', () => {});
