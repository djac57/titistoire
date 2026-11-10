/**
 * titistoire — Cloudflare Worker (voix + images, via Workers AI, gratuit).
 * Nécessite un binding "AI" (Workers AI) — voir DEPLOY ci-dessous.
 *   /tts?t=<texte>&lang=fr   -> audio MP3 (voix neuronale melotts)
 *   /img?p=<prompt>          -> image JPEG (illustration flux-1-schnell)
 * CORS ouvert (usage perso). Les réponses sont mises en cache (edge) via Cache-Control.
 *
 * DÉPLOIEMENT :
 *  1. Cloudflare → Workers & Pages → Create → Start with Hello World → nom "titistoire-ai" → Deploy
 *  2. Edit code → coller ce fichier → Deploy
 *  3. ⚙️ Settings → Bindings → + Add → "Workers AI" → Variable name: AI → Save
 *     (c'est ce binding qui donne accès à env.AI, sans token dans le code)
 *  URL finale : https://titistoire-ai.<ton-sous-domaine>.workers.dev
 */
export default {
  async fetch(req, env) {
    const u = new URL(req.url);
    const cors = { "access-control-allow-origin": "*" };
    try {
      if (u.pathname.startsWith("/tts")) {
        const t = (u.searchParams.get("t") || "").slice(0, 900);
        if (!t) return new Response("manque ?t=", { status: 400, headers: cors });
        // 1) ElevenLabs si la clé secrète ELEVEN_KEY est définie (voix premium)
        if (env.ELEVEN_KEY) {
          const voice = u.searchParams.get("v") || env.ELEVEN_VOICE || "21m00Tcm4TlvDq8ikWAM";
          const r = await fetch("https://api.elevenlabs.io/v1/text-to-speech/" + voice + "?output_format=mp3_44100_128", {
            method: "POST",
            headers: { "xi-api-key": env.ELEVEN_KEY, "content-type": "application/json" },
            body: JSON.stringify({ text: t, model_id: "eleven_multilingual_v2",
              voice_settings: { stability: 0.45, similarity_boost: 0.8, style: 0.15 } })
          });
          if (r.ok) return new Response(r.body, { headers: { "content-type": "audio/mpeg", "cache-control": "public, max-age=31536000", ...cors } });
          // sinon : on bascule sur melotts (quota ElevenLabs dépassé, etc.)
        }
        // 2) melotts (gratuit, secours)
        const lang = u.searchParams.get("lang") || "fr";
        const m = await env.AI.run("@cf/myshell-ai/melotts", { prompt: t, lang });
        return audio(b64(m.audio), cors);
      }
      if (u.pathname.startsWith("/img")) {
        const p = (u.searchParams.get("p") || "").slice(0, 1500);
        if (!p) return new Response("manque ?p=", { status: 400, headers: cors });
        const r = await env.AI.run("@cf/black-forest-labs/flux-1-schnell", { prompt: p, steps: 8 });
        return img(b64(r.image), cors);
      }
      return new Response("titistoire-ai OK — routes: /tts?t=..&lang=fr , /img?p=..", { headers: cors });
    } catch (e) {
      return new Response("Erreur AI: " + String(e), { status: 502, headers: cors });
    }
  }
};
function b64(s) { return Uint8Array.from(atob(s), c => c.charCodeAt(0)); }
function audio(bytes, cors) { return new Response(bytes, { headers: { "content-type": "audio/mpeg", "cache-control": "public, max-age=31536000", ...cors } }); }
function img(bytes, cors) { return new Response(bytes, { headers: { "content-type": "image/jpeg", "cache-control": "public, max-age=31536000", ...cors } }); }
