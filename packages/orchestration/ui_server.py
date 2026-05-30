"""
Localhost UI Server — read-only HTTP server for the Remedy UI.

Serves a single-page app shell and JSON API endpoints for job inspection.
Binds 127.0.0.1 only.  No mutation endpoints.  No POST/PUT/DELETE.
Token-gated API access via per-run random token in URL.

Scope:
  - Read-only only.
  - No repo mutation, no shell, no subprocess (except optional opener).
  - No external network, CDN, npm, or build step.
  - Serves only safe summaries, counts, statuses, IDs, hashes, next actions.
  - No raw artifact content, file content, diffs, stdout/stderr, approval
    reasons, secrets, or tracebacks in any response.

Public API::

    start_ui_server(job_id, host, port, token, open_browser, info_file)
"""

from __future__ import annotations

import json
import os
import secrets
import sys
from datetime import datetime, timezone
from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse
from uuid import UUID


# ---------------------------------------------------------------------------
# Safe data builders (no raw content leaks)
# ---------------------------------------------------------------------------

def _load_events(job: Any) -> list[dict[str, Any]]:
    """Load run-log events for a job."""
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.timeline import load_run_events
    return load_run_events(resolve_data_root(), job.id)


def _safe_error(code: int, message: str) -> tuple[int, dict[str, Any]]:
    return code, {"error": message}


def _load_job(job_id_str: str) -> Any:
    """Load a Job by UUID string, return (job, error_tuple)."""
    try:
        job_id = UUID(job_id_str)
    except ValueError:
        return None, _safe_error(400, "invalid job_id")
    try:
        from packages.orchestration.storage import JobNotFoundError, load_job
        job = load_job(job_id)
    except (FileNotFoundError, JobNotFoundError):
        return None, _safe_error(404, "job not found")
    return job, None


def _build_dashboard(job: Any) -> dict[str, Any]:
    """Build safe dashboard payload for a job."""
    events = _load_events(job)

    # Status
    state = job.state.value if hasattr(job.state, "value") else str(job.state)
    task_count = len(job.tasks)
    artifact_count = len(job.artifacts)

    # Lifecycle counts from events
    apply_count = sum(1 for e in events if e.get("event") == "patch_intent_applied")
    proof_count = sum(1 for e in events if e.get("event") == "proof_collected")
    test_count = sum(1 for e in events if e.get("event") == "test_run_completed")
    revert_count = sum(1 for e in events if e.get("event") == "patch_intent_reverted")

    # Approvals
    pending_approvals = 0
    for art in job.artifacts:
        meta = art.metadata or {}
        explanations = meta.get("patch_intent_explanations", [])
        for _idx, intent in enumerate(explanations):
            approval = intent.get("approval_state", "pending")
            if approval == "pending":
                pending_approvals += 1

    # Blockers / decisions
    blocker_count = sum(1 for e in events if e.get("event") == "stop_reason_recorded"
                        and e.get("outcome") != "resolved")
    decision_count = sum(1 for e in events if e.get("event") == "human_decision_requested"
                         and e.get("outcome") != "resolved")

    # Latest proof
    proof_events = [e for e in events if e.get("event") == "proof_collected"]
    latest_proof = None
    if proof_events:
        pe = proof_events[-1]
        pm = pe.get("metadata", {})
        latest_proof = {
            "hash": pm.get("content_hash", "")[:16],
            "intent_id": pm.get("intent_id", ""),
            "timestamp": pe.get("timestamp", ""),
        }

    # Latest test
    test_events = [e for e in events if e.get("event") == "test_run_completed"]
    latest_test = None
    if test_events:
        te = test_events[-1]
        tm = te.get("metadata", {})
        latest_test = {
            "exit_code": tm.get("exit_code"),
            "command_hash": tm.get("command_hash", "")[:16],
            "timestamp": te.get("timestamp", ""),
        }

    # Token budget
    token_mode = "compact"
    for e in reversed(events):
        if e.get("event") == "context_pack_created":
            token_mode = e.get("metadata", {}).get("mode", "compact")
            break

    # Guidance
    guidance_cards: list[dict[str, str]] = []
    try:
        from packages.orchestration.guidance import build_guidance_cards
        cards = build_guidance_cards(job, events)
        guidance_cards = [
            {
                "id": c.id,
                "title": c.title,
                "severity": c.severity,
                "why": c.why_it_matters,
                "action": c.safe_next_action,
                "command": c.command,
            }
            for c in cards
        ]
    except Exception:
        pass

    # Primary next action
    next_action = ""
    if guidance_cards:
        next_action = guidance_cards[0].get("command", "")

    # What-happened lifecycle
    lifecycle: list[dict[str, str]] = []
    lifecycle_types = [
        ("task_created", "Task created"),
        ("patch_intent_created", "Patch proposed"),
        ("patch_intent_approved", "Patch approved"),
        ("patch_intent_applied", "Patch applied"),
        ("proof_collected", "Proof collected"),
        ("test_run_completed", "Tests run"),
    ]
    for etype, label in lifecycle_types:
        matching = [e for e in events if e.get("event") == etype]
        if matching:
            lifecycle.append({
                "step": label,
                "count": len(matching),
                "latest": matching[-1].get("timestamp", ""),
            })

    return {
        "version": 1,
        "job_id": str(job.id),
        "job_name": job.name,
        "state": state,
        "task_count": task_count,
        "artifact_count": artifact_count,
        "apply_count": apply_count,
        "proof_count": proof_count,
        "test_count": test_count,
        "revert_count": revert_count,
        "pending_approvals": pending_approvals,
        "blocker_count": blocker_count,
        "decision_count": decision_count,
        "latest_proof": latest_proof,
        "latest_test": latest_test,
        "token_mode": token_mode,
        "next_action": next_action,
        "guidance": guidance_cards,
        "lifecycle": lifecycle,
    }


def _build_brain_json(job: Any) -> dict[str, Any]:
    """Build safe brain graph payload."""
    from packages.orchestration.brain_detail import (
        build_brain_node_detail,
        export_brain_node_detail_json,
    )
    from packages.orchestration.project_brain import (
        build_project_brain,
        export_project_brain_json,
    )

    events = _load_events(job)
    graph = build_project_brain(job, events)
    brain_json = export_project_brain_json(graph)

    details = {}
    for node in graph.nodes:
        try:
            detail = build_brain_node_detail(job, graph, node.id, events)
            details[node.id] = export_brain_node_detail_json(detail)
        except (ValueError, KeyError):
            details[node.id] = {"title": node.type, "id": node.id}

    return {
        "version": 1,
        "graph": brain_json,
        "details": details,
    }


def _build_events_json(job: Any) -> dict[str, Any]:
    """Build safe events timeline."""

    events = _load_events(job)
    safe_events = []
    for e in events[-100:]:
        safe_events.append({
            "event": e.get("event", ""),
            "timestamp": e.get("timestamp", ""),
            "outcome": e.get("outcome", ""),
        })
    return {"version": 1, "events": safe_events, "total": len(events)}


def _build_readiness_json(job: Any) -> dict[str, Any]:
    """Build safe readiness payload."""
    try:
        from packages.orchestration.readiness import assess_readiness, export_readiness_json

        events = _load_events(job)
        result = assess_readiness(job, events, scope="job")
        return export_readiness_json(result)
    except Exception:
        return {"version": 1, "error": "readiness unavailable"}


def _build_guide_json(job: Any) -> dict[str, Any]:
    """Build safe guidance payload."""
    try:
        from packages.orchestration.guidance import (
            build_guidance_cards,
            export_guidance_json,
        )

        events = _load_events(job)
        cards = build_guidance_cards(job, events)
        return export_guidance_json(job, cards)
    except Exception:
        return {"version": 1, "cards": [], "error": "guidance unavailable"}


def _build_brain_view_model_json(job: Any) -> dict[str, Any]:
    """Build semantic zoom view-model for the PixiJS brain canvas."""
    from packages.orchestration.ui_view_model import build_brain_view_model
    events = _load_events(job)
    return build_brain_view_model(job, events)


def _build_node_detail_json(job: Any, node_id: str) -> dict[str, Any]:
    """Build compact node detail for the floating card."""
    from packages.orchestration.ui_view_model import build_node_detail
    events = _load_events(job)
    return build_node_detail(job, events, node_id)


def _get_frontend_dist() -> Path | None:
    """Return path to built PixiJS frontend dist/ if it exists."""
    dist = Path(__file__).resolve().parent.parent.parent / "apps" / "ui" / "dist"
    index = dist / "index.html"
    if index.is_file():
        return dist
    return None


def _load_frontend(job_id: str, token: str) -> str:
    """Load frontend HTML — prefer PixiJS build, fall back to legacy shell."""
    dist = _get_frontend_dist()
    if dist is not None:
        html = (dist / "index.html").read_text(encoding="utf-8")
        html = html.replace("__JOB_ID__", job_id).replace("__TOKEN__", token)
        return html
    from packages.orchestration.ui_app_shell import build_app_shell
    return build_app_shell(job_id, token)


def _build_context_budget_json(job: Any) -> dict[str, Any]:
    """Build safe context budget payload."""
    try:
        from packages.orchestration.context_pack import build_context_pack, export_context_pack_json

        events = _load_events(job)
        pack = build_context_pack(job, events, budget=2000, mode="compact")
        data = export_context_pack_json(pack)
        # Strip section content — only return structure
        for s in data.get("sections", []):
            s.pop("content", None)
        return data
    except Exception:
        return {"version": 1, "error": "context budget unavailable"}


# ---------------------------------------------------------------------------
# HTTP Request Handler
# ---------------------------------------------------------------------------

class _RemedyHandler(BaseHTTPRequestHandler):
    """Read-only handler. No POST/PUT/DELETE. Token-gated API."""

    server_token: str = ""
    target_job_id: str = ""
    app_html: str = ""

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        """Suppress default stderr logging."""

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        qs = parse_qs(parsed.query)

        # App shell — no token required
        if path == "/":
            self._send_html(200, self.app_html)
            return

        # Static assets from PixiJS dist/ (JS/CSS bundles)
        if path.startswith("/assets/"):
            self._serve_static(path)
            return

        # API routes — token required
        token = (qs.get("token") or [""])[0]
        if token != self.server_token:
            self._send_json(*_safe_error(403, "invalid token"))
            return

        # Route dispatch
        if path == "/api/state":
            job_id = (qs.get("job_id") or [self.target_job_id])[0]
            job, err = _load_job(job_id)
            if err:
                self._send_json(*err)
                return
            self._send_json(200, _build_dashboard(job))
            return

        # /api/jobs/<job_id>/<endpoint>
        parts = path.split("/")
        if len(parts) == 5 and parts[1] == "api" and parts[2] == "jobs":
            job_id_str = parts[3]
            endpoint = parts[4]
            job, err = _load_job(job_id_str)
            if err:
                self._send_json(*err)
                return
            handlers = {
                "dashboard": _build_dashboard,
                "brain": _build_brain_json,
                "brain-view-model": _build_brain_view_model_json,
                "guide": _build_guide_json,
                "events": _build_events_json,
                "readiness": _build_readiness_json,
                "context-budget": _build_context_budget_json,
            }
            handler = handlers.get(endpoint)
            if handler:
                self._send_json(200, handler(job))
                return

        # /api/jobs/<job_id>/nodes/<node_id>/detail
        if (len(parts) == 7 and parts[1] == "api" and parts[2] == "jobs"
                and parts[4] == "nodes" and parts[6] == "detail"):
            job_id_str = parts[3]
            node_id = parts[5]
            job, err = _load_job(job_id_str)
            if err:
                self._send_json(*err)
                return
            self._send_json(200, _build_node_detail_json(job, node_id))
            return

        self._send_json(*_safe_error(404, "not found"))

    def do_POST(self) -> None:  # noqa: N802
        self._send_json(*_safe_error(405, "method not allowed"))

    def do_PUT(self) -> None:  # noqa: N802
        self._send_json(*_safe_error(405, "method not allowed"))

    def do_DELETE(self) -> None:  # noqa: N802
        self._send_json(*_safe_error(405, "method not allowed"))

    def _send_json(self, code: int, data: dict[str, Any]) -> None:
        body = json.dumps(data, default=str).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, code: int, html: str) -> None:
        body = html.encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    _MIME_TYPES: dict[str, str] = {
        ".js": "application/javascript",
        ".css": "text/css",
        ".svg": "image/svg+xml",
        ".png": "image/png",
        ".woff2": "font/woff2",
        ".json": "application/json",
    }

    def _serve_static(self, url_path: str) -> None:
        """Serve static files from PixiJS dist/assets/. Path-traversal safe."""
        dist = _get_frontend_dist()
        if dist is None:
            self._send_json(*_safe_error(404, "not found"))
            return
        # Resolve and ensure within dist/
        try:
            target = (dist / url_path.lstrip("/")).resolve()
            if not str(target).startswith(str(dist.resolve())):
                self._send_json(*_safe_error(403, "forbidden"))
                return
            if not target.is_file():
                self._send_json(*_safe_error(404, "not found"))
                return
        except (ValueError, OSError):
            self._send_json(*_safe_error(404, "not found"))
            return
        suffix = target.suffix.lower()
        content_type = self._MIME_TYPES.get(suffix, "application/octet-stream")
        body = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "public, max-age=31536000, immutable")
        self.end_headers()
        self.wfile.write(body)


# ---------------------------------------------------------------------------
# Server lifecycle
# ---------------------------------------------------------------------------

def start_ui_server(
    job_id: str,
    *,
    host: str = "127.0.0.1",
    port: int = 8787,
    token: str | None = None,
    open_browser: bool = False,
    info_file: str | None = None,
) -> None:
    """Start the read-only UI server. Blocks until Ctrl-C."""
    # Security: refuse non-localhost
    if host not in ("127.0.0.1", "localhost", "::1"):
        print(f"Error: refusing to bind {host} — only 127.0.0.1 allowed", file=sys.stderr)
        sys.exit(1)
    # Normalize to 127.0.0.1
    host = "127.0.0.1"

    # Validate job exists
    job, err = _load_job(job_id)
    if err:
        print(f"Error: {err[1]['error']}", file=sys.stderr)
        sys.exit(1)

    if token is None:
        token = secrets.token_urlsafe(24)

    # Prefer built PixiJS frontend; fall back to legacy inline shell
    app_html = _load_frontend(job_id, token)

    # Create handler class with bound state
    handler_class = type(
        "_BoundHandler",
        (_RemedyHandler,),
        {
            "server_token": token,
            "target_job_id": job_id,
            "app_html": app_html,
        },
    )

    server = HTTPServer((host, port), handler_class)
    actual_port = server.server_address[1]
    url = f"http://127.0.0.1:{actual_port}/?job={job_id}&token={token}"

    # Write info file
    if info_file:
        info = {
            "version": 1,
            "url": url,
            "host": host,
            "port": actual_port,
            "token": token,
            "job_id": job_id,
            "pid": os.getpid(),
            "started_at": datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        Path(info_file).write_text(json.dumps(info, indent=2))

    print(f"\nRemedy UI: {url}\n")
    print(f"Press Ctrl-C to stop.\n")

    # Optional browser open
    if open_browser:
        _try_open_browser(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def _try_open_browser(url: str) -> None:
    """Best-effort platform opener. Failure does not raise."""
    import platform
    import subprocess

    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.Popen(["open", url])
        elif system == "Linux":
            subprocess.Popen(["xdg-open", url])
        elif system == "Windows":
            os.startfile(url)  # type: ignore[attr-defined]
    except (OSError, FileNotFoundError):
        pass
