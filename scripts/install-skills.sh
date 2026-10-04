#!/bin/sh
set -eu
repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
force=false
[ "${1:-}" = "--force" ] && force=true
install_skill() {
  source_dir=$1
  destination=$2
  if [ -e "$destination" ] || [ -L "$destination" ]; then
    if [ "$force" != true ]; then
      echo "Refusing to overwrite $destination (use --force)." >&2
      exit 1
    fi
    rm -rf -- "$destination"
  fi
  mkdir -p -- "$(dirname -- "$destination")"
  cp -R -- "$source_dir" "$destination"
  printf '%s\n' "$repo_dir" > "$destination/.codemap-home"
  echo "Installed $destination"
}
install_skill "$repo_dir/skills/codemap" "${CODEX_HOME:-$HOME/.codex}/skills/codemap"
install_skill "$repo_dir/skills/codemap" "$HOME/.claude/skills/codemap"
