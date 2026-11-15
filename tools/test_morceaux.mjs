// Essai hors ligne de la voix en morceaux (worker/voix.js + voixConteuse) et des formes d'histoire par âge.
// Aucun réseau : la voix (Gemini) et la reconnaissance (Whisper) sont simulées.   node tools/test_morceaux.mjs
import { morceaux, rogner, assembler, fusionner, alignerMots, bilan, octets, pcmDepuis } from "../worker/voix.js";
import { voixConteuse, jugerHistoire, consigneHistoire } from "../worker/ai-worker.js";
let ko = 0; const ok = (c, m) => { console.log((c ? "  ok    " : "  ÉCHEC ") + m); if (!c) ko++; };

console.log("découpage en morceaux");
const P = n => "x".repeat(n);
let M = morceaux([[P(100), P(100)], [P(100), P(100)], [P(100), P(100)]], 700);
ok(M.length === 2 && M[0].pages.join() === "0,1,2,3" && M[1].pages.join() === "4,5", "jamais plus de deux tableaux par morceau : " + JSON.stringify(M.map(m => m.pages)));
ok(M[0].texte === [P(100), P(100)].join("\n\n") + "\n\n\n" + [P(100), P(100)].join("\n\n"), "séparateurs : page \\n\\n, tableau \\n\\n\\n");
M = morceaux([[P(420), P(420), P(420)]], 700);
ok(M.length === 3 && M.every(m => m.pages.length === 1), "pages de 420 car. : une par appel");
M = morceaux([[P(900), P(50)]], 700);
ok(M.length === 2 && M[0].texte.length === 900, "une page plus longue que la limite reste entière et seule");
M = morceaux([[P(330), P(330), P(330)]], 700);
ok(M.length === 2 && M[0].pages.join() === "0,1", "pages de 330 car. : 2 + 1");
ok(morceaux([[P(70), P(70)]], 700).length === 1, "tableau des 1-3 ans : un seul appel");

console.log("rognage, assemblage, minutage");
const son = (s, rate, v, lead = 0, trail = 0) => { const p = new Int16Array(Math.round((lead + s + trail) * rate)); for (let i = Math.round(lead * rate); i < Math.round((lead + s) * rate); i++) p[i] = (i % 2 ? v : -v); return p; };
const r1 = rogner(son(2, 24000, 3000, 1, 1), 24000);
ok(Math.abs(r1.length / 24000 - (2 + 0.12 + 0.25)) < 0.03, "silences rognés, marges 0,12 s / 0,25 s : " + (r1.length / 24000).toFixed(2) + " s");
const A = assembler([{ pcm: son(2, 24000, 3000), rate: 24000 }, { pcm: son(1, 16000, 3000), rate: 16000 }, { pcm: son(3, 24000, 3000), rate: 24000 }], 0.45);
ok(A.rate === 24000 && Math.abs(A.pcm.length / 24000 - (2 + 1 + 3 + 0.9)) < 0.01, "débits mélangés ramenés à 24 kHz, deux pauses de 0,45 s : " + (A.pcm.length / 24000).toFixed(2) + " s");
ok(A.debuts.map(x => x.toFixed(2)).join() === "0.00,2.45,3.90", "débuts des morceaux : " + A.debuts.map(x => x.toFixed(2)).join(", "));
ok(A.pcm[Math.round(2.2 * 24000)] === 0, "la pause est silencieuse");
const F = fusionner([{ pages: [0, 1], cal: { pages: [0, 1.2], mots: [[0.1, 0.5], [1.4, 1.8]] } }, { pages: [2], cal: { pages: [0], mots: [[0.15, 0.6]] } }], [0, 2.45], 3);
ok(JSON.stringify(F) === JSON.stringify({ pages: [0, 1.2, 2.45], mots: [[0.1, 0.5], [1.4, 1.8], [2.6, 3.05]] }), "minutage décalé de chaque morceau : " + JSON.stringify(F));

console.log("mots en trop et minutage incohérent");
const pages = ["Le petit lapin saute dans l'herbe mouillée du matin.", "Il trouve une grosse carotte orange près du ruisseau."];
const dire = (mots, t0 = 0, pas = 0.35) => mots.map((w, i) => ({ word: w, start: t0 + i * pas, end: t0 + i * pas + 0.3 }));
const juste = dire(pages.join(" ").split(" "));
let a = alignerMots(pages, juste), b = bilan(pages, a, juste.length * 0.35 + 0.3);
ok(a.qualite > 0.99 && !a.intrus.length && !b.grave.length && !b.leger.length, "lecture juste : aucun reproche (" + JSON.stringify(b) + ")");
const fantome = dire([...pages[0].split(" "), "Alors", "écoute", "bien", ...pages[1].split(" ")]);
a = alignerMots(pages, fantome); b = bilan(pages, a, fantome.length * 0.35 + 0.3);
ok(a.intrus.length === 3 && a.intrus.every(x => x.debutPage) && b.grave.length, "phrase inventée en début de page 2 : grave (" + b.grave.join(" | ") + ")");
const tete = dire(["Bonjour", "les", "enfants", ...pages.join(" ").split(" ")]);
b = bilan(pages, alignerMots(pages, tete), tete.length * 0.35 + 0.3);
ok(b.grave.some(x => /début de page/.test(x)), "mots inventés avant la 1re page : grave");
const hallu = dire([...pages.join(" ").split(" "), "Sous-titres", "réalisés", "par", "Amara.org"]);
b = bilan(pages, alignerMots(pages, hallu), hallu.length * 0.35 + 0.3);
ok(!b.grave.length, "« Sous-titres réalisés par Amara.org » en fin de son (invention de la reconnaissance) : ignoré");
const autre = dire([...pages[0].split(" "), "Puis", "il", "rentre", "vite", "chez", "lui", "en", "chantant", "très", "fort", ...pages[1].split(" ").slice(4)]);
b = bilan(pages, alignerMots(pages, autre), autre.length * 0.35 + 0.3);
ok(b.grave.length > 0, "page 2 qui commence par autre chose que son texte : grave (" + b.grave.join(" | ") + ")");
const lent = [...dire(pages[0].split(" ")), ...dire(pages[1].split(" "), 30)];           // 27 s de « vide » au milieu : une page beaucoup trop longue
b = bilan(pages, alignerMots(pages, lent), 34);
ok(b.grave.some(x => /durée anormale/.test(x)), "page d'une durée anormale : grave (" + b.grave.join(" | ") + ")");
ok(bilan(pages, null, 8).grave.length === 1 && !bilan([pages[0]], null, 4).grave.length, "reconnaissance en panne : refusée sur plusieurs pages, acceptée sur une seule (début de page exact)");

console.log("forme des histoires par âge");
let nm = 0; const mot = () => "mot" + (nm++).toString(26).replace(/\d/g, d => "qrstuvwxyz"[d]);       // des mots tous différents
const hist = (tab, ppt, mots = 10) => ({ tableaux: Array.from({ length: tab }, () => ({ pages: Array.from({ length: ppt }, () => Array.from({ length: mots }, mot).join(" ") + ".") })) });
const J = (h, age) => jugerHistoire(h, age);
ok(!J(hist(6, 2, 9), "petit").maigre, "1-3 ans, 6 × 2 pages de 9 mots : retenue");
ok(!J(hist(5, 2, 9), "petit").maigre && J(hist(4, 2, 9), "petit").maigre, "1-3 ans : 10 pages acceptées (≥ 75 % de 12), 8 refusées");
ok(J(hist(8, 3, 9), "petit").maigre, "1-3 ans en 8 × 3 pages (24 > 1,5 × 12) : trop long, mis de côté");
ok(J(hist(6, 2, 4), "petit").maigre, "1-3 ans, pages de 4 mots : trop maigres");
ok(!J(hist(7, 3, 20), "moyen").maigre && J(hist(5, 3, 20), "moyen").maigre, "3-6 ans : 21 pages retenues, 15 refusées (< 16)");
ok(!J(hist(7, 3, 30), "grand").maigre && !J(hist(6, 3, 30), "grand").maigre, "6-8 ans : 21 et 18 pages retenues");
ok(!J(hist(8, 3, 40), "tresgrand").maigre && J(hist(5, 3, 40), "tresgrand").maigre, "8-10 ans : 24 pages retenues, 15 refusées (< 18)");
const cp = consigneHistoire("un lapin", "la forêt", "le partage", "petit"), cm = consigneHistoire("", "", "", "moyen"), ct = consigneHistoire("", "", "", "tresgrand");
ok(/EXACTEMENT 6 tableaux de 2 pages/.test(cp) && /pendant ses deux pages/.test(cp) && /"pages":\["\.\.\.","\.\.\."\]/.test(cp) && /8 à 16 mots/.test(cp), "consigne 1-3 ans : 6 × 2, « deux pages », exemple JSON à 2 pages");
ok(/EXACTEMENT 7 tableaux de 3 pages/.test(cm) && /pendant ses trois pages/.test(cm), "consigne 3-6 ans : 7 × 3");
ok(/EXACTEMENT 8 tableaux de 3 pages/.test(ct) && /"pages":\["\.\.\.","\.\.\.","\.\.\."\]/.test(ct), "consigne 8-10 ans : 8 × 3 (inchangée)");

console.log("voixConteuse, réseau simulé");
// Voix simulée : un son de 0,05 s par caractère, dont la valeur (constante) désigne l'appel ; la reconnaissance simulée lit cette valeur et rend les mots.
const appels = []; let regle = () => ({});
globalThis.fetch = async (url, o) => {
  const b = JSON.parse(o.body), texte = b.contents[0].parts[0].text.split("#### TRANSCRIPT\n")[1], graine = b.generationConfig.seed, id = appels.length;
  const r = regle(texte, graine, id); appels.push({ texte, graine, r });
  if (r.jour) return new Response('{"error":{"message":"Quota exceeded GenerateRequestsPerDay"}}', { status: 429 });
  const pcm = new Int16Array(Math.round(texte.length * 0.05 * 24000)).fill(1000 + 10 * id), u = new Uint8Array(pcm.buffer);
  return new Response(`{"candidates":[{"content":{"parts":[{"inlineData":{"mimeType":"audio/L16;codec=pcm;rate=24000","data":"${Buffer.from(u).toString("base64")}"}}]}}]}`);
};
const env = { AI: { run: async (modele, x) => {
  const s = pcmDepuis(octets(x.audio), "audio/wav"), id = Math.round((s.pcm[0] - 1000) / 10), ap = appels[id], dur = s.pcm.length / s.rate;
  const mots = [...(ap.r.avant || []), ...ap.texte.split(/\s+/).filter(Boolean)]; if (ap.r.milieu) mots.splice(5, 0, ap.r.milieu);
  return { words: mots.map((w, i) => ({ word: w, start: dur * i / mots.length, end: dur * (i + 0.8) / mots.length })) };
} } };
const tb = [["Pompon le lapin bleu saute dans le jardin du matin.", "Il cherche sa carotte orange partout, sous les feuilles."],
            ["Sa copine la grenouille Zélie arrive en faisant hop hop.", "Elles cherchent ensemble derrière le grand arrosoir vert."]];
const lisse = t => t.replace(/\s+/g, " ").trim();
let out = await voixConteuse(env, "cle", [tb[0]], "Sulafat");
ok(!out.error && out.meta.appels === 1 && out.meta.morceaux === 1 && out.meta.calage === "reconnaissance", "tableau des 1-3 ans : un appel, calé par la reconnaissance (" + JSON.stringify({ appels: out.meta.appels, calage: out.meta.calage }) + ")");
ok(out.meta.mots.length === 2 && out.meta.mots[1][0] > out.meta.mots[0].at(-1), "minutage : 2 pages, la 2e après la 1re");
appels.length = 0; regle = (t, g) => /grenouille/.test(t) && g === 7 && !/Pompon/.test(t) ? { avant: ["Alors", "écoute", "bien"] } : {};
out = await voixConteuse({ ...env, VOIX_MAX_CAR: "150" }, "cle", tb, "Sulafat");
ok(!out.error && out.meta.morceaux === 2 && out.meta.refaits === 1 && out.meta.appels === 4, "phrase inventée dans le 2e morceau : relu page par page (4 appels : " + appels.map(a => a.graine + ":" + lisse(a.texte).slice(0, 18)).join(" | ") + ")");
const deb = out.meta.mots.map(w => w[0]);
ok(out.meta.mots.length === 4 && deb.every((t, k) => !k || t > deb[k - 1]) && out.meta.pages[2] > out.meta.pages[1], "minutage de l'ensemble croissant, décalé morceau par morceau : " + deb.join(", "));
ok(Math.abs(out.pcm.length / out.rate - out.meta.duree) < 0.02, "durée cohérente avec le son : " + out.meta.duree + " s");
appels.length = 0; regle = t => ({ avant: ["Il", "était", "une", "fois"] });
out = await voixConteuse(env, "cle", [tb[0]], "Sulafat");
ok(out.error === "voix mal calée" && out.refus && !out.pcm, "toujours faux après relecture : refusé, pas de son (" + out.detail + ")");
appels.length = 0; regle = (t, g, id) => id >= 1 ? { jour: true } : {};
out = await voixConteuse({ ...env, VOIX_MAX_CAR: "150" }, "cle", tb, "Sulafat");
ok(out.error && out.quota && !out.pcm, "quota du jour atteint au 2e morceau : erreur propre, aucune piste à moitié (" + out.error + ")");
appels.length = 0; regle = (t, g) => g === 11 ? { jour: true } : (/Pompon/.test(t) ? { milieu: "euh" } : {});
out = await voixConteuse(env, "cle", [["Pompon le lapin bleu saute dans le jardin, il saute très haut, puis il se repose un peu au soleil."]], "Sulafat");
ok(!out.error && out.quota && out.pcm, "quota atteint pendant une relecture d'un morceau acceptable : on garde la 1re lecture et on note le quota");

console.log(ko ? `${ko} ÉCHEC(S)` : "tout est bon");
process.exitCode = ko ? 1 : 0;
