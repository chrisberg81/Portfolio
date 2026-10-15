#!/usr/bin/env bash
# Usage: stats.sh <repo-dir> [subpath]   -> prints files + code LOC per language (numbers only, no code)
set -euo pipefail
cd "$1"; sub="${2:-.}"
git ls-files -- "$sub" | grep -Ev '(lock|-lock\.yaml|\.min\.)|(^|/)(node_modules|vendor|dist|build|graphify-out|\.claude)/' |
while IFS= read -r f; do
  case "${f##*.}" in
    py) l=Python;; ts|tsx) l=TypeScript;; js|jsx|mjs|cjs) l=JavaScript;; dart) l=Dart;;
    sql) l=SQL;; css|scss) l=CSS;; html) l=HTML;; rs) l=Rust;; *) continue;;
  esac
  [ -f "$f" ] && printf '%s\t%s\n' "$l" "$(wc -l < "$f")"
done | awk -F'\t' '{f[$1]++; n[$1]+=$2; T+=$2; F++} END{for(k in f) printf "| %s | %d | %d |\n",k,f[k],n[k]; printf "| **Total** | %d | %d |\n",F,T}' | sort -t'|' -k4 -nr
