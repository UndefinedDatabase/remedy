#!/usr/bin/env bash
# remedy_smoke.sh — end-to-end smoke for Brain Viewer v0.
#
# Requires: remedy CLI on PATH, python3, curl.
# Optional: Ollama running locally (for run-next-task-local).
#
# WARNING: starts python3 -m http.server bound to 0.0.0.0.
# Developer LAN helper only — no auth, trusted network use only.
#
# Overrides:
#   REMEDY_VIEWER_PORT  — starting port to try (default: 8787)
#   REMEDY_VIEWER_HOST  — override LAN IP printed in the open URL

set -euo pipefail

TARGET_REPO="/tmp/remedy-target-repo"
PROMPT="Smoke test job — verify brain viewer pipeline"

# ---------------------------------------------------------------------------
# 1. Create target repo
# ---------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------
# 2. Create job
# ---------------------------------------------------------------------------

echo "--- 2. Create job"
JOB_ID="$(remedy create-job "${PROMPT}")"
if [[ -z "${JOB_ID}" ]]; then
    echo "ERROR: create-job did not print a job ID" >&2
    exit 1
fi
echo "    JOB_ID=${JOB_ID}"

# ---------------------------------------------------------------------------
# 3. Attach repo + set permission
# ---------------------------------------------------------------------------

echo "--- 3. Attach repo + allow repo_generated_write"
remedy attach-repo "${JOB_ID}" "${TARGET_REPO}"
remedy set-permission "${JOB_ID}" allow repo_generated_write

# ---------------------------------------------------------------------------
# 4. Plan
# ---------------------------------------------------------------------------

echo "--- 4. plan-job"
remedy plan-job "${JOB_ID}"

# ---------------------------------------------------------------------------
# 5. Run next task (requires Ollama — skip gracefully if unavailable)
# ---------------------------------------------------------------------------

echo "--- 5. run-next-task-local"
if remedy run-next-task-local "${JOB_ID}"; then
    echo "    Task run: OK"
else
    echo "    Task run: SKIP (Ollama likely unavailable — continuing smoke)"
fi

# ---------------------------------------------------------------------------
# 6. Approve first patch intent if present
# ---------------------------------------------------------------------------

echo "--- 6. Approve first patch intent (if any)"
FIRST_INTENT_ID="$(remedy brain "${JOB_ID}" --json | python3 -c "
import json,sys
data=json.load(sys.stdin)
for n in data.get('nodes', []):
    if n.get('type') == 'patch_intent':
        nid = n['id']
        # node id is 'pi:<intent_id>' — strip the 'pi:' prefix
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

# ---------------------------------------------------------------------------
# 7. Assert: context score 0..85
# ---------------------------------------------------------------------------

echo "--- 7. Assert context score"
CTX_SCORE="$(remedy context "${JOB_ID}" --json | python3 -c "
import json,sys
data=json.load(sys.stdin)
print(data['score'])
")"
if [[ "${CTX_SCORE}" -lt 0 ]] || [[ "${CTX_SCORE}" -gt 85 ]]; then
    echo "ERROR: context score ${CTX_SCORE} is outside 0..85" >&2
    exit 1
fi
echo "    Context score: ${CTX_SCORE} (OK)"

# ---------------------------------------------------------------------------
# 8. Assert: brain JSON has required node types
# ---------------------------------------------------------------------------

echo "--- 8. Assert brain node types"
remedy brain "${JOB_ID}" --json | python3 -c "
import json,sys
data=json.load(sys.stdin)
types={n['type'] for n in data.get('nodes', [])}
# Always-present after plan-job
core=['job','task','context_coverage']
# Conditional on run-next-task-local succeeding
optional=['artifact','patch_intent','approval_decision','verification']
missing_core=[t for t in core if t not in types]
if missing_core:
    print('ERROR: brain missing core node types: '+', '.join(missing_core), file=sys.stderr)
    sys.exit(1)
missing_opt=[t for t in optional if t not in types]
if missing_opt:
    print('    WARN: optional types absent (need Ollama run): '+', '.join(missing_opt))
print('    Brain types: '+', '.join(sorted(types)))
"

# ---------------------------------------------------------------------------
# 9. Generate Brain Viewer
# ---------------------------------------------------------------------------

echo "--- 9. remedy brain-view"
BRAIN_VIEW_OUTPUT="$(remedy brain-view "${JOB_ID}")" || {
    echo "ERROR: brain-view failed" >&2
    exit 1
}
VIEW_PATH="$(echo "${BRAIN_VIEW_OUTPUT}" | grep '^Brain Viewer v0:' | sed 's/^Brain Viewer v0: //')"
if [[ -z "${VIEW_PATH}" ]]; then
    echo "ERROR: brain-view did not print a 'Brain Viewer v0:' line" >&2
    printf "Output was:\n%s\n" "${BRAIN_VIEW_OUTPUT}" >&2
    exit 1
fi
VIEW_DIR="$(dirname "${VIEW_PATH}")"

# ---------------------------------------------------------------------------
# 10. Assert viewer files
# ---------------------------------------------------------------------------

echo "--- 10. Assert viewer files"
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

# ---------------------------------------------------------------------------
# 11. Choose free port
# ---------------------------------------------------------------------------

echo "--- 11. Start http.server"
START_PORT="${REMEDY_VIEWER_PORT:-8787}"
VIEWER_PORT="$(python3 -c "
import socket,sys
start=int(sys.argv[1])
for p in range(start, start+20):
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind(('',p))
        s.close()
        print(p)
        break
    except OSError:
        pass
" "${START_PORT}")"

PID_FILE="/tmp/remedy-brain-viewer-${VIEWER_PORT}.pid"
LOG_FILE="/tmp/remedy-brain-viewer-${VIEWER_PORT}.log"

if [[ -f "${PID_FILE}" ]]; then
    OLD_PID="$(cat "${PID_FILE}")"
    if kill -0 "${OLD_PID}" 2>/dev/null; then
        kill "${OLD_PID}" || true
        sleep 0.3
    fi
    rm -f "${PID_FILE}"
fi

python3 -m http.server "${VIEWER_PORT}" \
    --bind 0.0.0.0 \
    --directory "${VIEW_DIR}" \
    >"${LOG_FILE}" 2>&1 &
SERVER_PID=$!
echo "${SERVER_PID}" >"${PID_FILE}"
sleep 0.6

if ! kill -0 "${SERVER_PID}" 2>/dev/null; then
    echo "ERROR: http.server failed to start" >&2
    echo "Log: ${LOG_FILE}" >&2
    cat "${LOG_FILE}" >&2
    exit 1
fi

# ---------------------------------------------------------------------------
# 12. Verify local server reachability
# ---------------------------------------------------------------------------

echo "--- 12. Verify localhost reachability"
LOCAL_URL="http://127.0.0.1:${VIEWER_PORT}/index.html"
if ! curl -sf --max-time 4 "${LOCAL_URL}" -o /dev/null; then
    echo "ERROR: localhost server not reachable at ${LOCAL_URL}" >&2
    echo "Log: ${LOG_FILE}" >&2
    cat "${LOG_FILE}" >&2
    kill "${SERVER_PID}" 2>/dev/null || true
    exit 1
fi
echo "    Localhost fetch: OK"

# ---------------------------------------------------------------------------
# 13. Detect LAN IP for Mac open URL
# ---------------------------------------------------------------------------

VIEWER_HOST="${REMEDY_VIEWER_HOST:-}"
if [[ -z "${VIEWER_HOST}" ]]; then
    VIEWER_HOST="$(ip route get 1.1.1.1 2>/dev/null \
        | awk '{for(i=1;i<=NF;i++) if($i=="src"){print $(i+1); exit}}' \
        || true)"
fi
if [[ -z "${VIEWER_HOST}" ]]; then
    VIEWER_HOST="$(hostname -I 2>/dev/null | awk '{print $1}' || true)"
fi
if [[ -z "${VIEWER_HOST}" ]]; then
    VIEWER_HOST="127.0.0.1"
fi
VIEW_URL="http://${VIEWER_HOST}:${VIEWER_PORT}/index.html"

# ---------------------------------------------------------------------------
# 14. Summary
# ---------------------------------------------------------------------------

echo ""
echo "========================================"
echo "JOB_ID     = ${JOB_ID}"
echo "VIEW_PATH  = ${VIEW_PATH}"
echo "VIEW_DIR   = ${VIEW_DIR}"
echo "SERVER_PID = ${SERVER_PID}"
echo "SERVER_LOG = ${LOG_FILE}"
echo "VIEW_URL   = ${VIEW_URL}"
echo ""
echo "COPY THIS ON YOUR MAC:"
echo "  open \"${VIEW_URL}\""
echo "========================================"
