"""amend1027-green-builds, Part F: send a real order as a client, wait for its end, keep its evidence.

`submit` posts the order text as the client NAME (its token read from the registry, never printed or
written) to the live supervisor and prints the order id. `collect` polls the order until it is no
longer running, then writes into evidence/current/amend1027_green_builds/<label>/ the order's poll,
story and review, each job's story, diff and evidence files (`GET /api/v1/jobs/{job}/evidence`, the
route this amendment adds), and a summary: the jobs, their state, who tested, the tokens and minutes.
Nothing is applied: the operator applies in the app.
Usage: REMEDY_DATA_DIR=<data root> python3 .agent/authored/amend1027-f-orders.py submit <client> <order file>
       REMEDY_DATA_DIR=<data root> python3 .agent/authored/amend1027-f-orders.py collect <client> <order id> <label>
"""
from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from packages.orchestration.api_clients import load_api_clients

API = "http://127.0.0.1:8450/api/v1"
OUT_ROOT = Path(__file__).resolve().parents[2] / "evidence" / "current" / "amend1027_green_builds"


def _token(name: str) -> str:
    return next(client.token for client in load_api_clients() if client.name == name)


def _call(client: str, method: str, route: str, body: dict | None = None) -> tuple[int, dict]:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    request = urllib.request.Request(f"{API}{route}", data=data, method=method, headers={
        "Authorization": f"Bearer {_token(client)}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=120) as answer:
            return answer.status, json.loads(answer.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode("utf-8") or "{}")


def _write(out: Path, name: str, value) -> None:
    text = value if isinstance(value, str) else json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)
    (out / name).write_text(text.rstrip("\n") + "\n", encoding="utf-8")


def submit(client: str, order_file: str) -> int:
    status, body = _call(client, "POST", "/orders", {"order": Path(order_file).read_text(encoding="utf-8"),
                                                     "capture_review": True})
    print(json.dumps({"status": status, "order_id": body.get("order_id"), "error": body.get("error"),
                      "message": body.get("message")}, ensure_ascii=False))
    return 0 if status == 202 else 1


def collect(client: str, order_id: str, label: str) -> int:
    while True:
        status, order = _call(client, "GET", f"/orders/{order_id}")
        if order.get("state") != "running":
            break
        time.sleep(30)
    out = OUT_ROOT / label
    out.mkdir(parents=True, exist_ok=True)
    _write(out, "order_poll.json", order)
    _write(out, "order_story.json", _call(client, "GET", f"/orders/{order_id}/story")[1])
    review = _call(client, "GET", f"/orders/{order_id}/review")[1]
    if review.get("markdown"):
        _write(out, "order_review.md", review["markdown"])
    answer = order.get("answer") or {}
    summary = {"order_id": order_id, "client": client, "state": order.get("state"), "phase": order.get("phase"),
               "exit_code": order.get("exit_code"), "shape": answer.get("shape"),
               "order_budget_used": (answer.get("order_budget") or {}).get("used"), "jobs": {}}
    for job_id in answer.get("job_ids") or []:
        job_out = out / job_id
        job_out.mkdir(exist_ok=True)
        story = _call(client, "GET", f"/jobs/{job_id}/story")[1]
        _write(job_out, "story.json", story)
        _write(job_out, "diff.json", _call(client, "GET", f"/jobs/{job_id}/diff")[1])
        evidence = _call(client, "GET", f"/jobs/{job_id}/evidence")[1]
        names = []
        for entry in evidence.get("files") or []:
            name = str(entry["name"])
            if name.endswith(("raw_stream.jsonl", "run_events.jsonl")):
                continue          # the streams stay under the data root; the route answers them on demand
            target = job_out / "evidence" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(entry["content"], encoding="utf-8")
            names.append(name)
        _write(job_out, "evidence_files.json", {"files": [{k: e[k] for k in ("name", "size", "truncated")}
                                                          for e in evidence.get("files") or []],
                                                "files_omitted": evidence.get("files_omitted"),
                                                "copied_here": names})
        summary["jobs"][job_id] = {"state": story.get("state"), "verification": story.get("verification"),
                                   "numbers": story.get("numbers"), "scope": story.get("scope"),
                                   "retries": story.get("retries"), "order_id": story.get("order_id")}
    _write(out, "summary.json", summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    action, *rest = sys.argv[1:]
    sys.exit(submit(*rest) if action == "submit" else collect(*rest))
