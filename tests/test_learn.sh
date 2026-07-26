#!/usr/bin/env bash

set -euo pipefail

source_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
test_root="$(mktemp -d)"
trap 'rm -rf "$test_root"' EXIT

cp -R "$source_root/." "$test_root/repo"
rm -rf "$test_root/repo/.git"

git -C "$test_root/repo" init -b main >/dev/null
git -C "$test_root/repo" config user.name "Learning Test"
git -C "$test_root/repo" config user.email "learning-test@example.com"
git -C "$test_root/repo" add --all
git -C "$test_root/repo" commit -m "test: initial fixture" >/dev/null
git init --bare "$test_root/remote.git" >/dev/null
git -C "$test_root/repo" remote add origin "$test_root/remote.git"
git -C "$test_root/repo" push --set-upstream origin main >/dev/null

note="$(
  "$test_root/repo/scripts/learn" capture \
    "Pull before push" \
    "Fetch and rebase remote changes before publishing local work."
)"

[[ -f "$test_root/repo/$note" ]]
grep -q '^status: inbox$' "$test_root/repo/$note"
python3 "$test_root/repo/scripts/validate.py" >/dev/null

"$test_root/repo/scripts/learn" sync >/dev/null
[[ -z "$(git -C "$test_root/repo" status --porcelain)" ]]
[[ "$(git -C "$test_root/repo" rev-parse HEAD)" == \
  "$(git --git-dir="$test_root/remote.git" rev-parse main)" ]]

distill_output="$(
  "$test_root/repo/scripts/learn" distill "$note" "Reliable Git Sync"
)"
grep -q 'created topics/reliable-git-sync.md' <<<"$distill_output"
[[ "$(git -C "$test_root/repo" branch --show-current)" == study/reliable-git-sync-* ]]
python3 "$test_root/repo/scripts/validate.py" >/dev/null

printf '%s%s\n' '-----BEGIN PRIVATE ' 'KEY-----' \
  >>"$test_root/repo/topics/reliable-git-sync.md"
if python3 "$test_root/repo/scripts/validate.py" >/dev/null 2>&1; then
  printf '%s\n' 'expected secret validation to fail' >&2
  exit 1
fi

printf '%s\n' 'learning CLI tests passed'
