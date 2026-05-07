#!/usr/bin/env bash
# remedy_smoke.sh — manual smoke helper for Brain Viewer over SSH / LAN
#
# Usage:
#   scripts/remedy_smoke.sh <job_id>
#
# Runs `remedy brain-view <job_id>`, then starts a python3 http.server bound
# to 0.0.0.0 so the viewer is reachable from a Mac browser on the same LAN
# (useful when Remedy runs on a remote workstation over SSH).
#
# Overrides:
#   REMEDY_VIEWER_HOST  — override the host printed in the open URL (default: auto-detected LAN IP)
#   REMEDY_VIEWER_PORT  — override the HTTP port (default: 8765)

set -euo pipefail

# ---------------------------------------------------------------------------
# Args
# ---------------------------------------------------------------------------

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <job_id>" >&2
    exit 1
fi

JOB_ID="$1"

# ---------------------------------------------------------------------------
# Run brain-view and capture the output path
# ---------------------------------------------------------------------------

echo ">>> remedy brain-view ${JOB_ID}"
VIEW_PATH="$(remedy brain-view "${JOB_ID}" | grep '^Brain Viewer v0:' | sed 's/^Brain Viewer v0: //')"

if [[ -z "${VIEW_PATH}" ]]; then
    echo "Error: brain-view did not print a 'Brain Viewer v0:' line." >&2
    exit 1
fi

VIEW_DIR="$(dirname "${VIEW_PATH}")"
echo "Brain Viewer path : ${VIEW_PATH}"
echo "Brain Viewer dir  : ${VIEW_DIR}"

# ---------------------------------------------------------------------------
# Detect LAN IP (ip route preferred; hostname -I fallback)
# ---------------------------------------------------------------------------

if [[ -z "${REMEDY_VIEWER_HOST:-}" ]]; then
    VIEWER_HOST="$(ip route get 1.1.1.1 2>/dev/null \
        | awk '{for(i=1;i<=NF;i++) if($i=="src"){print $(i+1); exit}}' \
        || true)"
    if [[ -z "${VIEWER_HOST}" ]]; then
        VIEWER_HOST="$(hostname -I 2>/dev/null | awk '{print $1}' || true)"
    fi
    if [[ -z "${VIEWER_HOST}" ]]; then
        VIEWER_HOST="127.0.0.1"
        echo "Warning: could not detect LAN IP; falling back to ${VIEWER_HOST}" >&2
    fi
else
    VIEWER_HOST="${REMEDY_VIEWER_HOST}"
fi

VIEWER_PORT="${REMEDY_VIEWER_PORT:-8765}"

# ---------------------------------------------------------------------------
# Kill previous server on the same port (if any)
# ---------------------------------------------------------------------------

PID_FILE="/tmp/remedy-brain-viewer-${VIEWER_PORT}.pid"
LOG_FILE="/tmp/remedy-brain-viewer-${VIEWER_PORT}.log"

if [[ -f "${PID_FILE}" ]]; then
    OLD_PID="$(cat "${PID_FILE}")"
    if kill -0 "${OLD_PID}" 2>/dev/null; then
        echo "Stopping previous Brain Viewer server (PID ${OLD_PID})"
        kill "${OLD_PID}" || true
        sleep 0.3
    fi
    rm -f "${PID_FILE}"
fi

# ---------------------------------------------------------------------------
# Start http.server in background
# ---------------------------------------------------------------------------

python3 -m http.server "${VIEWER_PORT}" \
    --bind 0.0.0.0 \
    --directory "${VIEW_DIR}" \
    >"${LOG_FILE}" 2>&1 &

SERVER_PID=$!
echo "${SERVER_PID}" > "${PID_FILE}"

echo "Brain Viewer server PID : ${SERVER_PID}"
echo "Brain Viewer log        : ${LOG_FILE}"

# ---------------------------------------------------------------------------
# Print Mac-friendly open command and URL
# ---------------------------------------------------------------------------

VIEWER_URL="http://${VIEWER_HOST}:${VIEWER_PORT}/index.html"

echo ""
echo "  open \"${VIEWER_URL}\""
echo ""
echo "${VIEWER_URL}"
