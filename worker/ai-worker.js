/**
 * titistoire — Cloudflare Worker (voix + images + histoires mode libre). [auto-deploy actif]
 * Routes :
 *   /tts?t=<texte>&lang=fr            -> audio MP3 (ElevenLabs si ELEVEN_KEY, sinon melotts)
 *   /img?p=<prompt>&seed=<n>&steps=<n>-> image JPEG (flux-1-schnell via binding AI)
 *   /story?hero=&lieu=&lecon=         -> JSON histoire enfant (Gemini via GEMINI_KEY ; AUCUNE clé côté navigateur)
 * CORS ouvert (usage perso). Réponses mises en cache (edge) via Cache-Control.
 *
 * CONFIG DASHBOARD (Workers & Pages → titistoire-ai → Settings) :
 *   • Bindings → + Add → "Workers AI" → Variable name: AI      (indispensable pour /img et melotts)
 *   • Variables and Secrets → ELEVEN_KEY   = <clé ElevenLabs>   (voix naturelle)
 *   • Variables and Secrets → ELEVEN_VOICE = <id voix>          (optionnel, sinon voix par défaut)
 *   • Variables and Secrets → GEMINI_KEY   = <clé Google Gemini>(mode libre sans clé navigateur)
 */
export default {
  async fetch(req, env) {
    const u = new URL(req.url);
    const cors = {
      "access-control-allow-origin": "*",
      "access-control-allow-methods": "GET,POST,OPTIONS",
      "access-control-allow-headers": "content-type",
    };
    if (req.method === "OPTIONS") return new Response(null, { headers: cors });
    try {
      // ---------- VOIX ----------
      if (u.pathname.startsWith("/tts")) {
        const t = (u.searchParams.get("t") || "").slice(0, 900);
        if (!t) return new Response("manque ?t=", { status: 400, headers: cors });
        // 1) ElevenLabs (voix naturelle) si la clé secrète est définie
        const ELEVEN = env.ELEVEN_KEY || env.ELEVENLABS_KEY;
        if (!ELEVEN && u.searchParams.get("debug")) return new Response("Aucune clé ELEVEN_KEY (ni ELEVENLABS_KEY) lue par le worker", { status: 200, headers: { "content-type": "text/plain", ...cors } });
        if (ELEVEN) {
          // voix "premade" accessibles en palier GRATUIT (les voix "library" exigent un plan payant) :
          //   Matilda XrExE9yKIg1WjnnlVkGX · Lily pFZP5JQG7iQjIQuC4Bku · Sarah EXAVITQu4vr4xnSDxMaL
          //   Alice Xb7hH8MSUJpSbSDYk0k2 · Laura FGY2WhTYpPnrIDTdsKH5
          const voice = u.searchParams.get("v") || env.ELEVEN_VOICE || "XrExE9yKIg1WjnnlVkGX";
          // "with-timestamps" : audio + alignement caractère→temps (pour un karaoké précis)
          const r = await fetch("https://api.elevenlabs.io/v1/text-to-speech/" + voice + "/with-timestamps?output_format=mp3_44100_128", {
            method: "POST",
            headers: { "xi-api-key": ELEVEN, "content-type": "application/json" },
            body: JSON.stringify({
              text: t, model_id: "eleven_multilingual_v2",
              voice_settings: { stability: 0.5, similarity_boost: 0.8, style: 0.1, use_speaker_boost: true }
            })
          });
          if (r.ok) {
            const j = await r.json();
            const out = { audio_base64: j.audio_base64, alignment: j.alignment || j.normalized_alignment || null };
            return new Response(JSON.stringify(out), { headers: { "content-type": "application/json", "cache-control": "public, max-age=31536000", ...cors } });
          }
          // échec ElevenLabs : si ?debug=1, on renvoie la raison au lieu de basculer en secours
          if (u.searchParams.get("debug")) {
            const msg = await r.text();
            return new Response("ElevenLabs HTTP " + r.status + " : " + msg.slice(0, 400), { status: 200, headers: { "content-type": "text/plain", ...cors } });
          }
          // quota dépassé / erreur -> on tente melotts si dispo
        }
        // 2) melotts (gratuit, secours) — nécessite le binding AI
        if (!env.AI) return new Response("TTS indisponible (ni ELEVEN_KEY ni binding AI)", { status: 502, headers: cors });
        const lang = u.searchParams.get("lang") || "fr";
        const m = await env.AI.run("@cf/myshell-ai/melotts", { prompt: t, lang });
        return audio(b64(m.audio), cors);
      }

      // ---------- IMAGE ----------
      if (u.pathname.startsWith("/img")) {
        const p = (u.searchParams.get("p") || "").slice(0, 1500);
        if (!p) return new Response("manque ?p=", { status: 400, headers: cors });
        if (!env.AI) return new Response("Image indisponible (binding AI manquant)", { status: 502, headers: cors });
        const steps = Math.max(1, Math.min(8, parseInt(u.searchParams.get("steps") || "8", 10) || 8));
        // NB: flux-1-schnell (Workers AI) n'accepte PAS de paramètre seed -> on ne le passe pas.
        const r = await env.AI.run("@cf/black-forest-labs/flux-1-schnell", { prompt: p, steps });
        return img(b64(r.image), cors);
      }

      // ---------- HISTOIRE (mode libre, sans clé navigateur) ----------
      if (u.pathname.startsWith("/story")) {
        const GKEY = env.GEMINI_KEY || env.GEMINI_API_KEY;
        if (!GKEY) return new Response(JSON.stringify({ error: "GEMINI_KEY manquante sur le worker (Cloudflare, pas GitHub)" }), { status: 502, headers: { "content-type": "application/json", ...cors } });
        const hero = (u.searchParams.get("hero") || "").slice(0, 200).trim();
        const lieu = (u.searchParams.get("lieu") || "").slice(0, 200).trim();
        const lecon = (u.searchParams.get("lecon") || "").slice(0, 200).trim();
        // On essaie plusieurs modèles dans l'ordre : le 1er qui répond gagne.
        // Ainsi, si un modèle est saturé (503) ou retiré (404), on bascule tout seul.
        const forced = u.searchParams.get("model");
        // modèles VALIDES uniquement (2.5/2.0 sont retirés pour les nouveaux comptes) ; le 1er qui répond gagne
        const models = forced ? [forced]
          : (env.GEMINI_MODEL ? [env.GEMINI_MODEL]
            : ["gemini-flash-latest", "gemini-3.8-flash", "gemini-flash-lite-latest"]);
        const prompt = `Tu es une conteuse pour enfants de 3 à 6 ans. Invente une vraie petite histoire en FRANÇAIS, douce, rassurante, à la fin heureuse. `
          + `Héros : ${hero || "un petit personnage attachant"}. Lieu : ${lieu || "un endroit magique"}. Leçon : ${lecon || "la gentillesse"}. `
          + `Structure-la comme un album jeunesse (schéma narratif) : incipit (on présente le héros et son petit monde), un élément perturbateur, une rencontre qui aide (un adjuvant), des péripéties, une résolution où le héros met en pratique la leçon, puis une conclusion heureuse. `
          + `Entre 18 et 22 pages. UNE à DEUX phrases courtes et simples par page. La TOUTE DERNIÈRE page est la morale et commence EXACTEMENT par "La morale de l'histoire :". `
          + `Réponds UNIQUEMENT en JSON : {"titre":"...","decor":"foret|ocean|espace|chevaliers|pirates|dino","emoji":"un seul emoji","pages":["...", "...", "..."]}`;
        async function askGemini(model){
          const ctrl = new AbortController(); const to = setTimeout(() => ctrl.abort(), 12000); // échoue vite si ça rame
          try {
            const gr = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${encodeURIComponent(GKEY)}`, {
              method: "POST", headers: { "content-type": "application/json" }, signal: ctrl.signal,
              body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }], generationConfig: { temperature: 0.95, responseMimeType: "application/json" } })
            });
            const gd = await gr.json();
            const t = gd && gd.candidates && gd.candidates[0] && gd.candidates[0].content
              && gd.candidates[0].content.parts && gd.candidates[0].content.parts[0] && gd.candidates[0].content.parts[0].text;
            if (t) return { txt: t };
            const msg = (gd && gd.error && gd.error.message) || "réponse vide";
            return { err: msg, busy: /high demand|overloaded|unavailable|503|429|quota|rate/i.test(msg) };
          } catch (e) { return { err: String(e), busy: true }; } finally { clearTimeout(to); }
        }
        let txt = null, lastErr = null, usedModel = null, busy = false;
        for (const model of models) {
          const res = await askGemini(model);
          if (res.txt) { txt = res.txt; usedModel = model; break; }
          lastErr = res.err; if (res.busy) busy = true;
        }
        if (!txt) return new Response(JSON.stringify({ error: "Gemini indisponible", busy, detail: lastErr, tried: models }), { status: 502, headers: { "content-type": "application/json", ...cors } });
        if (u.searchParams.get("debug")) return new Response(JSON.stringify({ usedModel, txt }), { headers: { "content-type": "application/json", ...cors } });
        // on renvoie tel quel le JSON du modèle (le navigateur le parse)
        return new Response(txt, { headers: { "content-type": "application/json", "cache-control": "no-store", ...cors } });
      }

      return new Response("titistoire-ai OK — routes: /tts?t=..&lang=fr , /img?p=..&seed=.. , /story?hero=..&lieu=..&lecon=..", { headers: cors });
    } catch (e) {
      return new Response("Erreur AI: " + String(e), { status: 502, headers: cors });
    }
  }
};
function b64(s) { return Uint8Array.from(atob(s), c => c.charCodeAt(0)); }
function audio(bytes, cors) { return new Response(bytes, { headers: { "content-type": "audio/wav", "cache-control": "public, max-age=31536000", ...cors } }); }
function img(bytes, cors) { return new Response(bytes, { headers: { "content-type": "image/jpeg", "cache-control": "public, max-age=31536000", ...cors } }); }
