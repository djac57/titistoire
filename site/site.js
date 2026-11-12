/* Le site titistoire.fr est fait de fichiers statiques. Ce programme ne voit passer que deux choses :
 *
 *   /assets/voix/…   les pistes de voix : l'hébergement de fichiers ne répond pas aux demandes partielles
 *                    (« Range »), dont Safari a besoin pour lire un son et s'y déplacer.
 *   /api/…           les COMPTES (réservés aux adultes) : connexion par code reçu par e-mail, réglages,
 *                    histoires gardées (20 au plus, images conservées), crédits de création.
 *
 * Données (KV « COMPTES ») :   u:<uid>  le compte        s:<empreinte du jeton>  une session
 *                              c:<uid>  un code en attente   h:<uid>:<id>  une histoire gardée   l:…  limites d'essais
 * Images des histoires gardées : R2 « MEDIAS », m/<clé de l'histoire>/<n>.
 * Aucun mot de passe, aucun cookie : la session est un jeton tiré au hasard, gardé par le navigateur.
 */
const IA = "https://titistoire-ai.djac-gene.workers.dev";      // seul endroit d'où une image peut être conservée
const MAX_HISTOIRES = 20, CREDITS_OFFERTS = 3, SESSION = 180 * 86400;
const INACTIF = 730 * 86400;        // un compte où personne ne s'est connecté depuis 24 mois s'efface de lui-même (durée de vie des données)
const CORS = { "access-control-allow-origin": "*", "access-control-allow-methods": "GET,POST,PUT,DELETE,OPTIONS", "access-control-allow-headers": "content-type, authorization", "access-control-max-age": "86400" };
const J = (o, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", ...CORS } });
const hex = b => [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, "0")).join("");
const sha = async t => hex(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(t)));
const hasard = n => hex(crypto.getRandomValues(new Uint8Array(n)));
const mel = e => { e = String(e || "").trim().toLowerCase(); return e.length <= 254 && /^[^\s@<>"]+@[^\s@<>"]+\.[a-z]{2,}$/.test(e) ? e : ""; };

export default {
  async fetch(req, env, ctx) {
    const u = new URL(req.url);
    if (u.pathname.startsWith("/api/")) {
      if (req.method === "OPTIONS") return new Response(null, { headers: CORS });
      try { return await api(req, env, ctx, u); } catch (e) { return J({ erreur: "panne", detail: String(e).slice(0, 200) }, 500); }
    }
    return voix(req, env);
  }
};

/* ===================== pistes de voix : demandes partielles ===================== */
async function voix(req, env) {
  const r = await env.ASSETS.fetch(req), range = req.headers.get("range");
  if (req.method !== "GET" || r.status !== 200) return r;
  const h = new Headers(r.headers); h.set("accept-ranges", "bytes");
  const m = range && /^bytes=(\d*)-(\d*)$/.exec(range.trim());
  if (!m || (m[1] === "" && m[2] === "")) return new Response(r.body, { status: 200, headers: h });
  const buf = await r.arrayBuffer(), n = buf.byteLength;
  const a = m[1] === "" ? Math.max(0, n - Number(m[2])) : Number(m[1]);
  const b = m[1] === "" || m[2] === "" ? n - 1 : Math.min(Number(m[2]), n - 1);
  if (a > b || a >= n) return new Response(null, { status: 416, headers: { "content-range": `bytes */${n}` } });
  h.set("content-range", `bytes ${a}-${b}/${n}`); h.set("content-length", String(b - a + 1));
  return new Response(buf.slice(a, b + 1), { status: 206, headers: h });
}

/* ===================== comptes ===================== */
/** au plus `max` essais par heure pour cette clé -> true si encore permis */
async function permis(env, cle, max) {
  const k = "l:" + cle + ":" + Math.floor(Date.now() / 3600000), n = parseInt(await env.COMPTES.get(k), 10) || 0;
  if (n >= max) return false;
  await env.COMPTES.put(k, String(n + 1), { expirationTtl: 3700 }); return true;
}
async function session(req, env) {
  const t = (req.headers.get("authorization") || "").replace(/^Bearer\s+/i, "").trim();
  if (!/^[0-9a-f]{64}$/.test(t)) return null;
  const uid = await env.COMPTES.get("s:" + await sha(t)); if (!uid) return null;
  const c = await env.COMPTES.get("u:" + uid, "json"); return c ? { uid, c, jeton: t } : null;
}
const vue = c => ({ email: c.email, credits: c.credits, prefs: c.prefs || {}, histoires: c.histoires || [], max: MAX_HISTOIRES });

async function api(req, env, ctx, u) {
  const p = u.pathname.replace(/\/+$/, ""), M = req.method;
  if (!env.COMPTES) return J({ erreur: "comptes indisponibles" }, 503);
  if (p === "/api/sante") return J({ ok: true, comptes: !!env.COMPTES, medias: !!env.MEDIAS, courrier: !!env.EMAIL });

  // --- image d'une histoire gardée (adresse impossible à deviner, donc sans jeton : une balise <img> n'en envoie pas)
  let m = /^\/api\/m\/([0-9a-f]{32})\/(\d{1,2})$/.exec(p);
  if (m && M === "GET") {
    const o = env.MEDIAS && await env.MEDIAS.get(`m/${m[1]}/${m[2]}`); if (!o) return new Response("introuvable", { status: 404, headers: CORS });
    return new Response(o.body, { headers: { "content-type": (o.httpMetadata && o.httpMetadata.contentType) || "image/jpeg", "cache-control": "public, max-age=31536000, immutable", ...CORS } });
  }

  // --- 1. demander un code de connexion
  if (p === "/api/compte/code" && M === "POST") {
    const b = await req.json().catch(() => ({})), email = mel(b.email); if (!email) return J({ erreur: "adresse" }, 400);
    const ip = req.headers.get("cf-connecting-ip") || "?", uid = (await sha("titistoire:" + email)).slice(0, 32);
    if (!(await permis(env, "ip:" + ip, 12)) || !(await permis(env, "mel:" + uid, 5))) return J({ erreur: "trop" }, 429);
    const code = String(crypto.getRandomValues(new Uint32Array(1))[0] % 1000000).padStart(6, "0");
    await env.COMPTES.put("c:" + uid, JSON.stringify({ h: await sha(uid + ":" + code), essais: 0 }), { expirationTtl: 900 });
    if (!env.EMAIL) return J({ erreur: "courrier indisponible" }, 503);
    try {
      await env.EMAIL.send({ to: email, from: "Titistoire <bonjour@titistoire.fr>", subject: `${code} — votre code Titistoire`,
        text: `Bonjour,\n\nVotre code de connexion à Titistoire : ${code}\n\nIl est valable 15 minutes. Si vous n'avez rien demandé, ignorez ce message.\n\nTitistoire — https://titistoire.fr`,
        html: `<div style="font-family:system-ui,sans-serif;font-size:16px;color:#2d2570"><p>Bonjour,</p><p>Votre code de connexion à Titistoire :</p><p style="font-size:34px;font-weight:700;letter-spacing:6px;margin:18px 0">${code}</p><p>Il est valable 15 minutes. Si vous n'avez rien demandé, ignorez ce message.</p><p style="color:#777;font-size:13px">Titistoire — <a href="https://titistoire.fr">titistoire.fr</a></p></div>` });
    } catch (e) { return J({ erreur: "courrier", detail: String(e).slice(0, 160) }, 502); }
    return J({ ok: true });
  }

  // --- 2. entrer avec le code
  if (p === "/api/compte/entrer" && M === "POST") {
    const b = await req.json().catch(() => ({})), email = mel(b.email), code = String(b.code || "").replace(/\D/g, ""); if (!email || code.length !== 6) return J({ erreur: "code" }, 400);
    const uid = (await sha("titistoire:" + email)).slice(0, 32), att = await env.COMPTES.get("c:" + uid, "json");
    if (!att) return J({ erreur: "code" }, 403);
    if (att.essais >= 5) { await env.COMPTES.delete("c:" + uid); return J({ erreur: "code" }, 403); }
    if (att.h !== await sha(uid + ":" + code)) { att.essais++; await env.COMPTES.put("c:" + uid, JSON.stringify(att), { expirationTtl: 900 }); return J({ erreur: "code" }, 403); }
    await env.COMPTES.delete("c:" + uid);
    let c = await env.COMPTES.get("u:" + uid, "json");
    if (!c) c = { email, cree: Date.now(), credits: CREDITS_OFFERTS, prefs: {}, histoires: [] };
    c.vu = Date.now(); await env.COMPTES.put("u:" + uid, JSON.stringify(c), { expirationTtl: INACTIF });
    const jeton = hasard(32); await env.COMPTES.put("s:" + await sha(jeton), uid, { expirationTtl: SESSION });
    return J({ jeton, compte: vue(c) });
  }

  // --- tout le reste demande une session
  const S = await session(req, env); if (!S) return J({ erreur: "session" }, 401);
  const { uid, c } = S, garder = () => env.COMPTES.put("u:" + uid, JSON.stringify(c), { expirationTtl: INACTIF });
  if (Date.now() - (c.vu || 0) > 30 * 86400000) {              // une visite par mois suffit à garder le compte et ses histoires en vie
    c.vu = Date.now(); await garder();
    for (const h of c.histoires || []) { const it = await env.COMPTES.get(`h:${uid}:${h.id}`); if (it) await env.COMPTES.put(`h:${uid}:${h.id}`, it, { expirationTtl: INACTIF }); }
  }

  if (p === "/api/compte" && M === "GET") return J(vue(c));
  if (p === "/api/compte/export" && M === "GET") {               // droit d'accès et de portabilité : tout ce que le compte contient, sans nous écrire
    const histoires = []; for (const h of c.histoires || []) { const it = await env.COMPTES.get(`h:${uid}:${h.id}`, "json"); if (it) histoires.push(it); }
    return new Response(JSON.stringify({ service: "Titistoire", exporte_le: new Date().toISOString(), compte: { email: c.email, cree_le: new Date(c.cree).toISOString(), derniere_visite: new Date(c.vu || c.cree).toISOString(), credits: c.credits, reglages: c.prefs || {} }, histoires_gardees: histoires }, null, 1),
      { headers: { "content-type": "application/json; charset=utf-8", "content-disposition": 'attachment; filename="titistoire-mes-donnees.json"', "cache-control": "no-store", ...CORS } });
  }
  if (p === "/api/compte/sortir" && M === "POST") { await env.COMPTES.delete("s:" + await sha(S.jeton)); return J({ ok: true }); }
  if (p === "/api/compte" && M === "DELETE") {                 // suppression du compte et de tout ce qu'il contient
    for (const h of c.histoires || []) await oublier(env, uid, h);
    await env.COMPTES.delete("u:" + uid); await env.COMPTES.delete("s:" + await sha(S.jeton)); return J({ ok: true });
  }
  if (p === "/api/compte/prefs" && M === "PUT") {
    const b = await req.json().catch(() => null); if (!b || typeof b !== "object") return J({ erreur: "forme" }, 400);
    const q = {}; for (const k of ["groupe", "conteur", "mode", "vitesse"]) if (typeof b[k] === "string") q[k] = b[k].slice(0, 30);
    if (Array.isArray(b.heard)) q.heard = [...new Set(b.heard.map(x => String(x).slice(0, 60)))].slice(0, 400);
    c.prefs = q; await garder(); return J({ ok: true });
  }
  // crédits : lus et débités par le worker d'IA, au nom de l'utilisateur, une fois l'histoire écrite et contrôlée
  if (p === "/api/compte/credit" && M === "POST") {
    if (!(c.credits > 0)) return J({ erreur: "credits", credits: 0 }, 402);
    c.credits--; await garder(); return J({ ok: true, credits: c.credits });
  }

  // --- histoires gardées
  if (p === "/api/compte/histoires" && M === "POST") {
    if ((c.histoires || []).length >= MAX_HISTOIRES) return J({ erreur: "plein", max: MAX_HISTOIRES }, 409);
    const corps = await req.text(); if (corps.length > 120000) return J({ erreur: "trop long" }, 413);
    let it; try { it = JSON.parse(corps); } catch (e) { return J({ erreur: "forme" }, 400); }
    if (!it || !Array.isArray(it.tableaux) || !it.tableaux.length || it.tableaux.length > 12) return J({ erreur: "forme" }, 400);
    const id = "h" + Date.now().toString(36) + hasard(3), cle = hasard(16), vues = new Map(); let n = 0;
    // Les images sont recopiées chez nous : une histoire gardée ne dépend plus du cache du générateur (sinon elle serait redessinée, autrement).
    // Seules les adresses signées de notre propre worker d'IA sont acceptées.
    for (const t of it.tableaux) {
      t.pages = (Array.isArray(t.pages) ? t.pages : []).map(x => String(x).slice(0, 800)).slice(0, 6);
      t.imgs = await Promise.all((Array.isArray(t.imgs) ? t.imgs : [t.img]).slice(0, 6).map(async a => {
        if (typeof a !== "string" || !a) return null;
        if (vues.has(a)) return vues.get(a);
        const chemin = a.startsWith(IA) ? a.slice(IA.length) : a; let neuf = (!env.MEDIAS && /^\/img\?/.test(chemin)) ? chemin : null;      // sans espace de stockage : on garde l'adresse du générateur
        if (env.MEDIAS && /^\/img\?/.test(chemin) && n < 30) {
          try { const r = await fetch(IA + chemin); if (r.ok) { const k = ++n; await env.MEDIAS.put(`m/${cle}/${k}`, r.body, { httpMetadata: { contentType: r.headers.get("content-type") || "image/jpeg" } }); neuf = `/api/m/${cle}/${k}`; } } catch (e) {}
        }
        vues.set(a, neuf); return neuf;
      }));
      t.img = t.imgs.find(Boolean) || null;
    }
    const h = { id, cle, n, titre: String(it.titre || "Mon histoire").slice(0, 90), emoji: [...String(it.emoji || "📖")][0], ts: Date.now() };
    await env.COMPTES.put(`h:${uid}:${id}`, JSON.stringify({ ...h, decor: String(it.decor || "").slice(0, 20), sig: String(it.sig || "").slice(0, 200), tableaux: it.tableaux.map(t => ({ pages: t.pages, imgs: t.imgs, img: t.img })) }), { expirationTtl: INACTIF });
    c.histoires = [h, ...(c.histoires || [])]; await garder();
    return J({ ok: true, histoire: h, histoires: c.histoires });
  }
  m = /^\/api\/compte\/histoires\/(h[0-9a-z]{6,24})$/.exec(p);
  if (m && M === "GET") { const it = await env.COMPTES.get(`h:${uid}:${m[1]}`, "json"); return it ? J(it) : J({ erreur: "introuvable" }, 404); }
  if (m && M === "DELETE") {
    const h = (c.histoires || []).find(x => x.id === m[1]); if (h) { await oublier(env, uid, h); c.histoires = c.histoires.filter(x => x.id !== m[1]); await garder(); }
    return J({ ok: true, histoires: c.histoires || [] });
  }
  return J({ erreur: "inconnu" }, 404);
}
async function oublier(env, uid, h) {
  await env.COMPTES.delete(`h:${uid}:${h.id}`);
  if (env.MEDIAS && h.cle) for (let k = 1; k <= (h.n || 0); k++) await env.MEDIAS.delete(`m/${h.cle}/${k}`);
}
