// Essai hors ligne du contrôle des dessins (/img du worker) : dessinateur, contrôle de sécurité et juge SIMULÉS, aucun réseau.
//   node tools/test_dessin.mjs
import worker, { lireVerdict, meilleurDessin, questionDessin } from "../worker/ai-worker.js";
const dire = (...a) => process.stdout.write(a.join(" ") + "\n");
let ko = 0; const ok = (c, m) => { dire((c ? "  ok    " : "  ÉCHEC ") + m); if (!c) ko++; };

dire("lecture des réponses du juge");
const sain = '{"characters": 2, "extra_limbs": false, "missing_limbs": false, "extra_heads": false, "merged_bodies": false, "duplicate": false, "text": false}';
ok(lireVerdict(sain, 2).ok && lireVerdict(sain, 2).note === 0, "image saine : acceptée");
ok(!lireVerdict(sain.replace('"extra_limbs": false', '"extra_limbs": true'), 2).ok, "membres en trop : rejetée");
ok(!lireVerdict("```json\n" + sain.replace('"extra_heads": false', '"extra_heads": "yes"') + "\n```", 2).ok, "tête en double, réponse entourée de ```json : rejetée");
ok(lireVerdict(sain.replace('"missing_limbs": false', '"missing_limbs": true'), 2).ok, "un seul défaut léger (membre caché) : acceptée");
ok(lireVerdict(sain.replace('"characters": 2', '"characters": 4'), 2).ok && lireVerdict(sain.replace('"characters": 2', '"characters": 4'), 2).defauts.length === 1, "4 personnages pour 2 : défaut léger noté");
ok(!lireVerdict(sain.replace('"characters": 2', '"characters": 4').replace('"duplicate": false', '"duplicate": true'), 2).ok, "personnage en double + trop de personnages : rejetée");
ok(!lireVerdict("extra_limbs: true, text: false", 1).ok, "réponse sans JSON mais lisible : comprise");
ok(lireVerdict("I cannot help with that.", 1) === null, "réponse illisible : null (traité comme panne)");
ok(meilleurDessin([{ juge: { note: 3 } }, { juge: { panne: "x" } }, { juge: { note: 2 } }]).juge.panne, "meilleur dessin : juge en panne (inconnu) préféré à un défaut certain");
ok(/exactly 2 main characters/.test(questionDessin("HERO and FRIEND", 2)) && !/exactly/.test(questionDessin("x", 0)), "question : nombre de personnages attendu quand les fiches le disent");

dire("chemin /img, réseau simulé");
const CLE = "cle-de-test-0123456789";
async function signer(t) { const k = await crypto.subtle.importKey("raw", new TextEncoder().encode("titistoire:" + CLE), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return [...new Uint8Array(await crypto.subtle.sign("HMAC", k, new TextEncoder().encode(t))).slice(0, 16)].map(b => b.toString(16).padStart(2, "0")).join(""); }
const cache = new Map();
globalThis.caches = { default: { match: async r => cache.get(r.url)?.clone(), put: async (r, v) => { cache.set(r.url, v); } } };
const logs = []; console.log = (...a) => logs.push(a.join(" "));      // le journal du worker est gardé pour être vérifié
function monde(verdicts, { securite = () => true, panne = false, lent = false } = {}) {
  let n = 0; const vus = { dessins: 0, juges: 0 }, kv = new Map();
  const env = { GEMINI_KEY: CLE, COMPTES: { get: async k => kv.get(k) ?? null, put: async (k, v) => { kv.set(k, v); } },
    AI: { run: async (modele, x) => {
      if (/flux/.test(modele)) { vus.dessins++; return { image: Buffer.from("dessin-" + (++n)).toString("base64") }; }
      const txt = x.messages[0].content[0].text, img = Buffer.from(x.messages[0].content[1].image_url.url.split(",")[1], "base64").toString();
      if (/3-year-old/.test(txt)) return { response: securite(img) ? "YES" : "NO" };
      vus.juges++;
      if (panne) throw new Error("modèle indisponible");
      if (lent) return new Promise(() => {});
      const v = verdicts[img]; return { response: v === undefined ? sain : v };
    } } };
  return { env, vus, kv };
}
const ctx = { attente: [], waitUntil(p) { this.attente.push(p); } };
async function page(m, nom) {
  cache.clear(); const p = "Flat 2D picture. " + nom + " the hero (exactly the character shown in image 1) waves.", a = "fiche " + nom;
  const s = await signer("img:" + p + "|" + a);
  const r = await worker.fetch(new Request("https://w.test/img?" + new URLSearchParams({ p, a, s })), m.env, ctx);
  await Promise.all(ctx.attente.splice(0)); return r;
}
const mauvais = sain.replace('"extra_limbs": false', '"extra_limbs": true');
let m = monde({}), r = await page(m, "A");
let corps = r.ok ? Buffer.from(await r.arrayBuffer()).toString() : "";
ok(r.ok && corps === "dessin-2" && m.vus.dessins === 2 && m.vus.juges === 1, `image saine : servie du 1er coup (${corps}, ${m.vus.dessins} dessins dont la fiche, ${m.vus.juges} jugement, x-juge « ${decodeURIComponent(r.headers.get("x-juge") || "")} »)`);
m = monde({ "dessin-2": mauvais }); r = await page(m, "B"); corps = r.ok ? Buffer.from(await r.arrayBuffer()).toString() : "";
ok(r.ok && corps === "dessin-3" && m.vus.juges === 2 && m.kv.get("img:rejets:" + new Date().toISOString().slice(0, 10)) === "1", `image rejetée (3 bras) puis redessinée et acceptée : sert ${corps}, compteur de rejets = ${m.kv.get("img:rejets:" + new Date().toISOString().slice(0, 10))}`);
m = monde({ "dessin-2": mauvais, "dessin-3": mauvais.replace('"extra_heads": false', '"extra_heads": true'), "dessin-4": mauvais.replace('"merged_bodies": false', '"merged_bodies": true') });
r = await page(m, "C"); corps = r.ok ? Buffer.from(await r.arrayBuffer()).toString() : "";
ok(r.ok && m.vus.dessins === 4 && corps === "dessin-2", `trois dessins ratés : jamais plus de 2 redessins, sert le moins mauvais (${corps}, ${m.vus.dessins - 1} dessins de page)`);
m = monde({}, { panne: true }); r = await page(m, "D"); corps = r.ok ? Buffer.from(await r.arrayBuffer()).toString() : "";
ok(r.ok && corps === "dessin-2" && m.vus.dessins === 2, "juge en panne : l'image est servie sans redessin");
const t0 = Date.now(); m = monde({}, { lent: true }); r = await page(m, "E");
ok(r.ok && m.vus.dessins === 2 && Date.now() - t0 < 16500, `juge muet : servie après le délai (${((Date.now() - t0) / 1000).toFixed(1)} s)`);
m = monde({ "dessin-2": mauvais }, { securite: img => img !== "dessin-3" }); r = await page(m, "F"); corps = r.ok ? Buffer.from(await r.arrayBuffer()).toString() : "";
ok(r.ok && corps === "dessin-4", `redessin écarté par le contrôle de sécurité : ignoré, on continue (${corps})`);
m = monde({}, { securite: img => img !== "dessin-2" }); r = await page(m, "G");
ok(r.status === 451 && m.vus.dessins === 2, "1er dessin écarté par le contrôle de sécurité : 451 comme avant (le site redemande avec r=2)");
ok(logs.some(l => /contrôle du dessin/.test(l) && /membres en trop/.test(l)), "décisions journalisées : " + (logs.find(l => /membres en trop/.test(l)) || "").slice(0, 160));

dire(ko ? `${ko} ÉCHEC(S)` : "tout est bon");
process.exitCode = ko ? 1 : 0;
