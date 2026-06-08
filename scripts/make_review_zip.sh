#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

STAMP="$(date +%Y%m%d-%H%M%S)"
OUT="remedy-review-${STAMP}.zip"

EXCLUDES=(
  '.data/*'
  'node_modules/*'
  '*/node_modules/*'
  'dist/*'
  '*/dist/*'
  'build/*'
  '*/build/*'
  '.cache/*'
  '*/.cache/*'
  '.pytest_cache/*'
  '*/.pytest_cache/*'
  '__pycache__/*'
  '*/__pycache__/*'
  '*.pyc'
  '*.pyo'
  '.venv/*'
  'venv/*'
  '.git/*'
  '*.zip'
  '*.tar'
  '*.tar.gz'
  '*.tgz'
  '*.log'

  # local/private agent settings
  '.claude/settings.local.json'
  '.claude/**/settings.local.json'
  '.pi/local/*'
  '.pi/**/local/*'

  # secrets
  '.env'
  '.env.*'
  '**/.env'
  '**/.env.*'
  '*token*'
  '*secret*'
  '*credentials*'
)

TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

# 1) All tracked files
git ls-files > "$TMP"

# 2) Important untracked project-state files
OPTIONAL_FILES=(
  ".agent/context.md"
  ".agent/plan.md"
  ".agent/live_review.md"
  ".agent/review.md"
  ".agent/review_protocol.md"
  ".agent/decisions.md"
  "AGENTS.md"
  "CLAUDE.md"
  "SYSTEM.md"
  ".mcp.json"
  ".vscode/mcp.json"
  "scripts/make_review_zip.sh"
)

for f in "${OPTIONAL_FILES[@]}"; do
  if [[ -f "$f" ]]; then
    echo "$f" >> "$TMP"
  fi
done

# 3) Important untracked agent/tooling directories, but only safe text/config docs.
OPTIONAL_DIRS=(
  ".claude"
  ".pi"
  ".vscode"
)

for d in "${OPTIONAL_DIRS[@]}"; do
  if [[ -d "$d" ]]; then
    find "$d" -type f \
      \( -name "*.md" -o -name "*.json" -o -name "*.yaml" -o -name "*.yml" -o -name "*.toml" -o -name "*.txt" \) \
      ! -name "settings.local.json" \
      ! -path "*/local/*" \
      ! -iname "*secret*" \
      ! -iname "*token*" \
      ! -iname "*credential*" \
      >> "$TMP"
  fi
done

# 4) Normalize list
sort -u "$TMP" -o "$TMP"

ZIP_EXCLUDES=()
for pattern in "${EXCLUDES[@]}"; do
  ZIP_EXCLUDES+=("-x" "$pattern")
done

zip -q -@ "$OUT" < "$TMP" "${ZIP_EXCLUDES[@]}"

echo "Created: $ROOT/$OUT"
du -h "$OUT"
echo
echo "Included files:"
wc -l "$TMP"