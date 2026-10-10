"""F302 T003: the fixed question and one small real task, before the cut and after it.

DECISION F302 D2 (4). Part one asks T002's fixed question through `build_claude_cli_args` and
`_guarded_cli_run`, the path every builder call takes, in a scratch repository and in a worktree of
Remedy: once with both keys true, which is the command line before F302, and once with the keys
unset, which is the lean start. Part two runs one small real task twice as a self-use job with the
claude-cli builder and reviewer: the next item Remedy's own generator offers, placed in two scratch
copies of the queue so the real queue is never written; the first job runs with both keys true
in its process's environment, the second with neither set; each job's budget is four provider calls.
At most twelve provider calls in all. A second `run` refuses to start once the readings exist.

    python3 -B f302-r4-measure.py run --out <dir> --work <dir> --remedy-rev <sha> [--skip-jobs]
    python3 -B f302-r4-measure.py render --out <dir>

`--skip-jobs` is the reviewer's dry run against a stand-in `claude`: it asks the question only.

`run` writes `f302_after.jsonl` (one line per reading, written as it is taken) and `render` writes
`f302_after.md` from those lines and from `.agent/f302_attribution.jsonl`, T002's readings, alone.
`--out` names a folder outside the checkout the jobs run on, so nothing is written there while a
job runs. No cost
in US dollars is kept (DECISION amend1007b D7).
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
import statistics
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

from packages.orchestration.claude_cli_command import build_claude_cli_args  # noqa: E402
from packages.orchestration.pingpong_provider import _guarded_cli_run, _stderr_tail  # noqa: E402
from packages.orchestration.token_actuals import parse_cli_envelope  # noqa: E402

MAX_CALLS = 12
JOB_CALLS = 4
TIMEOUT_SEC = 300
MODEL = "claude-sonnet-4-6"
WRITE_MODE = "allowed-tools"
PROMPT = "This is a measurement call. Answer with the one word READY and nothing else. Use no tool."
KINDS = ("input", "output", "cache_creation", "cache_read")
BEFORE_ENV = {"REMEDY_CLAUDE_CLI_CUSTOMIZATIONS": "true", "REMEDY_CLAUDE_CLI_ALL_TOOLS": "true"}
#: The two starts: "before" is the command line before F302, "after" the lean start.
STARTS = {"before": {"claude_cli.customizations": True, "claude_cli.all_tools": True}, "after": {}}
QUESTION_PLAN = [(place, start) for place in ("scratch", "remedy") for start in ("before", "after")]
assert len(QUESTION_PLAN) + 2 * JOB_CALLS <= MAX_CALLS

JOB_CODE = """
import json, sys
from pathlib import Path
sys.path.insert(0, ".")
from packages.orchestration.self_use_runner import run_next_self_use_item
entry, job_file, plan = run_next_self_use_item(Path(sys.argv[1]), queue_path=Path(sys.argv[2]),
                                              max_provider_calls=int(sys.argv[3]))
print("JOB_RESULT " + json.dumps({
    "entry": entry.id, "title": entry.title, "job_id": plan.job_id, "state": str(getattr(plan.state, "value", plan.state)),
    "error": plan.error, "stop_reason": plan.stop_reason,
    "provider_call_count": (plan.budget_actuals or {}).get("provider_call_count"),
    "tasks": [{"task_id": t.task_id, "status": t.status, "verdict": t.reviewer_verdict,
               "final_status": t.final_status, "run_id": t.run_id} for t in plan.tasks]}))
"""


def _git(*args: str) -> None:
    subprocess.run(["git", *args], check=True, capture_output=True, text=True)


def _write(lines_path: pathlib.Path, row: dict) -> None:
    with lines_path.open("a") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")


def _ask(claude: str, start: str, cwd: pathlib.Path) -> dict:
    argv = build_claude_cli_args(claude, PROMPT, write_mode=WRITE_MODE, model=MODEL, config=STARTS[start])
    row = {"switches": argv[argv.index("--allowedTools") + 2:]}
    try:
        proc = _guarded_cli_run(argv, timeout_sec=TIMEOUT_SEC, cwd=str(cwd))
    except subprocess.TimeoutExpired:
        row.update(exit_code=None, error="timeout")
        return row
    env = parse_cli_envelope(proc.stdout or "")
    u = env.usage_actuals
    row.update(exit_code=proc.returncode, is_error=env.is_error, result=(env.result_text or "")[:60],
               error=_stderr_tail(proc.stderr or "") if proc.returncode else "",
               input=u.input_tokens if u else None, output=u.output_tokens if u else None,
               cache_creation=u.cache_creation if u else None, cache_read=u.cache_read if u else None,
               num_turns=u.num_turns if u else None)
    return row


def _run_job(start: str, dest: pathlib.Path, queue: pathlib.Path) -> dict:
    env = {k: v for k, v in os.environ.items() if k not in BEFORE_ENV}
    if start == "before":
        env.update(BEFORE_ENV)
    proc = subprocess.run([sys.executable, "-B", "-c", JOB_CODE, str(dest), str(queue), str(JOB_CALLS)],
                          cwd=str(REPO), env=env, capture_output=True, text=True)
    found = [x for x in proc.stdout.splitlines() if x.startswith("JOB_RESULT ")]
    if proc.returncode != 0 or not found:
        return {"exit_code": proc.returncode, "error": (proc.stderr or proc.stdout)[-1500:]}
    return {"exit_code": 0, **json.loads(found[-1][len("JOB_RESULT "):])}


def _job_calls(run_id: str) -> list[dict]:
    proc = subprocess.run([sys.executable, "-m", "apps.cli.main", "run", "show", run_id, "--json"],
                          cwd=str(REPO), capture_output=True, text=True)
    if proc.returncode != 0:
        return [{"run_id": run_id, "error": f"run show exit {proc.returncode}"}]
    d = json.loads(proc.stdout)
    out = []
    for a in (d.get("provider_evidence") or {}).get("provider_attempts") or []:
        u = a.get("usage") or {}
        out.append({"run_id": run_id, "seq": a.get("seq"), "round": a.get("round"), "role": a.get("role"),
                    "provider": a.get("provider"), "error": a.get("error") or "",
                    "input": u.get("input_tokens"), "output": u.get("output_tokens"),
                    "cache_creation": u.get("cache_creation_input_tokens"),
                    "cache_read": u.get("cache_read_input_tokens")})
    return out


def run(out: pathlib.Path, work: pathlib.Path, rev: str, skip_jobs: bool = False) -> None:
    from packages.orchestration.self_use_generator import append_generated_item, generate_self_use_item
    from packages.orchestration.self_use_queue import default_self_use_queue_path

    lines_path = out / "f302_after.jsonl"
    if lines_path.exists():
        raise SystemExit(f"refusing: {lines_path} exists; the readings are taken once")
    if work.exists():
        raise SystemExit(f"refusing: {work} exists; the places are made fresh")
    claude = shutil.which("claude") or ""
    if not claude:
        raise SystemExit("refusing: no claude on PATH")
    scratch, remedy = work / "scratch", work / "remedy"
    scratch.mkdir(parents=True)
    _git("-C", str(scratch), "init", "-q")
    (scratch / "README.md").write_text("A scratch repository for one measurement.\n")
    _git("-C", str(REPO), "worktree", "add", "--detach", str(remedy), rev)
    calls = 0
    try:
        for place, start in QUESTION_PLAN:
            calls += 1
            row = _ask(claude, start, scratch if place == "scratch" else remedy)
            _write(lines_path, {"kind": "question", "place": place, "start": start, **row})
            print("question", place, start, row.get("exit_code"), *(row.get(k) for k in KINDS), flush=True)
        if skip_jobs:
            return
        real_queue = default_self_use_queue_path()
        entry = generate_self_use_item(real_queue)
        if entry is None:
            _write(lines_path, {"kind": "job", "start": "none", "error": "the generator offered no item"})
            print("no item")
            return
        for start in ("before", "after"):
            queue = work / f"queue-{start}.json"
            shutil.copyfile(real_queue, queue)
            append_generated_item(entry, queue)
            result = _run_job(start, work / f"dest-{start}", queue)
            _write(lines_path, {"kind": "job", "start": start, **result})
            print("job", start, json.dumps(result)[:400], flush=True)
            for task in result.get("tasks", []):
                if task.get("run_id"):
                    for row in _job_calls(task["run_id"]):
                        calls += 1
                        _write(lines_path, {"kind": "job_call", "start": start, "task_id": task["task_id"], **row})
    finally:
        if remedy.exists():
            _git("-C", str(REPO), "worktree", "remove", "--force", str(remedy))
        shutil.rmtree(work, ignore_errors=True)
    print("provider calls read:", calls)


def _ctx(r: dict) -> int | None:
    if any(not isinstance(r.get(k), int) for k in ("input", "cache_creation", "cache_read")):
        return None
    return r["input"] + r["cache_creation"] + r["cache_read"]


def _f(v) -> str:
    return f"{v:,}" if isinstance(v, int) else "—"


def render(out: pathlib.Path) -> None:
    rows = [json.loads(x) for x in (out / "f302_after.jsonl").read_text().splitlines()]
    t002 = [json.loads(x) for x in (REPO / ".agent/f302_attribution.jsonl").read_text().splitlines()]
    w = ["# F302 T003 — the fixed question and one real task, before the cut and after it", "",
         "> Written by `.agent/authored/f302-r4-measure.py render` from `.agent/f302_after.jsonl` and",
         "> `.agent/f302_attribution.jsonl` alone; every figure below is computed, none typed.", ""]
    questions = [r for r in rows if r["kind"] == "question"]
    job_calls = [r for r in rows if r["kind"] == "job_call"]
    w.append(f"Provider calls: {len(questions)} for the question and {len(job_calls)} read from the two jobs' "
             f"run records, of at most {MAX_CALLS} (DECISION F302 D2 (4)). \"Before\" is the command line")
    w.append("before F302, with both keys true; \"after\" is the lean start, with neither set. Context is input")
    w.append("plus cache creation plus cache read: what the call's requests read, however much was cached.")
    w.append("")
    w.append("## The fixed question")
    w.append("")
    w.append("| Place | Start | Switches | Exit | Turns | Input | Output | Cache creation | Cache read | Context |")
    w.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in questions:
        sw = " ".join(f"`{s}`" for s in r.get("switches", [])) or "none"
        w.append(f"| {r['place']} | {r['start']} | {sw} | {r.get('exit_code')} | {_f(r.get('num_turns'))} | "
                 + " | ".join(_f(r.get(k)) for k in KINDS) + f" | {_f(_ctx(r))} |")
    w.append("")
    for place in ("scratch", "remedy"):
        before = [_ctx(r) for r in questions if r["place"] == place and r["start"] == "before" and r.get("exit_code") == 0]
        after = [_ctx(r) for r in questions if r["place"] == place and r["start"] == "after" and r.get("exit_code") == 0]
        base = [_ctx(r) for r in t002 if r["place"] == place and r["config"] in ("baseline", "baseline-repeat")
                and r.get("exit_code") == 0]
        if before and after and None not in before + after:
            w.append(f"In the {place} place the context fell from {_f(before[0])} to {_f(after[0])}, by "
                     f"{_f(before[0] - after[0])}; T002's two baselines there read "
                     f"{', '.join(_f(b) for b in base)}.")
    w.append("")
    w.append("## One real task as a job")
    w.append("")
    w.append("A job's call works through many turns of its own tool loop, and each turn reads the context")
    w.append("again, so a job call's context below counts every turn's reading.")
    for r in [x for x in rows if x["kind"] == "job"]:
        w.append("")
        if r.get("exit_code") != 0 or "job_id" not in r:
            w.append(f"- {r['start']}: the job did not run: " + str(r.get("error", "")).replace("\n", " ")[:400])
            continue
        tasks = "; ".join(f"{t['task_id']} {t['status']}, verdict {t['verdict'] or 'none'}, {t['final_status']}"
                          for t in r.get("tasks", []))
        calls = [c for c in job_calls if c["start"] == r["start"]]
        sums = {k: sum(c[k] for c in calls if isinstance(c.get(k), int)) for k in KINDS}
        w.append(f"- {r['start']}: `{r['entry']}`, \"{r['title']}\", job `{r['job_id']}` ended `{r['state']}`"
                 f" ({tasks}); {len(calls)} calls; " + ", ".join(f"{k.replace('_', ' ')} {_f(v)}" for k, v in sums.items())
                 + ".")
    w.append("")
    if job_calls:
        w.append("| Start | Run | Seq | Round | Role | Input | Output | Cache creation | Cache read | Context |")
        w.append("|---|---|---|---|---|---|---|---|---|---|")
        for c in job_calls:
            w.append(f"| {c['start']} | `{c['run_id']}` | {c.get('seq')} | {c.get('round')} | {c.get('role')} | "
                     + " | ".join(_f(c.get(k)) for k in KINDS) + f" | {_f(_ctx(c))} |")
        firsts = {s: [_ctx(c) for c in job_calls if c["start"] == s and c.get("role") == "builder"
                      and c.get("seq") == 1] for s in ("before", "after")}
        if all(firsts.values()) and None not in firsts["before"] + firsts["after"]:
            w.append("")
            w.append(f"The builder's first call read {_f(firsts['before'][0])} before and "
                     f"{_f(firsts['after'][0])} after.")
    (out / "f302_after.md").write_text("\n".join(w).rstrip("\n") + "\n")
    print("rendered", len(rows), "rows")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("run", "render"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--work", default="")
    ap.add_argument("--remedy-rev", default="")
    ap.add_argument("--skip-jobs", action="store_true", help="the reviewer's dry run: the question only")
    a = ap.parse_args(argv)
    out = pathlib.Path(a.out)
    if a.mode == "run":
        if not a.work or not a.remedy_rev:
            raise SystemExit("run needs --work and --remedy-rev")
        run(out, pathlib.Path(a.work), a.remedy_rev, a.skip_jobs)
    render(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
