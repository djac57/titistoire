/* Outils audio du worker pour les histoires inventées : décodage du son rendu par Gemini TTS,
   découpage pour la reconnaissance vocale, et calage mot à mot du texte sur la voix.
   Fonctions pures (aucun accès réseau) : testées hors ligne par tools/test_voix.mjs. */

/** base64 -> octets (sans passer par une chaîne binaire géante quand le moteur le permet) */
export function octets(b64) {
  if (typeof Uint8Array.fromBase64 === "function") return Uint8Array.fromBase64(b64);
  const s = atob(b64), n = s.length, u = new Uint8Array(n);
  for (let i = 0; i < n; i++) u[i] = s.charCodeAt(i);
  return u;
}
export function base64(u8) {
  if (typeof u8.toBase64 === "function") return u8.toBase64();
  let s = ""; for (let i = 0; i < u8.length; i += 32768) s += String.fromCharCode.apply(null, u8.subarray(i, i + 32768));
  return btoa(s);
}
/** Son renvoyé par Gemini (WAV ou PCM brut 16 bits) -> { pcm: Int16Array, rate } */
export function pcmDepuis(u8, mime) {
  let off = 0, len = u8.length, rate = 24000;
  const m = /rate=(\d+)/.exec(mime || ""); if (m) rate = +m[1];
  if (u8[0] === 0x52 && u8[1] === 0x49 && u8[2] === 0x46 && u8[3] === 0x46) {       // "RIFF"
    const dv = new DataView(u8.buffer, u8.byteOffset, u8.byteLength); let p = 12;
    while (p + 8 <= u8.length) {
      const id = String.fromCharCode(u8[p], u8[p + 1], u8[p + 2], u8[p + 3]), sz = dv.getUint32(p + 4, true);
      if (id === "fmt ") rate = dv.getUint32(p + 12, true);
      if (id === "data") { off = p + 8; len = Math.min(sz, u8.length - off); break; }
      p += 8 + sz + (sz & 1);
    }
  }
  len -= len & 1;
  const copie = u8.slice(off, off + len);                       // aligné sur 2 octets
  return { pcm: new Int16Array(copie.buffer, 0, len >> 1), rate };
}
/** En-tête WAV + données, mono 16 bits */
export function wav(pcm, rate) {
  const n = pcm.length * 2, u = new Uint8Array(44 + n), dv = new DataView(u.buffer);
  const txt = (o, s) => { for (let i = 0; i < s.length; i++) u[o + i] = s.charCodeAt(i); };
  txt(0, "RIFF"); dv.setUint32(4, 36 + n, true); txt(8, "WAVEfmt "); dv.setUint32(16, 16, true); dv.setUint16(20, 1, true); dv.setUint16(22, 1, true);
  dv.setUint32(24, rate, true); dv.setUint32(28, rate * 2, true); dv.setUint16(32, 2, true); dv.setUint16(34, 16, true); txt(36, "data"); dv.setUint32(40, n, true);
  u.set(new Uint8Array(pcm.buffer, pcm.byteOffset, n), 44);
  return u;
}
/** Rééchantillonnage linéaire (la reconnaissance vocale travaille en 16 kHz) */
export function reech(pcm, de, vers) {
  if (de === vers) return pcm;
  const n = Math.floor(pcm.length * vers / de), out = new Int16Array(n), r = de / vers;
  for (let i = 0; i < n; i++) { const x = i * r, a = Math.floor(x), f = x - a; out[i] = pcm[a] + ((pcm[a + 1] ?? pcm[a]) - pcm[a]) * f; }
  return out;
}
/** Tranches d'au plus `max` secondes, coupées à l'endroit le plus calme des dernières secondes */
export function tranches(pcm, rate, max = 45) {
  const out = [], pas = Math.round(rate * 0.02); let d = 0;
  while (d < pcm.length) {
    let f = Math.min(pcm.length, d + max * rate);
    if (f < pcm.length) {
      let best = f, bv = Infinity;
      for (let i = f - 10 * rate; i + pas <= f; i += pas) { let s = 0; for (let j = i; j < i + pas; j++) s += pcm[j] * pcm[j]; if (s <= bv) { bv = s; best = i + (pas >> 1); } }
      f = best;
    }
    out.push({ debut: d / rate, pcm: pcm.subarray(d, f) }); d = f;
  }
  return out;
}

const norme = s => s.normalize("NFD").toLowerCase().replace(/[^0-9a-z]/g, "");

/** Calage exact : texte attendu (pages) contre mots entendus [{word,start,end}] (ordre chronologique).
    -> { mots:[[débuts par page]], pages:[débuts], qualite: part du texte retrouvée } */
export function alignerMots(pages, entendus) {
  const jetons = []; pages.forEach((p, pi) => p.split(/\s+/).filter(Boolean).forEach(t => jetons.push([pi, t])));
  const tc = [], tw = []; jetons.forEach(([, t], wi) => { for (const ch of norme(t)) { tc.push(ch); tw.push(wi); } });
  const hc = [], ht = [];
  for (const w of entendus) { const n = norme(String(w.word || "")); for (let i = 0; i < n.length; i++) { hc.push(n[i]); ht.push(w.start + (w.end - w.start) * i / n.length); } }
  const n = tc.length, m = hc.length, debut = new Array(jetons.length).fill(null);
  let ok = 0;
  if (n && m) {
    // plus longue sous-séquence commune, caractère par caractère
    const W = m + 1, L = new Uint16Array((n + 1) * W);
    for (let i = 1; i <= n; i++) { const a = tc[i - 1], r = i * W, q = r - W; for (let j = 1; j <= m; j++) L[r + j] = a === hc[j - 1] ? L[q + j - 1] + 1 : (L[q + j] >= L[r + j - 1] ? L[q + j] : L[r + j - 1]); }
    for (let i = n, j = m; i > 0 && j > 0;) {
      if (tc[i - 1] === hc[j - 1] && L[i * W + j] === L[(i - 1) * W + j - 1] + 1) { ok++; debut[tw[i - 1]] = ht[j - 1]; i--; j--; }   // en remontant, on finit sur le 1er caractère du mot
      else if (L[(i - 1) * W + j] >= L[i * W + j - 1]) i--; else j--;
    }
  }
  const connus = []; debut.forEach((t, i) => { if (t !== null) connus.push([i, t]); });
  if (!connus.length) return { mots: null, pages: null, qualite: 0 };
  let c = 0;
  for (let i = 0; i < debut.length; i++) {                      // mots sans repère : interpolation entre voisins
    while (c < connus.length && connus[c][0] < i) c++;
    if (debut[i] !== null) continue;
    const av = c > 0 ? connus[c - 1] : null, ap = c < connus.length ? connus[c] : null;
    debut[i] = av && ap ? av[1] + (ap[1] - av[1]) * (i - av[0]) / (ap[0] - av[0]) : ap ? Math.max(0, ap[1] - 0.05) : av[1] + 0.05;
  }
  for (let i = 1; i < debut.length; i++) if (debut[i] < debut[i - 1]) debut[i] = debut[i - 1];
  const mots = pages.map(() => []); jetons.forEach(([pi], i) => mots[pi].push(Math.round(debut[i] * 100) / 100));
  return { mots, pages: mots.map((w, k) => k === 0 ? 0 : Math.max(0, Math.round((w[0] - 0.18) * 100) / 100)), qualite: ok / (n || 1) };
}

/* Calage de SECOURS, sans reconnaissance vocale : on raisonne en « temps de parole » (silences retirés),
   chaque page durant en proportion de ses lettres, et on choisit par programmation dynamique les silences
   qui découpent le mieux. Mesuré sur deux histoires enregistrées : bon si le débit est régulier (médiane
   0,3 s), mauvais si la voix ralentit en cours de route. */
const lettres = m => m.replace(/[^0-9A-Za-zÀ-ÿ]/g, "").length;
export function caler(x, sr, pages) {
  const PAS = 0.02, pas = Math.round(sr * PAS), n = Math.floor(x.length / pas), rms = new Float32Array(n);
  for (let i = 0; i < n; i++) { let s = 0; for (let j = i * pas, e = j + pas; j < e; j++) s += x[j] * x[j]; rms[i] = Math.sqrt(s / pas); }
  const tri = Array.from(rms).sort((a, b) => a - b), seuil = (tri[Math.floor(n * 0.9)] || 1e-3) * 0.06;
  let deb = 0, fin = n - 1; while (deb < n && rms[deb] <= seuil) deb++; while (fin > deb && rms[fin] <= seuil) fin--;
  const cum = new Float32Array(n + 1); for (let i = 0; i < n; i++) cum[i + 1] = cum[i] + (i >= deb && i <= fin && rms[i] > seuil ? PAS : 0);
  const V = cum[n] || 1;
  const versReel = v => { let a = 0, b = n; while (a < b) { const m = (a + b) >> 1; if (cum[m + 1] <= v) a = m + 1; else b = m; } return a * PAS; };
  const sil = [];
  for (let i = deb, s = -1; i <= fin + 1; i++) {
    const calme = i <= fin && rms[i] <= seuil;
    if (calme && s < 0) s = i;
    if (!calme && s >= 0) { if (i - s >= 8) sil.push([s, i]); s = -1; }
  }
  const mots = pages.map(p => p.split(/\s+/).filter(Boolean)), L = mots.map(ms => ms.reduce((a, m) => a + lettres(m), 0) + 2);
  const Lt = L.reduce((a, b) => a + b, 0), E = L.map(l => V * l / Lt), K = pages.length, S = sil.length;
  let coupes = [];
  if (K > 1 && S >= K - 1) {
    const v = sil.map(([a]) => cum[a]), bonus = sil.map(([a, b]) => 0.35 * Math.min((b - a) * PAS, 1.5));
    const INF = 1e18, cout = Array.from({ length: K }, () => new Float64Array(S).fill(INF)), prec = Array.from({ length: K }, () => new Int32Array(S).fill(-1));
    const c = (d, e) => (d - e) * (d - e) / e;
    for (let j = 0; j < S; j++) cout[1][j] = c(v[j], E[0]) - bonus[j];
    for (let k = 2; k < K; k++) for (let j = k - 1; j < S; j++) {
      let best = INF, bi = -1;
      for (let i = k - 2; i < j; i++) { if (cout[k - 1][i] >= INF) continue; const cc = cout[k - 1][i] + c(v[j] - v[i], E[k - 1]); if (cc < best) { best = cc; bi = i; } }
      if (bi >= 0) { cout[k][j] = best - bonus[j]; prec[k][j] = bi; }
    }
    let bj = -1, bb = INF;
    for (let j = K - 2; j < S; j++) { const cc = cout[K - 1][j] + c(V - v[j], E[K - 1]); if (cc < bb) { bb = cc; bj = j; } }
    for (let k = K - 1, j = bj; k >= 1 && j >= 0; k--) { coupes.unshift(j); j = prec[k][j]; }
  }
  const debuts = [deb * PAS], vDeb = [0];
  if (coupes.length === K - 1) coupes.forEach(j => { debuts.push(Math.max(sil[j][0] * PAS, sil[j][1] * PAS - 0.12)); vDeb.push(cum[sil[j][0]]); });
  else { let a = 0; for (let k = 0; k < K - 1; k++) { a += E[k]; debuts.push(versReel(a)); vDeb.push(a); } }
  vDeb.push(V);
  const motsT = mots.map((ms, k) => { const w = ms.map(m => lettres(m) + 0.6), tot = w.reduce((a, b) => a + b, 0) || 1, d = vDeb[k + 1] - vDeb[k];
    let acc = 0; return ms.map((m, i) => { const t = i === 0 ? debuts[k] : Math.max(debuts[k], versReel(vDeb[k] + d * acc / tot)); acc += w[i]; return Math.round(t * 100) / 100; }); });
  return { pages: debuts.map(t => Math.round(t * 100) / 100), mots: motsT };
}
