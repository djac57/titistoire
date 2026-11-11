// La liste de mots interdits ne doit bloquer aucune histoire du recueil, et doit arrêter les demandes déplacées.
import fs from "node:fs";
import { motInterdit, normaliser } from "../worker/controle.js";
const st = JSON.parse(fs.readFileSync(new URL("../stories.js", import.meta.url), "utf8").split("=").slice(1).join("=").trim().replace(/;$/, ""));
let faux = 0;
for (const [id, h] of Object.entries(st)) { const m = motInterdit(h.t + "\n" + h.sc.flat().join("\n")); if (m) { faux++; console.log("  faux positif", id, "->", m); } }
const src = ["filou", "nestor", "rosie", "plume", "saisons"].map(f => fs.readFileSync(new URL(`../histoires/${f}.txt`, import.meta.url), "utf8")).join("\n");
const desc = src.split("\n").filter(l => /^[@>]/.test(l));
let fauxImg = 0; for (const l of desc) { const m = motInterdit(l); if (m) { fauxImg++; if (fauxImg <= 12) console.log("  faux positif (image)", m, "|", l.slice(0, 70)); } }
console.log(`recueil : ${faux} histoire(s) bloquée(s) à tort sur ${Object.keys(st).length} ; descriptions d'images : ${fauxImg} sur ${desc.length}`);
const mauvais = ["un soldat qui fait la guerre", "un loup qui tue les moutons", "une histoire avec du sang", "un pirate avec un pistolet", "papa boit de la bière", "un zombie dans un cimetière", "la mort du grand-père", "une fille toute nue", "a fox with a gun", "un vampire", "Hitler", "il fume une cigarette"];
const bons = ["un petit lapin bleu nommé Pompon", "une forêt enchantée sous la pluie", "il faut être patient", "un dragon gentil qui a peur du noir", "un pirate qui cherche un trésor", "une sorcière rigolote", "un chevalier courageux et son épée en bois", "le chat de mamie est parti au ciel"];
console.log("demandes déplacées arrêtées :", mauvais.filter(motInterdit).length, "/", mauvais.length, mauvais.filter(x => !motInterdit(x)).length ? "| passées : " + mauvais.filter(x => !motInterdit(x)).join(" ; ") : "");
console.log("demandes normales laissées aux juges :", bons.filter(x => !motInterdit(x)).length, "/", bons.length, bons.filter(motInterdit).length ? "| bloquées : " + bons.filter(motInterdit).map(x => x + " (" + motInterdit(x) + ")").join(" ; ") : "");
const h = normaliser(JSON.stringify({ titre: "T", decor: "lune", emoji: "🐰🐻", heros: "a blue rabbit", ami: "a frog", tableaux: Array.from({ length: 8 }, (_, i) => ({ image: "HERO and FRIEND play", pages: ["a" + i, "La morale de l'histoire : sois sage.", "c"] })) }));
console.log("mise en forme :", h && h.tableaux.length === 8 && h.tableaux[0].pages.length === 2 && h.decor === "foret" && h.emoji === "🐰" ? "ok" : "ÉCHEC", "| ancien format :", normaliser(JSON.stringify({ titre: "x", pages: Array.from({ length: 12 }, (_, i) => "p" + i) }))?.tableaux.length, "tableaux", "| illisible :", normaliser("{}"));
