"""amend1024-one-real-order, Part G: collect the real run's evidence into evidence/current/f317_real_order.

Reads the temporary data root and project of the run (never the client token), asks the run's
own supervisor over the public API with the client's token, and copies what proves each line of
F317's Acceptance. Usage: python3 .agent/authored/amend1024-g-evidence.py <order_id> <run_label>
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

BASE = Path("/tmp/amend1024-g")
DATA = BASE / "data"
PROJECT = BASE / "greet-project"
API = "http://127.0.0.1:18731/api/v1"
OUT_ROOT = Path(__file__).resolve().parents[2] / "evidence" / "current" / "f317_real_order"


def _get(route: str) -> dict:
    token = (BASE / "client.token").read_text().strip()
    request = urllib.request.Request(f"{API}{route}", headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(request, timeout=30) as answer:
        return json.loads(answer.read().decode("utf-8"))


def _write(out: Path, name: str, value) -> None:
    text = value if isinstance(value, str) else json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)
    (out / name).write_text(text.rstrip("\n") + "\n", encoding="utf-8")


def _bash_calls(raw_stream: Path) -> list[dict]:
    """Every Bash tool call of a streamed claude-cli call, with its command, from the raw stream."""
    calls = []
    for line in raw_stream.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        message = event.get("message") if isinstance(event, dict) else None
        for part in (message or {}).get("content", []) if isinstance(message, dict) else []:
            if isinstance(part, dict) and part.get("type") == "tool_use" and part.get("name") == "Bash":
                calls.append({"tool_use_id": part.get("id"), "command": (part.get("input") or {}).get("command")})
            if isinstance(part, dict) and part.get("type") == "tool_result":
                for call in calls:
                    if call["tool_use_id"] == part.get("tool_use_id"):
                        content = part.get("content")
                        text = content if isinstance(content, str) else json.dumps(content, ensure_ascii=False)
                        call["result_tail"] = text[-600:]
                        call["is_error"] = bool(part.get("is_error"))
    return calls


def _denials(raw_stream: Path) -> list[dict]:
    """The `permission_denials` of a stream's final result line: the commands the CLI refused."""
    found = []
    for line in raw_stream.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if isinstance(event, dict) and event.get("type") == "result":
            for denial in event.get("permission_denials") or []:
                found.append({"tool": denial.get("tool_name"), "command": (denial.get("tool_input") or {}).get("command")})
    return found


def main(order_id: str, label: str) -> int:
    out = OUT_ROOT / label
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    order = _get(f"/orders/{order_id}")
    _write(out, "order_poll.json", order)
    _write(out, "order_story.json", _get(f"/orders/{order_id}/story"))
    order_file = Path(order["order_file"])
    _write(out, "order_file.md", order_file.read_text(encoding="utf-8"))
    answer = order.get("answer") or {}
    summary = {"order_id": order_id, "state": order.get("state"), "exit_code": order.get("exit_code"),
               "shape": answer.get("shape"), "shape_source": answer.get("shape_source"),
               "job_ids": answer.get("job_ids"), "order_budget_used": (answer.get("order_budget") or {}).get("used"),
               "planner_calls_by_reason": (answer.get("order_budget") or {}).get("planner_calls_by_reason"),
               "jobs": {}}
    for job_id in answer.get("job_ids") or []:
        job_out = out / job_id
        job_out.mkdir()
        _write(job_out, "story.json", _get(f"/jobs/{job_id}/story"))
        _write(job_out, "diff.json", _get(f"/jobs/{job_id}/diff"))
        _write(job_out, "proof.json", _get(f"/jobs/{job_id}/proof"))
        evidence = DATA / "jobs" / job_id / "evidence"
        for name in ("scope_decision.json", "dod.json", "dod_result.json"):
            if (evidence / name).is_file():
                shutil.copyfile(evidence / name, job_out / name)
        job = json.loads((DATA / "jobs" / job_id / "job.json").read_text(encoding="utf-8"))
        _write(job_out, "execution_config.json", job.get("execution_config"))
        bash, refused = [], []
        for run in sorted((evidence / "task_runs").glob("*")):
            run_out = job_out / "task_runs" / run.name
            run_out.mkdir(parents=True)
            for name in ("worker_isolation.jsonl", "worker_sandbox.jsonl", "builder_command_refusals.jsonl",
                         "capability_decisions.jsonl"):
                if (run / name).is_file():
                    shutil.copyfile(run / name, run_out / name)
            for raw in sorted(run.glob("streams/*/**/raw_stream.jsonl")):
                rel = raw.relative_to(run)
                (run_out / rel.parent).mkdir(parents=True, exist_ok=True)
                shutil.copyfile(raw, run_out / rel)
                if "builder" in rel.parts:
                    bash.extend({"task_run": run.name, "stream": str(rel), **call} for call in _bash_calls(raw))
                    refused.extend({"task_run": run.name, **denial} for denial in _denials(raw))
        _write(job_out, "builder_refused_commands.json", refused)
        _write(job_out, "builder_bash_calls.json", bash)
        summary["jobs"][job_id] = {
            "builder": (job.get("execution_config") or {}).get("builder"),
            "reviewer": (job.get("execution_config") or {}).get("reviewer"),
            "stream_evidence": (job.get("execution_config") or {}).get("stream_evidence"),
            "builder_bash_calls": len(bash), "builder_refused_commands": len(refused),
            "builder_test_runs": [call["command"] for call in bash if "pytest" in (call.get("command") or "")],
        }
    log = subprocess.run(["git", "log", "--oneline", "-n", "5"], cwd=PROJECT, capture_output=True, text=True).stdout
    status = subprocess.run(["git", "status", "--short"], cwd=PROJECT, capture_output=True, text=True).stdout
    _write(out, "project_after.txt", f"git log:\n{log}\ngit status --short:\n{status}")
    _write(out, "summary.json", summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1], sys.argv[2]))
