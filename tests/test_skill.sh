#!/usr/bin/env bash

set -euo pipefail

source_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skill_root="$source_root/.agents/skills/continue-study"
test_root="$(mktemp -d)"
trap 'rm -rf "$test_root"' EXIT

required_files=(
  "$skill_root/SKILL.md"
  "$skill_root/agents/openai.yaml"
  "$skill_root/references/learning-model.md"
  "$skill_root/references/web-ui.md"
  "$skill_root/assets/web-ui-template/package.json"
  "$skill_root/assets/web-ui-template/package-lock.json"
  "$skill_root/assets/web-ui-template/src/content.config.ts"
  "$skill_root/assets/web-ui-template/src/content/assignments/git-state-guided.json"
  "$skill_root/assets/web-ui-template/src/content/assignments/git-state-independent.json"
  "$skill_root/assets/web-ui-template/src/content/assessments/git-state.json"
  "$skill_root/assets/web-ui-template/src/content/lessons/git-working-tree.json"
  "$skill_root/assets/web-ui-template/src/data/checkpoint.json"
  "$skill_root/assets/web-ui-template/src/pages/index.astro"
  "$skill_root/assets/web-ui-template/src/pages/lessons/[id].astro"
)

for path in "${required_files[@]}"; do
  [[ -f "$path" ]] || {
    printf 'missing required skill file: %s\n' "$path" >&2
    exit 1
  }
done

grep -q '^name: continue-study$' "$skill_root/SKILL.md"
grep -q '^description: .\+' "$skill_root/SKILL.md"
grep -Fq '$continue-study' "$skill_root/agents/openai.yaml"

if grep -R -E -n \
  'TODO|TBD|FIXME|implement later' \
  "$skill_root/SKILL.md" \
  "$skill_root/agents" \
  "$skill_root/references" \
  "$skill_root/assets/web-ui-template/src" \
  "$skill_root/assets/web-ui-template/package.json" \
  "$source_root/curriculum" \
  "$source_root/lessons" \
  "$source_root/assignments" \
  "$source_root/assessments" \
  "$source_root/templates"; then
  printf '%s\n' 'skill or learning contracts contain a placeholder' >&2
  exit 1
fi

mkdir -p "$test_root/repo"
tar \
  --exclude='./.git' \
  --exclude='*/node_modules' \
  --exclude='*/dist' \
  --exclude='*/.astro' \
  -C "$source_root" -cf - . |
  tar -C "$test_root/repo" -xf -

cp "$test_root/repo/templates/lesson.md" \
  "$test_root/repo/lessons/git-working-tree.md"
cp "$test_root/repo/templates/assignment.md" \
  "$test_root/repo/assignments/git-state-guided.md"
cp "$test_root/repo/templates/assignment-independent.md" \
  "$test_root/repo/assignments/git-state-independent.md"
cp "$test_root/repo/templates/assessment.json" \
  "$test_root/repo/assessments/git-state.json"

python3 "$test_root/repo/scripts/validate.py" >/dev/null

cp "$test_root/repo/lessons/git-working-tree.md" \
  "$test_root/repo/lessons/duplicate-id.md"
if python3 "$test_root/repo/scripts/validate.py" >/dev/null 2>&1; then
  printf '%s\n' 'expected duplicate content ID validation to fail' >&2
  exit 1
fi
rm "$test_root/repo/lessons/duplicate-id.md"

sed \
  -e 's/id: lesson-git-working-tree-001/id: lesson-invalid-contract/' \
  -e '/^kind: lesson$/d' \
  "$test_root/repo/templates/lesson.md" \
  >"$test_root/repo/lessons/invalid-contract.md"
if python3 "$test_root/repo/scripts/validate.py" >/dev/null 2>&1; then
  printf '%s\n' 'expected lesson contract validation to fail' >&2
  exit 1
fi
rm "$test_root/repo/lessons/invalid-contract.md"

printf '%s\n' '{"id":"duplicate","id":"duplicate"}' \
  >"$test_root/repo/assessments/duplicate-key.json"
if python3 "$test_root/repo/scripts/validate.py" >/dev/null 2>&1; then
  printf '%s\n' 'expected duplicate assessment key validation to fail' >&2
  exit 1
fi
rm "$test_root/repo/assessments/duplicate-key.json"

printf '%s\n' '{"id":' >"$test_root/repo/assessments/malformed.json"
if python3 "$test_root/repo/scripts/validate.py" >/dev/null 2>&1; then
  printf '%s\n' 'expected malformed assessment JSON validation to fail' >&2
  exit 1
fi
rm "$test_root/repo/assessments/malformed.json"

python3 - "$test_root/repo/templates/assessment.json" \
  "$test_root/repo/assessments/invalid-structure.json" <<'PY'
import json
import sys

source, target = sys.argv[1:]
with open(source, encoding="utf-8") as handle:
    assessment = json.load(handle)
assessment["id"] = "assessment-invalid-structure"
assessment["objectives"] = [{"id": "missing-statement"}]
assessment["rubric"]["criteria"][0]["critical"] = "yes"
assessment["reassessment"]["variant"] = {}
with open(target, "w", encoding="utf-8") as handle:
    json.dump(assessment, handle)
PY
if python3 "$test_root/repo/scripts/validate.py" >/dev/null 2>&1; then
  printf '%s\n' 'expected invalid assessment structure validation to fail' >&2
  exit 1
fi
rm "$test_root/repo/assessments/invalid-structure.json"

sed \
  -e 's/id: assignment-git-state-guided-001/id: assignment-missing-lesson/' \
  -e 's/lesson: lesson-git-working-tree-001/lesson: lesson-does-not-exist/' \
  "$test_root/repo/templates/assignment.md" \
  >"$test_root/repo/assignments/missing-lesson.md"
if python3 "$test_root/repo/scripts/validate.py" >/dev/null 2>&1; then
  printf '%s\n' 'expected missing lesson relationship validation to fail' >&2
  exit 1
fi
rm "$test_root/repo/assignments/missing-lesson.md"

mkdir -p "$test_root/repo/node_modules/ignored-fixture"
printf '%s%s\n' '-----BEGIN PRIVATE ' 'KEY-----' \
  >"$test_root/repo/node_modules/ignored-fixture/generated.txt"
python3 "$test_root/repo/scripts/validate.py" >/dev/null

printf '%s%s\n' 'SUPABASE_SERVICE_ROLE_' \
  'KEY=fake-service-role-value-for-validation' \
  >"$test_root/repo/.env.example"
if python3 "$test_root/repo/scripts/validate.py" >/dev/null 2>&1; then
  printf '%s\n' 'expected service-role credential validation to fail' >&2
  exit 1
fi

printf '%s\n' 'continue-study skill tests passed'
