/* Titistoire — service de l'appli installée et de l'écoute sans réseau.
   RÈGLE : avec du réseau, tout vient du réseau, comme avant (pas de version périmée possible). Deux exceptions, voulues par l'utilisateur :
   - les IMAGES d'une histoire qu'il a « gardée » (cache GARDEES, rempli par index.html) sortent de ce cache ;
   - quand le réseau ÉCHOUE, et seulement là, la page de l'appli, ses scripts et ses polices (cache COQUILLE) servent de repli.
   Tant qu'aucune histoire n'est gardée, ces deux caches n'existent pas et rien n'est conservé.
   Les voix (/assets/voix/) et l'API ne passent pas par ici : index.html lit lui-même les pistes gardées. */
const GARDEES = 'titi-gardees-v1', COQUILLE = 'titi-coquille-v1', POLICES = /^https:\/\/fonts\.(googleapis|gstatic)\.com\//;
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));

async function deLaCoquille(cle) {
  if (!(await caches.has(COQUILLE))) return null;
  const c = await caches.open(COQUILLE);
  return (await c.match(cle)) || (await c.match(cle, { ignoreSearch: true })) || null;
}
/* Réseau d'abord, toujours. La copie de secours n'est rafraîchie que si elle existe déjà (une histoire au moins est gardée). */
async function reseauPuisCoquille(e, cle) {
  let r;
  try { r = await fetch(e.request); }
  catch (err) { const secours = await deLaCoquille(cle).catch(() => null); if (secours) return secours; throw err; }
  if (r.status === 200 && r.type === 'basic' && !r.redirected) {
    const copie = r.clone();
    e.waitUntil((async () => { if (await caches.has(COQUILLE)) { const c = await caches.open(COQUILLE); if (await c.match(cle)) await c.put(cle, copie); } })().catch(() => {}));
  }
  return r;
}
/* Image : celle d'une histoire gardée vient du cache ; toutes les autres du réseau, comme avant. */
async function image(e) {
  try { if (await caches.has(GARDEES)) { const r = await (await caches.open(GARDEES)).match(e.request.url); if (r) return r; } } catch (err) {}
  try { return await fetch(e.request); }
  catch (err) { const secours = await deLaCoquille(e.request.url).catch(() => null); if (secours) return secours; throw err; }      // l'icône de l'appli
}

self.addEventListener('fetch', e => {
  const req = e.request; if (req.method !== 'GET') return;
  if (POLICES.test(req.url)) { e.respondWith(reseauPuisCoquille(e, req.url)); return; }
  const u = new URL(req.url), racine = new URL('./', self.registration.scope);
  if (u.origin !== racine.origin || !u.pathname.startsWith(racine.pathname)) return;
  const p = u.pathname.slice(racine.pathname.length);
  if (p.startsWith('api/') || p.startsWith('assets/voix/')) return;
  if (req.mode === 'navigate') { if (p === '' || p === 'index.html') e.respondWith(reseauPuisCoquille(e, racine.href)); return; }      // les autres pages (légales, h/…) ne sont jamais gardées
  if (/\.(jpe?g|png|webp)$/.test(p)) { e.respondWith(image(e)); return; }
  if (/\.(js|webmanifest)$/.test(p)) e.respondWith(reseauPuisCoquille(e, req.url));
});
