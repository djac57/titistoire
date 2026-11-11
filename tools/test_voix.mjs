// Tests hors ligne de worker/voix.js contre le minutage exact d'histoires enregistrées.
//   node tools/test_voix.mjs <dossier : <id>.pcm (16 bits mono 24 kHz), <id>.json {pages, truth}, <id>.heard.json [{word,start,end}]>
import fs from "node:fs"; import path from "node:path";
import { alignerMots, caler, wav, pcmDepuis, reech, tranches, base64, octets } from "../worker/voix.js";
const dir = process.argv[2], med = a => a.slice().sort((p, q) => p - q)[a.length >> 1], p90 = a => a.slice().sort((p, q) => p - q)[Math.floor(a.length * 0.9)];
for (const f of fs.readdirSync(dir).filter(f => f.endsWith(".heard.json"))) {
  const id = f.replace(".heard.json", ""), { pages, truth } = JSON.parse(fs.readFileSync(path.join(dir, id + ".json")));
  const b = fs.readFileSync(path.join(dir, id + ".pcm")), pcm = new Int16Array(b.buffer, b.byteOffset, b.length >> 1);
  const err = r => { const ep = pages.map((_, k) => Math.abs(r.mots[k][0] - truth[k][0])), em = []; truth.forEach((ws, k) => ws.forEach((t, i) => em.push(Math.abs(r.mots[k][i] - t))));
    return `pages médiane ${med(ep).toFixed(2)} s, max ${Math.max(...ep).toFixed(2)} s | mots médiane ${med(em).toFixed(2)} s, 90 % ${p90(em).toFixed(2)} s`; };
  const t0 = Date.now(), a = alignerMots(pages, JSON.parse(fs.readFileSync(path.join(dir, f))));
  console.log(id, "\n  reconnaissance vocale :", err(a), "| qualité", a.qualite.toFixed(3), `(${Date.now() - t0} ms)`);
  const x = new Float32Array(pcm.length); for (let i = 0; i < x.length; i++) x[i] = pcm[i] / 32768;
  console.log("  secours (silences)    :", err(caler(x, 24000, pages)));
  // aller-retour WAV / base64 / tranches
  const w = wav(pcm, 24000), back = pcmDepuis(octets(base64(w)), "audio/wav"), tr = tranches(reech(pcm, 24000, 16000), 16000, 45);
  console.log("  WAV aller-retour :", back.rate === 24000 && back.pcm.length === pcm.length && back.pcm[12345] === pcm[12345] ? "ok" : "ÉCHEC",
              "| tranches :", tr.map(t => (t.pcm.length / 16000).toFixed(0) + " s").join(", "));
}
