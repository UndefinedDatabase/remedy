#!/usr/bin/env bash
set -euo pipefail

# Worker/Remedy self-job-flow starter
#
# Runs Remedy against its own repo using do job-flow.
# Produces evidence artifacts and a review zip for final reviewer.
#
# Usage:
#   scripts/remedy_self_job_flow.sh --goal-file <path> [options]
#
# Options:
#   --goal-file <path>    Job/goal markdown file (required)
#   --out <path>          Evidence output dir (default: .data/self-runs/<timestamp>/evidence)
#   --builder <name>      Builder provider (default: claude-cli)
#   --reviewer <name>     Reviewer provider (default: claude-cli)
#   --allow-dirty         Allow running with dirty git state
#   --dry-run             Print commands without executing
#   --json                Pass --json to job-flow for structured output
#
# This script will NEVER:
#   - approve, apply, commit, push, merge, or delete branches
#   - mutate the target repo
#   - call external providers unless explicitly selected via --builder/--reviewer
#
# Next phase command (for Claude in Worker/Remedy mode):
#   scripts/remedy_self_job_flow.sh --goal-file <goal.md> --json

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

GOAL_FILE=""
OUT_DIR=""
BUILDER="claude-cli"
REVIEWER="claude-cli"
ALLOW_DIRTY=false
DRY_RUN=false
EXTRA_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --goal-file)
      GOAL_FILE="$2"
      shift 2
      ;;
    --out)
      OUT_DIR="$2"
      shift 2
      ;;
    --builder)
      BUILDER="$2"
      shift 2
      ;;
    --reviewer)
      REVIEWER="$2"
      shift 2
      ;;
    --allow-dirty)
      ALLOW_DIRTY=true
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --json)
      EXTRA_ARGS+=("--json")
      shift
      ;;
    -*)
      echo "Unknown option: $1" >&2
      echo "Usage: $0 --goal-file <path> [--out <dir>] [--builder <name>] [--reviewer <name>] [--allow-dirty] [--dry-run] [--json]" >&2
      exit 2
      ;;
    *)
      echo "Unexpected argument: $1" >&2
      exit 2
      ;;
  esac
done

if [[ -z "$GOAL_FILE" ]]; then
  echo "Error: --goal-file is required." >&2
  echo "Usage: $0 --goal-file <path> [--out <dir>] [--allow-dirty] [--dry-run] [--json]" >&2
  echo "" >&2
  echo "Create a goal file:" >&2
  echo "  echo '# Job: My Task' > goal.md" >&2
  echo "  echo '' >> goal.md" >&2
  echo "  echo '## Task 1' >> goal.md" >&2
  echo "  echo 'Description of what to do.' >> goal.md" >&2
  echo "  echo '' >> goal.md" >&2
  echo "  echo 'Acceptance:' >> goal.md" >&2
  echo "  echo '- criterion 1' >> goal.md" >&2
  exit 2
fi

if [[ ! -f "$GOAL_FILE" ]]; then
  echo "Error: goal file does not exist: $GOAL_FILE" >&2
  exit 2
fi

# --- Dirty state check ---
if [[ "$ALLOW_DIRTY" != "true" ]]; then
  DIRTY="$(git status --porcelain 2>/dev/null | head -5)"
  if [[ -n "$DIRTY" ]]; then
    echo "Error: dirty git state detected. Commit or stash changes first." >&2
    echo "  Or use --allow-dirty to proceed anyway." >&2
    echo "" >&2
    echo "Dirty files:" >&2
    echo "$DIRTY" >&2
    exit 1
  fi
fi

# --- Evidence dir ---
if [[ -z "$OUT_DIR" ]]; then
  STAMP="$(date +%Y%m%d-%H%M%S)"
  OUT_DIR="$ROOT/.data/self-runs/$STAMP/evidence"
fi

TRANSCRIPT_FILE="$(dirname "$OUT_DIR")/run_transcript.txt"

echo "=== Remedy self-job-flow ==="
echo "Goal file:    $GOAL_FILE"
echo "Evidence dir: $OUT_DIR"
echo "Builder:      $BUILDER"
echo "Reviewer:     $REVIEWER"
echo "Repo:         $ROOT"
echo

JOB_FLOW_CMD=(
  python3 -m apps.cli.grouped do job-flow
  --job-file "$GOAL_FILE"
  --repo "$ROOT"
  --builder "$BUILDER"
  --reviewer "$REVIEWER"
  --out "$OUT_DIR"
)
JOB_FLOW_CMD+=("${EXTRA_ARGS[@]}")

REVIEW_ZIP_CMD=(
  bash scripts/make_review_zip.sh --evidence-dir "$OUT_DIR"
)

if [[ "$DRY_RUN" == "true" ]]; then
  echo "[dry-run] Would execute:"
  echo "  ${JOB_FLOW_CMD[*]}"
  echo ""
  echo "[dry-run] Then:"
  echo "  ${REVIEW_ZIP_CMD[*]}"
  echo ""
  echo "[dry-run] Evidence would be written to: $OUT_DIR"
  echo "[dry-run] Transcript would be saved to: $TRANSCRIPT_FILE"
  echo ""
  echo "Next step: remove --dry-run to execute."
  exit 0
fi

mkdir -p "$(dirname "$TRANSCRIPT_FILE")"

echo "--- Step 1: Running job-flow ---"
"${JOB_FLOW_CMD[@]}" 2>&1 | tee "$TRANSCRIPT_FILE"

echo
echo "--- Step 2: Evidence artifacts ---"
find "$OUT_DIR" -type f | sort | while read -r f; do
  echo "  $(echo "$f" | sed "s|^$OUT_DIR/||")"
done

echo
echo "--- Step 3: Building review zip ---"
"${REVIEW_ZIP_CMD[@]}"

REVIEW_ZIP="$(ls -t "$ROOT"/remedy-review-*.zip 2>/dev/null | head -1 || true)"

echo
echo "=== Done ==="
echo "Evidence dir:    $OUT_DIR"
echo "Transcript:      $TRANSCRIPT_FILE"
if [[ -n "$REVIEW_ZIP" ]]; then
  echo "Review zip:      $REVIEW_ZIP"
fi
echo
echo "Next step: send the review zip to the final reviewer."
echo "  Do NOT approve, apply, commit, push, or merge."
