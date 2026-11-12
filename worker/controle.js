/* Contrôles sans réseau du mode « J'invente la mienne » : mots interdits et mise en forme de l'histoire.
   Fonctions pures, testées par tools/test_controle.mjs. */
export const DECORS = ["foret", "ocean", "espace", "chevaliers", "pirates", "dino", "noel", "halloween", "ski", "mer"];

// Mots qui n'ont rien à faire dans une histoire pour tout-petits (les cas plus subtils sont laissés aux deux juges).
const INTERDITS_FR = /(^|[^a-zà-ÿ])(tuer|tu[ée]e?s?|tuent|tua|meurtres?|meurtri[eè]re?s?|assassin[a-zà-ÿ]*|morts?|morte?s?|mourir|meurt|mourut|cadavres?|sang|sanglante?s?|saign[a-zà-ÿ]*|armes?|fusils?|pistolets?|revolvers?|mitraill[a-zà-ÿ]*|poignard[a-zà-ÿ]*|bombes?|guerres?|soldats?|tortur[a-zà-ÿ]*|viol|viols|viol[ée]e?s?|violeur[a-zà-ÿ]*|sexe|sexuel[a-zà-ÿ]*|sexy|nudit[ée]|toute? nue?|p[ée]nis|vagin[a-zà-ÿ]*|drogu[a-zà-ÿ]*|coca[ïi]ne|h[ée]ro[ïi]ne|cannabis|alcool[a-zà-ÿ]*|ivre|ivres|bi[èe]res?|whisky|vodka|cigarettes?|suicid[a-zà-ÿ]*|pendus?|[ée]gorg[a-zà-ÿ]*|d[ée]capit[a-zà-ÿ]*|d[ée]mons?|diable|satan[a-zà-ÿ]*|zombies?|vampires?|horreur|terroris[a-zà-ÿ]*|nazis?|hitler|racis[a-zà-ÿ]*|merde|putain|connard[a-zà-ÿ]*|salope[a-zà-ÿ]*|encul[a-zà-ÿ]*|kidnapp[a-zà-ÿ]*)(?![a-zà-ÿ])/i;
const INTERDITS_EN = /(?<![a-zà-ÿ])(kill\w*|murder\w*|dead|death|die[sd]?|dying|corpse\w*|blood\w*|bleed\w*|gore|gory|gun\w*|rifle\w*|pistol\w*|knife|knives|weapon\w*|bombs?|bombed|bombing|bomber\w*|war|soldier\w*|tortur\w*|raped?|raping|rapist\w*|sex\w*|naked|nude|nudity|breasts?|penis|vagina|drug\w*|cocaine|alcohol\w*|drunk|beer|whisky|whiskey|vodka|cigarette\w*|suicid\w*|hanged|demon\w*|devil|satan\w*|zombie\w*|vampire\w*|horror|terrif\w+|nazi\w*|hitler|creepy|skull\w*|skeleton\w*|wounded|wounds|injur\w*)(?![a-zà-ÿ])/i;

// expressions innocentes de la nature, qu'il ne faut pas prendre pour des mots interdits
const INNOCENTS = /feuilles? mortes?|branches? mortes?|bois mort|arbres? morts?|dead (leaves|leaf|trees?|branch(es)?|wood|grass)|morte? de (rire|fatigue|faim|froid)|morts? de (rire|fatigue|faim|froid)|à tue-tête|bomb(e|ant|ait|é|ée|ées|és|er) le torse|torse bombé|s'(est|était|étaient|sont|étant) tue?s?(?![a-zà-ÿ])|se sont tue?s(?![a-zà-ÿ])/gi;
export function motInterdit(texte) {
  texte = String(texte || "").replace(INNOCENTS, " ");
  const mf = INTERDITS_FR.exec(texte); if (mf) return mf[2];
  const me = INTERDITS_EN.exec(texte); return me ? me[0] : null;
}

/** Met l'histoire au format { titre, decor, emoji, heros, ami, tableaux:[{image, pages}] } ou renvoie null. */
export function normaliser(txt) {
  let o; try { o = JSON.parse(txt); } catch (e) { return null; }
  if (!o || typeof o !== "object") return null;
  const chaine = (x, n) => String(x == null ? "" : x).replace(/\s+/g, " ").trim().slice(0, n);
  const moral = /\bla morale\b|la le[çc]on (de|à retenir)|cette (petite |belle )?histoire (nous )?(montre|apprend|enseigne|rappelle)|retiens bien que|il faut (toujours )?(se rappeler|retenir)/i;
  let tb = Array.isArray(o.tableaux) ? o.tableaux.map(t => {
    const images = (Array.isArray(t && t.images) ? t.images : [t && t.image]).map(x => chaine(x, 400)).filter(Boolean);   // "image" unique accepté aussi
    return { images, image: images[0] || "", pages: (Array.isArray(t && t.pages) ? t.pages : []).map(p => chaine(p, 700)).filter(p => p && !moral.test(p)) };
  }) : [];
  if (!tb.length && Array.isArray(o.pages)) {                 // ancien format : pages à plat -> tableaux de 3 pages, sans image
    const pg = o.pages.map(p => chaine(p, 700)).filter(p => p && !moral.test(p));
    for (let i = 0; i < pg.length; i += 3) tb.push({ image: "", images: [], pages: pg.slice(i, i + 3) });
  }
  tb = tb.filter(t => t.pages.length).slice(0, 10);
  if (tb.length < 4 || tb.reduce((a, t) => a + t.pages.length, 0) < 9) return null;
  return { titre: chaine(o.titre, 90) || "Mon histoire", decor: DECORS.includes(o.decor) ? o.decor : "foret",
           emoji: [...chaine(o.emoji, 8)][0] || "🧒", heros: chaine(o.heros, 220), ami: chaine(o.ami, 220), lieu: chaine(o.lieu, 160), tableaux: tb };
}
