#!/usr/bin/env bash
set -euo pipefail

# Worker/Remedy self-job-flow starter
#
# Runs Remedy against its own repo using do job-flow with the fake provider.
# Produces evidence artifacts and a review zip for inspection.
#
# Usage:
#   scripts/remedy_self_job_flow.sh <job-file>
#   scripts/remedy_self_job_flow.sh <job-file> --json
#
# Example:
#   scripts/remedy_self_job_flow.sh jobs/sample.md
#   scripts/remedy_self_job_flow.sh jobs/sample.md --json

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

JOB_FILE="${1:?Usage: $0 <job-file> [--json]}"
shift

EXTRA_ARGS=("$@")

STAMP="$(date +%Y%m%d-%H%M%S)"
EVIDENCE_DIR="/tmp/remedy-job-evidence-selftest-${STAMP}"

echo "=== Remedy self-job-flow ==="
echo "Job file:     $JOB_FILE"
echo "Evidence dir: $EVIDENCE_DIR"
echo "Repo:         $ROOT"
echo

python3 -m apps.cli.grouped do job-flow \
  --job-file "$JOB_FILE" \
  --repo "$ROOT" \
  --builder fake \
  --reviewer fake \
  --out "$EVIDENCE_DIR" \
  "${EXTRA_ARGS[@]}"

echo
echo "=== Evidence artifacts ==="
find "$EVIDENCE_DIR" -type f | sort | while read -r f; do
  echo "  $(echo "$f" | sed "s|^$EVIDENCE_DIR/||")"
done

echo
echo "=== Review zip ==="
bash scripts/make_review_zip.sh --evidence-dir "$EVIDENCE_DIR"

echo
echo "=== Done ==="
echo "Evidence dir: $EVIDENCE_DIR"
echo "Inspect: cat $EVIDENCE_DIR/job_flow.json | python3 -m json.tool"
echo "Manifest: cat $EVIDENCE_DIR/command_transcript.json | python3 -m json.tool"
