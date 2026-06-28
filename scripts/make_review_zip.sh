#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

STAMP="$(date +%Y%m%d-%H%M%S)"
OUT="remedy-review-${STAMP}.zip"
EVIDENCE_DIR="${1:-}"

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
    -path './*/.ruff_cache' -o \
    -path './htmlcov' -o \
    -path './*/htmlcov' -o \
    -path './.tox' -o \
    -path './*/.tox' -o \
    -path './.coverage_reports' -o \
    -path './*/.coverage_reports' \
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

BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
COMMIT="$(git rev-parse HEAD 2>/dev/null || echo unknown)"
DIRTY="$(git status --porcelain 2>/dev/null | head -20 || echo unknown)"

# --- Build observability artifact checklist ---
_check() { if [[ -f "$1" ]]; then echo "present"; else echo "absent"; fi; }

AGENT_LIVE_REVIEW="$(_check ".agent/live_review.md")"
AGENT_PLAN="$(_check ".agent/plan.md")"
AGENT_REVIEW_PROTOCOL="$(_check ".agent/review_protocol.md")"

# Evidence dir artifacts (optional — only checked when evidence dir provided)
EV_JOB_FLOW="absent_no_evidence_dir"
EV_AGENT_TRACE="absent_no_evidence_dir"
EV_AGENT_TRACE_SUMMARY="absent_no_evidence_dir"
EV_PROMPT_TRACE_SUMMARY="absent_no_evidence_dir"
EV_MANIFEST="absent_no_evidence_dir"

if [[ -n "$EVIDENCE_DIR" && -d "$EVIDENCE_DIR" ]]; then
  EV_JOB_FLOW="$(_check "$EVIDENCE_DIR/job_flow.json")"
  EV_AGENT_TRACE="$(_check "$EVIDENCE_DIR/agent_run_trace.jsonl")"
  EV_AGENT_TRACE_SUMMARY="$(_check "$EVIDENCE_DIR/agent_run_trace_summary.json")"
  EV_PROMPT_TRACE_SUMMARY="$(_check "$EVIDENCE_DIR/prompt_trace_summary.json")"
  EV_MANIFEST="$(_check "$EVIDENCE_DIR/manifest.json")"

  # Include evidence dir files in zip (under evidence/ prefix)
  if [[ -d "$EVIDENCE_DIR" ]]; then
    find "$EVIDENCE_DIR" -type f \
      ! -name '*.pyc' ! -name '*.pyo' \
      -print \
      | sort -u >> "$TMP"
    sort -u "$TMP" -o "$TMP"
  fi
fi

# Task run artifacts (scan evidence dir for task_runs/)
TASK_RUN_ARTIFACTS="[]"
if [[ -n "$EVIDENCE_DIR" && -d "$EVIDENCE_DIR/task_runs" ]]; then
  TASK_RUN_ARTIFACTS="["
  FIRST=true
  for task_dir in "$EVIDENCE_DIR/task_runs"/*/; do
    [[ -d "$task_dir" ]] || continue
    task_name="$(basename "$task_dir")"
    $FIRST || TASK_RUN_ARTIFACTS+=","
    FIRST=false
    TASK_RUN_ARTIFACTS+="{"
    TASK_RUN_ARTIFACTS+="\"task\":\"$task_name\""
    TASK_RUN_ARTIFACTS+=",\"prompt_trace\":\"$(_check "${task_dir}prompt_trace.jsonl")\""
    TASK_RUN_ARTIFACTS+=",\"prompt_trace_summary\":\"$(_check "${task_dir}prompt_trace_summary.json")\""
    TASK_RUN_ARTIFACTS+=",\"review\":\"$(_check "${task_dir}review.json")\""
    TASK_RUN_ARTIFACTS+=",\"repair_loop\":\"$(_check "${task_dir}repair_loop.json")\""
    TASK_RUN_ARTIFACTS+=",\"token_accounting\":\"$(_check "${task_dir}token_accounting.json")\""
    TASK_RUN_ARTIFACTS+=",\"provider_evidence\":\"$(_check "${task_dir}provider_evidence.json")\""
    TASK_RUN_ARTIFACTS+="}"
  done
  TASK_RUN_ARTIFACTS+="]"
fi

cat > "$MANIFEST" <<MANIFEST_EOF
{
  "bundle_kind": "remedy_review_zip",
  "bundle_version": 6,
  "generated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "branch": "$BRANCH",
  "commit": "$COMMIT",
  "dirty_files": $(echo "$DIRTY" | python3 -c 'import sys,json; print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))' 2>/dev/null || echo '[]'),
  "evidence_dir": "$(echo "$EVIDENCE_DIR")",
  "policy": "Includes whole relevant project folders, tracked and untracked. Excludes .git, .data, node_modules, caches, build outputs, env files, private keys, logs, old archives.",
  "required_observability_artifacts": {
    "agent_state": {
      ".agent/live_review.md": "$AGENT_LIVE_REVIEW",
      ".agent/plan.md": "$AGENT_PLAN",
      ".agent/review_protocol.md": "$AGENT_REVIEW_PROTOCOL"
    },
    "evidence_root": {
      "job_flow.json": "$EV_JOB_FLOW",
      "agent_run_trace.jsonl": "$EV_AGENT_TRACE",
      "agent_run_trace_summary.json": "$EV_AGENT_TRACE_SUMMARY",
      "prompt_trace_summary.json": "$EV_PROMPT_TRACE_SUMMARY",
      "manifest.json": "$EV_MANIFEST"
    },
    "task_runs": $TASK_RUN_ARTIFACTS
  }
}
MANIFEST_EOF

echo "$MANIFEST" >> "$TMP"
sort -u "$TMP" -o "$TMP"

# Fail fast on known debug/test detritus in repo root
DETRITUS="$(find . -maxdepth 1 -name '*_WAS_HERE.txt' -o -name 'BUILDER_WAS_HERE.txt' -o -name 'REVIEWER_WAS_HERE.txt' 2>/dev/null | sed 's#^\./##' || true)"
if [[ -n "$DETRITUS" ]]; then
  echo "Debug/test detritus found in repo root — remove before review zip:"
  echo "$DETRITUS"
  exit 1
fi

rm -f "$OUT"
zip -q -@ "$OUT" < "$TMP"

BAD="$(unzip -Z1 "$OUT" | grep -E '(^|/)(__pycache__|node_modules|\.git|\.data|\.venv|venv|htmlcov|\.tox|\.coverage_reports)(/|$)|\.pyc$|\.pyo$|(^|/)\.env($|\.)|\.log$|(^|/)\.coverage$|(^|/)coverage\.xml$' || true)"
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
if [[ -n "$EVIDENCE_DIR" ]]; then
  echo "Evidence dir: $EVIDENCE_DIR"
fi
