#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
codex_home="${CODEX_HOME:-$HOME/.codex}"

src="$repo_root/paper-reading-notion/"
dst="$codex_home/skills/paper-reading-notion/"

if [[ ! -f "$src/SKILL.md" ]]; then
  echo "missing source skill: $src/SKILL.md" >&2
  exit 1
fi

mkdir -p "$dst"
rsync -a --delete \
  --exclude ".DS_Store" \
  "$src" "$dst"

echo "synced paper-reading-notion to $dst"
