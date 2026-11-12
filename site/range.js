/* Le site est fait de fichiers statiques. Seule exception : les pistes de voix. L'hébergement de fichiers
   ne répond pas aux demandes partielles (« Range »), dont Safari a besoin pour lire un son et s'y déplacer.
   Ce petit programme ne voit passer que /assets/voix/… et renvoie le morceau demandé. */
export default {
  async fetch(req, env) {
    const r = await env.ASSETS.fetch(req);
    const range = req.headers.get("range");
    if (req.method !== "GET" || r.status !== 200) return r;
    const h = new Headers(r.headers); h.set("accept-ranges", "bytes");
    const m = range && /^bytes=(\d*)-(\d*)$/.exec(range.trim());
    if (!m || (m[1] === "" && m[2] === "")) return new Response(r.body, { status: 200, headers: h });
    const buf = await r.arrayBuffer(), n = buf.byteLength;
    const a = m[1] === "" ? Math.max(0, n - Number(m[2])) : Number(m[1]);
    const b = m[1] === "" || m[2] === "" ? n - 1 : Math.min(Number(m[2]), n - 1);
    if (a > b || a >= n) return new Response(null, { status: 416, headers: { "content-range": `bytes */${n}` } });
    h.set("content-range", `bytes ${a}-${b}/${n}`); h.set("content-length", String(b - a + 1));
    return new Response(buf.slice(a, b + 1), { status: 206, headers: h });
  }
};
