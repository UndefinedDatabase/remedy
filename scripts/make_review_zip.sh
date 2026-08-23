#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

STAMP="$(date +%Y%m%d-%H%M%S)"

# --- Publication target (package-hygiene amendment, 2026-08-23) ---
# Finished packages are OPERATOR artifacts, not repository state, so they are published to a
# sibling archive instead of the repository root. Two failures came from publishing into the root:
# a worker cleaning up with `glob('remedy-review-*.zip')` reached ~78 of them, and every package
# showed up in `git status` as an 80 MB untracked file. REMEDY_REVIEW_DIR redirects the target; a
# RELATIVE value resolves against the repository root, which is how the test suites point the
# pipeline at their own mini repository instead of the operator's archive.
if [[ -z "${REMEDY_REVIEW_DIR:-}" ]]; then
  if [[ -z "${HOME:-}" ]]; then
    echo "REVIEW_ZIP_ERROR: neither REMEDY_REVIEW_DIR nor HOME is set; cannot resolve the" >&2
    echo "package target directory. Set REMEDY_REVIEW_DIR explicitly." >&2
    exit 2
  fi
  REMEDY_REVIEW_DIR="$HOME/Repos/remedy-history/zips"
fi
case "$REMEDY_REVIEW_DIR" in
  /*) ;;
  *) REMEDY_REVIEW_DIR="$ROOT/$REMEDY_REVIEW_DIR" ;;
esac
mkdir -p "$REMEDY_REVIEW_DIR"

# Round 34 F1: there is NO public intermediate ZIP. The Python coordinator derives the exact
# status-bearing final path from the verified in-memory manifest and publishes its private `.part`
# DIRECTLY to it. This shell never creates, deletes, validates or renames a public temporary ZIP; it
# only passes the final-name TEMPLATE (with a {package_status} placeholder) and trusts the coordinator's
# verified JSON result. The single publication and all Git/publication decisions live in `safe_publish`.
FINAL_TEMPLATE="${REMEDY_REVIEW_DIR}/remedy-review-${STAMP}-{package_status}.zip"

# F3 (round 29) collision safety for the ONE remaining root scratch path this invocation writes — the
# root manifest. NEVER delete or overwrite a TRACKED project file that collides with it — refuse loudly
# (exit 3) and leave it byte-identical. The ZIP output is no longer a shell-managed path (the coordinator
# owns its single atomic publication), so no ZIP collision guard lives here.
_refuse_tracked_output() {
  local path="$1" what="$2"
  if git ls-files --error-unmatch -- "$path" >/dev/null 2>&1; then
    echo "REVIEW_ZIP_ERROR: refusing to $what tracked project file '$path' (packaging output collision)" >&2
    exit 3
  fi
}
_refuse_tracked_output ".review_zip_manifest.json" "reserve/delete as its root manifest"

# Parse arguments
EVIDENCE_DIR=""
SELECTION_MODE=""
REQUESTED_JOB_ID=""
INCLUDE_RECENT=0
HISTORY_ENTRIES=""
SELECTED_JOB_ID=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --evidence-dir)
      EVIDENCE_DIR="$2"
      SELECTION_MODE="explicit"
      shift 2
      ;;
    --job-id)
      REQUESTED_JOB_ID="$2"
      shift 2
      ;;
    --include-recent)
      INCLUDE_RECENT="$2"
      shift 2
      ;;
    --allow-incomplete-evidence|--allow-blocked-alignment)
      echo "NOTE: $1 is now a no-op — zip always builds. Alignment/validity warnings are printed but never block."
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

# Alignment/validity checks are warnings only — zip always builds.

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
  # --- Index-driven selection (never by filesystem mtime) ---
  SELECT_OUT="$(python3 scripts/select_review_evidence.py --repo "$ROOT" --job-id "$REQUESTED_JOB_ID" --include-recent "$INCLUDE_RECENT" 2>/dev/null || true)"
  SEL_STATUS="$(echo "$SELECT_OUT" | sed -n 's/^STATUS=//p')"
  SEL_JOB_ID="$(echo "$SELECT_OUT" | sed -n 's/^JOB_ID=//p')"
  SEL_DIR="$(echo "$SELECT_OUT" | sed -n 's/^EVIDENCE_DIR=//p')"
  SEL_REASON="$(echo "$SELECT_OUT" | sed -n 's/^REASON=//p')"
  HISTORY_ENTRIES="$(echo "$SELECT_OUT" | sed -n 's/^HISTORY=//p')"

  if [[ "$SEL_STATUS" == "selected" && -n "$SEL_DIR" && -d "$SEL_DIR" ]]; then
    EVIDENCE_DIR="$SEL_DIR"
    SELECTED_JOB_ID="$SEL_JOB_ID"
    SELECTION_MODE="indexed"
    SELECTION_REASON="$SEL_REASON"
    echo "Selected evidence job: $SEL_JOB_ID"
    echo "  evidence dir: $SEL_DIR"
    echo "  reason:       $SEL_REASON"
  elif [[ -n "$REQUESTED_JOB_ID" ]]; then
    # An explicit job id must never be silently substituted. Try to export it.
    echo "No indexed evidence for job $REQUESTED_JOB_ID ($SEL_REASON) — exporting it now."
    if python3 -m apps.cli.grouped do job-evidence "$REQUESTED_JOB_ID" --json >/dev/null 2>&1; then
      SELECT_OUT="$(python3 scripts/select_review_evidence.py --repo "$ROOT" --job-id "$REQUESTED_JOB_ID" --include-recent "$INCLUDE_RECENT" 2>/dev/null || true)"
      SEL_STATUS="$(echo "$SELECT_OUT" | sed -n 's/^STATUS=//p')"
      SEL_DIR="$(echo "$SELECT_OUT" | sed -n 's/^EVIDENCE_DIR=//p')"
      HISTORY_ENTRIES="$(echo "$SELECT_OUT" | sed -n 's/^HISTORY=//p')"
    fi
    if [[ "$SEL_STATUS" == "selected" && -n "$SEL_DIR" && -d "$SEL_DIR" ]]; then
      EVIDENCE_DIR="$SEL_DIR"
      SELECTED_JOB_ID="$REQUESTED_JOB_ID"
      SELECTION_MODE="indexed_exported"
      SELECTION_REASON="explicit_job_id_exported"
      echo "Exported and selected evidence for job $REQUESTED_JOB_ID"
    else
      echo "Requested job $REQUESTED_JOB_ID has no usable evidence; refusing to substitute another job." >&2
      SELECTION_MODE="none"
      SELECTION_REASON="requested_job_unavailable"
    fi
  fi
fi

if [[ -z "$EVIDENCE_DIR" && -z "$REQUESTED_JOB_ID" ]]; then
  # --- Deprecated root-style evidence directories: hard-refuse ---
  # Legacy remedy-job-evidence-* dirs in the repo root are deprecated. Silently
  # picking one by mtime risks selecting the wrong feature's evidence. Use
  # --evidence-dir or --job-id for explicit selection.
  LEGACY_COUNT="$(find . -maxdepth 1 -type d -name 'remedy-job-evidence-*' 2>/dev/null | wc -l)"
  if [[ "$LEGACY_COUNT" -gt 0 ]]; then
    echo "WARNING: $LEGACY_COUNT deprecated remedy-job-evidence-* dir(s) in repo root — IGNORED." >&2
    echo "Auto-selection from root dirs is disabled (cannot distinguish features)." >&2
    echo "To use one: --evidence-dir <path>. To index: 'do job-evidence'." >&2
  fi
  echo "No matching review evidence exists for the current branch/worktree."
  echo "This is a code snapshot, not a final review package."
  SELECTION_MODE="none"
  SELECTION_REASON="${SELECTION_REASON:-no_matching_evidence}"
fi

if [[ -n "$EVIDENCE_DIR" && ! -d "$EVIDENCE_DIR" ]]; then
  echo "Evidence dir does not exist: $EVIDENCE_DIR" >&2
  exit 2
fi

# --- Set selection metadata ---
if [[ "$SELECTION_MODE" == "explicit" ]]; then
  SELECTION_REASON="explicit_override"
  CANDIDATE_COUNT=0
  SELECTED_MTIME=""
fi

TMP="$(mktemp)"
TMP0="$(mktemp)"        # NUL-delimited repo file list (F8, round 17)
TMP_EV0="$(mktemp)"     # NUL-delimited evidence file list
MANIFEST=".review_zip_manifest.json"
rm -f "$MANIFEST"
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
    -path './.agent/Evidence' -o \
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
    -path './.remedy-wt' -o \
    -path './*/.remedy-wt' -o \
    "${EVIDENCE_EXCLUDE_ARGS[@]}" \
    -false \
  \) -prune -o \
  \( -type f -o -type l -o -type p -o -type s -o -type b -o -type c \) \
  ! -name '.coverage' \
  ! -name '.coverage.*' \
  ! -name 'coverage.xml' \
  ! -name '*.pyc' \
  ! -name '*.pyo' \
  ! -name 'run_transcript.txt' \
  ! -name '.review_zip_manifest.json' \
  -print0 \
  | sed -z 's#^\./##' \
  | sort -z -u > "$TMP0"
# F8 (round 17): the repo file list is NUL-delimited so a filename containing a newline survives
# into the archive. `$TMP` (newline) stays for the manifest/alignment steps, which only ever see
# ordinary source paths.
tr '\0' '\n' < "$TMP0" > "$TMP"

# F1 (round 20): SAFE EVIDENCE SNAPSHOT PRECEDES EVERY EVIDENCE READ. Stage the Evidence to a
# private immutable snapshot FIRST — anchored, no-follow, hashed, bounded — and then validate,
# build the manifest, derive Subject/Proof/Gates and package ONLY the staged bytes. Nothing reads
# the original EVIDENCE_DIR again after this point.
# The private staging snapshot lives under the repo's gitignored .data/ so it stays CONTAINED
# within source_root (the manifest refuses evidence from outside the trusted root). It is still a
# fresh, private, immutable per-build directory, removed on exit.
mkdir -p "$ROOT/.data"
EVIDENCE_STAGING="$(mktemp -d "$ROOT/.data/review_staging.XXXXXX")"
trap 'rm -rf "$EVIDENCE_STAGING" "$TMP" "$TMP0" "$TMP_EV0" "$MANIFEST"' EXIT

CURRENT_PREFIX="evidence/current"
OBS_INDEX_NAME="self_run_observability_index.json"
OBS_INDEX_STAGED=""
STAGED_CURRENT="$EVIDENCE_STAGING/$CURRENT_PREFIX"

if [[ -n "$EVIDENCE_DIR" ]]; then
  mkdir -p "$STAGED_CURRENT"

  # F1/F3/F9/F10 (round 20): typed no-follow snapshot. Copies once, hashes each staged member into
  # evidence_snapshot_inventory.json, and enforces count/aggregate limits DURING the walk. A
  # symlink/FIFO/device or an over-limit tree BLOCKS before the rest is copied.
  if ! python3 scripts/stage_review_evidence.py stage \
       --src "$EVIDENCE_DIR" --dest "$STAGED_CURRENT" --inventory-out "$STAGED_CURRENT" >/dev/null; then
    echo "Evidence staging refused an unsafe or over-limit member in $EVIDENCE_DIR." >&2
    exit 2
  fi

  # --- F018 Scope 2: refresh derivable gates in the STAGED copy (after staging,
  #     before manifest). Ensures the packaged runtime gate matches production v1.1.0. ---
  if [[ -f "scripts/refresh_review_evidence.py" ]]; then
    if python3 scripts/refresh_review_evidence.py \
         --staged-dir "$STAGED_CURRENT" --repo-root "$ROOT"; then
      echo "Evidence refresh completed for staged copy."
    else
      echo "WARNING: Evidence refresh failed for staged copy." >&2
    fi
  fi

  # --- Observability index generated from the STAGED bytes (F1, round 20) ---
  OBS_INDEX_STAGED="$STAGED_CURRENT/$OBS_INDEX_NAME"
  if [[ -f "scripts/build_observability_index.py" ]]; then
    if python3 scripts/build_observability_index.py \
         --evidence-dir "$STAGED_CURRENT" \
         --output "$OBS_INDEX_STAGED" >/dev/null 2>&1; then
      echo "Observability index generated from staged bytes: $CURRENT_PREFIX/$OBS_INDEX_NAME"
    else
      echo "Warning: observability index generation failed for staged evidence" >&2
    fi
  else
    echo "Warning: scripts/build_observability_index.py not found; index not generated" >&2
  fi

  # --- Supplemental history (context only; never affects package status) — also staged safely ---
  if [[ -n "$HISTORY_ENTRIES" ]]; then
    IFS=',' read -r -a _HIST <<< "$HISTORY_ENTRIES"
    for entry in "${_HIST[@]}"; do
      [[ -z "$entry" ]] && continue
      h_job="${entry%%:*}"
      h_dir="${entry#*:}"
      [[ -z "$h_job" || -z "$h_dir" || ! -d "$h_dir" ]] && continue
      [[ "$h_job" == "$SELECTED_JOB_ID" ]] && continue   # never duplicate current
      h_prefix="evidence/history/$h_job"
      mkdir -p "$EVIDENCE_STAGING/$h_prefix"
      if ! python3 scripts/stage_review_evidence.py stage \
           --src "$h_dir" --dest "$EVIDENCE_STAGING/$h_prefix" >/dev/null; then
        echo "History staging refused an unsafe member in $h_dir." >&2
        exit 2
      fi
      echo "Included supplemental history: $h_prefix (context only)"
    done
  fi
fi

# --- The EXACT repo-root outputs THIS invocation generates (F3, round 29 / F1, round 34) ---
# The only packaging output that can appear in `git status` at manifest-build time is the root
# manifest; the status-bearing final ZIP is published only at the very end, by the coordinator, and a
# `remedy-review-*.zip` name is excluded from the dirty source set anyway. The authoritative manifest is
# rebuilt by build_review_zip.py, which DERIVES every candidate final ZIP path internally from the
# final-name template + --manifest-rel.
GENERATED_OUTPUT_ARGS=(
  --generated-output "$MANIFEST"
)

# --- Build manifest from the STAGED snapshot (F1/F8, round 20) — never the original EVIDENCE_DIR ---
MANIFEST_EVIDENCE_ARG=""
if [[ -n "$EVIDENCE_DIR" ]]; then
  MANIFEST_EVIDENCE_ARG="$STAGED_CURRENT"
fi
python3 scripts/build_review_manifest.py \
  --evidence-dir "${MANIFEST_EVIDENCE_ARG}" \
  --selection-mode "${SELECTION_MODE:-none}" \
  --selection-reason "${SELECTION_REASON:-no_evidence_available}" \
  --candidate-count "$CANDIDATE_COUNT" \
  --rejected-candidate-count "$REJECTED_COUNT" \
  --selected-mtime "${SELECTED_MTIME:-}" \
  "${GENERATED_OUTPUT_ARGS[@]}" \
  --output "$MANIFEST"

echo "$MANIFEST" >> "$TMP"

# --- Check alignment verdict ---
ALIGNMENT_VERDICT="$(python3 -c "
import json, sys
try:
    m = json.load(open('$MANIFEST'))
    a = m.get('review_subject_evidence_alignment', {})
    print(a.get('verdict', 'absent'))
except:
    print('absent')
" 2>/dev/null || echo "absent")"

if [[ "$ALIGNMENT_VERDICT" == "BLOCKED" ]]; then
  echo "WARNING: Review subject/evidence alignment is BLOCKED."
  echo "Dirty files outside evidence scope will be included for reviewer visibility."
fi

# --- Check evidence validity ---
EVIDENCE_VALID="$(python3 -c "
import json, sys
try:
    m = json.load(open('$MANIFEST'))
    ce = m.get('current_evidence', {})
    v = ce.get('validation', {})
    print('true' if v.get('is_valid_current_run') else 'false')
except:
    print('false')
" 2>/dev/null || echo "false")"

if [[ "$EVIDENCE_VALID" == "false" && -n "$EVIDENCE_DIR" ]]; then
  echo "WARNING: Evidence validation failed (is_valid_current_run=false)."
  echo "Zip will be built anyway — reviewer will see validation status in manifest."
fi

# --- The staged evidence file list (typed no-follow walk of the snapshot; includes the manifest
#     is NOT here — the manifest is a repo-root member). Built AFTER the manifest so the list is
#     complete for the archive builder. ---
if [[ -n "$EVIDENCE_DIR" ]]; then
  if ! python3 scripts/stage_review_evidence.py list \
       --root "$EVIDENCE_STAGING" --nul-out "$TMP_EV0" --text-out "$TMP_EV0.txt"; then
    echo "Evidence staging tree contains an unsafe member." >&2
    exit 2
  fi
  cat "$TMP_EV0.txt" >> "$TMP"
  rm -f "$TMP_EV0.txt"
fi

sort -u "$TMP" -o "$TMP"

# --- Create zip (round 20 two-phase, directed hash chain) ---
# Phase 1 snapshots every source member; phases 2-3 emit the directed chain
# (plan -> expectation -> manifest) as in-memory bytes; phase 4 builds the deterministic ZIP from
# the immutable bytes; phase 5 reopens and verifies; phase 6 publishes the verified private `.part`
# directly to the status-bearing final path. Subject/Proof are STAGED bytes. There is NO public
# intermediate ZIP, so nothing is deleted or renamed here.
cd "$ROOT"

EV_ROOT_ARG=""
EV_FILES_ARG=""
if [[ -n "$EVIDENCE_DIR" ]]; then
  EV_ROOT_ARG="$EVIDENCE_STAGING"
  EV_FILES_ARG="$TMP_EV0"
fi

# Round 20: Subject, Content-Proof and the generated plan all live in the STAGED snapshot, never
# the original EVIDENCE_DIR.
SUBJECT_JSON_ARG=""
CONTENT_PROOF_ARG=""
PLAN_OUT_ARG=""
if [[ -n "$EVIDENCE_DIR" && -f "$STAGED_CURRENT/review_subject.json" ]]; then
  SUBJECT_JSON_ARG="$STAGED_CURRENT/review_subject.json"
fi
if [[ -n "$EVIDENCE_DIR" && -f "$STAGED_CURRENT/current_change_content_proof.json" ]]; then
  CONTENT_PROOF_ARG="$STAGED_CURRENT/current_change_content_proof.json"
fi
if [[ -n "$EV_ROOT_ARG" ]]; then
  PLAN_OUT_ARG="$STAGED_CURRENT/review_archive_plan.json"
  # Stale plan from a prior zip build may have been copied during evidence
  # staging. Delete it — build_review_zip.py generates a fresh one at this
  # path. Reading a stale plan causes hash mismatches.
  rm -f "$PLAN_OUT_ARG"
fi

# F6/F7 (round 21): capture build_review_zip's verified-model result (package_status,
# evidence_authoritative, review_subject_alignment, manifest sha) so the final filename and status
# come from the VERIFIED package, never a post-build reread of the mutable disk manifest.
BUILD_RESULT="$(python3 scripts/build_review_zip.py \
  --final-template "$FINAL_TEMPLATE" \
  --repo-root "$ROOT" \
  --repo-files0 "$TMP0" \
  --evidence-root "$EV_ROOT_ARG" \
  --evidence-files0 "$EV_FILES_ARG" \
  --subject-json "$SUBJECT_JSON_ARG" \
  --content-proof-json "$CONTENT_PROOF_ARG" \
  --current-prefix "$CURRENT_PREFIX" \
  --plan-out "$PLAN_OUT_ARG" \
  --manifest-rel "$MANIFEST" \
  --manifest-disk "$MANIFEST" \
  --selection-mode "${SELECTION_MODE:-none}" \
  --selection-reason "${SELECTION_REASON:-no_evidence_available}" \
  --candidate-count "$CANDIDATE_COUNT" \
  --rejected-candidate-count "$REJECTED_COUNT" \
  --selected-mtime "${SELECTED_MTIME:-}")" || BUILD_RC=$?
BUILD_RC="${BUILD_RC:-0}"
echo "$BUILD_RESULT"
if [[ "$BUILD_RC" -ne 0 ]]; then
  echo "REVIEW_ZIP_ERROR: coordinator failed to build/publish the review ZIP (exit $BUILD_RC)." >&2
  echo "No public intermediate ZIP was created; nothing to clean up." >&2
  exit "$BUILD_RC"
fi

# --- Trust ONLY the coordinator's verified JSON result (F1, round 34) ---
# The coordinator already published its verified private `.part` DIRECTLY to the exact status-bearing
# final path (a single atomic no-replace link, source bytes bound to the verified SHA-256) and returned
# that path + SHA. This shell derives no filename, publishes nothing, and renames nothing. Every check
# below is READ-ONLY against the returned final path; a failure never deletes or alters the package.
_result_field() { BR="$BUILD_RESULT" python3 -c "import json,os,sys; print(json.loads(os.environ['BR']).get(sys.argv[1],''))" "$1"; }
PACKAGE_STATUS="$(_result_field package_status)"; PACKAGE_STATUS="${PACKAGE_STATUS:-UNKNOWN}"
EVIDENCE_AUTH="$(BR="$BUILD_RESULT" python3 -c "import json,os; print('true' if json.loads(os.environ['BR']).get('evidence_authoritative') else 'false')")"
_ALIGN_FROM_RESULT="$(_result_field review_subject_alignment)"
ALIGNMENT_VERDICT="${_ALIGN_FROM_RESULT:-$ALIGNMENT_VERDICT}"
OUT="$(_result_field final_path)"
FINAL_SHA="$(_result_field final_sha256)"
# The coordinator returns a repository-relative path when it published INSIDE the repository and an
# absolute one when it published to the archive outside it. Resolve both to the one full path every
# status line and every read-only check below names, so the operator is never shown a bare filename
# they then have to guess the directory for.
if [[ "$OUT" == /* ]]; then
  ZIP_FULL_PATH="$OUT"
else
  ZIP_FULL_PATH="${ROOT}/${OUT}"
fi

if [[ -z "$OUT" || ! -f "$ZIP_FULL_PATH" ]]; then
  echo "REVIEW_ZIP_ERROR: coordinator reported no published ZIP (final_path='$OUT')." >&2
  exit 3
fi
# The published ZIP must be the exact bytes the coordinator verified before publication.
ACTUAL_SHA="$(sha256sum "$ZIP_FULL_PATH" | awk '{print $1}')"
if [[ -n "$FINAL_SHA" && "$ACTUAL_SHA" != "$FINAL_SHA" ]]; then
  echo "REVIEW_ZIP_ERROR: published ZIP sha256 ($ACTUAL_SHA) != coordinator-verified sha256 ($FINAL_SHA)." >&2
  exit 3
fi

# --- Read-only post-publication checks against the exact published final path ---
# The coordinator already verified typed membership and hashes; these are a defensive, READ-ONLY
# re-scan of the published ZIP. On any problem the shell exits non-zero and reports it, but NEVER
# deletes or rewrites the published, coordinator-verified package.
ZIP_LISTING="$(unzip -Z1 "$ZIP_FULL_PATH")"

BAD="$(echo "$ZIP_LISTING" | grep -E '(^|/)(__pycache__|node_modules|\.git|\.data|\.venv|venv|htmlcov|\.tox|\.coverage_reports|\.remedy-wt)(/|$)|\.pyc$|\.pyo$|(^|/)\.env($|\.)|\.log$|(^|/)\.coverage$|(^|/)coverage\.xml$' || true)"
if [[ -n "$BAD" ]]; then
  echo "REVIEW_ZIP_ERROR: unsafe file found in published zip (not deleting the coordinator-verified package):"
  echo "$BAD"
  exit 1
fi

LEAKED="$(echo "$ZIP_LISTING" | grep -E '^(tmp/|home/|Users/|private/|mnt/|remedy-job-evidence-)' || true)"
if [[ -n "$LEAKED" ]]; then
  echo "REVIEW_ZIP_ERROR: local path structure leaked into published zip:"
  echo "$LEAKED"
  exit 1
fi

VERIFY_ERRORS=""
for AGENT_FILE in .agent/live_review.md .agent/plan.md .agent/review_protocol.md; do
  MANIFEST_STATUS="$(python3 -c "
import json, sys
m = json.load(open('$MANIFEST'))
print(m.get('agent_state', {}).get('$AGENT_FILE', 'absent'))
" 2>/dev/null || echo "error")"
  if [[ "$MANIFEST_STATUS" == "present" ]]; then
    if ! grep -qF "$AGENT_FILE" <<< "$ZIP_LISTING"; then
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
    if ! grep -qF "$expected" <<< "$ZIP_LISTING"; then
      VERIFY_ERRORS="${VERIFY_ERRORS}Manifest says $expected present but missing from zip\n"
    fi
  done <<< "$EXPECTED_EVIDENCE"
fi

STALE_EV="$(echo "$ZIP_LISTING" | grep -E '^remedy-job-evidence-' || true)"
if [[ -n "$STALE_EV" ]]; then
  VERIFY_ERRORS="${VERIFY_ERRORS}Stale evidence dir included in zip: $STALE_EV\n"
fi

if [[ -n "$EVIDENCE_DIR" ]]; then
  if [[ -n "$OBS_INDEX_STAGED" && -f "$OBS_INDEX_STAGED" ]]; then
    if ! grep -qF "$CURRENT_PREFIX/$OBS_INDEX_NAME" <<< "$ZIP_LISTING"; then
      VERIFY_ERRORS="${VERIFY_ERRORS}Observability index generated but missing from zip: $CURRENT_PREFIX/$OBS_INDEX_NAME\n"
    fi
  else
    VERIFY_ERRORS="${VERIFY_ERRORS}Observability index not generated: $CURRENT_PREFIX/$OBS_INDEX_NAME\n"
  fi
fi

if [[ -n "$VERIFY_ERRORS" ]]; then
  echo "REVIEW_ZIP_ERROR: read-only post-publication verification failed (package left intact):"
  echo -e "$VERIFY_ERRORS"
  exit 1
fi

BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
COMMIT="$(git rev-parse HEAD 2>/dev/null || echo unknown)"

# --- Terminal status block ---
echo
echo "============================================"
echo "REVIEW_PACKAGE_CREATED=true"
echo "PACKAGE_STATUS=${PACKAGE_STATUS}"
echo "PACKAGING_CWD=$(pwd)"
echo "EVIDENCE_DIR=${EVIDENCE_DIR:-(none)}"
echo "REVIEW_SUBJECT_ALIGNMENT=${ALIGNMENT_VERDICT}"
echo "EVIDENCE_AUTHORITATIVE=${EVIDENCE_AUTH}"
echo "REVIEW_PACKAGE_DIR=${REMEDY_REVIEW_DIR}"
echo "ZIP_PATH=${ZIP_FULL_PATH}"
if [[ "$PACKAGE_STATUS" != "READY_FOR_REVIEW" ]]; then
  echo "DO_NOT_COMMIT=true"
  echo "============================================"
  echo
  echo "*** ZIP CREATED, BUT THIS PACKAGE IS NOT COMMIT-READY ***"
  echo
else
  echo "============================================"
  echo
  echo "ZIP CREATED AND READY FOR FINAL REVIEW"
  echo
fi

du -h "$ZIP_FULL_PATH"
echo "Included files: $(echo "$ZIP_LISTING" | wc -l | tr -d ' ')"
echo "Branch: $BRANCH"
echo "Commit: $COMMIT"
if [[ -n "$EVIDENCE_DIR" ]]; then
  echo "Evidence: $CURRENT_PREFIX/"
else
  echo "Evidence: (none)"
fi
