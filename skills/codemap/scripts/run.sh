#!/bin/sh
set -eu
skill_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
if [ -f "$skill_dir/.codemap-home" ]; then
  repo_dir=$(sed -n '1p' "$skill_dir/.codemap-home")
else
  repo_dir=$(CDPATH= cd -- "$skill_dir/../.." && pwd)
fi
caller_dir=$PWD
has_out=false
for argument in "$@"; do
  [ "$argument" = "--out" ] && has_out=true
done
if [ "$#" -eq 0 ]; then
  set -- "$caller_dir"
fi
if [ "$has_out" = false ]; then
  set -- "$@" --out "$caller_dir/codemap-output"
fi
exec node "$repo_dir/scripts/codemap.ts" "$@"
