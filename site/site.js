/* Le site titistoire.fr est fait de fichiers statiques. Ce programme ne voit passer que deux choses :
 *
 *   /assets/voix/…   les pistes de voix : l'hébergement de fichiers ne répond pas aux demandes partielles
 *                    (« Range »), dont Safari a besoin pour lire un son et s'y déplacer.
 *   /api/…           les COMPTES (réservés aux adultes) : connexion par code reçu par e-mail, réglages,
 *                    histoires gardées (20 au plus, images conservées), crédits de création.
 *
 * Données (KV « COMPTES ») :
 *   u:<uid>   le compte (e-mail, dates, réglages, liste des histoires, « gen »)      cr:<uid>  ses crédits (à part : aucune autre écriture ne peut les rétablir)
 *   s:<empreinte du jeton>  une session {uid, gen}                                    c:<uid>   un code en attente
 *   h:<uid>:<id>  une histoire gardée                                                 x:<uid>   trace d'un compte supprimé (empreinte seule) : crédits déjà offerts
 *   p:<clé>  lien de partage d'une histoire gardée -> <uid>:<id>
 *   a:<uid>  compte de l'éditeur (créations illimitées, tableau de bord)   n:m:<mois> nouveaux comptes   d:m:<mois> dons reçus (montants seuls)   k:kofi secret de l'avis de don
 *   l:…  limites d'essais                                                             b:… v:…   plafonds de dépense et verrous, tenus par le worker d'IA
 * Images des histoires gardées : R2 « MEDIAS », m/<clé de l'histoire>/<n>.
 * Aucun mot de passe, aucun cookie : la session est un jeton tiré au hasard, gardé par le navigateur.
 * Le worker d'IA (worker/ai-worker.js) lit et débite les crédits directement dans la même base.
 */
const IA = "https://titistoire-ai.djac-gene.workers.dev";      // seul endroit d'où une image peut être conservée
const MAX_HISTOIRES = 20, CREDITS_OFFERTS = 3, SESSION = 180 * 86400, GARDER_PAR_JOUR = 30;
const INACTIF = 730 * 86400;        // un compte où personne ne s'est connecté depuis 24 mois s'efface de lui-même (durée de vie des données)
const CORS = { "access-control-allow-origin": "*", "access-control-allow-methods": "GET,POST,PUT,DELETE,OPTIONS", "access-control-allow-headers": "content-type, authorization", "access-control-max-age": "86400" };
const J = (o, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", "x-content-type-options": "nosniff", ...CORS } });
const hex = b => [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, "0")).join("");
const sha = async t => hex(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(t)));
const hasard = n => hex(crypto.getRandomValues(new Uint8Array(n)));
const mel = e => { e = String(e || "").trim().toLowerCase(); return e.length <= 254 && /^[^\s@<>"]+@[^\s@<>"]+\.[a-z]{2,}$/.test(e) ? e : ""; };
/** identifiant du compte : empreinte de l'adresse, sans le « +suffixe » (prenom+1@… et prenom+2@… sont le même compte) */
const uidDe = async email => { const [loc, dom] = email.split("@"); return (await sha("titistoire:" + loc.split("+")[0] + "@" + dom)).slice(0, 32); };

export default {
  async fetch(req, env, ctx) {
    const u = new URL(req.url);
    if (u.pathname.startsWith("/api/")) {
      if (req.method === "OPTIONS") return new Response(null, { headers: CORS });
      try { return await api(req, env, ctx, u); } catch (e) { console.error(e); return J({ erreur: "panne" }, 500); }
    }
    return voix(req, env);
  },
  /* Ménage hebdomadaire : les images d'une histoire qui n'existe plus (compte expiré, écriture perdue) sont effacées. */
  async scheduled(evt, env, ctx) { ctx.waitUntil(menage(env)); }
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
/** au plus `max` essais par période (une heure par défaut) pour cette clé -> true si encore permis.
    (KV n'est pas un compteur exact : une rafale simultanée peut dépasser un peu ; c'est un frein, pas un verrou.) */
async function permis(env, cle, max, periode = 3600) {
  const k = "l:" + cle + ":" + Math.floor(Date.now() / (periode * 1000)), n = parseInt(await env.COMPTES.get(k), 10) || 0;
  if (n >= max) return false;
  await env.COMPTES.put(k, String(n + 1), { expirationTtl: periode + 100 }); return true;
}
const ipDe = async req => (await sha("ip:" + (req.headers.get("cf-connecting-ip") || "?"))).slice(0, 24);      // jamais l'adresse en clair
async function session(req, env) {
  const t = (req.headers.get("authorization") || "").replace(/^Bearer\s+/i, "").trim();
  if (!/^[0-9a-f]{64}$/.test(t)) return null;
  const v = await env.COMPTES.get("s:" + await sha(t)); if (!v) return null;
  let uid = v, gen = ""; if (v[0] === "{") { try { const o = JSON.parse(v); uid = o.uid; gen = o.gen || ""; } catch (e) { return null; } }
  const c = await env.COMPTES.get("u:" + uid, "json"); if (!c || (c.gen || "") !== gen) return null;      // un compte supprimé puis recréé n'accepte plus les anciens jetons
  return { uid, c, jeton: t };
}
async function credits(env, uid, c) { const v = await env.COMPTES.get("cr:" + uid); return v === null ? Math.max(0, parseInt(c && c.credits, 10) || 0) : (parseInt(v, 10) || 0); }
const vue = (c, cr, admin) => ({ email: c.email, credits: cr, admin: admin || undefined, prefs: c.prefs || {}, histoires: (c.histoires || []).map(h => ({ id: h.id, titre: h.titre, emoji: h.emoji, ts: h.ts })), max: MAX_HISTOIRES });

async function api(req, env, ctx, u) {
  const p = u.pathname.replace(/\/+$/, ""), M = req.method;
  if (!env.COMPTES) return J({ erreur: "comptes indisponibles" }, 503);
  if (p === "/api/sante") return J({ ok: true, comptes: !!env.COMPTES, medias: !!env.MEDIAS, courrier: !!env.EMAIL });

  // --- image d'une histoire gardée (adresse impossible à deviner, donc sans jeton : une balise <img> n'en envoie pas)
  let m = /^\/api\/m\/([0-9a-f]{32})\/(\d{1,2})$/.exec(p);
  if (m && M === "GET") {
    const o = env.MEDIAS && await env.MEDIAS.get(`m/${m[1]}/${m[2]}`); if (!o) return new Response("introuvable", { status: 404, headers: CORS });
    const type = (o.httpMetadata && o.httpMetadata.contentType) || "";
    return new Response(o.body, { headers: { "content-type": /^image\/(png|jpeg|webp)$/.test(type) ? type : "image/jpeg", "x-content-type-options": "nosniff", "cache-control": "public, max-age=604800", ...CORS } });
  }

  // --- histoire partagée par son auteur : lisible par quiconque a le lien (code impossible à deviner), sans compte
  m = /^\/api\/p\/([0-9a-f]{32})$/.exec(p);
  if (m && M === "GET") {
    const v = await env.COMPTES.get("p:" + m[1]), it = v && await env.COMPTES.get("h:" + v, "json");
    return it ? J({ titre: it.titre, emoji: [...String(it.emoji || "")].filter(ch => ch.codePointAt(0) > 0x2000).slice(0, 4).join("") || "📖", decor: it.decor, sig: it.sig, tableaux: it.tableaux }) : J({ erreur: "introuvable" }, 404);
  }

  // --- dons : Ko-fi prévient cette adresse (dont la fin est un secret gardé dans la base, « k:kofi ») à chaque don.
  //     On n'en retient que le montant et le mois — ni nom, ni adresse, ni message.
  m = /^\/api\/kofi\/([0-9a-f]{32})$/.exec(p);
  if (m && M === "POST") {
    if (m[1] !== await env.COMPTES.get("k:kofi")) return J({ erreur: "inconnu" }, 404);
    let d = null; try { d = JSON.parse((await req.formData()).get("data")); } catch (e) {}
    const montant = d && parseFloat(d.amount);
    if (d && montant > 0 && montant < 100000) {
      const k = "d:m:" + new Date().toISOString().slice(0, 7), o = await env.COMPTES.get(k, "json") || { n: 0, total: 0, devise: "" };
      if (!(o.ids || []).includes(d.message_id)) {             // Ko-fi renvoie parfois deux fois le même avis
        o.n++; o.total = Math.round((o.total + montant) * 100) / 100; o.devise = String(d.currency || o.devise || "").slice(0, 4); o.ids = [...(o.ids || []), String(d.message_id || "").slice(0, 60)].slice(-200);
        await env.COMPTES.put(k, JSON.stringify(o), { expirationTtl: 1100 * 86400 });
      }
    }
    return J({ ok: true });
  }

  // --- 1. demander un code de connexion
  if (p === "/api/compte/code" && M === "POST") {
    const b = await req.json().catch(() => ({})), email = mel(b.email); if (!email) return J({ erreur: "adresse" }, 400);
    const uid = await uidDe(email);
    if (!(await permis(env, "ip:" + await ipDe(req), 12)) || !(await permis(env, "mel:" + uid, 5)) || !(await permis(env, "melj:" + uid, 12, 86400))) return J({ erreur: "trop" }, 429);
    const code = String(crypto.getRandomValues(new Uint32Array(1))[0] % 1000000).padStart(6, "0"), fin = Math.floor(Date.now() / 1000) + 900;
    await env.COMPTES.put("c:" + uid, JSON.stringify({ h: await sha(uid + ":" + code), essais: 0, fin }), { expiration: fin });
    if (!env.EMAIL) return J({ erreur: "courrier indisponible" }, 503);
    try {
      await env.EMAIL.send({ to: email, from: "Titistoire <bonjour@titistoire.fr>", subject: `${code} — votre code Titistoire`,
        text: `Bonjour,\n\nVotre code de connexion à Titistoire : ${code}\n\nIl est valable 15 minutes. Si vous n'avez rien demandé, ignorez ce message.\n\nTitistoire — https://titistoire.fr`,
        html: `<div style="font-family:system-ui,sans-serif;font-size:16px;color:#2d2570"><p>Bonjour,</p><p>Votre code de connexion à Titistoire :</p><p style="font-size:34px;font-weight:700;letter-spacing:6px;margin:18px 0">${code}</p><p>Il est valable 15 minutes. Si vous n'avez rien demandé, ignorez ce message.</p><p style="color:#777;font-size:13px">Titistoire — <a href="https://titistoire.fr">titistoire.fr</a></p></div>` });
    } catch (e) { console.error(e); return J({ erreur: "courrier" }, 502); }
    return J({ ok: true });
  }

  // --- 2. entrer avec le code
  if (p === "/api/compte/entrer" && M === "POST") {
    const b = await req.json().catch(() => ({})), email = mel(b.email), code = String(b.code || "").replace(/\D/g, ""); if (!email || code.length !== 6) return J({ erreur: "code" }, 400);
    if (!(await permis(env, "entrer:" + await ipDe(req), 30))) return J({ erreur: "trop" }, 429);
    const uid = await uidDe(email), att = await env.COMPTES.get("c:" + uid, "json");
    if (!att || !(att.fin > Date.now() / 1000 + 1)) return J({ erreur: "code" }, 403);
    if (att.essais >= 5) { await env.COMPTES.delete("c:" + uid); return J({ erreur: "code" }, 403); }
    if (att.h !== await sha(uid + ":" + code)) { att.essais++; await env.COMPTES.put("c:" + uid, JSON.stringify(att), { expiration: Math.max(att.fin, Math.floor(Date.now() / 1000) + 61) }); return J({ erreur: "code" }, 403); }
    await env.COMPTES.delete("c:" + uid);
    let c = await env.COMPTES.get("u:" + uid, "json"), cr;
    if (!c) {                                                  // nouveau compte ; s'il a déjà existé, il retrouve les créations qui lui restaient (pas trois de plus)
      const trace = await env.COMPTES.get("x:" + uid); cr = trace === null ? CREDITS_OFFERTS : (parseInt(trace, 10) || 0);
      c = { email, cree: Date.now(), vu: Date.now(), gen: hasard(8), prefs: {}, histoires: [] };
      if (trace === null) { const kn = "n:m:" + new Date().toISOString().slice(0, 7); await env.COMPTES.put(kn, String((parseInt(await env.COMPTES.get(kn), 10) || 0) + 1), { expirationTtl: 1100 * 86400 }); }      // nouveaux comptes du mois (tableau de bord)
      await env.COMPTES.put("cr:" + uid, String(cr), { expirationTtl: INACTIF }); await env.COMPTES.put("u:" + uid, JSON.stringify(c), { expirationTtl: INACTIF });
    } else cr = await credits(env, uid, c);
    const jeton = hasard(32); await env.COMPTES.put("s:" + await sha(jeton), JSON.stringify({ uid, gen: c.gen || "" }), { expirationTtl: SESSION });
    return J({ jeton, compte: vue(c, cr, !!(await env.COMPTES.get("a:" + uid))) });
  }

  // --- tout le reste demande une session
  const S = await session(req, env); if (!S) return J({ erreur: "session" }, 401);
  const { uid, c } = S, garder = () => env.COMPTES.put("u:" + uid, JSON.stringify(c), { expirationTtl: INACTIF });
  let cr = await credits(env, uid, c);
  if (Date.now() - (c.vu || 0) > 30 * 86400000) {              // une visite par mois suffit à garder le compte, ses crédits et ses histoires en vie
    c.vu = Date.now();
    await env.COMPTES.put("cr:" + uid, String(cr), { expirationTtl: INACTIF });
    for (const h of c.histoires || []) { const it = await env.COMPTES.get(`h:${uid}:${h.id}`); if (it) await env.COMPTES.put(`h:${uid}:${h.id}`, it, { expirationTtl: INACTIF });
      if (h.cle && await env.COMPTES.get("p:" + h.cle)) await env.COMPTES.put("p:" + h.cle, uid + ":" + h.id, { expirationTtl: INACTIF }); }      // le lien de partage vit aussi longtemps que l'histoire
    if (M === "GET") await garder();                            // sinon l'écriture de la requête elle-même s'en charge (une seule écriture du compte par requête)
  }

  const admin = !!(await env.COMPTES.get("a:" + uid));         // compte de l'éditeur : clé posée à la main dans la base, jamais par le site
  if (p === "/api/compte" && M === "GET") return J(vue(c, cr, admin));
  if (p === "/api/admin" && M === "GET") return admin ? J(await tableau(env)) : J({ erreur: "inconnu" }, 404);
  if (p === "/api/compte/export" && M === "GET") {               // droit d'accès et de portabilité : tout ce que le compte contient, sans nous écrire
    const histoires = []; for (const h of c.histoires || []) { const it = await env.COMPTES.get(`h:${uid}:${h.id}`, "json"); if (it) histoires.push(it); }
    return new Response(JSON.stringify({ service: "Titistoire", exporte_le: new Date().toISOString(), compte: { email: c.email, cree_le: new Date(c.cree).toISOString(), derniere_visite: new Date(c.vu || c.cree).toISOString(), credits: cr, reglages: c.prefs || {} }, histoires_gardees: histoires }, null, 1),
      { headers: { "content-type": "application/json; charset=utf-8", "content-disposition": 'attachment; filename="titistoire-mes-donnees.json"', "cache-control": "no-store", ...CORS } });
  }
  if (p === "/api/compte/sortir" && M === "POST") { await env.COMPTES.delete("s:" + await sha(S.jeton)); return J({ ok: true }); }
  if (p === "/api/compte" && M === "DELETE") {                 // suppression du compte et de tout ce qu'il contient ; les autres sessions tombent d'elles-mêmes (« gen »)
    for (const h of c.histoires || []) await oublier(env, uid, h);
    await env.COMPTES.put("x:" + uid, String(cr), { expirationTtl: INACTIF });      // seule trace : une empreinte et un nombre, pour ne pas offrir trois créations à chaque recréation
    await env.COMPTES.delete("cr:" + uid); await env.COMPTES.delete("u:" + uid); await env.COMPTES.delete("s:" + await sha(S.jeton)); return J({ ok: true });
  }
  if (p === "/api/compte/prefs" && M === "PUT") {
    const b = await req.json().catch(() => null); if (!b || typeof b !== "object") return J({ erreur: "forme" }, 400);
    const q = {}; for (const k of ["groupe", "conteur", "mode", "vitesse"]) if (typeof b[k] === "string") q[k] = b[k].slice(0, 30);
    if (Array.isArray(b.heard)) q.heard = [...new Set(b.heard.map(x => String(x).slice(0, 60)))].slice(0, 400);
    const frais = await env.COMPTES.get("u:" + uid, "json") || c; frais.prefs = q; frais.vu = c.vu;       // relu juste avant d'écrire : ne pas effacer une histoire gardée entre-temps
    await env.COMPTES.put("u:" + uid, JSON.stringify(frais), { expirationTtl: INACTIF }); return J({ ok: true });
  }

  // --- histoires gardées
  if (p === "/api/compte/histoires" && M === "POST") {
    if ((c.histoires || []).length >= MAX_HISTOIRES) return J({ erreur: "plein", max: MAX_HISTOIRES }, 409);
    if (!(await permis(env, "garder:" + uid, GARDER_PAR_JOUR, 86400))) return J({ erreur: "trop" }, 429);
    const corps = await req.text(); if (corps.length > 120000) return J({ erreur: "trop long" }, 413);
    let it; try { it = JSON.parse(corps); } catch (e) { return J({ erreur: "forme" }, 400); }
    if (!it || !Array.isArray(it.tableaux) || !it.tableaux.length || it.tableaux.length > 12) return J({ erreur: "forme" }, 400);
    const id = "h" + Date.now().toString(36) + hasard(3), cle = hasard(16), vues = new Map(); let n = 0, manque = 0;
    // Les images sont recopiées chez nous : une histoire gardée ne dépend plus du cache du générateur (sinon elle serait redessinée, autrement).
    // Seules les adresses signées de notre propre worker d'IA sont acceptées, réduites à leurs paramètres signés (rien qui fasse redessiner à volonté).
    for (const t of it.tableaux) {
      t.pages = (Array.isArray(t.pages) ? t.pages : []).map(x => String(x).slice(0, 800)).slice(0, 6);
      const imgs = [];
      for (const a of (Array.isArray(t.imgs) ? t.imgs : [t.img]).slice(0, 6)) {
        if (typeof a !== "string" || !a) { imgs.push(null); continue; }
        if (vues.has(a)) { imgs.push(vues.get(a)); continue; }
        let neuf = null;
        try {
          const src = new URL(a, IA); if (src.origin !== IA || src.pathname !== "/img") throw 0;
          const q = new URLSearchParams(); for (const k of ["p", "a", "b", "s"]) { const v = src.searchParams.get(k); if (v) q.set(k, v); }
          if (src.searchParams.get("r") === "2") q.set("r", "2");
          if (!env.MEDIAS) neuf = "/img?" + q.toString();      // sans espace de stockage : on garde l'adresse du générateur
          else if (n < 12) { const r = await fetch(IA + "/img?" + q.toString()); const type = r.headers.get("content-type") || "";
            if (r.ok && /^image\/(png|jpeg|webp)$/.test(type)) { const k = ++n; await env.MEDIAS.put(`m/${cle}/${k}`, r.body, { httpMetadata: { contentType: type }, customMetadata: { uid, id } }); neuf = `/api/m/${cle}/${k}`; } }
        } catch (e) {}
        if (!neuf) manque++;
        vues.set(a, neuf); imgs.push(neuf);
      }
      t.imgs = imgs; t.img = imgs.find(Boolean) || null;
    }
    const h = { id, cle, n, titre: String(it.titre || "Mon histoire").slice(0, 90), emoji: String(it.emoji || "📖").slice(0, 16), ts: Date.now() };
    await env.COMPTES.put(`h:${uid}:${id}`, JSON.stringify({ id, titre: h.titre, emoji: h.emoji, ts: h.ts, decor: String(it.decor || "").slice(0, 20), sig: String(it.sig || "").slice(0, 200), tableaux: it.tableaux.map(t => ({ pages: t.pages, imgs: t.imgs, img: t.img })) }), { expirationTtl: INACTIF });
    const frais = await env.COMPTES.get("u:" + uid, "json") || c; frais.histoires = [h, ...(frais.histoires || [])].slice(0, MAX_HISTOIRES); frais.vu = c.vu;      // relu juste avant d'écrire
    await env.COMPTES.put("u:" + uid, JSON.stringify(frais), { expirationTtl: INACTIF });
    return J({ ok: true, histoire: vue(frais, cr).histoires[0], histoires: vue(frais, cr).histoires, images_manquantes: manque });
  }
  m = /^\/api\/compte\/histoires\/(h[0-9a-z]{6,24})\/partage$/.exec(p);
  if (m && M === "POST") {                                     // l'auteur demande un lien de partage : le code est la clé (secrète) de l'histoire ; supprimer l'histoire coupe le lien
    const h = (c.histoires || []).find(x => x.id === m[1]); if (!h || !h.cle) return J({ erreur: "introuvable" }, 404);
    if (await env.COMPTES.get("p:" + h.cle)) return J({ ok: true, code: h.cle });
    // Ce qui est gardé vient du navigateur : avant de le rendre public, le worker d'IA confirme que le texte est bien celui qu'il a écrit et contrôlé
    // (signature), et contrôle le titre. Une histoire retouchée à la main ne se partage pas.
    if (!(await permis(env, "partage:" + uid, 20, 86400))) return J({ erreur: "trop" }, 429);
    const it = await env.COMPTES.get(`h:${uid}:${h.id}`, "json"); if (!it) return J({ erreur: "introuvable" }, 404);
    let v = null; try { v = await (await fetch(IA + "/verif", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ tableaux: it.tableaux.map(t => t.pages), sig: it.sig, titre: it.titre }) })).json(); } catch (e) {}
    if (!v || v.ok !== true) return J({ erreur: "refus" }, 403);
    await env.COMPTES.put("p:" + h.cle, uid + ":" + h.id, { expirationTtl: INACTIF }); return J({ ok: true, code: h.cle });
  }
  m = /^\/api\/compte\/histoires\/(h[0-9a-z]{6,24})$/.exec(p);
  if (m && M === "GET") { const it = await env.COMPTES.get(`h:${uid}:${m[1]}`, "json"); return it ? J(it) : J({ erreur: "introuvable" }, 404); }
  if (m && M === "DELETE") {
    const frais = await env.COMPTES.get("u:" + uid, "json") || c, h = (frais.histoires || []).find(x => x.id === m[1]);
    if (h) { await oublier(env, uid, h); frais.histoires = frais.histoires.filter(x => x.id !== m[1]); frais.vu = c.vu; await env.COMPTES.put("u:" + uid, JSON.stringify(frais), { expirationTtl: INACTIF }); }
    return J({ ok: true, histoires: vue(frais, cr).histoires });
  }
  return J({ erreur: "inconnu" }, 404);
}
/** Tableau de bord de l'éditeur : des nombres seulement, aucune donnée d'un compte. */
const COUT_HISTOIRE = 0.30;         // ESTIMATION en euros d'une histoire créée (8 images, texte, voix) — à recaler sur les factures
async function tableau(env) {
  const compter = async prefixe => { let n = 0, curseur, tours = 0; do { const L = await env.COMPTES.list({ prefix: prefixe, limit: 1000, cursor: curseur }); n += L.keys.length; curseur = L.list_complete ? undefined : L.cursor; } while (curseur && ++tours < 3); return n; };
  const nb = async k => parseInt(await env.COMPTES.get(k), 10) || 0;
  const [comptes, gardees, partagees, supprimes] = await Promise.all(["u:", "h:", "p:", "x:"].map(compter));
  const jours = [], mois = [], t = new Date();
  for (let i = 0; i < 7; i++) { const j = new Date(t.getTime() - i * 86400000).toISOString().slice(0, 10); jours.push(j); }
  for (let i = 0; i < 3; i++) { const d = new Date(Date.UTC(t.getUTCFullYear(), t.getUTCMonth() - i, 1)); mois.push(d.toISOString().slice(0, 7)); }
  const pj = await Promise.all(jours.map(async j => ({ jour: j, public: await nb("b:j:" + j), moi: await nb("ba:j:" + j) })));
  const pm = await Promise.all(mois.map(async m => { const pub = await nb("b:m:" + m), moi = await nb("ba:m:" + m), don = await env.COMPTES.get("d:m:" + m, "json");
    return { mois: m, public: pub, moi, nouveaux_comptes: await nb("n:m:" + m), cout_estime: Math.round((pub + moi) * COUT_HISTOIRE * 100) / 100, dons: don ? { n: don.n, total: don.total, devise: don.devise } : { n: 0, total: 0, devise: "" } }; }));
  return { comptes, comptes_supprimes: supprimes, histoires_gardees: gardees, histoires_partagees: partagees, jours: pj, mois: pm, cout_par_histoire: COUT_HISTOIRE, dons_branches: !!(await env.COMPTES.get("k:kofi")) };
}
async function oublier(env, uid, h) {
  await env.COMPTES.delete(`h:${uid}:${h.id}`); if (h.cle) await env.COMPTES.delete("p:" + h.cle);      // le lien de partage tombe avec l'histoire
  if (env.MEDIAS && h.cle && h.n) await env.MEDIAS.delete(Array.from({ length: h.n }, (_, k) => `m/${h.cle}/${k + 1}`));      // un seul appel pour toutes les images
}
/** Efface les images dont l'histoire n'existe plus dans la base (compte expiré après 24 mois, écriture perdue). */
async function menage(env) {
  if (!env.MEDIAS || !env.COMPTES) return;
  let curseur, vus = new Map(), tours = 0;
  do {
    const L = await env.MEDIAS.list({ prefix: "m/", limit: 500, cursor: curseur, include: ["customMetadata"] }); curseur = L.truncated ? L.cursor : undefined;
    const aEffacer = [];
    for (const o of L.objects) {
      const md = o.customMetadata || {}, k = md.uid && md.id ? `h:${md.uid}:${md.id}` : null;
      if (!k) continue;                                         // image sans étiquette (ancienne) : on n'y touche pas
      if (Date.now() - new Date(o.uploaded).getTime() < 3600000) continue;      // histoire en cours d'enregistrement
      if (!vus.has(k)) vus.set(k, (await env.COMPTES.get(k)) !== null);
      if (!vus.get(k)) aEffacer.push(o.key);
    }
    if (aEffacer.length) await env.MEDIAS.delete(aEffacer);
  } while (curseur && ++tours < 20);
}
