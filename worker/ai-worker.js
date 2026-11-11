/**
 * titistoire — Cloudflare Worker (voix + images + histoires mode libre). [auto-deploy actif · openrouter]
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
          const voice = u.searchParams.get("v") || env.ELEVEN_VOICE || "Xb7hH8MSUJpSbSDYk0k2"; // Alice par défaut
          // "with-timestamps" : audio + alignement caractère→temps (pour un karaoké précis)
          const r = await fetch("https://api.elevenlabs.io/v1/text-to-speech/" + voice + "/with-timestamps?output_format=mp3_44100_128", {
            method: "POST",
            headers: { "xi-api-key": ELEVEN, "content-type": "application/json" },
            body: JSON.stringify({
              text: t, model_id: "eleven_multilingual_v2",
              // stabilité plus basse + style plus haut = lecture plus vivante/expressive (moins plate)
              voice_settings: { stability: 0.38, similarity_boost: 0.85, style: 0.45, use_speaker_boost: true }
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

      // ---------- IMAGE via Gemini (quota SÉPARÉ de Cloudflare, pour le mode libre) ----------
      if (u.pathname.startsWith("/gimg")) {
        const p = (u.searchParams.get("p") || "").slice(0, 1500);
        if (!p) return new Response("manque ?p=", { status: 400, headers: cors });
        const GKEY = env.GEMINI_KEY || env.GEMINI_API_KEY;
        if (!GKEY) return new Response("GEMINI_KEY manquante", { status: 502, headers: cors });
        const models = ["gemini-2.5-flash-image", "gemini-2.0-flash-preview-image-generation"];
        let lastMsg = "échec";
        for (const model of models) {
          try {
            const gr = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${encodeURIComponent(GKEY)}`, {
              method: "POST", headers: { "content-type": "application/json" },
              body: JSON.stringify({ contents: [{ parts: [{ text: p }] }], generationConfig: { responseModalities: ["TEXT", "IMAGE"] } })
            });
            const d = await gr.json();
            const parts = (d && d.candidates && d.candidates[0] && d.candidates[0].content && d.candidates[0].content.parts) || [];
            const ip = parts.find(x => (x.inlineData && x.inlineData.data) || (x.inline_data && x.inline_data.data));
            if (ip) { const data = (ip.inlineData || ip.inline_data).data; return new Response(b64(data), { headers: { "content-type": "image/png", "cache-control": "public, max-age=31536000", ...cors } }); }
            lastMsg = (d && d.error && d.error.message) || "pas d'image";
            if (u.searchParams.get("debug")) return new Response("Gemini img [" + model + "] : " + lastMsg.slice(0, 300), { status: 200, headers: { "content-type": "text/plain", ...cors } });
          } catch (e) { lastMsg = String(e); }
        }
        return new Response("Gemini image indisponible : " + lastMsg.slice(0, 200), { status: 502, headers: cors });
      }

      // ---------- HISTOIRE (mode libre, sans clé navigateur) ----------
      if (u.pathname.startsWith("/story")) {
        const GKEY = env.GEMINI_KEY || env.GEMINI_API_KEY;
        if (u.searchParams.get("diag")) return new Response(JSON.stringify({ hasOpenRouter: !!env.OPENROUTER_KEY, hasGemini: !!GKEY, hasEleven: !!(env.ELEVEN_KEY||env.ELEVENLABS_KEY), hasAI: !!env.AI, locked: !!env.LIBRE_PASS }), { headers: { "content-type": "application/json", ...cors } });
        // Verrou du mode libre (réservé à l'user + ses amis) : actif seulement si LIBRE_PASS est défini
        if (env.LIBRE_PASS && u.searchParams.get("pass") !== env.LIBRE_PASS) return new Response(JSON.stringify({ error: "locked" }), { status: 403, headers: { "content-type": "application/json", ...cors } });
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
          + `Structure-la comme un album jeunesse : incipit (présente le héros et son petit monde), un élément perturbateur, une rencontre qui aide, des péripéties, une résolution où le héros met en pratique la leçon, et une conclusion heureuse. `
          + `Soigne le style : phrases vivantes et imagées, un peu de dialogue, du rythme, de la douceur et un brin d'humour. Entre 18 et 22 pages, UNE à DEUX phrases courtes et simples par page. `
          + `TRÈS IMPORTANT : n'énonce JAMAIS la morale explicitement (interdit : "la morale de l'histoire", "cette histoire montre que", "la leçon est"...). La leçon doit se ressentir à travers les actions. La dernière page est une jolie phrase de conclusion qui réchauffe le cœur, sans donner de leçon. `
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
        // Modèles OpenRouter GRATUITS (le 1er qui répond gagne ; les :free sont parfois rate-limited)
        const OR_MODELS = (env.OPENROUTER_MODEL ? [env.OPENROUTER_MODEL] : [
          "nvidia/nemotron-3-ultra-550b-a55b:free",
          "nvidia/nemotron-3.5-super-vl:free",
          "google/gemma-4-31b-it:free"
        ]);
        async function askOpenRouter(key){
          let err = "OpenRouter indisponible";
          for (const model of OR_MODELS) {
            const ctrl = new AbortController(); const to = setTimeout(() => ctrl.abort(), 28000);
            try{
              const r = await fetch("https://openrouter.ai/api/v1/chat/completions", { method:"POST", signal:ctrl.signal,
                headers:{ "Authorization":"Bearer "+key, "content-type":"application/json", "HTTP-Referer":"https://djac57.github.io/titistoire/", "X-Title":"Titistoire" },
                body: JSON.stringify({ model,
                  messages:[{role:"system",content:"Tu es une conteuse pour enfants. Réponds UNIQUEMENT par un objet JSON valide, sans texte autour."},{role:"user",content:prompt}],
                  max_tokens:3000 }) });
              const d = await r.json();
              let raw = d && d.choices && d.choices[0] && d.choices[0].message && d.choices[0].message.content;
              if (raw) { const a = raw.indexOf("{"), b = raw.lastIndexOf("}"); if (a >= 0 && b > a) { const c = raw.slice(a, b + 1); try { JSON.parse(c); return { txt: c, model }; } catch (e) {} } }
              err = (d && d.error && (d.error.message || JSON.stringify(d.error))) || err;
            } catch (e) { err = String(e); } finally { clearTimeout(to); }
          }
          return { err };
        }
        let txt = null, lastErr = null, usedModel = null, busy = false;
        // 1) OpenRouter (modèles gratuits, bon français, quota séparé de Gemini) si clé présente
        if (env.OPENROUTER_KEY) { const r = await askOpenRouter(env.OPENROUTER_KEY); if (r.txt) { txt = r.txt; usedModel = "or:" + r.model; } else lastErr = "OpenRouter: " + r.err; }
        // 2) Gemini (si clé) — en secours
        if (!txt && GKEY) for (const model of models) {
          const res = await askGemini(model);
          if (res.txt) { txt = res.txt; usedModel = model; break; }
          lastErr = res.err; if (res.busy) busy = true;
        }
        // Secours GRATUIT sans clé externe : Workers AI (Llama), utile quand Gemini sature
        if (!txt && env.AI) {
          try {
            const ar = await env.AI.run("@cf/meta/llama-3.3-70b-instruct-fp8-fast", {
              messages: [
                { role: "system", content: "Tu es une conteuse pour enfants. Réponds UNIQUEMENT par un objet JSON valide, sans aucun texte autour." },
                { role: "user", content: prompt }
              ], max_tokens: 2048
            });
            let raw = (ar && (ar.response || ar.result)) || "";
            if (typeof raw !== "string") raw = JSON.stringify(raw);
            const a = raw.indexOf("{"), b = raw.lastIndexOf("}");
            if (a >= 0 && b > a) { const cand = raw.slice(a, b + 1); try { JSON.parse(cand); txt = cand; usedModel = "workers-ai-llama"; } catch (e) { lastErr = "Llama: JSON invalide"; } }
          } catch (e) { lastErr = lastErr || ("WorkersAI: " + String(e)); }
        }
        if (!txt) return new Response(JSON.stringify({ error: "Conteuse indisponible", busy, detail: lastErr, tried: models.concat(["workers-ai-llama"]) }), { status: 502, headers: { "content-type": "application/json", ...cors } });
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
