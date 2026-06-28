#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

STAMP="$(date +%Y%m%d-%H%M%S)"
OUT="remedy-review-${STAMP}.zip"

# Parse arguments
EVIDENCE_DIR=""
SELECTION_MODE=""
ALLOW_INCOMPLETE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --evidence-dir)
      EVIDENCE_DIR="$2"
      SELECTION_MODE="explicit"
      shift 2
      ;;
    --allow-incomplete-evidence)
      ALLOW_INCOMPLETE=true
      shift
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
      SELECTION_MODE="explicit"
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

# --- Candidate validation helper ---
validate_candidate() {
  local cdir="$1"
  python3 -c "
import json, os, sys
d = sys.argv[1]
REQUIRED_ROOT = ['job_flow.json','manifest.json','agent_run_trace.jsonl',
    'agent_run_trace_summary.json','prompt_trace_summary.json','command_transcript.json']
REQUIRED_TASK = ['prompt_trace.jsonl','prompt_trace_summary.json','review.json',
    'repair_loop.json','token_accounting.json','provider_evidence.json']
errors = []
for art in REQUIRED_ROOT:
    if not os.path.isfile(os.path.join(d, art)):
        errors.append(f'missing: {art}')
jf = os.path.join(d, 'job_flow.json')
job_id = ''
if os.path.isfile(jf):
    try:
        data = json.load(open(jf))
        job_id = data.get('job_id', '')
        if not job_id: errors.append('empty job_id')
        audit = data.get('final_audit', {})
        if not audit.get('status'): errors.append('no final_audit.status')
        if audit.get('missing_observability_artifacts'): errors.append('missing_observability_artifacts')
        if data.get('target_guard',{}).get('mutated_target'): errors.append('target_mutation')
    except: errors.append('job_flow.json parse error')
else:
    job_id = ''
tr_dir = os.path.join(d, 'task_runs')
task_count = 0
if os.path.isdir(tr_dir):
    for entry in sorted(os.listdir(tr_dir)):
        tp = os.path.join(tr_dir, entry)
        if not os.path.isdir(tp): continue
        task_count += 1
        for art in REQUIRED_TASK:
            if not os.path.isfile(os.path.join(tp, art)):
                errors.append(f'task_runs/{entry}: missing {art}')
if task_count == 0: errors.append('no task runs')
valid = 'valid' if not errors else 'incomplete'
reason = '; '.join(errors[:3]) if errors else ''
if len(errors) > 3: reason += f' (+{len(errors)-3} more)'
print(f'{valid}|{job_id}|{reason}')
" "$cdir"
}

# --- Evidence selection ---
SELECTED_MTIME=""
CANDIDATE_COUNT=0
SELECTION_REASON=""
REJECTED_COUNT=0

if [[ -z "$EVIDENCE_DIR" ]]; then
  # Discover candidates
  CANDIDATES=()
  while IFS= read -r -d '' dir; do
    CANDIDATES+=("$dir")
  done < <(find . -maxdepth 1 -type d -name 'remedy-job-evidence-*' -print0 2>/dev/null | sort -z)

  CANDIDATE_COUNT=${#CANDIDATES[@]}

  if [[ $CANDIDATE_COUNT -eq 0 ]]; then
    echo "No evidence dir provided and no remedy-job-evidence-* dirs found."
    echo "Usage: $0 --evidence-dir <path>"
    echo "  or:  $0 <evidence-dir>"
    exit 2
  fi

  # Required root artifacts for auto-selection
  ARTIFACT_NAMES=("job_flow.json" "command_transcript.json" "agent_run_trace.jsonl" "agent_run_trace_summary.json" "prompt_trace_summary.json" "manifest.json")

  # Validate all candidates and print summary table
  echo "Evidence candidate summary:"
  printf "  %-45s %-12s %-12s %s\n" "PATH" "STATUS" "JOB_ID" "REASON"
  printf "  %-45s %-12s %-12s %s\n" "----" "------" "------" "------"

  VALID_DIRS=()
  VALID_MTIMES=()
  VALID_REASONS=()

  for cdir in "${CANDIDATES[@]}"; do
    VRESULT="$(validate_candidate "$cdir")"
    VSTATUS="$(echo "$VRESULT" | cut -d'|' -f1)"
    VJOB_ID="$(echo "$VRESULT" | cut -d'|' -f2)"
    VREASON="$(echo "$VRESULT" | cut -d'|' -f3)"

    rel="$(echo "$cdir" | sed 's#^\./##')"
    printf "  %-45s %-12s %-12s %s\n" "$rel" "$VSTATUS" "${VJOB_ID:-(none)}" "$VREASON"

    if [[ "$VSTATUS" == "valid" ]]; then
      # Compute mtime for ranking
      DIR_MTIME="0"
      DIR_REASON=""

      if [[ -f "$cdir/job_flow.json" ]]; then
        JF_MTIME="$(stat -c '%Y' "$cdir/job_flow.json" 2>/dev/null || stat -f '%m' "$cdir/job_flow.json" 2>/dev/null || echo 0)"
        if [[ "$JF_MTIME" -gt "$DIR_MTIME" ]]; then
          DIR_MTIME="$JF_MTIME"
          DIR_REASON="job_flow_json_mtime"
        fi
      fi

      if [[ "$DIR_MTIME" == "0" ]]; then
        for art in "${ARTIFACT_NAMES[@]}"; do
          if [[ -f "$cdir/$art" ]]; then
            ART_MTIME="$(stat -c '%Y' "$cdir/$art" 2>/dev/null || stat -f '%m' "$cdir/$art" 2>/dev/null || echo 0)"
            if [[ "$ART_MTIME" -gt "$DIR_MTIME" ]]; then
              DIR_MTIME="$ART_MTIME"
              DIR_REASON="artifact_mtime"
            fi
          fi
        done
      fi

      if [[ "$DIR_MTIME" == "0" ]]; then
        DIR_MTIME="$(stat -c '%Y' "$cdir" 2>/dev/null || stat -f '%m' "$cdir" 2>/dev/null || echo 0)"
        DIR_REASON="dir_mtime"
      fi

      VALID_DIRS+=("$cdir")
      VALID_MTIMES+=("$DIR_MTIME")
      VALID_REASONS+=("$DIR_REASON")
    else
      REJECTED_COUNT=$((REJECTED_COUNT + 1))
    fi
  done

  echo ""

  VALID_COUNT=${#VALID_DIRS[@]}

  if [[ $VALID_COUNT -eq 0 ]]; then
    echo "No valid complete evidence among $CANDIDATE_COUNT candidate(s)."
    echo "All candidates are incomplete or malformed."
    echo ""
    echo "To produce valid evidence, run:"
    echo "  ./scripts/remedy_self_job_flow.sh --goal-file <goal.md>"
    echo ""
    echo "To use incomplete evidence for debugging:"
    echo "  $0 --evidence-dir <path> --allow-incomplete-evidence"
    exit 2
  fi

  # Select newest valid candidate
  BEST_DIR=""
  BEST_MTIME="0"
  BEST_REASON=""
  TIE_WARNING=""

  for i in "${!VALID_DIRS[@]}"; do
    cdir="${VALID_DIRS[$i]}"
    DIR_MTIME="${VALID_MTIMES[$i]}"
    DIR_REASON="${VALID_REASONS[$i]}"

    if [[ "$DIR_MTIME" -gt "$BEST_MTIME" ]]; then
      BEST_DIR="$cdir"
      BEST_MTIME="$DIR_MTIME"
      BEST_REASON="$DIR_REASON"
      TIE_WARNING=""
    elif [[ "$DIR_MTIME" == "$BEST_MTIME" && "$DIR_MTIME" != "0" ]]; then
      if [[ "$cdir" > "$BEST_DIR" ]]; then
        BEST_DIR="$cdir"
        BEST_REASON="$DIR_REASON"
      fi
      TIE_WARNING="Warning: timestamps tied between candidates. Used deterministic tie-breaker (lexicographic path order)."
    fi
  done

  EVIDENCE_DIR="$BEST_DIR"
  SELECTION_MODE="auto_latest"
  SELECTION_REASON="${BEST_REASON:-latest_valid_modified_time}"
  SELECTED_MTIME="$(date -d "@$BEST_MTIME" -u '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || date -r "$BEST_MTIME" -u '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || echo "$BEST_MTIME")"

  echo "Auto-selected latest valid evidence dir: $EVIDENCE_DIR"
  if [[ -n "$TIE_WARNING" ]]; then
    echo "$TIE_WARNING"
  fi
fi

if [[ ! -d "$EVIDENCE_DIR" ]]; then
  echo "Evidence dir does not exist: $EVIDENCE_DIR" >&2
  exit 2
fi

# --- Validate selected evidence ---
if [[ "$SELECTION_MODE" == "explicit" ]]; then
  SELECTION_REASON="explicit_override"
  CANDIDATE_COUNT=0
  SELECTED_MTIME=""

  VRESULT="$(validate_candidate "$EVIDENCE_DIR")"
  VSTATUS="$(echo "$VRESULT" | cut -d'|' -f1)"
  VREASON="$(echo "$VRESULT" | cut -d'|' -f3)"

  if [[ "$VSTATUS" != "valid" ]]; then
    if [[ "$ALLOW_INCOMPLETE" == "true" ]]; then
      echo "Warning: selected evidence is incomplete: $VREASON"
      echo "Proceeding with --allow-incomplete-evidence (debug mode)."
      SELECTION_REASON="explicit_incomplete_override"
    else
      echo "Selected evidence is incomplete: $VREASON"
      echo ""
      echo "To use incomplete evidence for debugging:"
      echo "  $0 --evidence-dir $EVIDENCE_DIR --allow-incomplete-evidence"
      exit 2
    fi
  fi
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
  --selection-mode "${SELECTION_MODE:-auto_latest}" \
  --selection-reason "${SELECTION_REASON:-unknown}" \
  --candidate-count "$CANDIDATE_COUNT" \
  --rejected-candidate-count "$REJECTED_COUNT" \
  --selected-mtime "${SELECTED_MTIME:-}" \
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
# Capture listing once to avoid SIGPIPE from grep -q killing unzip under pipefail
ZIP_LISTING="$(unzip -Z1 "$OUT")"

# 1. Verify no unsafe files
BAD="$(echo "$ZIP_LISTING" | grep -E '(^|/)(__pycache__|node_modules|\.git|\.data|\.venv|venv|htmlcov|\.tox|\.coverage_reports)(/|$)|\.pyc$|\.pyo$|(^|/)\.env($|\.)|\.log$|(^|/)\.coverage$|(^|/)coverage\.xml$' || true)"
if [[ -n "$BAD" ]]; then
  echo "Unsafe file found in zip:"
  echo "$BAD"
  rm -f "$OUT"
  exit 1
fi

# 2. Verify no raw evidence paths leaked
LEAKED="$(echo "$ZIP_LISTING" | grep -E '^(tmp/|home/|Users/|private/|mnt/|remedy-job-evidence-)' || true)"
if [[ -n "$LEAKED" ]]; then
  echo "Local path structure leaked into zip:"
  echo "$LEAKED"
  rm -f "$OUT"
  exit 1
fi

# 3. Verify manifest content against zip
VERIFY_ERRORS=""

for AGENT_FILE in .agent/live_review.md .agent/plan.md .agent/review_protocol.md; do
  MANIFEST_STATUS="$(python3 -c "
import json, sys
m = json.load(open('$MANIFEST'))
print(m.get('agent_state', {}).get('$AGENT_FILE', 'absent'))
" 2>/dev/null || echo "error")"
  if [[ "$MANIFEST_STATUS" == "present" ]]; then
    if ! echo "$ZIP_LISTING" | grep -qF "$AGENT_FILE"; then
      VERIFY_ERRORS="${VERIFY_ERRORS}Manifest says $AGENT_FILE present but missing from zip\n"
    fi
  fi
done

if python3 -c "import json; m=json.load(open('$MANIFEST')); exit(0 if m.get('current_evidence') else 1)" 2>/dev/null; then
  EXPECTED_EVIDENCE="$(python3 -c "
import json, sys
m = json.load(open('$MANIFEST'))
ce = m.get('current_evidence', {})
for name, status in ce.get('root_artifacts', {}).items():
    if status == 'present':
        print(f'evidence/current/{name}')
" 2>/dev/null || true)"
  while read -r expected; do
    [[ -z "$expected" ]] && continue
    if ! echo "$ZIP_LISTING" | grep -qF "$expected"; then
      VERIFY_ERRORS="${VERIFY_ERRORS}Manifest says $expected present but missing from zip\n"
    fi
  done <<< "$EXPECTED_EVIDENCE"
fi

STALE_EV="$(echo "$ZIP_LISTING" | grep -E '^remedy-job-evidence-' || true)"
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
echo "Included files: $(echo "$ZIP_LISTING" | wc -l | tr -d ' ')"
echo "Branch: $BRANCH"
echo "Commit: $COMMIT"
echo "Evidence: $CURRENT_PREFIX/"
