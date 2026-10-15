#!/usr/bin/env python3
"""Pull the diagram out of an archify HTML file as standalone light/dark SVGs.
Usage: extract_svg.py <architecture.html> <out_prefix>   -> <out_prefix>-dark.svg, -light.svg"""
import re, sys
h = open(sys.argv[1]).read()
svg = re.search(r'<svg[\s\S]*?</svg>', h).group(0)
used = set()
for m in re.finditer(r'class="([^"]+)"', svg): used.update(m.group(1).split())
css = re.findall(r'<style[^>]*>([\s\S]*?)</style>', h)[1]
css = re.sub(r'/\*[\s\S]*?\*/', '', css)
rules, depth, buf = [], 0, ''
for ch in css:
    buf += ch
    if ch == '{': depth += 1
    elif ch == '}':
        depth -= 1
        if depth == 0: rules.append(buf.strip()); buf = ''
def keep(r):
    sel = r.split('{')[0]
    if re.search(r'\b(body|html)\b', sel) or '@media' in sel and 'prefers' not in sel: pass
    if re.search(r'html|body|\.viewer|#|\.toolbar|\.panel|\.legend', sel): return False
    if sel.strip().startswith('[data-theme') or sel.strip().startswith(':root'): return True
    return any(('.'+c) in sel for c in used) or sel.strip().startswith('svg')
kept = [r for r in rules if keep(r)]
style = '\n'.join(kept)
FONT = 'ui-monospace,SFMono-Regular,Menlo,Consolas,monospace'
for theme in ('dark', 'light'):
    s = svg.replace('<svg ', f'<svg xmlns="http://www.w3.org/2000/svg" data-theme="{theme}" font-family="{FONT}" ', 1)
    st = style.replace(':root,', '').replace('[data-theme="dark"]', 'svg[data-theme="dark"]').replace('[data-theme="light"]', 'svg[data-theme="light"]')
    st = re.sub(r'(^|\n)\s*(svg\[data-theme="dark"\])\s*\{', r'\1\2 {', st)
    s = re.sub(r'(<svg[^>]*>)', lambda m: m.group(1) + f'<style>{st}</style><rect x="-2000" y="-2000" width="6000" height="6000" fill="var(--bg)"/>', s, count=1)
    open(f'{sys.argv[2]}-{theme}.svg', 'w').write(s)
