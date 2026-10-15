#!/usr/bin/env bash
# Usage: render_diagram.sh <slug> <spec.json>  -> assets/<slug>/architecture.html + architecture-{dark,light}.svg
set -euo pipefail
R=~/Developer/portfolio-showcase; A=$R/assets/$1; mkdir -p "$A"
(cd ~/.claude/skills/archify && node bin/archify.mjs deliver architecture "$2" "$A/architecture.html" --quality showcase --json | grep -m1 '"ok"')
(cd "$A" && python3 $R/scripts/extract_svg.py architecture.html architecture)
