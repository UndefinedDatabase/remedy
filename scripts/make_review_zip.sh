#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

STAMP="$(date +%Y%m%d-%H%M%S)"
OUT="remedy-review-${STAMP}.zip"

TMP="$(mktemp)"
MANIFEST=".review_zip_manifest.json"
trap 'rm -f "$TMP" "$MANIFEST"' EXIT

# Include whole relevant folders, tracked AND untracked.
# Exclude only junk, caches, build output, env/secrets, old archives/logs.
find . \
  \( \
    -path './.git' -o \
    -path './.data' -o \
    -path './node_modules' -o \
    -path './*/node_modules' -o \
    -path './dist' -o \
    -path './*/dist' -o \
    -path './build' -o \
    -path './*/build' -o \
    -path './.cache' -o \
    -path './*/.cache' -o \
    -path './.pytest_cache' -o \
    -path './*/.pytest_cache' -o \
    -path './__pycache__' -o \
    -path './*/__pycache__' -o \
    -path './.venv' -o \
    -path './venv' -o \
    -path './*/.venv' -o \
    -path './*/venv' -o \
    -path './.mypy_cache' -o \
    -path './*/.mypy_cache' -o \
    -path './.ruff_cache' -o \
    -path './*/.ruff_cache' \
  \) -prune -o \
  -type f \
  ! -name '*.zip' \
  ! -name '*.tar' \
  ! -name '*.tar.gz' \
  ! -name '*.tgz' \
  ! -name '*.log' \
  ! -name '*.pyc' \
  ! -name '*.pyo' \
  ! -name '.env' \
  ! -name '.env.*' \
  ! -name '*.pem' \
  ! -name '*.key' \
  ! -name '*.p12' \
  ! -name '*.pfx' \
  ! -name '*.crt' \
  ! -name '*.cer' \
  ! -name 'settings.local.json' \
  ! -name 'credentials.json' \
  ! -name 'service-account.json' \
  ! -name 'service_account.json' \
  ! -name 'client_secret.json' \
  ! -name 'firebase-adminsdk.json' \
  ! -name 'id_rsa' \
  ! -name 'id_dsa' \
  ! -name 'id_ecdsa' \
  ! -name 'id_ed25519' \
  -print \
  | sed 's#^\./##' \
  | sort -u > "$TMP"

BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
COMMIT="$(git rev-parse HEAD 2>/dev/null || echo unknown)"

cat > "$MANIFEST" <<MANIFEST_EOF
{
  "bundle_kind": "remedy_review_zip",
  "bundle_version": 5,
  "generated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "branch": "$BRANCH",
  "commit": "$COMMIT",
  "policy": "Includes whole relevant project folders, tracked and untracked. Excludes .git, .data, node_modules, caches, build outputs, env files, private keys, logs, old archives."
}
MANIFEST_EOF

echo "$MANIFEST" >> "$TMP"
sort -u "$TMP" -o "$TMP"

rm -f "$OUT"
zip -q -@ "$OUT" < "$TMP"

BAD="$(unzip -Z1 "$OUT" | grep -E '(^|/)(__pycache__|node_modules|\.git|\.data|\.venv|venv)(/|$)|\.pyc$|\.pyo$|(^|/)\.env($|\.)|\.log$' || true)"
if [[ -n "$BAD" ]]; then
  echo "Unsafe file found in zip:"
  echo "$BAD"
  rm -f "$OUT"
  exit 1
fi

echo "Created: $ROOT/$OUT"
du -h "$OUT"
echo
echo "Included files: $(wc -l < "$TMP" | tr -d ' ')"
echo "Branch: $BRANCH"
echo "Commit: $COMMIT"
