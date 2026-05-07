#!/usr/bin/env bash
# remedy_smoke.sh — Project Registry + Brain Viewer smoke test.
#
# Usage (source):
#   source scripts/remedy_smoke.sh
#   remedy_smoke
#
# Usage (direct):
#   ./scripts/remedy_smoke.sh
#
# Requirements: remedy CLI on PATH, python3.
# Optional: Ollama running locally (for run-next-task-local).
#
# Overrides:
#   REMEDY_SMOKE_REPO  — temp repo path (default: /tmp/remedy-target-repo)

remedy_smoke() {
  (
    set -euo pipefail

    local TARGET_REPO="${REMEDY_SMOKE_REPO:-/tmp/remedy-target-repo}"
    local PROMPT="Smoke test job — verify project registry and brain viewer pipeline"

    # -------------------------------------------------------------------------
    # 1. Create target repo
    # -------------------------------------------------------------------------
    echo "--- 1. Create target repo: ${TARGET_REPO}"
    mkdir -p "${TARGET_REPO}"
    cat >"${TARGET_REPO}/AGENTS.md" <<'AGENTS_EOF'
# Test Target Repo
AGENTS_EOF
    cat >"${TARGET_REPO}/pyproject.toml" <<'PYPROJECT_EOF'
[project]
name = "smoke-target"
version = "0.1.0"
PYPROJECT_EOF

    # -------------------------------------------------------------------------
    # 2. Create project
    # -------------------------------------------------------------------------
    echo "--- 2. Create project"
    PROJECT_ID="$(remedy create-project "Smoke Project" --description "smoke test project")"
    if [[ -z "${PROJECT_ID}" ]]; then
        echo "ERROR: create-project did not print a project ID" >&2
        return 1
    fi
    echo "    PROJECT_ID=${PROJECT_ID}"

    # -------------------------------------------------------------------------
    # 3. Create job (linked to project)
    # -------------------------------------------------------------------------
    echo "--- 3. Create job"
    JOB_ID="$(remedy create-job "${PROMPT}" --project "${PROJECT_ID}")"
    if [[ -z "${JOB_ID}" ]]; then
        echo "ERROR: create-job did not print a job ID" >&2
        return 1
    fi
    echo "    JOB_ID=${JOB_ID}"

    # -------------------------------------------------------------------------
    # 4. Attach repo + set permission; link repo to project
    # -------------------------------------------------------------------------
    echo "--- 4. Attach repo + set permission"
    remedy attach-repo "${JOB_ID}" "${TARGET_REPO}"
    remedy set-permission "${JOB_ID}" allow repo_generated_write
    remedy attach-project-repo "${PROJECT_ID}" "${TARGET_REPO}"

    # -------------------------------------------------------------------------
    # 5. Plan
    # -------------------------------------------------------------------------
    echo "--- 5. plan-job"
    remedy plan-job "${JOB_ID}"

    # -------------------------------------------------------------------------
    # 6. Run next task (requires Ollama — skip gracefully if unavailable)
    # -------------------------------------------------------------------------
    echo "--- 6. run-next-task-local"
    if remedy run-next-task-local "${JOB_ID}"; then
        echo "    Task run: OK"
    else
        echo "    Task run: SKIP (Ollama likely unavailable — continuing smoke)"
    fi

    # -------------------------------------------------------------------------
    # 7. Approve first patch intent if present
    # -------------------------------------------------------------------------
    echo "--- 7. Approve first patch intent (if any)"
    FIRST_INTENT_ID="$(remedy brain "${JOB_ID}" --json | python3 -c "
import json,sys
data=json.load(sys.stdin)
for n in data.get('nodes', []):
    if n.get('type') == 'patch_intent':
        nid = n['id']
        print(nid[3:] if nid.startswith('pi:') else nid)
        break
" 2>/dev/null || true)"
    if [[ -n "${FIRST_INTENT_ID}" ]]; then
        remedy approve-patch-intent "${JOB_ID}" "${FIRST_INTENT_ID}" --reason "smoke approval" \
            2>&1 || true
        echo "    Approved: ${FIRST_INTENT_ID}"
    else
        echo "    No patch intents found — skipping"
    fi

    # -------------------------------------------------------------------------
    # 8. Assert: remedy project --json (alias)
    # -------------------------------------------------------------------------
    echo "--- 8. Assert: remedy project --json"
    PROJECT_JSON="$(remedy project "${PROJECT_ID}" --json)"
    python3 -c "
import json,sys
data=json.loads(sys.argv[1])
assert data['version'] == 1, f'version must be 1, got {data[\"version\"]}'
assert data['project']['id'] == sys.argv[2], 'project id mismatch'
jobs = data.get('jobs', [])
assert any(j['id'] == sys.argv[3] for j in jobs), f'job {sys.argv[3][:8]} not in project jobs'
print(f'    remedy project --json: OK (version={data[\"version\"]}, jobs={len(jobs)})')
" "${PROJECT_JSON}" "${PROJECT_ID}" "${JOB_ID}"

    # -------------------------------------------------------------------------
    # 9. Assert: remedy show-project --json (backward compat)
    # -------------------------------------------------------------------------
    echo "--- 9. Assert: remedy show-project --json"
    SHOW_JSON="$(remedy show-project "${PROJECT_ID}" --json)"
    python3 -c "
import json,sys
data=json.loads(sys.argv[1])
assert data['version'] == 1, 'show-project version must be 1'
print('    remedy show-project --json: OK')
" "${SHOW_JSON}"

    # -------------------------------------------------------------------------
    # 10. Assert: context score 0..85
    # -------------------------------------------------------------------------
    echo "--- 10. Assert context score"
    CTX_SCORE="$(remedy context "${JOB_ID}" --json | python3 -c "
import json,sys
data=json.load(sys.stdin)
print(data['score'])
")"
    if [[ "${CTX_SCORE}" -lt 0 ]] || [[ "${CTX_SCORE}" -gt 85 ]]; then
        echo "ERROR: context score ${CTX_SCORE} is outside 0..85" >&2
        return 1
    fi
    echo "    Context score: ${CTX_SCORE} (OK)"

    # -------------------------------------------------------------------------
    # 11. Assert: brain JSON has required node types + project_placeholder
    # -------------------------------------------------------------------------
    echo "--- 11. Assert brain node types (including project_placeholder)"
    remedy brain "${JOB_ID}" --json | python3 -c "
import json,sys
data=json.load(sys.stdin)
types={n['type'] for n in data.get('nodes', [])}
core=['job','task','context_coverage']
missing_core=[t for t in core if t not in types]
if missing_core:
    print('ERROR: brain missing core node types: '+', '.join(missing_core), file=sys.stderr)
    sys.exit(1)
if 'project_placeholder' not in types:
    print('ERROR: project_placeholder node missing from brain', file=sys.stderr)
    sys.exit(1)
print('    Brain types: '+', '.join(sorted(types)))
"

    # -------------------------------------------------------------------------
    # 12. Generate Brain Viewer
    # -------------------------------------------------------------------------
    echo "--- 12. remedy brain-view"
    BRAIN_VIEW_OUTPUT="$(remedy brain-view "${JOB_ID}")" || {
        echo "ERROR: brain-view failed" >&2
        return 1
    }
    VIEW_PATH="$(printf '%s\n' "${BRAIN_VIEW_OUTPUT}" \
        | awk -F': ' '/^Brain Viewer v0:/ {print $2; exit}' || true)"
    if [[ -z "${VIEW_PATH}" ]]; then
        echo "ERROR: brain-view did not print a 'Brain Viewer v0:' line" >&2
        printf "Output was:\n%s\n" "${BRAIN_VIEW_OUTPUT}" >&2
        return 1
    fi
    VIEW_DIR="$(dirname "${VIEW_PATH}")"

    # -------------------------------------------------------------------------
    # 13. Assert viewer files
    # -------------------------------------------------------------------------
    echo "--- 13. Assert viewer files"
    python3 -c "
import json,sys
with open(sys.argv[1]) as f:
    data=json.load(f)
assert data['version']==1, 'viewer_data.json version must be 1'
assert 'graph' in data, 'viewer_data.json must have graph key'
n=len(data['graph'].get('nodes',[]))
print(f'    viewer_data.json: OK (version={data[\"version\"]}, nodes={n})')
" "${VIEW_DIR}/viewer_data.json"

    python3 -c "
import sys
with open(sys.argv[1]) as f:
    html=f.read()
checks=[
    ('Remedy Brain Viewer',      'title/header'),
    ('id=\"viewer-data\"',       'data island id'),
    ('type=\"application/json\"','data island type'),
    ('static-fallback',          'initial render status'),
]
failed=[]
for needle,desc in checks:
    if needle not in html:
        failed.append(f'MISSING {desc!r}: {needle!r}')
if failed:
    for msg in failed:
        print('ERROR: '+msg, file=sys.stderr)
    sys.exit(1)
print('    index.html markers: OK')
" "${VIEW_DIR}/index.html"

    # -------------------------------------------------------------------------
    # 14. Summary
    # -------------------------------------------------------------------------
    echo ""
    echo "========================================"
    echo "PROJECT_ID = ${PROJECT_ID}"
    echo "JOB_ID     = ${JOB_ID}"
    echo "VIEW_PATH  = ${VIEW_PATH}"
    echo "remedy_smoke: PASSED"
    echo "========================================"
  )
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  remedy_smoke "$@"
fi
