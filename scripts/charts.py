#!/usr/bin/env python3
"""Where-the-code-lives bar charts, from a mirror folder of source files.
Usage: charts.py <mirror-dir> <out.svg> <title> <subtitle> [depth=2] [strip_prefix=] [max_rows=9]
Counts lines only; no code ever leaves the mirror."""
import os, sys, collections
root, out, title, sub = sys.argv[1:5]
depth = int(sys.argv[5]) if len(sys.argv) > 5 else 2
strip = sys.argv[6] if len(sys.argv) > 6 else ''
maxr = int(sys.argv[7]) if len(sys.argv) > 7 else 9
import json
c = collections.Counter(); tests = 0
if root.endswith('.json'):
    c.update(json.load(open(root)))
for dp, dn, fn in (os.walk(root) if not root.endswith('.json') else []):
    for f in fn:
        p = os.path.join(dp, f); rel = os.path.relpath(p, root)
        if strip and rel.startswith(strip): rel = rel[len(strip):]
        try: n = sum(1 for _ in open(p, errors='ignore'))
        except Exception: continue
        parts = rel.split(os.sep)
        key = '/'.join(parts[:depth]) if len(parts) > depth else (parts[0] if len(parts) > 1 else '(root files)')
        c[key] += n
rows = c.most_common(maxr)
rest = sum(c.values()) - sum(v for _, v in rows)
if rest > 0: rows.append(('other', rest))
BG, INK, MUTE, GRID = '#0b0f14', '#d7e3ea', '#7f93a0', '#1b2530'
cols = ['#5eead4', '#60a5fa', '#a78bfa', '#fbbf24', '#f472b6', '#34d399', '#38bdf8', '#fb923c', '#c084fc', '#94a3b8']
W = 900; L = 230; R = 90; T = 100; rh = 34; H = T + rh * len(rows) + 56
mx = max(v for _, v in rows)
tot = sum(c.values())
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="ui-monospace,SFMono-Regular,Menlo,monospace">',
     f'<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>',
     f'<text x="32" y="44" fill="{INK}" font-size="19" font-weight="700">{title}</text>',
     f'<text x="32" y="68" fill="{MUTE}" font-size="12.5">{sub} ({tot:,} lines)</text>']
for i, (k, v) in enumerate(rows):
    y = T + i * rh; w = (W - L - R) * v / mx
    col = cols[i % len(cols)] if k != 'other' else '#475569'
    o.append(f'<text x="{L-12}" y="{y+19}" fill="{INK}" font-size="12.5" text-anchor="end">{k}</text>')
    o.append(f'<rect x="{L}" y="{y+4}" width="{max(w,3):.1f}" height="{rh-12}" rx="4" fill="{col}" opacity="0.92"/>')
    o.append(f'<text x="{L+max(w,3)+8:.1f}" y="{y+19}" fill="{MUTE}" font-size="12">{v:,}</text>')
o.append('</svg>')
open(out, 'w').write('\n'.join(o))
