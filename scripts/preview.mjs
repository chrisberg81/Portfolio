#!/usr/bin/env node
// Usage: preview.mjs <readme.md> <out.html>
// Renders a README to one self-contained HTML file: images inlined as data URIs, mermaid via CDN, dark/light.
// Needs `marked` (NODE_PATH or local install).
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { dirname, resolve, extname } from "node:path";
import { createRequire } from "node:module";
const require = createRequire(process.env.MARKED_FROM || import.meta.url);
const { marked } = require("marked");
const [src, out] = process.argv.slice(2);
const dir = dirname(resolve(src));
let md = readFileSync(src, "utf8");
const mime = { ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".gif": "image/gif" };
const inline = (p) => {
  const f = resolve(dir, p);
  if (!existsSync(f) || !mime[extname(f)]) return p;
  return `data:${mime[extname(f)]};base64,${readFileSync(f).toString("base64")}`;
};
md = md.replace(/```mermaid\n([\s\S]*?)```/g, (_, c) => `<pre class="mermaid">${c.replace(/</g, "&lt;")}</pre>`);
let html = marked.parse(md);
html = html.replace(/(src|srcset)="([^"]+)"/g, (m, a, p) => (/^(https?:|data:)/.test(p) ? m : `${a}="${inline(p)}"`));
writeFileSync(out, `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{color-scheme:light dark;--bg:#fff;--fg:#1f2328;--mute:#59636e;--line:#d1d9e0;--code:#f6f8fa}
@media(prefers-color-scheme:dark){:root{--bg:#0d1117;--fg:#e6edf3;--mute:#8b949e;--line:#30363d;--code:#161b22}}
body{background:var(--bg);color:var(--fg);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;max-width:980px;margin:0 auto;padding:32px 24px}
h1,h2{border-bottom:1px solid var(--line);padding-bottom:.3em}h2{margin-top:2em}
table{border-collapse:collapse;display:block;overflow:auto;margin:1em 0}th,td{border:1px solid var(--line);padding:6px 12px;vertical-align:top}th{background:var(--code)}
code{background:var(--code);padding:.2em .4em;border-radius:6px;font-size:85%}pre{background:var(--code);padding:16px;border-radius:6px;overflow:auto}
img{max-width:100%;height:auto}a{color:#4493f8}blockquote{color:var(--mute);border-left:4px solid var(--line);margin:0;padding:0 1em}hr{border:0;border-top:1px solid var(--line)}
pre.mermaid{background:transparent;text-align:center}
</style></head><body>${html}
<script type="module">import m from "https://cdn.jsdelivr.net/npm/mermaid@11.4.0/dist/mermaid.esm.min.mjs";m.initialize({startOnLoad:false,theme:matchMedia("(prefers-color-scheme: dark)").matches?"dark":"default"});await m.run({querySelector:"pre.mermaid"});</script>
</body></html>`);
console.log("wrote", out);
