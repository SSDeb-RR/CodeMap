#!/bin/sh
set -eu
repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
destination="$repo_dir/.env.local"
if [ -e "$destination" ]; then
  echo "Refusing to overwrite $destination" >&2
  exit 1
fi
cp -- "$repo_dir/.env.example" "$destination"
chmod 600 "$destination"
echo "Created $destination. Add credentials locally and never commit it."
