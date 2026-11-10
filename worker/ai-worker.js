/**
 * titistoire — Cloudflare Worker (voix + images + histoires mode libre).
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
        if (ELEVEN) {
          const voice = u.searchParams.get("v") || env.ELEVEN_VOICE || "21m00Tcm4TlvDq8ikWAM";
          const r = await fetch("https://api.elevenlabs.io/v1/text-to-speech/" + voice + "?output_format=mp3_44100_128", {
            method: "POST",
            headers: { "xi-api-key": ELEVEN, "content-type": "application/json" },
            body: JSON.stringify({
              text: t, model_id: "eleven_multilingual_v2",
              voice_settings: { stability: 0.5, similarity_boost: 0.8, style: 0.1, use_speaker_boost: true }
            })
          });
          if (r.ok) return new Response(r.body, { headers: { "content-type": "audio/mpeg", "cache-control": "public, max-age=31536000", ...cors } });
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
        const model = "gemini-2.0-flash";
        const prompt = `Conteuse pour enfants de 3 à 6 ans. Invente une histoire en FRANÇAIS, douce, rassurante, à la fin heureuse. `
          + `Héros : ${hero || "un petit personnage attachant"}. Lieu : ${lieu || "un endroit magique"}. Leçon : ${lecon || "la gentillesse"}. `
          + `Exactement 7 pages, UNE phrase courte et simple par page, la dernière page est la morale et commence par "La morale de l'histoire :". `
          + `Réponds UNIQUEMENT en JSON : {"titre":"...","decor":"foret|ocean|espace|chevaliers|pirates|dino","emoji":"un seul emoji","pages":["...","...","...","...","...","...","..."]}`;
        const gr = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${encodeURIComponent(GKEY)}`, {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }], generationConfig: { temperature: 0.95, responseMimeType: "application/json" } })
        });
        const gd = await gr.json();
        const txt = gd && gd.candidates && gd.candidates[0] && gd.candidates[0].content
          && gd.candidates[0].content.parts && gd.candidates[0].content.parts[0] && gd.candidates[0].content.parts[0].text;
        if (!txt) return new Response(JSON.stringify({ error: "Gemini: réponse vide", raw: gd }), { status: 502, headers: { "content-type": "application/json", ...cors } });
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
