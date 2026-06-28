#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

STAMP="$(date +%Y%m%d-%H%M%S)"
OUT="remedy-review-${STAMP}.zip"

# Parse arguments
EVIDENCE_DIR=""
INCLUDE_STALE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --evidence-dir)
      EVIDENCE_DIR="$2"
      shift 2
      ;;
    --include-stale-evidence)
      echo "--include-stale-evidence is not implemented yet." >&2
      echo "Only current-run evidence is supported. Remove this flag." >&2
      exit 2
      ;;
    -*)
      echo "Unknown option: $1" >&2
      exit 2
      ;;
    *)
      # Positional arg = evidence dir (backward compat)
      EVIDENCE_DIR="$1"
      shift
      ;;
  esac
done

# --- Detritus check (before evidence selection — always runs) ---
DETRITUS="$(find . -maxdepth 1 \( -name '*_WAS_HERE.txt' -o -name 'BUILDER_WAS_HERE.txt' -o -name 'REVIEWER_WAS_HERE.txt' \) 2>/dev/null | sed 's#^\./##' || true)"
if [[ -n "$DETRITUS" ]]; then
  echo "Debug/test detritus found in repo root — remove before review zip:"
  echo "$DETRITUS"
  exit 1
fi

# --- Current-run evidence selection ---
if [[ -z "$EVIDENCE_DIR" ]]; then
  CANDIDATES=()
  while IFS= read -r -d '' dir; do
    CANDIDATES+=("$dir")
  done < <(find . -maxdepth 1 -type d -name 'remedy-job-evidence-*' -print0 2>/dev/null | sort -z)

  if [[ ${#CANDIDATES[@]} -eq 0 ]]; then
    echo "No evidence dir provided and no remedy-job-evidence-* dirs found."
    echo "Usage: $0 --evidence-dir <path>"
    echo "  or:  $0 <evidence-dir>"
    exit 2
  elif [[ ${#CANDIDATES[@]} -eq 1 ]]; then
    EVIDENCE_DIR="${CANDIDATES[0]}"
    echo "Auto-detected evidence dir: $EVIDENCE_DIR"
  else
    echo "Multiple evidence dirs found. Select one with --evidence-dir:"
    for c in "${CANDIDATES[@]}"; do
      echo "  $c"
    done
    exit 2
  fi
fi

if [[ ! -d "$EVIDENCE_DIR" ]]; then
  echo "Evidence dir does not exist: $EVIDENCE_DIR" >&2
  exit 2
fi

TMP="$(mktemp)"
MANIFEST=".review_zip_manifest.json"
trap 'rm -f "$TMP" "$MANIFEST"' EXIT

# --- Build file list: repo files (excluding evidence dirs and junk) ---
EVIDENCE_EXCLUDE_ARGS=()
while IFS= read -r -d '' dir; do
  rel="$(echo "$dir" | sed 's#^\./##')"
  EVIDENCE_EXCLUDE_ARGS+=(-path "./$rel" -o)
done < <(find . -maxdepth 1 -type d -name 'remedy-job-evidence-*' -print0 2>/dev/null | sort -z)

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
    -path './*/.ruff_cache' -o \
    -path './htmlcov' -o \
    -path './*/htmlcov' -o \
    -path './.tox' -o \
    -path './*/.tox' -o \
    -path './.coverage_reports' -o \
    -path './*/.coverage_reports' -o \
    "${EVIDENCE_EXCLUDE_ARGS[@]}" \
    -false \
  \) -prune -o \
  -type f \
  ! -name '.coverage' \
  ! -name '.coverage.*' \
  ! -name 'coverage.xml' \
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

# --- Build manifest using Python (always-valid JSON) ---
python3 scripts/build_review_manifest.py \
  --evidence-dir "$EVIDENCE_DIR" \
  --output "$MANIFEST"

echo "$MANIFEST" >> "$TMP"

# --- Include current evidence under evidence/current/ prefix ---
EVIDENCE_STAGING="$(mktemp -d)"
trap 'rm -rf "$EVIDENCE_STAGING" "$TMP" "$MANIFEST"' EXIT

CURRENT_PREFIX="evidence/current"
mkdir -p "$EVIDENCE_STAGING/$CURRENT_PREFIX"

find "$EVIDENCE_DIR" -type f \
  ! -name '*.pyc' ! -name '*.pyo' \
  -print0 \
| while IFS= read -r -d '' src; do
    rel="${src#$EVIDENCE_DIR/}"
    dest="$EVIDENCE_STAGING/$CURRENT_PREFIX/$rel"
    mkdir -p "$(dirname "$dest")"
    cp "$src" "$dest"
  done

find "$EVIDENCE_STAGING" -type f -print \
  | sed "s#^${EVIDENCE_STAGING}/##" \
  | sort -u >> "$TMP"

sort -u "$TMP" -o "$TMP"

# --- Create zip ---
rm -f "$OUT"

cd "$ROOT"
REPO_FILES="$(grep -v '^evidence/current/' "$TMP" || true)"
if [[ -n "$REPO_FILES" ]]; then
  echo "$REPO_FILES" | zip -q -@ "$OUT"
fi

cd "$EVIDENCE_STAGING"
EV_FILES="$(find evidence/current -type f 2>/dev/null || true)"
if [[ -n "$EV_FILES" ]]; then
  echo "$EV_FILES" | zip -q -@ "$ROOT/$OUT" -g
fi

cd "$ROOT"
zip -q "$OUT" "$MANIFEST" -g

# --- Post-build verification ---

# 1. Verify no unsafe files
BAD="$(unzip -Z1 "$OUT" | grep -E '(^|/)(__pycache__|node_modules|\.git|\.data|\.venv|venv|htmlcov|\.tox|\.coverage_reports)(/|$)|\.pyc$|\.pyo$|(^|/)\.env($|\.)|\.log$|(^|/)\.coverage$|(^|/)coverage\.xml$' || true)"
if [[ -n "$BAD" ]]; then
  echo "Unsafe file found in zip:"
  echo "$BAD"
  rm -f "$OUT"
  exit 1
fi

# 2. Verify no raw evidence paths leaked
LEAKED="$(unzip -Z1 "$OUT" | grep -E '^(tmp/|home/|Users/|private/|remedy-job-evidence-)' || true)"
if [[ -n "$LEAKED" ]]; then
  echo "Local path structure leaked into zip:"
  echo "$LEAKED"
  rm -f "$OUT"
  exit 1
fi

# 3. Verify manifest content against zip
VERIFY_ERRORS=""

# Check agent_state files match manifest claims
for AGENT_FILE in .agent/live_review.md .agent/plan.md .agent/review_protocol.md; do
  MANIFEST_STATUS="$(python3 -c "
import json, sys
m = json.load(open('$MANIFEST'))
print(m.get('agent_state', {}).get('$AGENT_FILE', 'absent'))
" 2>/dev/null || echo "error")"
  if [[ "$MANIFEST_STATUS" == "present" ]]; then
    if ! unzip -Z1 "$OUT" | grep -qF "$AGENT_FILE"; then
      VERIFY_ERRORS="${VERIFY_ERRORS}Manifest says $AGENT_FILE present but missing from zip\n"
    fi
  fi
done

# Check evidence artifacts marked present exist under evidence/current/
if python3 -c "import json; m=json.load(open('$MANIFEST')); exit(0 if m.get('current_evidence') else 1)" 2>/dev/null; then
  python3 -c "
import json, sys
m = json.load(open('$MANIFEST'))
ce = m.get('current_evidence', {})
for name, status in ce.get('root_artifacts', {}).items():
    if status == 'present':
        print(f'evidence/current/{name}')
" 2>/dev/null | while read -r expected; do
    if ! unzip -Z1 "$OUT" | grep -qF "$expected"; then
      VERIFY_ERRORS="${VERIFY_ERRORS}Manifest says $expected present but missing from zip\n"
    fi
  done
fi

# Check no stale evidence dirs included
STALE_EV="$(unzip -Z1 "$OUT" | grep -E '^remedy-job-evidence-' || true)"
if [[ -n "$STALE_EV" ]]; then
  VERIFY_ERRORS="${VERIFY_ERRORS}Stale evidence dir included in zip: $STALE_EV\n"
fi

if [[ -n "$VERIFY_ERRORS" ]]; then
  echo "Post-build verification failed:"
  echo -e "$VERIFY_ERRORS"
  rm -f "$OUT"
  exit 1
fi

BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
COMMIT="$(git rev-parse HEAD 2>/dev/null || echo unknown)"

echo "Created: $ROOT/$OUT"
du -h "$OUT"
echo
echo "Included files: $(unzip -Z1 "$OUT" | wc -l | tr -d ' ')"
echo "Branch: $BRANCH"
echo "Commit: $COMMIT"
echo "Evidence: $CURRENT_PREFIX/"
