"""Operator amendment amend1026-go-live-and-ask, Part E1: one real ask over HTTP, kept as evidence.

Run from the repository root after the supervisor runs main's code:
    python3 .agent/authored/amend1026-e1-evidence.py
It reads the client `orb-universe`'s token from the data root's `api/clients.json` (it is never
written anywhere), asks the project `remedy` the operator's question through
`POST /api/v1/projects/remedy/ask` on 127.0.0.1:8450, and copies the ask's own evidence folder from
the data root into `evidence/current/amend1026_ask/`, beside the HTTP answers it read.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

DATA = Path.home() / "Repos" / "remedy" / ".data"
OUT = Path("evidence/current/amend1026_ask")
PORT = 8450
CLIENT = "orb-universe"
PROJECT = "remedy"
QUESTION = "Welche Datei entscheidet, ob ein Auftrag ein Job oder mehrere wird, und wie?"


def _token() -> str:
    registry = json.loads((DATA / "api" / "clients.json").read_text(encoding="utf-8"))
    return next(entry["token"] for entry in registry["clients"] if entry["name"] == CLIENT)


def _call(method: str, path: str, body: dict | None = None, timeout: float = 1200) -> tuple[int, dict]:
    request = urllib.request.Request(
        f"http://127.0.0.1:{PORT}{path}", method=method,
        data=None if body is None else json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {_token()}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as answer:
            return answer.status, json.loads(answer.read())
    except urllib.error.HTTPError as refused:
        return refused.code, json.loads(refused.read())


def _write(name: str, value: object) -> None:
    (OUT / name).write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    status_before = _git("status", "--porcelain=v1", "-uall")
    head_before = _git("rev-parse", "HEAD").strip()
    _write("interface_version.json", {"status": _call("GET", "/api/v1/interface")[0],
                                      "interface_version": _call("GET", "/api/v1/interface")[1].get("interface_version")})
    status, execution = _call("GET", "/api/v1/execution")
    _write("execution_offer.json", {"status": status, "host_tools": execution.get("host_tools"),
                                    "autonomy": execution.get("autonomy"),
                                    "defaults": {role: {"default_provider": entry["default_provider"],
                                                        "claude_cli_available": next(
                                                            (p["available"] for p in entry["providers"]
                                                             if p["id"] == "claude-cli"), None)}
                                                 for role, entry in execution.get("roles", {}).items()}})
    status, projects = _call("GET", "/api/v1/projects")
    _write("projects.json", {"status": status, **projects})
    body = {"question": QUESTION, "max_total_tokens": 150000}
    _write("ask_request.json", {"method": "POST", "path": f"/api/v1/projects/{PROJECT}/ask", "client": CLIENT,
                                "body": body})
    status, answer = _call("POST", f"/api/v1/projects/{PROJECT}/ask", body)
    _write("ask_answer.json", {"status": status, **answer})
    if answer.get("evidence"):
        source = DATA / answer["evidence"]
        target = OUT / "ask_evidence"
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)
    _write("repository_state.json", {
        "head_before": head_before, "head_after": _git("rev-parse", "HEAD").strip(),
        "status_before": status_before.splitlines(),
        "status_after": [line for line in _git("status", "--porcelain=v1", "-uall").splitlines()
                         if not line[3:].startswith(str(OUT))]})
    sys.stdout.write(json.dumps({"status": status, "tokens_used": answer.get("tokens_used"),
                      "calls_used": answer.get("calls_used"), "model": answer.get("model"),
                      "names_scope_decision": "scope_decision.py" in str(answer.get("answer"))}) + "\n")
    return 0 if status == 200 and "scope_decision.py" in str(answer.get("answer")) else 1


if __name__ == "__main__":
    sys.exit(main())
